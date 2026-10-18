"""Memasukkan event runlog/handoff ke graf FalkorDB.

Format JSONL per baris (lihat data/sample_runlog.jsonl):
  {"kind": "decision", "id": "D1", "text": "...", "by": "chief-of-staff", "replaces": null}
  {"kind": "task", "id": "T1", "title": "...", "owner": "frontend-dev"}
  {"kind": "receipt", "id": "R1", "task": "T1", "verdict": "APPROVED", "by": "quality-auditor"}

Jalankan:  python -m src.ingest --runlog-dir data
"""
import argparse
import json
import os

from .graph import get_graph, init_schema


def ingest_event(g, ev):
    kind = ev.get("kind")
    if kind == "decision":
        g.query(
            "MERGE (e:Employee {id: $by}) "
            "MERGE (d:Decision {id: $id}) SET d.text = $text "
            "MERGE (e)-[:MEMUTUSKAN]->(d)",
            {"by": ev["by"], "id": ev["id"], "text": ev["text"]},
        )
        if ev.get("replaces"):
            g.query(
                "MATCH (lama:Decision {id: $lama}), (baru:Decision {id: $baru}) "
                "MERGE (lama)-[:DIGANTIKAN_OLEH]->(baru)",
                {"lama": ev["replaces"], "baru": ev["id"]},
            )
    elif kind == "task":
        g.query(
            "MERGE (e:Employee {id: $owner}) "
            "MERGE (t:Task {id: $id}) SET t.title = $title "
            "MERGE (e)-[:MENGERJAKAN]->(t)",
            {"owner": ev["owner"], "id": ev["id"], "title": ev["title"]},
        )
    elif kind == "receipt":
        g.query(
            "MERGE (e:Employee {id: $by}) "
            "MERGE (r:Receipt {id: $id}) SET r.verdict = $verdict "
            "MERGE (e)-[:MEMBUAT]->(r) "
            "WITH r MATCH (t:Task {id: $task}) MERGE (r)-[:MENYETUJUI]->(t)",
            {"by": ev["by"], "id": ev["id"], "verdict": ev["verdict"],
             "task": ev["task"]},
        )


def ingest_dir(runlog_dir):
    g = get_graph()
    init_schema(g)
    total = 0
    for name in sorted(os.listdir(runlog_dir)):
        if not name.endswith(".jsonl"):
            continue
        with open(os.path.join(runlog_dir, name), encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    ingest_event(g, json.loads(line))
                    total += 1
    print(f"Selesai: {total} event masuk ke graf.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--runlog-dir", default="data")
    ingest_dir(p.parse_args().runlog_dir)
