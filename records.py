import json
from pathlib import Path

RECORDS_FILE = Path(__file__).resolve().parent / "records.json"
MAX_RECORDS = 10

def load_records():
    if RECORDS_FILE.exists():
        try:
            return json.loads(RECORDS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_record(name: str, score: int):
    records = load_records()
    records.append({"name": name[:16] or "Player", "score": int(score)})
    records.sort(key=lambda r: r["score"], reverse=True)
    records = records[:MAX_RECORDS]
    RECORDS_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

def top_records():
    return load_records()
