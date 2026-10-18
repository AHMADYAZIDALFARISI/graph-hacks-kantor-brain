"""Koneksi ke FalkorDB dan skema graf company brain.

Model graf:
  (:Employee)-[:MEMUTUSKAN]->(:Decision)
  (:Decision)-[:DIGANTIKAN_OLEH]->(:Decision)
  (:Employee)-[:MENGERJAKAN]->(:Task)
  (:Receipt)-[:MENYETUJUI]->(:Task)
"""
from falkordb import FalkorDB

from .config import FALKORDB_HOST, FALKORDB_PORT, GRAPH_NAME


def get_graph():
    """Buka koneksi dan pilih graf kerja."""
    db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
    return db.select_graph(GRAPH_NAME)


INDEXES = [
    "CREATE INDEX FOR (e:Employee) ON (e.id)",
    "CREATE INDEX FOR (d:Decision) ON (d.id)",
    "CREATE INDEX FOR (t:Task) ON (t.id)",
]


def init_schema(g):
    """Buat index; aman dipanggil ulang (index yang sudah ada diabaikan)."""
    for q in INDEXES:
        try:
            g.query(q)
        except Exception:
            pass
