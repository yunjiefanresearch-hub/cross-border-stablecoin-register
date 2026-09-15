# Hosted MCP container

This image serves the current checkout's register over Streamable HTTP. It
builds the CBSR wheel from source in an isolated builder stage, then runs it as
an unprivileged user in a smaller runtime stage.

## Build

Use the repository root as the build context:

```sh
docker build --platform linux/amd64 \
  --file hosted-mcp/Dockerfile \
  --tag cbsr-hosted-mcp:local .
```

The image is deliberately limited to `linux/amd64`: the reviewed hash locks
currently cover Linux x86_64 (and the project's non-container CI targets), not
Linux arm64. An unsupported platform fails closed instead of falling back to an
unlocked source distribution.

The build has three supply-chain boundaries:

1. The Docker Official Python image is fixed to its full index digest.
2. Builder and runtime Python packages come only from the repository's
   wheel-only, SHA-256-checked locks under `constraints/`.
3. The locally built CBSR wheel is hashed and installed with `--no-index` and
   `--no-deps` by `tools/install_local_wheel.py`.

Run the service with a persistent observation log:

```sh
docker run --rm --publish 127.0.0.1:8000:8000 \
  --mount type=volume,source=cbsr-observations,target=/app/var \
  cbsr-hosted-mcp:local
```

The example deliberately does not expose the unauthenticated MCP transport on
public interfaces. Put an authenticated, TLS-terminating reverse proxy in front
of the loopback-bound service before offering remote access.

The repository's Hosted MCP smoke workflow supplies the missing Linux Docker
evidence: it builds this image, starts it with a read-only filesystem and no
Linux capabilities, binds an ephemeral port only on `127.0.0.1`, checks the
side-effect-free `/health` route, and confirms that an incomplete plain `GET
/mcp` is rejected by the protocol boundary. It never pushes or deploys an
image. A local Docker build was not available when this workflow was added, so
the first successful GitHub-hosted run is the authoritative container result.

## Updating inputs

Do not replace the image digest with a mutable tag. Resolve the intended
Docker Official Image (for example with `docker buildx imagetools inspect
python:3.12-slim`), review the patch release and Debian suite, then update both
`FROM` lines and the exact-image test together.

Regenerate Python hashes only through `tools/hash_constraints.py` and the
procedure in `constraints/README.md`. `hosted-mcp/requirements.txt` is retained
only as a compatibility entry point for manual installs; it delegates to the
same canonical runtime hash lock and intentionally does not request the unused
`mcp[cli]` extra.
