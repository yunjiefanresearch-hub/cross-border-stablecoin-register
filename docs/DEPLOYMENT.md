# Deploy the mapper: the snapshot runs anywhere, the AI features need a proxy

The frontend (`stablecoin-dimension-mapper`) is a single self-contained file that embeds the
register as a **static snapshot**. That snapshot is the product: the dimension map, the corridor
explorer, the 12×12 feasibility matrix, the time-travel slider, and the CSV / BibTeX exports are all
**deterministic** and run with **no server, no key, and no network** — open the file and they work.

Three optional features reach out over the network, and only these need setup:

| Feature | Config constant | What it needs |
|---|---|---|
| Live data sync (pull the newest register instead of the bundled snapshot) | `REGISTER_API` | A URL to a deployed `api/` directory (static JSON — no auth). |
| Document / URL import, auto-map router, question generation | `LLM_PROXY` | **Your own authenticated proxy** in front of an LLM `/v1/messages` endpoint. |
| Contact / CTA seam | `CONTACT` | A `mailto:` or form URL. |

All three constants sit at the top of the mapper file and default to `""`, which means "run purely on
the bundled snapshot." **You never put an API key in the frontend.** The key lives in the proxy.

If you only want to host the tool as-is, you are already done: serve the file from any static host
(GitHub Pages, Netlify, S3, `python -m http.server`) and every deterministic feature works. The rest
of this document is only for the two networked paths.

---

## Why the AI features need a proxy at all

Inside Anthropic's artifact sandbox, the mapper's model calls succeed because the sandbox **injects
authentication** for you — so the bundled code calls the endpoint with no key and it just works. On any
other host that injection isn't there, so the same call returns `401` (or is blocked by CORS). The fix
is not to paste a key into the page — anyone could read it in the browser — but to stand up a small
**authenticated proxy** that holds the key server-side, and point `LLM_PROXY` at it.

When `LLM_PROXY` is left empty on a non-Anthropic host, the mapper detects this and **degrades
gracefully**: it shows an "AI-assisted features are off" banner, hides the import controls, and routes
you to the deterministic manual-mapping path. Nothing silently fails, and the deterministic core is
unaffected. Setting `LLM_PROXY` to a working proxy turns the AI features back on.

### What the proxy must do

The mapper sends a normal Messages-API request and expects a normal Messages-API response back. Your
proxy has exactly three jobs:

1. **Add credentials** the browser can't safely hold: the `x-api-key` and `anthropic-version` headers.
2. **Answer CORS preflight** so a browser on your domain may call the proxy cross-origin.
3. **Forward the JSON body unchanged** to the upstream endpoint and stream the reply back.

The request body the mapper sends looks like this (the `tools` field is present only for URL import,
which uses web search):

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1000,
  "messages": [{ "role": "user", "content": "…" }],
  "tools": [{ "type": "web_search_20250305", "name": "web_search" }]
}
```

Your proxy should treat the body as opaque and pass it through, so it keeps working if the model string
or options change.

---

## Cloudflare Worker (copy-paste)

This is the smallest thing that works: a Cloudflare Worker that injects the key, handles CORS, and
forwards to the upstream Messages endpoint. It costs nothing on the free tier and needs no server to
maintain.

```js
// worker.js — authenticated proxy for the CBSR mapper's AI features.
// Deploy on Cloudflare Workers; set ANTHROPIC_API_KEY as an encrypted secret (see below).
// Then set LLM_PROXY in the mapper to this Worker's URL.

const UPSTREAM = "https://api.anthropic.com/v1/messages";
const ANTHROPIC_VERSION = "2023-06-01";

// Lock this down to the exact origin you serve the mapper from.
// Use "*" only for a throwaway test — it lets any site spend your key.
const ALLOWED_ORIGIN = "https://your-mapper-host.example";

function corsHeaders(origin) {
  const allow = origin === ALLOWED_ORIGIN ? origin : ALLOWED_ORIGIN;
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    // 1) CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    // 2) Only POST is proxied
    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405, headers: corsHeaders(origin) });
    }

    // 3) Forward the body unchanged, adding server-held credentials
    let upstream;
    try {
      upstream = await fetch(UPSTREAM, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": env.ANTHROPIC_API_KEY,
          "anthropic-version": ANTHROPIC_VERSION,
        },
        body: request.body,        // pass the mapper's JSON straight through
      });
    } catch (e) {
      return new Response(JSON.stringify({ error: "upstream fetch failed" }), {
        status: 502,
        headers: { "Content-Type": "application/json", ...corsHeaders(origin) },
      });
    }

    // 4) Relay the upstream response (status + body) back to the browser with CORS
    const body = await upstream.text();
    return new Response(body, {
      status: upstream.status,
      headers: { "Content-Type": "application/json", ...corsHeaders(origin) },
    });
  },
};
```

### Deploy it

Using the Cloudflare CLI (`wrangler`):

```bash
npm install -g wrangler
wrangler login

# scaffold, then replace the generated src/index.js with worker.js above
wrangler init cbsr-proxy

# store the key as an ENCRYPTED secret — never in code, never in wrangler.toml
wrangler secret put ANTHROPIC_API_KEY   # paste your key when prompted

wrangler deploy
```

`wrangler deploy` prints the Worker URL (e.g. `https://cbsr-proxy.<you>.workers.dev`). Put that URL in
the mapper:

```js
const LLM_PROXY = "https://cbsr-proxy.<you>.workers.dev";
```

Reload the mapper. The "AI-assisted features are off" banner disappears and import / auto-map work.

> The same shape ports directly to other runtimes — a Vercel/Netlify serverless function, a Deno Deploy
> script, or a tiny Express handler. The three jobs are identical: add `x-api-key` +
> `anthropic-version`, answer the CORS preflight, forward the body. Only the request/response glue
> differs.

---

## Security: this proxy spends money, so gate it

An open proxy in front of a paid API is a standing invitation to abuse. Before you point real traffic
at it:

- **Pin `ALLOWED_ORIGIN`** to the exact host you serve the mapper from. `"*"` lets any website on the
  internet spend your key.
- **Add a rate limit.** Cloudflare's dashboard (WAF → Rate limiting rules) can cap requests per IP
  without touching the Worker code. Even a loose cap turns a runaway loop into a bounded cost.
- **Set a spend cap** on the upstream account/key so a mistake can't run unbounded.
- **Consider a shared-secret header** if the mapper is behind your own auth: have the page send a header
  your Worker checks before forwarding. (This raises the bar; it is not a substitute for origin-pinning,
  since anything the browser holds is readable.)
- **Watch the logs** for the first few days. `wrangler tail` streams live requests.

None of this touches the deterministic core — it is only about protecting the paid model calls the
proxy fronts.

---

## Live data sync (`REGISTER_API`) — no proxy needed

`REGISTER_API` is unrelated to the AI proxy: it pulls the newest register data instead of the bundled
snapshot, and it reads **plain static JSON with no auth**. Point it at a deployed copy of this repo's
[`api/`](../api/) directory:

```js
const REGISTER_API = "https://<user>.github.io/<repo>/api";
```

The mapper fetches `records.json` and `meta.json` from that base, recomputes the citable subset by the
same invariant the register uses (`tier1_legal ∧ in_force ∧ resolution_text`), and swaps the
snapshot banner from "frozen" to "live." If the fetch fails, it silently keeps the bundled snapshot —
so a broken or offline `REGISTER_API` never degrades the tool; it just falls back to what's embedded.

To publish the `api/` directory, serve it from any static host (the build already emits it; GitHub
Pages pointed at `/api/` is the zero-cost path). Because it's static JSON, there is nothing to
authenticate and nothing to protect.

---

## Quick reference

| You want to… | Set | Needs a key? | Fails safe if broken? |
|---|---|---|---|
| Host the tool as-is | *(nothing)* | No | — (no network) |
| Serve fresh register data | `REGISTER_API` | No | Yes → bundled snapshot |
| Enable import / auto-map off-sandbox | `LLM_PROXY` | Yes (in the proxy) | Yes → manual mode + banner |
| Wire up the contact CTA | `CONTACT` | No | — |

The deterministic core never depends on any of these. Everything networked degrades to the bundled,
offline behavior when it's absent or unreachable.
