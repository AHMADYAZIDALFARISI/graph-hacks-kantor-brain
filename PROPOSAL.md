# KantorBrain — Company Brain di atas Graf FalkorDB
## Proposal ringkas — Graph Hacks: Context for AI Agents (WeMakeDevs × FalkorDB)

> Versi lengkap dan editable ada di dokumen proposal terpisah.
> Semua bagian di bawah ditulis Bahasa Indonesia, tanpa klaim fiktif.

## 1. Nama & ringkasan

**KantorBrain**: graf konteks bersama untuk 18 agen AI sebuah studio digital.
Setiap keputusan, receipt audit, dan handoff antar-agen disimpan sebagai
node dan edge di **FalkorDB**. Agen (atau manusia) bertanya dalam bahasa
sehari-hari — misalnya *"keputusan mana soal landing page yang masih berlaku?"* —
dan jawabannya **ditelusuri lewat path di graf**, lengkap dengan sumbernya.

## 2. Kaitan dengan tema "Context for AI Agents"

Agen hanya sebagus konteks yang ia pegang. Konteks di sini bukan tumpukan teks
mirip (vector search), melainkan **graf yang bisa di-reason**: relasi
"DIGANTIKAN_OLEH" antar-keputusan, "MENYETUJUI" antara receipt dan task.
Pertanyaan multi-hop seperti *"keputusan mana yang sudah kedaluwarsa?"*
dijawab satu query Cypher — sesuatu yang tidak bisa dilakukan pencarian
kemiripan kosinus.

## 3. Arsitektur

**Sudah jalan (dipakai apa adanya):**
- Hermes agent v0.19.0 (terinstal, terverifikasi)
- Provider router LLM: Gemini (round-robin) + failover OpenRouter/Groq (terverifikasi)
- Gateway Telegram: bot polling berjalan
  (catatan: backend NVIDIA NIM me-return 403 sejak 15 Okt — path LLM yang
  dipakai adalah router kantor, bukan NVIDIA)
- Event layer runlog/handoff antar-agen (teruji end-to-end)

**Baru dibangun saat hackathon (inti submission):**
- FalkorDB sebagai *company brain* (docker-compose satu perintah)
- `src/ingest.py`: runlog JSONL → node & edge
- `src/agent.py`: tanya-jawab lewat Cypher + sumber tertelusur
- `src/demo.py`: demo end-to-end dengan data contoh

**Uji sentralitas graf:** cabut FalkorDB → agen tidak bisa menjawab apa pun
soal keputusan dan riwayat. Produk mati. Graf bukan hiasan.

## 4. Timeline 15–18 Oktober 2026

> Hari ini **18 Oktober = hari deadline**. Hari 1–3 sudah lewat; yang realistis
> tersisa hanya kolom "Hari ini".

| Hari | Rencana ideal | Status |
|------|---------------|--------|
| 15 Okt (Kamis) | Setup FalkorDB + skema graf | Lewat |
| 16 Okt (Jumat) | Ingest runlog + query Cypher inti | Lewat |
| 17 Okt (Sabtu) | Agen tanya-jawab + polishing demo | Lewat |
| **18 Okt (Minggu)** | **Finalisasi, rekam video < 3 mnt, submit** | **Hari ini** |

## 5. Rencana submit (langkahmu)

1. Daftar di halaman hackathon WeMakeDevs (gratis).
2. Push repo ini ke GitHub sebagai repo **publik** + tambahkan lisensi (mis. MIT).
3. Rekam video demo < 3 menit.
4. Submit sebelum 18 Oktober 2026 berakhir (cek jam pasti di halaman hackathon).

## 6. Batasan yang diakui

- Demo memakai data contoh; hasil di data asli tergantung kelengkapan runlog.
- Router pertanyaan masih berbasis kata kunci (starter) — bukan LLM penuh.
- Tidak ada angka performa yang diklaim; semua yang didemo bisa dijalankan ulang.
- Tanpa secret yang ter-commit (`.env` masuk `.gitignore`).
