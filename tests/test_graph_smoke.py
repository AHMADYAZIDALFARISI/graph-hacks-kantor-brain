"""Smoke test: pastikan koneksi FalkorDB hidup dan query dasar jalan.

Butuh FalkorDB menyala (docker compose up -d). Lewati otomatis kalau mati.
"""
import pytest

from src.graph import get_graph


def test_koneksi_dan_query_dasar():
    try:
        g = get_graph()
        hasil = g.query("RETURN 1 AS satu")
    except Exception as e:
        pytest.skip(f"FalkorDB tidak menyala: {e}")
    assert hasil.result_set[0][0] == 1
