# KantorBrain — Company Brain di atas Graf FalkorDB

Starter repo untuk hackathon **Graph Hacks: Context for AI Agents**
(WeMakeDevs × FalkorDB, 15–18 Oktober 2026).

## Ide dalam satu paragraf

18 agen AI di sebuah studio digital menulis setiap **keputusan**, **receipt audit**,
dan **handoff** ke satu *graf konteks bersama* di FalkorDB. Agen lain — atau manusia —
bertanya dalam bahasa sehari-hari, dan jawabannya **ditelusuri lewat path di graf**,
bukan sekadar teks yang mirip.

**Kenapa graf, bukan vector search?** Pertanyaan seperti
*"keputusan mana soal X yang sudah digantikan?"* adalah pertanyaan **path**
(multi-hop), bukan kemiripan kosinus. Satu query Cypher menjawabnya.
Cabut FalkorDB dan produk ini mati — grafnya sentral, bukan hiasan.

## Prasyarat

- Docker (untuk FalkorDB) — atau akun FalkorDB Cloud
- Python 3.10+

## Cara menjalankan

```bash
docker compose up -d          # FalkorDB di localhost:6379
pip install -r requirements.txt
cp .env.example .env          # boleh kosong; LLM opsional
python -m src.demo            # seed data contoh + 3 pertanyaan demo
```

Pakai data aslimu:

```bash
python -m src.ingest --runlog-dir /path/ke/runlog
python -m src.agent "keputusan apa soal landing page yang masih berlaku?"
```

## Struktur

```
├── docker-compose.yml   # FalkorDB sekali perintah
├── requirements.txt
├── .env.example         # contoh config TANPA secret asli
├── src/
│   ├── config.py        # baca env, tanpa hardcode secret
│   ├── graph.py         # koneksi + skema graf
│   ├── ingest.py        # runlog/handoff JSONL -> node & edge
│   ├── agent.py         # tanya-jawab lewat Cypher (router kata kunci)
│   └── demo.py          # demo end-to-end
├── data/sample_runlog.jsonl
└── tests/               # smoke test koneksi
```

## Cara submit (langkah kamu, tidak bisa diwakilkan)

1. Daftar di halaman hackathon WeMakeDevs (gratis).
2. Push repo ini ke GitHub sebagai repo **publik** dan tambahkan lisensi (mis. MIT).
3. Rekam video demo **< 3 menit**.
4. Submit sebelum **18 Oktober 2026** berakhir (cek jam pastinya di halaman hackathon).

## Catatan jujur

- Demo memakai data contoh (`data/sample_runlog.jsonl`). Hasil pada data asli
  tergantung kelengkapan runlog-mu.
- Tanpa `LLM_API_KEY`, jawaban diformat langsung dari hasil Cypher —
  tetap benar dan tetap bisa ditelusuri sumbernya.
- Jangan commit file `.env` berisi kunci asli (sudah masuk `.gitignore`).
