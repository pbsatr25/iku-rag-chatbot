"""
Unit test deteksi intent (src/generation/intent.py) terhadap dataset tim tests/intent_cases.json.

Label dataset dipetakan seperti di test_intent_baseline.py: "hybrid" butuh data -> "data",
"general" (sapaan, di luar topik) dijawab lewat jalur dokumen -> "definisi". Field `scope`
opsional: kasus PAGE-* menguji konteks halaman dasbor.
"""

import json
from pathlib import Path

import pytest

from cakupan import baca_cakupan
from intent import DATA, DEFINISI, FORMULA, deteksi_intent, normalisasi

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((PROJECT_ROOT / "tests" / "intent_cases.json").read_text(encoding="utf-8"))["cases"]
LABEL = {"data": DATA, "hybrid": DATA, "formula": FORMULA, "definisi": DEFINISI, "general": DEFINISI}


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_dataset_intent(case):
    cakupan = baca_cakupan(case.get("scope"))
    assert deteksi_intent(case["question"], cakupan) == LABEL[case["expected_intent"]], case["notes"]


def test_konteks_halaman_mengubah_jalur():
    """Pertanyaan yang sama: di halaman IKU = data dasbor; tanpa halaman = penjelasan cara hitung."""
    pertanyaan = "Berapa capaian IKU 1?"
    assert deteksi_intent(pertanyaan, baca_cakupan({"kind": "iku", "ikuCode": "IKU 001"})) == DATA
    assert deteksi_intent(pertanyaan, None) == FORMULA


def test_overview_tidak_memakai_konteks_halaman():
    """Data Overview lintas IKU, sedangkan fetch_data saat ini mengambil satu IKU."""
    assert deteksi_intent("rangkum analisis", baca_cakupan({"kind": "overview"})) == DEFINISI


@pytest.mark.parametrize("teks, harapan", [
    ("IKU001 saya", "iku 1 saya"),
    ("iku-009", "iku 9"),
    ("  Capaian   IKU 3 ", "capaian iku 3"),
    ("Data IKU 2025", "data iku 2025"),        # tahun tidak dianggap kode IKU
    ("IKU 9 dihitung bagaimana", "iku 9 dihitung bagaimana"),   # "d" bukan sub-indikator
    ("Predikat IKU 11b", "predikat iku 11"),
])
def test_normalisasi(teks, harapan):
    assert normalisasi(teks) == harapan
