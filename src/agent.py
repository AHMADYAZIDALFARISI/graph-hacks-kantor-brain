"""Agen company brain: menjawab pertanyaan lewat query Cypher ke FalkorDB.

Router pertanyaan masih berbasis kata kunci (starter). Tanpa LLM pun jawaban
tetap benar karena diambil dari graf — bukan karangan model. Setiap jawaban
disertai sumber (id keputusan/receipt) sehingga bisa ditelusuri.

Jalankan:  python -m src.agent "keputusan apa soal landing page yang masih berlaku?"
"""
import argparse
import sys

from .graph import get_graph


def keputusan_terkait(g, topik):
    """Semua keputusan yang menyebut topik + statusnya (berlaku/digantikan)."""
    res = g.query(
        "MATCH (d:Decision) WHERE toLower(d.text) CONTAINS toLower($topik) "
        "OPTIONAL MATCH (d)-[:DIGANTIKAN_OLEH]->(pengganti:Decision) "
        "OPTIONAL MATCH (e:Employee)-[:MEMUTUSKAN]->(d) "
        "RETURN d.id AS id, d.text AS teks, e.id AS oleh, "
        "       pengganti.id AS digantikan_oleh",
        {"topik": topik},
    )
    baris = []
    for r in res.result_set:
        status = ("DIGANTIKAN oleh " + r[3]) if r[3] else "MASIH BERLAKU"
        baris.append(f"- [{r[0]}] {r[1]} (oleh {r[2]}) → {status}")
    return baris or ["Tidak ada keputusan soal topik itu di graf."]


def keputusan_kedaluwarsa(g):
    """Keputusan yang sudah punya pengganti."""
    res = g.query(
        "MATCH (lama:Decision)-[:DIGANTIKAN_OLEH]->(baru:Decision) "
        "RETURN lama.id, lama.text, baru.id"
    )
    baris = [f"- [{r[0]}] {r[1]} → digantikan oleh [{r[2]}]"
             for r in res.result_set]
    return baris or ["Belum ada keputusan yang digantikan."]


def jejak_keputusan(g, decision_id):
    """Rantai penggantian sebuah keputusan (multi-hop)."""
    res = g.query(
        "MATCH p = (awal:Decision {id: $id})-[:DIGANTIKAN_OLEH*0..5]->(akhir:Decision) "
        "RETURN [n IN nodes(p) | n.id + ': ' + n.text]",
        {"id": decision_id},
    )
    if not res.result_set:
        return [f"Keputusan {decision_id} tidak ada di graf."]
    rantai = res.result_set[0][0]
    return [" → ".join(rantai)]


def siapa_menyetujui(g, task_id):
    res = g.query(
        "MATCH (e:Employee)-[:MEMBUAT]->(r:Receipt)-[:MENYETUJUI]->(t:Task {id: $id}) "
        "RETURN e.id, r.id, r.verdict",
        {"id": task_id},
    )
    baris = [f"- {r[0]} via receipt {r[1]}: {r[2]}" for r in res.result_set]
    return baris or [f"Task {task_id} belum punya receipt."]


def tanya(g, pertanyaan):
    """Router sederhana: petakan pertanyaan ke query Cypher yang tepat."""
    q = pertanyaan.lower()
    if "kedaluwarsa" in q or "digantikan" in q or "usang" in q:
        return "Keputusan yang sudah digantikan:", keputusan_kedaluwarsa(g)
    if "jejak" in q or "rantai" in q:
        kata = pertanyaan.split()
        did = next((k.strip("?.,") for k in kata if k.strip("?.,").startswith("D")), None)
        if not did:
            return "Sebutkan id keputusannya (mis. D1).", []
        return f"Jejak keputusan {did}:", jejak_keputusan(g, did)
    if "menyetujui" in q or "approve" in q or "receipt" in q:
        kata = pertanyaan.split()
        tid = next((k.strip("?.,") for k in kata if k.strip("?.,").startswith("T")), None)
        if not tid:
            return "Sebutkan id task-nya (mis. T1).", []
        return f"Persetujuan untuk {tid}:", siapa_menyetujui(g, tid)
    # default: anggap topik = kata benda terpanjang (heuristic starter)
    topik = max((k.strip("?.,") for k in pertanyaan.split() if len(k) > 3),
                key=len, default="")
    return f"Keputusan terkait '{topik}':", keputusan_terkait(g, topik)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("pertanyaan", nargs="?", default="")
    pertanyaan = p.parse_args().pertanyaan or " ".join(
        input("Tanya company brain: ").split())
    judul, baris = tanya(get_graph(), pertanyaan)
    print(judul)
    print("\n".join(baris))
    sys.exit(0)
