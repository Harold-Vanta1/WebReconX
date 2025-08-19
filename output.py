import json
from datetime import datetime
from html import escape

class ReportWriter:
    def __init__(self, results: dict, target: str):
        self.results = results
        self.target = target
        self.generated_at = datetime.utcnow().isoformat() + "Z"

    def write_json(self, path: str):
        payload = {
            "target": self.target,
            "generated_at": self.generated_at,
            "results": self.results,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def write_html(self, path: str):
        rows = []
        for mod, data in self.results.items():
            if isinstance(data, list):
                body = "<br>".join(escape(str(x)) for x in data) or "-"
            else:
                body = f"<pre>{escape(json.dumps(data, ensure_ascii=False, indent=2))}</pre>"
            rows.append(f"<tr><td><b>{escape(mod)}</b></td><td>{body}</td></tr>")
        html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>WebReconX Report</title>
<style>body{{font-family:system-ui,Arial;}} table{{border-collapse:collapse;width:100%;}}
td,th{{border:1px solid #ddd;padding:8px;}} th{{background:#f4f4f4;}}</style></head>
<body>
<h2>WebReconX Report</h2>
<p><b>Target:</b> {escape(self.target)}<br><b>Generated:</b> {escape(self.generated_at)}</p>
<table><thead><tr><th>Module</th><th>Findings</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody></table>
</body></html>"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
