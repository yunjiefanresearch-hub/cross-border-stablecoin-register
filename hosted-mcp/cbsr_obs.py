"""
CBSR observability: corridor-demand telemetry for the HOSTED MCP only.
Dependency-free. Never import this into the published wheel (keep 'no network calls' true).

Two ways to use it (pick one):

  A) GUARANTEED: decorator. In server.py, add `@logged` ABOVE each corridor tool, e.g.:
         from cbsr_obs import logged
         @mcp.tool()
         @logged
         def compose_corridor(origin, destination, as_of=None): ...
     (Order matters: @mcp.tool() on top, @logged directly above the def.)

  B) ZERO-EDIT (best-effort): call cbsr_obs.instrument(mcp) in serve_http.py.
     It wraps already-registered tools. If the FastMCP internals differ from what
     it expects, it NO-OPS and logs a hint telling you to use (A).

Log sink: env CBSR_OBS_LOG=/path/to/file.jsonl  (default: stderr, which most hosts capture).
Logged fields: timestamp, tool name, args (origin/destination/corridor_id are NOT PII).
"""
from __future__ import annotations
import functools, json, os, sys, time

_SINK = os.environ.get("CBSR_OBS_LOG", "")

def _emit(rec: dict) -> None:
    line = json.dumps(rec, default=str, ensure_ascii=False)
    if _SINK:
        try:
            with open(_SINK, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            return
        except Exception:
            pass
    print(line, file=sys.stderr, flush=True)

def logged(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        _emit({"t": time.time(), "tool": getattr(fn, "__name__", "?"),
               "args": kwargs if kwargs else [str(a) for a in args]})
        return fn(*args, **kwargs)
    return wrapper

DEFAULT_TOOLS = ("corridor_directed", "compose_corridor", "get_corridor", "corridor_timeline",
                 "explain_feasibility", "compose_via_substrate", "profile_for",
                 "corridor_skeleton")

def instrument(mcp, tool_names=DEFAULT_TOOLS) -> int:
    """Best-effort wrap of registered FastMCP tools. Returns count wrapped (0 = no-op)."""
    mgr = getattr(mcp, "_tool_manager", None)
    tools = getattr(mgr, "_tools", None) if mgr is not None else None
    if not isinstance(tools, dict):
        _emit({"t": time.time(), "obs": "instrument_noop",
               "hint": "FastMCP registry not found; use the @logged decorator in server.py"})
        return 0
    n = 0
    for name in tool_names:
        t = tools.get(name)
        if t is None:
            continue
        attr = "fn" if hasattr(t, "fn") else ("func" if hasattr(t, "func") else None)
        if not attr:
            continue
        try:
            setattr(t, attr, logged(getattr(t, attr)))
            n += 1
        except Exception:
            pass
    _emit({"t": time.time(), "obs": "instrument", "wrapped": n})
    return n
