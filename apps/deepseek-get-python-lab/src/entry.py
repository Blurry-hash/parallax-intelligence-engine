"""Read-only Python Worker: fixed checks only; no caller-supplied code."""
from workers import Response, WorkerEntrypoint
from urllib.parse import parse_qs, urlsplit
import statistics

ALLOWED = ("stats", "determinants", "all")

def stats():
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    return {"mean": statistics.mean(data), "sample_stdev": statistics.stdev(data)}

def determinants():
    def det2(m):
        (a, b), (c, d) = m
        return a * d - b * c
    (a, b, c), (d, e, f), (g, h, i) = ((2, 0, 1), (1, 3, 2), (1, 1, 1))
    det3 = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return {"det2": det2(((1, 2), (3, 4))), "checksum": sum(i * i for i in range(1, 11)), "det3": det3}

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlsplit(str(request.url))
        if url.path == "/health":
            return Response.json({"ok": True, "execution": "Cloudflare Python Worker", "model_runtime": False})
        if url.path != "/run":
            return Response.json({"error": "not found"}, status=404)
        name = parse_qs(url.query).get("case", ["all"])[0]
        if name not in ALLOWED:
            return Response.json({"error": "unknown case", "available": list(ALLOWED)}, status=400)
        result = {}
        if name in ("stats", "all"):
            result["stats"] = stats()
        if name in ("determinants", "all"):
            result["determinants"] = determinants()
        return Response.json({"ok": True, "case": name, "results": result, "method": "Python evaluated on server, not in DeepSeek", "supports_arbitrary_code": False})
