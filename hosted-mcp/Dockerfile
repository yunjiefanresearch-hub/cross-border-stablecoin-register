# Hosted MCP container. Deploy on Fly.io / Render / Railway / any container host.
#
# Serves the CURRENT dataset by installing the register FROM SOURCE (so the
# dataset.json in your checkout: which you keep fresh: is what's served), NOT the
# frozen PyPI wheel. Build context = a directory containing:
#     ./register/           (the register source, incl. its current dataset.json + pyproject)
#     serve_http.py  cbsr_obs.py  requirements.txt   (this folder's files)
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY register/ ./register/
RUN pip install --no-cache-dir ./register    # installs cbsr_mcp with the current dataset.json

COPY serve_http.py cbsr_obs.py ./

ENV CBSR_HTTP_HOST=0.0.0.0 \
    CBSR_HTTP_PORT=8000 \
    CBSR_OBS_LOG=/app/obs.jsonl
EXPOSE 8000
CMD ["python", "serve_http.py"]
