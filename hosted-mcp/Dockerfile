# Hosted MCP container. Build from the repository root:
#   docker build --platform linux/amd64 -f hosted-mcp/Dockerfile .
#
# The dependency locks cover Linux x86_64. Pinning both the platform and Docker
# Official Image index prevents another architecture or a moved tag from
# silently changing the build inputs.
FROM --platform=linux/amd64 python:3.12.14-slim-trixie@sha256:09f7da3bc104798d0afb40bc08d23ab2da20a76130cec1f2ef170848f5d85217 AS wheel-builder

WORKDIR /build

# Build tooling and every transitive dependency are wheel-only and hash checked.
COPY constraints/dev-hashes.txt constraints/runtime-hashes.txt /locks/
RUN python -m pip install --disable-pip-version-check --no-cache-dir \
        --require-hashes --only-binary=:all: \
        --requirement /locks/dev-hashes.txt

# Copy only inputs used by the wheel build. The current dataset is force-included
# by pyproject.toml, so the hosted service cannot drift from this checkout.
COPY pyproject.toml README-PYPI.md LICENSE-CODE dataset.json ./
COPY src/ ./src/
COPY schemas/ ./schemas/
RUN python -m build --wheel --no-isolation --outdir /wheel


FROM --platform=linux/amd64 python:3.12.14-slim-trixie@sha256:09f7da3bc104798d0afb40bc08d23ab2da20a76130cec1f2ef170848f5d85217 AS runtime

WORKDIR /app

# Install the reviewed runtime graph from official wheels with exact hashes.
COPY constraints/runtime-hashes.txt /locks/runtime-hashes.txt
RUN python -m pip install --disable-pip-version-check --no-cache-dir \
        --require-hashes --only-binary=:all: \
        --requirement /locks/runtime-hashes.txt

# The wheel is produced locally, then hashed and installed offline without
# dependency resolution by the same helper used in release verification.
COPY --from=wheel-builder /wheel/ /wheel/
COPY tools/install_local_wheel.py /tmp/install_local_wheel.py
RUN python /tmp/install_local_wheel.py --wheel-dir /wheel \
    && rm -rf /wheel /locks /tmp/install_local_wheel.py

COPY hosted-mcp/serve_http.py hosted-mcp/cbsr_obs.py ./

# The service needs write access only to its observation log directory.
RUN groupadd --gid 10001 cbsr \
    && useradd --uid 10001 --gid 10001 --home-dir /app --no-create-home \
        --shell /usr/sbin/nologin cbsr \
    && install -d --owner=10001 --group=10001 /app/var

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CBSR_HTTP_HOST=0.0.0.0 \
    CBSR_HTTP_PORT=8000 \
    CBSR_OBS_LOG=/app/var/obs.jsonl

USER 10001:10001
EXPOSE 8000
CMD ["python", "serve_http.py"]
