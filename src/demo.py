"""Demo end-to-end: seed data contoh, jawab 3 pertanyaan, cetak hasilnya."""
import os

from .graph import get_graph, init_schema
from .ingest import ingest_dir
from .agent import tanya

DEMO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

PERTANYAAN = [
    "Keputusan apa soal landing page yang masih berlaku?",
    "Keputusan mana yang sudah kedaluwarsa?",
    "Siapa yang menyetujui T1?",
]


def main():
    g = get_graph()
    init_schema(g)
    ingest_dir(DEMO_DIR)
    for q in PERTANYAAN:
        print("=" * 60)
        print("Q:", q)
        judul, baris = tanya(g, q)
        print(judul)
        print("\n".join(baris))
    print("=" * 60)
    print("Demo selesai. Coba pertanyaanmu sendiri:")
    print('  python -m src.agent "jejak D1"')


if __name__ == "__main__":
    main()
