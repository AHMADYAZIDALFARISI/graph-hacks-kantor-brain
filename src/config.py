"""Konfigurasi: dibaca dari environment, tanpa secret yang di-hardcode."""
import os

FALKORDB_HOST = os.environ.get("FALKORDB_HOST", "localhost")
FALKORDB_PORT = int(os.environ.get("FALKORDB_PORT", "6379"))
GRAPH_NAME = os.environ.get("GRAPH_NAME", "kantor_brain")

# Opsional: kunci LLM untuk ringkasan jawaban. Boleh kosong — demo tetap jalan
# karena jawaban inti diformat dari hasil query Cypher.
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "gemini-2.5-flash")
