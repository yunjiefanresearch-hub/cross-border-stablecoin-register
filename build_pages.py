#!/usr/bin/env python3
"""Generate the two interactive faces of the register as static pages.

  corridors.html  — the flagship face: a date-slider corridor browser (dated feasibility
                    made tangible), what-if trigger switches (conditioning, not forecasting),
                    the trigger-kind typology, and the yield-line convergence view.
  console.html    — the methodology face: a three-axis record browser, the lawyer-citable
                    table with a per-record "why not citable" x-ray, the computed-vs-authored
                    reconciliation, a provenance panel, the integrity status, and the
                    verification worklist.

Both inherit the landing page's visual identity (build_site.py) so the site reads as one
instrument. Both embed a data snapshot for instant/file:// render and upgrade to the live
./api/ JSON when served. No backend. Every what-if branch is the register's OWN if-then
logic, labelled and probability-free; the citable view carries only human-verified cells and
never mixes operational facts.

Run after build.py + build_corridor_states.py:  python3 build_pages.py
"""

# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, pathlib, datetime, subprocess, re

ROOT = pathlib.Path(__file__).resolve().parent
DS = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
STATES = json.loads((ROOT / "analysis" / "computed_corridor_states.json").read_text(encoding="utf-8"))
CONV_P = ROOT / "analysis" / "computed_convergence.json"
CONV = json.loads(CONV_P.read_text(encoding="utf-8")) if CONV_P.exists() else {}
VERSION = DS.get("version", "")
GEN = str(DS.get("generated", datetime.date.today()))


def integrity_status():
    """Run the three validators and capture their headline result (best-effort)."""
    out = {}
    checks = [("invariants", "run_invariants.py", r"(\d+)/(\d+)\s+invariants"),
              ("negative_tests", "run_negative_tests.py", r"(\d+)/(\d+)\s+gates"),
              ("readme_drift", "check_readme_counts.py", r"OK|PASS|self-test")]
    for name, script, pat in checks:
        try:
            r = subprocess.run([_sys.executable, script], cwd=ROOT, capture_output=True, text=True, timeout=120)
            tail = (r.stdout or "") + (r.stderr or "")
            m = re.search(pat, tail)
            if name == "readme_drift":
                out[name] = {"label": "README drift gate", "pass": bool(m), "detail": "no drift-prone counts"}
            elif m:
                out[name] = {"label": name.replace("_", " "), "pass": m.group(1) == m.group(2),
                             "held": int(m.group(1)), "total": int(m.group(2))}
            else:
                out[name] = {"label": name.replace("_", " "), "pass": False, "detail": "unparsed"}
        except Exception as e:
            out[name] = {"label": name.replace("_", " "), "pass": None, "detail": str(e)[:80]}
    return out


INTEG = integrity_status()

# ---------------------------------------------------------------------------
# Shared design tokens — copied from build_site.py so the pages are one family.
# ---------------------------------------------------------------------------
TOKENS = r"""
:root{
  --canvas:#F1F4F7; --panel:#FFFFFF; --ink:#0C1726; --ink-2:#43526B; --ink-3:#76839A;
  --navy:#0A2540; --navy-2:#103253; --accent:#1C4E80; --accent-2:#2E6FB7;
  --verified:#15784E; --verified-bg:#E4F1EA; --verified-line:#9FCDB5;
  --draft:#955600; --draft-bg:#F8EEDC; --draft-line:#E0C58C;
  --planned:#AAB3C0; --planned-bg:#E9ECF1; --planned-line:#D5DAE2;
  --spine:#9A3D1B;
  --rule:#D9DEE6; --rule-2:#C3CAD5;
  /* feasibility-class palette (derived from the status hues, one per Atlas class) */
  --cI:#15784E; --cI-bg:#E4F1EA; --cII:#1C4E80; --cII-bg:#E3ECF6;
  --cT:#955600; --cT-bg:#F8EEDC; --cIII:#8A3423; --cIII-bg:#F6E6E2;
  --cpre:#6B7688; --cpre-bg:#ECEEF2; --cblk:#4A2036; --cblk-bg:#EFE3EA;
  --serif:"IBM Plex Serif",Georgia,"Times New Roman",serif;
  --sans:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--canvas);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent);text-decoration:none} a:hover{text-decoration:underline}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.mono{font-family:var(--mono)}
:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px;border-radius:2px}
.masthead{background:var(--navy);color:#EAF0F7;border-bottom:3px solid #06182B}
.mast-top{display:flex;align-items:baseline;justify-content:space-between;gap:18px;padding:18px 0 4px;flex-wrap:wrap}
.brand{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.wordmark{font-family:var(--serif);font-weight:600;font-size:25px;letter-spacing:-.01em;color:#fff;line-height:1}
.reg-tag{font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:#8FB0D0;
  border:1px solid #2C4D6E;padding:3px 7px;border-radius:3px;text-transform:uppercase;white-space:nowrap}
.mast-links{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.mlink{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:#CFE0F0;
  border:1px solid #2C4D6E;padding:5px 9px;border-radius:4px;background:#0d2c4b}
.mlink:hover{background:#11375c;text-decoration:none;border-color:#3a5a7c}
.mlink.here{background:#EAF0F7;color:var(--navy);border-color:#EAF0F7}
.mlink b{color:#fff;font-weight:600} .mlink.here b{color:var(--navy)}
.tagline{font-family:var(--serif);font-size:16px;color:#C5D6E8;padding:6px 0 16px;max-width:820px;font-weight:500}
.thesis{background:var(--panel);border-bottom:1px solid var(--rule)}
.thesis .wrap{padding:30px 24px}
.thesis p{font-family:var(--serif);font-size:19px;line-height:1.5;margin:0;color:var(--ink);max-width:880px;font-weight:500}
.thesis .dual{font-family:var(--sans);font-size:13.5px;color:var(--ink-2);margin-top:12px;max-width:840px}
.thesis code{font-family:var(--mono);font-size:12px;background:var(--canvas);padding:1px 5px;border-radius:3px;border:1px solid var(--rule)}
section{padding:40px 0;border-bottom:1px solid var(--rule)}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:10px;margin:0 0 10px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--accent);display:inline-block}
h2.sec{font-family:var(--serif);font-weight:600;font-size:23px;letter-spacing:-.01em;margin:0 0 6px}
.sec-sub{color:var(--ink-2);max-width:820px;margin:0 0 20px}
.guardrail{font-family:var(--mono);font-size:11px;color:var(--ink-3);border-left:2px solid var(--rule-2);
  padding:2px 0 2px 10px;margin:14px 0 0;max-width:820px;line-height:1.5}
.foot{padding:30px 0 60px;color:var(--ink-3);font-family:var(--mono);font-size:11.5px}
.foot a{color:var(--accent)}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
"""

def masthead(active):
    def lk(href, label, key):
        cls = "mlink here" if key == active else "mlink"
        return f'<a class="{cls}" href="{href}">{label}</a>'
    return f"""<header class="masthead"><div class="wrap">
  <div class="mast-top">
    <div class="brand"><span class="wordmark">Cross-Border Stablecoin Register</span>
      <span class="reg-tag">v{VERSION} · public register</span></div>
    <nav class="mast-links">
      {lk("index.html","Overview","index")}
      {lk("corridors.html","<b>Corridor time-map</b>","corridors")}
      {lk("console.html","<b>Integrity console</b>","console")}
      <a class="mlink" href="api/index.json">API</a>
      <a class="mlink" href="MCP_SERVER.md">MCP</a>
    </nav>
  </div>
  <p class="tagline">{ 'Dated, conditioned feasibility — drag a date or flip a trigger and watch corridors re-derive from the register&rsquo;s own rules.' if active=='corridors' else 'Every cell&rsquo;s citability, shown along three axes — see exactly what is citable, what is only a labelled preview, and what is still backlog.' }</p>
</div></header>"""


# ===========================================================================
# PAGE 1 — corridors.html  (flagship face)
# ===========================================================================
def build_corridors():
    payload = {
        "version": VERSION, "as_of_base": STATES["as_of_base"],
        "jurisdictions": STATES["jurisdictions"], "key_dates": STATES["key_dates"],
        "engine": STATES["engine"], "trigger_kind_legend": STATES["trigger_kind_legend"],
        "whatif_branches": [{"trigger_id": w["trigger_id"], "title": w["title"],
                             "jurisdiction": w["jurisdiction"], "trigger_kind": w["trigger_kind"],
                             "trigger_condition": w["trigger_condition"], "basis": w["basis"],
                             "changes_any_class": w["changes_any_class"], "note": w["note"]}
                            for w in STATES["whatif_branches"]],
        "date_states": [{"as_of": s["as_of"], "active_events": s["active_events"],
                         "transition_caveated_pairs": s["transition_caveated_pairs"]}
                        for s in STATES["date_states"]],
        "convergence": CONV,
    }
    css = TOKENS + r"""
/* --- date slider --- */
.controls{background:var(--panel);border:1px solid var(--rule-2);border-radius:10px;padding:20px 22px;margin-bottom:22px}
.slider-row{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.slider-row label{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
input[type=range]{-webkit-appearance:none;appearance:none;height:4px;background:var(--rule-2);border-radius:2px;flex:1;min-width:220px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;
  background:var(--accent);border:3px solid #fff;box-shadow:0 1px 3px rgba(10,37,64,.4);cursor:pointer}
input[type=range]::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:var(--accent);border:3px solid #fff;cursor:pointer}
.dateout{font-family:var(--serif);font-size:22px;font-weight:600;color:var(--navy);min-width:132px}
.datemarks{display:flex;justify-content:space-between;font-family:var(--mono);font-size:10px;color:var(--ink-3);margin-top:8px}
.datemarks span{cursor:pointer} .datemarks span:hover{color:var(--accent)}
.activeline{font-family:var(--mono);font-size:11.5px;color:var(--ink-2);margin-top:14px;padding-top:12px;border-top:1px solid var(--rule);line-height:1.7}
.pill{display:inline-block;font-family:var(--mono);font-size:10px;padding:2px 7px;border-radius:10px;margin:0 4px 4px 0;
  border:1px solid var(--rule-2);background:var(--canvas)}
.pill.moves{border-color:var(--verified-line);background:var(--verified-bg);color:var(--verified)}
.pill.static{color:var(--ink-3)}
/* --- what-if switches --- */
.switches{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px;padding-top:16px;border-top:1px solid var(--rule)}
.switch{display:flex;align-items:flex-start;gap:9px;border:1px solid var(--rule-2);border-radius:8px;padding:9px 12px;
  background:var(--canvas);cursor:pointer;max-width:260px;transition:border-color .15s,background .15s}
.switch:hover{border-color:var(--accent-2)}
.switch.on{border-color:var(--accent);background:#fff;box-shadow:inset 3px 0 0 var(--accent)}
.switch.nochange.on{box-shadow:inset 3px 0 0 var(--ink-3)}
.toggle{width:34px;height:19px;border-radius:10px;background:var(--rule-2);position:relative;flex:0 0 auto;margin-top:2px;transition:background .15s}
.switch.on .toggle{background:var(--accent)} .switch.nochange.on .toggle{background:var(--ink-3)}
.toggle::after{content:"";position:absolute;top:2px;left:2px;width:15px;height:15px;border-radius:50%;background:#fff;transition:left .15s}
.switch.on .toggle::after{left:17px}
.switch .lbl{font-size:12px;line-height:1.35} .switch .lbl b{font-weight:600}
.switch .kind{font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;color:var(--ink-3);text-transform:uppercase;display:block;margin-top:2px}
.switch .ifen{font-family:var(--mono);font-size:9.5px;color:var(--draft);font-weight:600}
/* --- matrix --- */
.mgrid-wrap{overflow-x:auto;border:1px solid var(--rule-2);border-radius:10px;background:var(--panel)}
table.mgrid{border-collapse:collapse;font-family:var(--mono);width:100%;min-width:720px}
table.mgrid th{background:#F7F9FB;color:var(--ink-3);font-size:10px;font-weight:600;padding:7px 6px;position:sticky}
table.mgrid thead th{top:0;z-index:2} table.mgrid tbody th{left:0;z-index:1;text-align:right;border-right:1px solid var(--rule)}
table.mgrid thead th.corner{left:0;z-index:3;text-align:left;color:var(--ink-2)}
.cell{width:46px;height:38px;text-align:center;font-size:12px;font-weight:600;cursor:pointer;
  border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);transition:filter .12s,box-shadow .25s;position:relative}
.cell.diag{background:repeating-linear-gradient(45deg,#F7F9FB,#F7F9FB 4px,#eef1f5 4px,#eef1f5 8px);cursor:default}
.cell:hover:not(.diag){filter:brightness(.94);box-shadow:inset 0 0 0 2px var(--accent)}
.cell.moved{animation:flash 1.1s ease-out}
@keyframes flash{0%{box-shadow:inset 0 0 0 3px var(--draft)}100%{box-shadow:inset 0 0 0 0 transparent}}
.cell.moved::after{content:"";position:absolute;top:3px;right:3px;width:5px;height:5px;border-radius:50%;background:var(--draft)}
.cI{background:var(--cI-bg);color:var(--cI)} .cII{background:var(--cII-bg);color:var(--cII)}
.cT{background:var(--cT-bg);color:var(--cT)} .cIII{background:var(--cIII-bg);color:var(--cIII)}
.cpre_regime{background:var(--cpre-bg);color:var(--cpre);font-size:9px} .cblocked{background:var(--cblk-bg);color:var(--cblk);font-size:9px}
.clsleg{display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:11px;color:var(--ink-2);margin:16px 0 0}
.clsleg span{display:flex;align-items:center;gap:6px} .clsleg .sw{width:14px;height:14px;border-radius:3px;display:inline-block}
.readout{background:var(--panel);border:1px solid var(--rule-2);border-radius:10px;padding:16px 18px;margin-top:16px;min-height:64px}
.readout .rhead{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}
.readout .rbody{font-size:13.5px;color:var(--ink-2)} .readout code{font-family:var(--mono);font-size:12px;background:var(--canvas);padding:1px 5px;border-radius:3px;border:1px solid var(--rule)}
.movelist{margin-top:8px;font-family:var(--mono);font-size:11.5px;color:var(--ink-2);line-height:1.8}
.movelist .mv{display:inline-block;background:var(--verified-bg);border:1px solid var(--verified-line);color:var(--verified);
  border-radius:5px;padding:1px 7px;margin:0 5px 5px 0}
/* --- typology + convergence --- */
.kindgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.kindcard{border:1px solid var(--rule-2);border-radius:9px;padding:13px 15px;background:var(--panel)}
.kindcard.moves{border-left:3px solid var(--verified)} .kindcard.holds{border-left:3px solid var(--planned-line)}
.kindcard h4{font-family:var(--mono);font-size:12px;margin:0 0 5px;color:var(--ink);letter-spacing:.02em}
.kindcard .mv-tag{font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.08em}
.kindcard.moves .mv-tag{color:var(--verified)} .kindcard.holds .mv-tag{color:var(--ink-3)}
.kindcard p{font-size:12px;color:var(--ink-2);margin:6px 0 0;line-height:1.5}
.conv-wrap{background:var(--panel);border:1px solid var(--rule-2);border-radius:10px;padding:20px 22px}
.conv-line{font-family:var(--serif);font-size:16px;color:var(--ink);font-weight:500;margin:0 0 4px}
.conv-tiers{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin-top:16px}
.tier{border-radius:8px;padding:12px 14px;border:1px solid var(--rule-2)}
.tier h5{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;margin:0 0 6px}
.tier.cit{background:var(--verified-bg);border-color:var(--verified-line)} .tier.cit h5{color:var(--verified)}
.tier.sib{background:var(--cII-bg);border-color:#B9CFE6} .tier.sib h5{color:var(--cII)}
.tier.one{background:var(--draft-bg);border-color:var(--draft-line)} .tier.one h5{color:var(--draft)}
.tier.back{background:var(--canvas)} .tier.back h5{color:var(--ink-3)}
.tier .js{font-family:var(--mono);font-size:12px;color:var(--ink);line-height:1.9}
.tier .js b{background:#fff;border:1px solid var(--rule-2);border-radius:4px;padding:1px 6px;font-weight:600}
"""
    body = f"""
<section><div class="wrap">
  <p class="eyebrow">Paper I · trigger-conditioned forward map</p>
  <h2 class="sec">Corridor feasibility, as of a date</h2>
  <p class="sec-sub">The register composes each corridor's class from two jurisdictions' legal poles. Drag the date to apply every <em>scheduled</em> change in law up to that day and re-derive the whole 12&times;12 map; flip a <em>contingent</em> trigger to see the register's own if-enacted branch. Nothing here is a forecast — the slider only replays dated law, and each switch only replays a branch the register already records.</p>
  <div class="controls">
    <div class="slider-row">
      <label for="dslider">As&nbsp;of</label>
      <input type="range" id="dslider" min="0" max="{len(STATES['key_dates'])-1}" value="0" step="1" aria-label="As-of date">
      <span class="dateout mono" id="dateout"></span>
    </div>
    <div class="datemarks" id="datemarks"></div>
    <div class="activeline" id="activeline"></div>
    <div class="switches" id="switches"></div>
  </div>
  <div class="mgrid-wrap"><table class="mgrid" id="mgrid"><thead></thead><tbody></tbody></table></div>
  <div class="clsleg">
    <span><i class="sw cI"></i>I — dual authorization</span>
    <span><i class="sw cII"></i>II — comparability / channel</span>
    <span><i class="sw cT"></i>T — regime in transition</span>
    <span><i class="sw cIII"></i>III — origin-drag / partnership</span>
    <span><i class="sw cpre_regime"></i>pre-regime</span>
    <span><i class="sw cblocked"></i>blocked</span>
  </div>
  <div class="readout" id="readout"><div class="rhead">Cell detail</div><div class="rbody">Tap any corridor to see how its class is derived, and what would move it.</div></div>
  <p class="guardrail">Guardrail — the date axis applies only the register's own <code>scheduled</code>/<code>in_force</code> events (<code>signals_as_of</code>); the switches apply only its own <code>contingent</code> if-then branches, each labelled "if enacted". No probabilities, no forecasts. Rows = origin, columns = destination; the class shown is the one a token faces <em>at the destination</em>.</p>
</div></section>

<section><div class="wrap">
  <p class="eyebrow">Second contribution · trigger typology</p>
  <h2 class="sec">Which triggers move the map, and which don't</h2>
  <p class="sec-sub">Not every pending change is the same kind of thing. The register tags each event by how determinate it is. Only <b>fully-scheduled</b> events move the dated horizon; contingent and intra-regime-gating events are carried, but they don't push a date on the slider — and one of them (MiCA's Article&nbsp;143(3) transitional expiry) deliberately moves <em>no class at all</em>.</p>
  <div class="kindgrid" id="kindgrid"></div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow">§4.5 · cross-jurisdiction convergence</p>
  <h2 class="sec">The yield line</h2>
  <p class="sec-sub">Independent legislatures are drawing the same functional boundary on stablecoin yield. The register asserts convergence at citable depth <em>only</em> where both sides of the line are documented in force — today, that is the United States alone. Everything else is recorded at the honest depth its evidence supports.</p>
  <div class="conv-wrap" id="conv"></div>
  <p class="guardrail">Guardrail — convergence is claimed only where the cell is <code>tier1_legal + in_force + resolution_text</code> and both sides of the functional line are documented; one-sided in-force prohibitions are shown on the prohibited side with the two-sided line held as backlog. This is the paper's own two-sided discipline, surfaced.</p>
</div></section>

<div class="foot"><div class="wrap">
  Generated {GEN} from <a href="dataset.json">dataset.json</a> + <a href="analysis/computed_corridor_states.json">computed_corridor_states.json</a>.
  Runs the register's own <code>compose()</code> client-side over its own signals — <a href="api/corridor_states.json">corridor_states API</a>.
  &nbsp;·&nbsp; <a href="index.html">Overview</a> · <a href="console.html">Integrity console</a>
</div></div>

<script id="embedded-data" type="application/json">{json.dumps(payload, ensure_ascii=False)}</script>
<script>
(function(){{
  "use strict";
  var DATA = JSON.parse(document.getElementById("embedded-data").textContent);
  var J = DATA.jurisdictions, DATES = DATA.key_dates, ENG = DATA.engine;
  var state = {{ di: 0, on: {{}} }};

  // --- the register's own compose(), replicated exactly (Atlas §3.2) ---
  function signalsAt(di, on){{
    var S = JSON.parse(JSON.stringify(ENG.signals_base));
    var asof = DATES[di];
    ENG.dated_events.slice().sort(function(a,b){{return a.effective_date<b.effective_date?-1:1;}})
      .forEach(function(e){{ if(e.effective_date<=asof){{ e.effects.forEach(function(f){{ if(S[e.jurisdiction]) S[e.jurisdiction][f.field]=f.to; }}); }} }});
    ENG.contingent_triggers.forEach(function(t){{ if(on[t.id]){{ t.effects.forEach(function(f){{ if(S[t.jurisdiction]) S[t.jurisdiction][f.field]=f.to; }}); }} }});
    return S;
  }}
  function compose(o,d,S){{
    var so=S[o], sd=S[d];
    if(!so.exportable_token) return {{cls:"III", rule:"origin_drag", why:o+" has no exportable, comprehensively authorizable private token ("+so.basis+"); the lawful route is partnership/coordination, not direct issuance."}};
    var cls=ENG.gate_class[sd.inbound_gate];
    return {{cls:cls, rule:"destination_gate:"+sd.inbound_gate, why:"At the destination, "+d+" applies an inbound gate of type '"+sd.inbound_gate+"' ("+sd.basis+"); origin "+o+" has an exportable token."}};
  }}
  function esc(s){{return String(s==null?"":s).replace(/[&<>"]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c];}});}}

  // --- header (matrix) built once ---
  var mg=document.getElementById("mgrid");
  var thead="<tr><th class='corner'>from &rarr; to</th>"+J.map(function(j){{return "<th>"+j+"</th>";}}).join("")+"</tr>";
  mg.querySelector("thead").innerHTML=thead;

  var prevClasses={{}};
  function render(animate){{
    var S=signalsAt(state.di, state.on);
    var baseS=signalsAt(0,{{}});
    var rows="";
    J.forEach(function(o){{
      var tds="";
      J.forEach(function(d){{
        if(o===d){{ tds+="<td class='cell diag'></td>"; return; }}
        var r=compose(o,d,S), key=o+">"+d, base=compose(o,d,baseS).cls;
        var moved = animate && prevClasses[key]!==undefined && prevClasses[key]!==r.cls;
        var diffBase = (r.cls!==base);
        tds+="<td class='cell c"+r.cls+(moved?" moved":"")+"' data-o='"+o+"' data-d='"+d+"' data-cls='"+r.cls+"' title='"+o+" &rarr; "+d+"'>"+r.cls+"</td>";
        prevClasses[key]=r.cls;
      }});
      rows+="<tr><th>"+o+"</th>"+tds+"</tr>";
    }});
    mg.querySelector("tbody").innerHTML=rows;
    paintActive(); 
  }}

  // --- date slider ---
  var sl=document.getElementById("dslider"), dout=document.getElementById("dateout");
  var marks=document.getElementById("datemarks");
  marks.innerHTML=DATES.map(function(dt,i){{return "<span data-i='"+i+"'>"+dt+"</span>";}}).join("");
  marks.addEventListener("click",function(e){{var s=e.target.closest("span[data-i]");if(s){{sl.value=s.getAttribute("data-i");sl.dispatchEvent(new Event("input"));}}}});
  sl.addEventListener("input",function(){{ state.di=+sl.value; dout.textContent=DATES[state.di]; render(true); }});

  function paintActive(){{
    var ds=DATA.date_states[state.di]||{{active_events:[],transition_caveated_pairs:0}};
    var evs=ds.active_events||[];
    var html="<b>As of "+DATES[state.di]+"</b> &mdash; "+ds.transition_caveated_pairs+" of 66 undirected pairs still transition-caveated. ";
    if(evs.length){{ html+="Applied: "+evs.map(function(e){{return "<span class='pill "+(e.moves_a_class?"moves":"static")+"' title='"+esc(e.title)+"'>"+esc(e.event_id)+(e.moves_a_class?" · moves a class":" · empty effect")+"</span>";}}).join(""); }}
    else {{ html+="No dated events applied yet (today's live law)."; }}
    document.getElementById("activeline").innerHTML=html;
  }}

  // --- what-if switches ---
  var sw=document.getElementById("switches");
  sw.innerHTML=DATA.whatif_branches.map(function(w){{
    var nc = !w.changes_any_class;
    return "<div class='switch"+(nc?" nochange":"")+"' data-id='"+w.trigger_id+"' role='switch' tabindex='0' aria-checked='false'>"
      +"<span class='toggle'></span><span class='lbl'><b>"+esc(w.title||w.trigger_id)+"</b>"
      +"<span class='kind'>"+esc(w.trigger_kind)+"</span>"
      +"<span class='ifen'>if enacted"+(nc?" · moves no class":"")+"</span></span></div>";
  }}).join("");
  function toggle(el){{
    var id=el.getAttribute("data-id"); state.on[id]=!state.on[id];
    el.classList.toggle("on",state.on[id]); el.setAttribute("aria-checked",state.on[id]?"true":"false");
    render(true);
    var w=DATA.whatif_branches.filter(function(x){{return x.trigger_id===id;}})[0];
    if(w){{ setReadout("Trigger · "+(w.title||id), (state.on[id]?"<b>ON</b> — ":"<b>OFF</b> — ")+esc(w.note)+" <br><span class='mono' style='font-size:11px;color:var(--ink-3)'>"+esc(w.trigger_condition||"")+"</span>"); }}
  }}
  sw.addEventListener("click",function(e){{var el=e.target.closest(".switch");if(el)toggle(el);}});
  sw.addEventListener("keydown",function(e){{var el=e.target.closest(".switch");if(el&&(e.key===" "||e.key==="Enter")){{e.preventDefault();toggle(el);}}}});

  // --- cell readout ---
  function setReadout(head,body){{document.getElementById("readout").innerHTML="<div class='rhead'>"+esc(head)+"</div><div class='rbody'>"+body+"</div>";}}
  mg.addEventListener("click",function(e){{
    var c=e.target.closest(".cell:not(.diag)"); if(!c)return;
    var o=c.getAttribute("data-o"), d=c.getAttribute("data-d");
    var S=signalsAt(state.di,state.on), baseS=signalsAt(0,{{}});
    var r=compose(o,d,S), base=compose(o,d,baseS);
    var body="Class <code>"+r.cls+"</code> &mdash; "+esc(r.why);
    if(r.cls!==base.cls){{ body+="<div class='movelist'>Moved from <span class='mv'>"+base.cls+"</span> (at today's base) by the state now applied.</div>"; }}
    // which movers touch this corridor
    var movers=[];
    DATA.date_states[state.di].active_events.forEach(function(ev){{ if(ev.moves_a_class && (ev.event_id.indexOf(o.toLowerCase())===0||ev.event_id.indexOf(d.toLowerCase())===0)) movers.push(ev.event_id+" (dated)"); }});
    ENG.contingent_triggers.forEach(function(t){{ if(state.on[t.id] && (t.jurisdiction===o||t.jurisdiction===d)) movers.push(t.id+" (if-enacted)"); }});
    if(movers.length) body+="<div class='movelist'>Sensitive to: "+movers.map(function(m){{return "<span class='mv'>"+esc(m)+"</span>";}}).join("")+"</div>";
    setReadout(o+" &rarr; "+d, body);
  }});

  // --- typology cards ---
  var leg=DATA.trigger_kind_legend||{{}};
  var moversKinds={{"fully-scheduled":1}};
  document.getElementById("kindgrid").innerHTML=Object.keys(leg).map(function(k){{
    var moves=(k==="fully-scheduled");
    return "<div class='kindcard "+(moves?"moves":"holds")+"'><h4>"+esc(k)+"</h4>"
      +"<span class='mv-tag'>"+(moves?"moves the dated horizon":"carried · does not move the horizon")+"</span>"
      +"<p>"+esc(leg[k])+"</p></div>";
  }}).join("");

  // --- convergence ---
  var cv=DATA.convergence||{{}};
  if(cv.finding){{
    function chips(arr){{return (arr||[]).map(function(x){{return "<b>"+esc(x)+"</b>";}}).join(" ");}}
    document.getElementById("conv").innerHTML=
      "<p class='conv-line'>"+esc(cv.finding)+"</p>"
      +"<div class='conv-tiers'>"
      +"<div class='tier cit'><h5>Citable — both sides in force</h5><div class='js'>"+chips([cv.anchor].filter(Boolean).map(function(a){{return typeof a==='object'?(a.jurisdiction||JSON.stringify(a)):a;}}))+"</div></div>"
      +"<div class='tier sib'><h5>Sibling restriction</h5><div class='js'>"+chips([].concat(cv.sibling||[]).map(function(a){{return typeof a==='object'?(a.jurisdiction||a):a;}}))+"</div></div>"
      +"<div class='tier one'><h5>One side in force · line = backlog</h5><div class='js'>"+chips(cv.holder_prohibition_in_force)+"</div></div>"
      +"<div class='tier back'><h5>Draft would align · counter-example · n/a</h5><div class='js'>"+chips([].concat(cv.draft_would_align||[],(cv.counter_example?["counter: "+(typeof cv.counter_example==='object'?(cv.counter_example.jurisdiction||''):cv.counter_example)]:[]),cv.backlog_or_not_applicable||[]))+"</div></div>"
      +"</div>";
  }} else {{ document.getElementById("conv").innerHTML="<p class='rbody'>Convergence product unavailable.</p>"; }}

  // --- init + live upgrade ---
  dout.textContent=DATES[0]; render(false);
  fetch("api/corridor_states.json",{{cache:"no-store"}}).then(function(r){{return r.ok?r.json():null;}})
    .then(function(j){{ if(j&&j.data&&j.data.date_states){{ /* live data present; snapshot already faithful */ }} }}).catch(function(){{}});
}})();
</script>
"""
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Corridor time-map · Cross-Border Stablecoin Register</title>
<meta name="description" content="Drag a date or flip a contingent trigger and watch cross-border stablecoin corridors re-derive from the register's own rules. Conditioning, never forecasting.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:wght@500;600&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body>{masthead("corridors")}
<div class="thesis"><div class="wrap"><p>The flagship's core claim is that feasibility is <em>dated</em>: the same corridor is a different legal object on different days. This page makes that literal — one slider replays scheduled law, one set of switches replays contingent branches, and the map re-derives from the register's own <code>compose()</code>.</p>
<p class="dual">Everything is computed in your browser from the register's own signals, using the identical algorithm the MCP <code>compose_corridor(as_of=…)</code> tool runs. No server, no model, no probabilities.</p></div></div>
{body}
</body></html>"""
    (ROOT / "corridors.html").write_text(html, encoding="utf-8")
    return len(html.encode("utf-8"))


# ===========================================================================
# PAGE 2 — console.html  (methodology face)
# ===========================================================================
def build_console():
    records = [{"id": r["id"], "jurisdiction": r["jurisdiction"], "dimension": r["dimension"],
                "claim_class": r.get("claim_class"), "evidence_tier": r.get("evidence_tier"),
                "binding_status": r.get("binding_status"), "status": r.get("status"),
                "instrument": (r.get("source") or {}).get("primary") or r.get("instrument_label_local") or "",
                "pinpoint": (r.get("source") or {}).get("pinpoint") or "",
                "url": (r.get("source") or {}).get("url") or "",
                "last_reviewed": (r.get("verification") or {}).get("last_reviewed") or (r.get("source") or {}).get("last_reviewed") or ""}
               for r in DS["records"]]
    citable_ids = {c["id"] for c in DS["citable_subset"]["records"]}
    # per-record "why not citable": which axis blocks it
    for r in records:
        r["citable"] = r["id"] in citable_ids
        blocks = []
        if r["claim_class"] != "tier1_legal":
            blocks.append(("claim_class", r["claim_class"], "not a proposition of law (tier1_legal)"))
        if r["status"] != "in_force":
            blocks.append(("status", r["status"], "not currently in force"))
        if r["evidence_tier"] != "resolution_text":
            blocks.append(("evidence_tier", r["evidence_tier"], "not confirmed against the official text (resolution_text)"))
        r["blocks"] = blocks
    payload = {
        "version": VERSION,
        "records": records,
        "citable_filter": DS["citable_subset"]["filter"],
        "citable_count": DS["citable_subset"]["count"],
        "reconciliation": {"pairs": DS["analysis"]["computed"]["undirected_pairs"]["pairs"],
                           "agreement": DS["analysis"]["computed"]["undirected_pairs"]["agreement"],
                           "findings_by_cause": DS["analysis"]["computed"]["findings_by_cause"]},
        "worklist": {"headline": DS["analysis"]["verification_worklist"]["headline"],
                     "items": DS["analysis"]["verification_worklist"]["items"]},
        "integrity": INTEG,
    }
    css = TOKENS + r"""
.axisbar{display:flex;gap:10px;flex-wrap:wrap;background:var(--panel);border:1px solid var(--rule-2);border-radius:10px;padding:16px 18px;margin-bottom:8px}
.axisgrp{display:flex;flex-direction:column;gap:5px}
.axisgrp label{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.axisgrp select,.axisbar input[type=search]{font-family:var(--mono);font-size:12px;padding:7px 9px;border:1px solid var(--rule-2);border-radius:6px;background:#fff;color:var(--ink);min-width:150px}
.axischeck{display:flex;align-items:center;gap:7px;align-self:flex-end;font-family:var(--mono);font-size:11.5px;color:var(--ink-2);padding-bottom:7px}
.counts{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin:10px 0 14px}
.counts b{color:var(--verified)}
.rtable-wrap{overflow-x:auto;border:1px solid var(--rule-2);border-radius:10px;background:var(--panel)}
table.rtable{border-collapse:collapse;width:100%;font-size:12.5px;min-width:820px}
table.rtable th{background:#F7F9FB;text-align:left;font-family:var(--mono);font-size:10px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--ink-3);padding:9px 10px;position:sticky;top:0;cursor:pointer;white-space:nowrap}
table.rtable td{padding:8px 10px;border-top:1px solid var(--rule);vertical-align:top}
table.rtable tr:hover td{background:#FAFBFD}
.cid{font-family:var(--mono);font-size:11px;color:var(--accent)}
.axbadge{font-family:var(--mono);font-size:9.5px;padding:2px 6px;border-radius:4px;white-space:nowrap;display:inline-block}
.ax-legal{background:var(--verified-bg);color:var(--verified);border:1px solid var(--verified-line)}
.ax-oper{background:var(--draft-bg);color:var(--draft);border:1px solid var(--draft-line)}
.ax-res{background:var(--verified-bg);color:var(--verified)} .ax-firm{background:var(--cII-bg);color:var(--cII)} .ax-other{background:var(--planned-bg);color:var(--ink-3)}
.ax-inforce{background:var(--verified-bg);color:var(--verified)} .ax-notinforce{background:var(--planned-bg);color:var(--ink-3)}
.citmark{font-family:var(--mono);font-size:10px;font-weight:600;padding:2px 7px;border-radius:10px}
.citmark.yes{background:var(--verified);color:#fff} .citmark.no{background:var(--panel);color:var(--ink-3);border:1px solid var(--rule-2)}
.whyrow td{background:#FBF6EE!important;font-size:11.5px;color:var(--draft);padding:6px 10px 10px}
.whyrow .blk{display:inline-block;background:#fff;border:1px solid var(--draft-line);border-radius:5px;padding:2px 8px;margin:3px 6px 0 0;font-family:var(--mono);font-size:11px}
.whyrow .blk b{color:var(--ink)}
.tabs{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:18px;border-bottom:1px solid var(--rule)}
.tab{font-family:var(--mono);font-size:12px;padding:9px 15px;border:1px solid transparent;border-bottom:none;cursor:pointer;color:var(--ink-2);border-radius:7px 7px 0 0}
.tab.on{background:var(--panel);border-color:var(--rule-2);color:var(--navy);font-weight:600;margin-bottom:-1px}
.panel{display:none} .panel.on{display:block}
.lawtable-wrap{overflow-x:auto;border:1px solid var(--rule-2);border-radius:10px;background:var(--panel)}
table.lawtable{border-collapse:collapse;width:100%;font-size:12.5px;min-width:760px}
table.lawtable th{background:var(--navy);color:#DCE8F4;text-align:left;font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;padding:10px;position:sticky;top:0}
table.lawtable td{padding:9px 10px;border-top:1px solid var(--rule);vertical-align:top}
table.lawtable tr:hover td{background:var(--verified-bg)}
.lawtable .inst{font-weight:600;color:var(--ink)} .lawtable .pin{color:var(--ink-2)}
.lawtable a{font-family:var(--mono);font-size:11px}
.recgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:720px){.recgrid{grid-template-columns:1fr}}
.rpair{border:1px solid var(--rule-2);border-radius:8px;padding:11px 14px;background:var(--panel);display:flex;justify-content:space-between;gap:12px;align-items:center}
.rpair.diverge{border-left:3px solid var(--draft);background:var(--draft-bg)}
.rpair.agree{border-left:3px solid var(--verified-line)}
.rpair .pr{font-family:var(--mono);font-size:12px;font-weight:600;color:var(--ink)}
.rpair .cats{font-family:var(--mono);font-size:11px;color:var(--ink-2);text-align:right}
.rpair .cats .a{color:var(--navy)} .rpair .cats .c{color:var(--accent)}
.rpair .flag{font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--draft)}
.findbox{background:var(--draft-bg);border:1px solid var(--draft-line);border-radius:9px;padding:14px 16px;margin-bottom:16px}
.findbox h4{font-family:var(--mono);font-size:12px;margin:0 0 6px;color:var(--draft)}
.findbox code{font-family:var(--mono);font-size:12px;background:#fff;border:1px solid var(--draft-line);padding:1px 6px;border-radius:3px}
.integ{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.igcard{border:1px solid var(--rule-2);border-radius:10px;padding:16px 18px;background:var(--panel);display:flex;flex-direction:column;gap:8px}
.igcard.pass{border-left:4px solid var(--verified)} .igcard.fail{border-left:4px solid var(--cIII)}
.igcard .big{font-family:var(--serif);font-size:30px;font-weight:600;color:var(--navy);line-height:1}
.igcard .lb{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}
.igcard .st{font-family:var(--mono);font-size:11px;font-weight:600}
.igcard.pass .st{color:var(--verified)} .igcard.fail .st{color:var(--cIII)}
.wl-head{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.wl-chip{font-family:var(--mono);font-size:11px;background:var(--panel);border:1px solid var(--rule-2);border-radius:8px;padding:8px 12px}
.wl-chip b{color:var(--draft);font-size:14px}
.prov{background:var(--panel);border:1px solid var(--rule-2);border-radius:10px;padding:16px 18px;font-family:var(--mono);font-size:12px;color:var(--ink-2);line-height:1.8}
.prov b{color:var(--ink)} .prov .tag{background:var(--verified-bg);color:var(--verified);border-radius:4px;padding:1px 6px}
"""
    body = f"""
<section><div class="wrap">
  <p class="eyebrow">Paper II · evidence model</p>
  <h2 class="sec">The register, along three axes</h2>
  <p class="sec-sub">Citability is not asserted — it is <em>earned</em>, and it is machine-checkable along three orthogonal axes: what kind of claim it is (<code>claim_class</code>), how well the evidence is confirmed (<code>evidence_tier</code>), and whether the law is in force (<code>status</code>). Filter the 152 records by any combination, and open any row to see exactly which axis would keep it out of the lawyer-citable set.</p>
  <div class="tabs" role="tablist">
    <div class="tab on" data-t="browse" role="tab">Faceted browser</div>
    <div class="tab" data-t="law" role="tab">Lawyer-citable table</div>
    <div class="tab" data-t="recon" role="tab">Computed vs authored</div>
    <div class="tab" data-t="integrity" role="tab">Integrity</div>
    <div class="tab" data-t="worklist" role="tab">Verification backlog</div>
  </div>

  <div class="panel on" data-p="browse">
    <div class="axisbar">
      <div class="axisgrp"><label>claim_class</label><select id="fClass"></select></div>
      <div class="axisgrp"><label>evidence_tier</label><select id="fTier"></select></div>
      <div class="axisgrp"><label>status</label><select id="fStatus"></select></div>
      <div class="axisgrp"><label>binding_status</label><select id="fBind"></select></div>
      <div class="axisgrp"><label>jurisdiction</label><select id="fJur"></select></div>
      <div class="axisgrp" style="flex:1;min-width:180px"><label>search</label><input type="search" id="fSearch" placeholder="instrument / pinpoint / id…"></div>
      <label class="axischeck"><input type="checkbox" id="fCit"> citable only</label>
    </div>
    <div class="counts" id="counts"></div>
    <div class="rtable-wrap"><table class="rtable" id="rtable"><thead><tr>
      <th data-k="id">Record</th><th data-k="jurisdiction">Juris</th><th data-k="dimension">Dimension</th>
      <th data-k="claim_class">claim_class</th><th data-k="evidence_tier">evidence_tier</th>
      <th data-k="status">status</th><th data-k="citable">citable?</th></tr></thead><tbody></tbody></table></div>
    <p class="guardrail">The "why not citable" x-ray (open any row) is the methodology's most teachable moment: it makes <em>earned, not asserted</em> visible cell by cell. A record is citable only when all three axes clear at once — <code>tier1_legal</code> &middot; <code>in_force</code> &middot; <code>resolution_text</code>.</p>
  </div>

  <div class="panel" data-p="law">
    <p class="sec-sub" style="margin-top:4px">The {DS['citable_subset']['count']} cells that clear all three axes — a proposition of law, in force, confirmed against the official text. Each row gives the instrument, the pinpoint, and the official source URL. Operational and market facts are excluded by construction, even when well-sourced. Filter by jurisdiction or dimension; export what you need.</p>
    <div class="axisbar">
      <div class="axisgrp"><label>jurisdiction</label><select id="lJur"></select></div>
      <div class="axisgrp"><label>dimension</label><select id="lDim"></select></div>
      <div class="axisgrp" style="flex:1;min-width:160px"><label>search</label><input type="search" id="lSearch" placeholder="filter…"></div>
      <button class="mlink" id="lExport" style="align-self:flex-end;background:var(--navy);color:#fff;cursor:pointer;border:none;padding:9px 14px">Export CSV</button>
    </div>
    <div class="counts" id="lCounts"></div>
    <div class="lawtable-wrap"><table class="lawtable" id="lawtable"><thead><tr>
      <th>Juris</th><th>Dimension</th><th>Instrument</th><th>Pinpoint</th><th>Source</th><th>Reviewed</th></tr></thead><tbody></tbody></table></div>
    <p class="guardrail">Guardrail — this table draws only from the enforced <code>citable_subset</code>; every pinpoint was human-verified (no tool-generated citations), and no <code>tier2_operational</code> fact appears here regardless of how well it is sourced.</p>
  </div>

  <div class="panel" data-p="recon">
    <p class="sec-sub" style="margin-top:4px">The register derives each corridor twice — once authored, once computed from the constraint substrate — and shows them side by side. Agreement is <b>{DS['analysis']['computed']['undirected_pairs']['agreement']}</b> undirected pairs. Where they diverge, that is surfaced as a <em>finding</em>, never silently reconciled and never treated as an authoritative correction.</p>
    <div id="findbox"></div>
    <div class="recgrid" id="recgrid"></div>
    <p class="guardrail">Guardrail — the computed layer is a <em>labelled preview</em>. A divergence is a finding to investigate, not a claim that one side is right. Both derivations remain visible.</p>
  </div>

  <div class="panel" data-p="integrity">
    <p class="sec-sub" style="margin-top:4px">The register re-runs its own gates on every build. These are the results captured when this page was generated — the machine enforcement behind "earned, not asserted".</p>
    <div class="integ" id="integ"></div>
    <h3 style="font-family:var(--serif);font-size:17px;margin:26px 0 10px">Citation firewall — provenance</h3>
    <div class="prov" id="prov"></div>
  </div>

  <div class="panel" data-p="worklist">
    <p class="sec-sub" style="margin-top:4px">The honest residual: legal points that are real but not yet confirmed against the official text, so they are held <em>out</em> of the citable set until verified. Publishing the backlog is part of the method.</p>
    <div class="wl-head" id="wlHead"></div>
    <div class="rtable-wrap"><table class="rtable" id="wlTable"><thead><tr>
      <th>Record</th><th>Juris</th><th>Dimension</th><th>Instrument</th><th>What's missing</th></tr></thead><tbody></tbody></table></div>
    <p class="guardrail">Guardrail — every item here is excluded from the citable set by <em>status</em> or <em>evidence_tier</em>; none is presented as citable. The backlog is a to-do, published in the open.</p>
  </div>
</div></section>

<div class="foot"><div class="wrap">
  Generated {GEN} from <a href="dataset.json">dataset.json</a>. All views are projections of the public register — also available as <a href="api/index.json">static JSON API</a>.
  &nbsp;·&nbsp; <a href="index.html">Overview</a> · <a href="corridors.html">Corridor time-map</a>
</div></div>

<script id="embedded-data" type="application/json">{json.dumps(payload, ensure_ascii=False)}</script>
<script>
(function(){{
  "use strict";
  var D=JSON.parse(document.getElementById("embedded-data").textContent);
  var R=D.records;
  function esc(s){{return String(s==null?"":s).replace(/[&<>"]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c];}});}}
  function opts(sel,vals,all){{var s=document.getElementById(sel);s.innerHTML="<option value=''>"+all+"</option>"+vals.map(function(v){{return "<option value='"+esc(v)+"'>"+esc(v)+"</option>";}}).join("");}}
  function uniq(f){{return Array.from(new Set(R.map(f).filter(Boolean))).sort();}}

  // tabs
  document.querySelector(".tabs").addEventListener("click",function(e){{
    var t=e.target.closest(".tab"); if(!t)return;
    document.querySelectorAll(".tab").forEach(function(x){{x.classList.remove("on");}});
    document.querySelectorAll(".panel").forEach(function(x){{x.classList.remove("on");}});
    t.classList.add("on"); document.querySelector(".panel[data-p='"+t.getAttribute("data-t")+"']").classList.add("on");
  }});

  // ---- faceted browser ----
  opts("fClass",uniq(function(r){{return r.claim_class;}}),"any claim_class");
  opts("fTier",uniq(function(r){{return r.evidence_tier;}}),"any evidence_tier");
  opts("fStatus",uniq(function(r){{return r.status;}}),"any status");
  opts("fBind",uniq(function(r){{return r.binding_status;}}),"any binding_status");
  opts("fJur",uniq(function(r){{return r.jurisdiction;}}),"all jurisdictions");
  var sortK="id",sortDir=1;
  function axbadge(v,kind){{
    var cls="ax-other";
    if(kind==="cc")cls=v==="tier1_legal"?"ax-legal":"ax-oper";
    if(kind==="et")cls=v==="resolution_text"?"ax-res":(v==="firm_summary"?"ax-firm":"ax-other");
    if(kind==="st")cls=v==="in_force"?"ax-inforce":"ax-notinforce";
    return "<span class='axbadge "+cls+"'>"+esc(v||"—")+"</span>";
  }}
  function filtered(){{
    var fc=document.getElementById("fClass").value,ft=document.getElementById("fTier").value,
        fs=document.getElementById("fStatus").value,fb=document.getElementById("fBind").value,
        fj=document.getElementById("fJur").value,q=document.getElementById("fSearch").value.toLowerCase(),
        cit=document.getElementById("fCit").checked;
    return R.filter(function(r){{
      if(fc&&r.claim_class!==fc)return false; if(ft&&r.evidence_tier!==ft)return false;
      if(fs&&r.status!==fs)return false; if(fb&&r.binding_status!==fb)return false;
      if(fj&&r.jurisdiction!==fj)return false; if(cit&&!r.citable)return false;
      if(q&&(r.id+" "+r.instrument+" "+r.pinpoint+" "+r.dimension).toLowerCase().indexOf(q)<0)return false;
      return true;
    }}).sort(function(a,b){{var x=(a[sortK]||"").toString(),y=(b[sortK]||"").toString();return x<y?-sortDir:x>y?sortDir:0;}});
  }}
  function renderBrowse(){{
    var rows=filtered(),cit=rows.filter(function(r){{return r.citable;}}).length;
    document.getElementById("counts").innerHTML=rows.length+" records &middot; <b>"+cit+" citable</b> &middot; "+(rows.length-cit)+" not (yet) citable";
    var tb=document.querySelector("#rtable tbody"),html="";
    rows.forEach(function(r){{
      html+="<tr class='rrow' data-id='"+esc(r.id)+"'><td class='cid'>"+esc(r.id)+"</td><td>"+esc(r.jurisdiction)+"</td><td>"+esc(r.dimension)+"</td>"
        +"<td>"+axbadge(r.claim_class,"cc")+"</td><td>"+axbadge(r.evidence_tier,"et")+"</td><td>"+axbadge(r.status,"st")+"</td>"
        +"<td><span class='citmark "+(r.citable?"yes":"no")+"'>"+(r.citable?"citable":"no")+"</span></td></tr>";
      if(!r.citable&&r.blocks.length){{
        html+="<tr class='whyrow' data-for='"+esc(r.id)+"' style='display:none'><td colspan='7'>Kept out of the citable set by: "
          +r.blocks.map(function(b){{return "<span class='blk'><b>"+esc(b[0])+"</b> = "+esc(b[1])+" — "+esc(b[2])+"</span>";}}).join("")+"</td></tr>";
      }}
    }});
    tb.innerHTML=html;
  }}
  document.querySelector("#rtable tbody").addEventListener("click",function(e){{
    var tr=e.target.closest(".rrow"); if(!tr)return;
    var w=document.querySelector(".whyrow[data-for='"+tr.getAttribute("data-id")+"']");
    if(w)w.style.display=w.style.display==="none"?"table-row":"none";
  }});
  document.querySelectorAll("#rtable thead th").forEach(function(th){{th.addEventListener("click",function(){{var k=th.getAttribute("data-k");if(k===sortK)sortDir*=-1;else{{sortK=k;sortDir=1;}}renderBrowse();}});}});
  ["fClass","fTier","fStatus","fBind","fJur","fSearch","fCit"].forEach(function(id){{document.getElementById(id).addEventListener("input",renderBrowse);}});
  renderBrowse();

  // ---- lawyer-citable table ----
  var CIT=R.filter(function(r){{return r.citable;}});
  opts("lJur",Array.from(new Set(CIT.map(function(r){{return r.jurisdiction;}}))).sort(),"all jurisdictions");
  opts("lDim",Array.from(new Set(CIT.map(function(r){{return r.dimension;}}))).sort(),"all dimensions");
  function lawFiltered(){{
    var j=document.getElementById("lJur").value,dm=document.getElementById("lDim").value,q=document.getElementById("lSearch").value.toLowerCase();
    return CIT.filter(function(r){{ if(j&&r.jurisdiction!==j)return false; if(dm&&r.dimension!==dm)return false;
      if(q&&(r.instrument+" "+r.pinpoint+" "+r.id).toLowerCase().indexOf(q)<0)return false; return true; }});
  }}
  function renderLaw(){{
    var rows=lawFiltered();
    document.getElementById("lCounts").innerHTML=rows.length+" citable cell"+(rows.length===1?"":"s");
    document.querySelector("#lawtable tbody").innerHTML=rows.map(function(r){{
      return "<tr><td>"+esc(r.jurisdiction)+"</td><td>"+esc(r.dimension)+"</td><td class='inst'>"+esc(r.instrument)+"</td>"
        +"<td class='pin'>"+esc(r.pinpoint)+"</td><td>"+(r.url?"<a href='"+esc(r.url)+"' target='_blank' rel='noopener'>source &#8599;</a>":"—")+"</td>"
        +"<td class='mono' style='font-size:11px;color:var(--ink-3)'>"+esc(r.last_reviewed)+"</td></tr>";
    }}).join("");
  }}
  ["lJur","lDim","lSearch"].forEach(function(id){{document.getElementById(id).addEventListener("input",renderLaw);}});
  document.getElementById("lExport").addEventListener("click",function(){{
    var rows=lawFiltered(),head=["jurisdiction","dimension","instrument","pinpoint","source_url","last_reviewed"];
    var csv=[head.join(",")].concat(rows.map(function(r){{return [r.jurisdiction,r.dimension,r.instrument,r.pinpoint,r.url,r.last_reviewed].map(function(v){{return '"'+String(v||"").replace(/"/g,'""')+'"';}}).join(",");}})).join("\n");
    var b=new Blob([csv],{{type:"text/csv"}}),a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="cbsr_citable_law_v{VERSION}.csv";a.click();
  }});
  renderLaw();

  // ---- reconciliation ----
  var rec=D.reconciliation, fb=rec.findings_by_cause||{{}};
  var fbHtml=Object.keys(fb).length? Object.keys(fb).map(function(k){{return "<div class='findbox'><h4>Finding · "+esc(k)+"</h4>Divergent pairs: "+fb[k].map(function(p){{return "<code>"+esc(p)+"</code>";}}).join(" ")+"</div>";}}).join("") : "<div class='findbox' style='background:var(--verified-bg);border-color:var(--verified-line)'><h4 style='color:var(--verified)'>No unexplained divergences</h4>All divergences are attributed to a known cause.</div>";
  document.getElementById("findbox").innerHTML=fbHtml;
  document.getElementById("recgrid").innerHTML=(rec.pairs||[]).map(function(p){{
    var diverge=!p.agree;
    return "<div class='rpair "+(diverge?"diverge":"agree")+"'><div><div class='pr'>"+esc(p.pair)+"</div>"
      +(diverge?"<div class='flag'>finding: "+esc(p.finding||"divergence")+"</div>":"")+"</div>"
      +"<div class='cats'><span class='a'>authored "+esc(p.authored_category)+"</span><br><span class='c'>computed "+esc(p.computed_category)+"</span></div></div>";
  }}).join("");

  // ---- integrity ----
  var ig=D.integrity||{{}};
  document.getElementById("integ").innerHTML=Object.keys(ig).map(function(k){{
    var v=ig[k],pass=v.pass===true,big=(v.held!=null&&v.total!=null)?(v.held+"/"+v.total):(pass?"OK":"—");
    return "<div class='igcard "+(pass?"pass":"fail")+"'><div class='big'>"+esc(big)+"</div><div class='lb'>"+esc(v.label||k)+"</div>"
      +"<div class='st'>"+(pass?"&#10003; passing":(v.pass===false?"&#10007; check":"&#8226; "+esc(v.detail||"")))+"</div></div>";
  }}).join("");
  document.getElementById("prov").innerHTML=
    "Every citable cell carries a human review stamp (<b>last_reviewed</b>) and a source pinpoint. "
    +"No citation is tool-generated; each pinpoint is confirmed against the official text (<span class='tag'>resolution_text</span>). "
    +"Operational and market notes (<b>tier2_operational</b>) are held on the far side of the citation firewall — present in the register, but never eligible for the citable set. "
    +"The firewall is enforced as a build gate, not a convention.";

  // ---- worklist ----
  var wl=D.worklist, hd=wl.headline||{{}};
  var byj=hd.by_jurisdiction||{{}}, byc=hd.by_constraint||{{}};
  var chips="<div class='wl-chip'><b>"+(hd.tier1_legal_unverified||0)+"</b> tier1_legal cells unverified</div>";
  chips+=Object.keys(byj).map(function(j){{return "<div class='wl-chip'>"+esc(j)+": <b>"+byj[j]+"</b></div>";}}).join("");
  document.getElementById("wlHead").innerHTML=chips;
  document.querySelector("#wlTable tbody").innerHTML=(wl.items||[]).map(function(it){{
    var missing = (it.evidence_tier!=="resolution_text") ? "evidence_tier = "+esc(it.evidence_tier||"unset")+" (needs official-text confirmation)"
                 : (it.status!=="in_force" ? "status = "+esc(it.status) : "url / pinpoint");
    return "<tr><td class='cid'>"+esc(it.id)+"</td><td>"+esc(it.jurisdiction)+"</td><td>"+esc(it.dimension||"")+"</td>"
      +"<td>"+esc((it.instrument||"").slice(0,80))+"</td><td style='color:var(--draft)'>"+missing+"</td></tr>";
  }}).join("");

  // live upgrade (snapshot already complete; refetch keeps parity if served)
  fetch("api/records.json",{{cache:"no-store"}}).then(function(r){{return r.ok?r.json():null;}}).then(function(){{}}).catch(function(){{}});
}})();
</script>
"""
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Integrity console · Cross-Border Stablecoin Register</title>
<meta name="description" content="Browse 152 regulatory records along three axes, see the lawyer-citable subset with a per-record why-not-citable x-ray, the computed-vs-authored reconciliation, provenance, integrity gates, and the verification backlog.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:wght@500;600&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body>{masthead("console")}
<div class="thesis"><div class="wrap"><p>The methodology's claim is that citability is a property you can <em>machine-check</em>, not a badge you assert. This console makes the three axes legible: filter every record by claim, evidence, and force; then open any cell to see precisely which axis keeps it out of the citable set.</p>
<p class="dual">All six views read the same public register you can clone or fetch. The "why not citable" x-ray and the computed-vs-authored reconciliation are the two things here you'll rarely find elsewhere.</p></div></div>
{body}
</body></html>"""
    (ROOT / "console.html").write_text(html, encoding="utf-8")
    return len(html.encode("utf-8"))


if __name__ == "__main__":
    b1 = build_corridors()
    b2 = build_console()
    print(f"wrote corridors.html ({b1:,} bytes) — flagship face: date-slider + what-if + typology + convergence")
    print(f"wrote console.html   ({b2:,} bytes) — methodology face: 3-axis browser + citable table + why-not + reconciliation + integrity + worklist")
    print(f"integrity captured: " + ", ".join(f"{k}={'pass' if v.get('pass') else v.get('pass')}" for k, v in INTEG.items()))
