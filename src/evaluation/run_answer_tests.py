"""
run_answer_tests.py
Jalankan soal test set ke chatbot (tahap 7: retriever + LLM + kalkulator) dan bandingkan
jawabannya dengan jawaban yang diharapkan.

Sumber jawaban yang diharapkan:
- data/evaluation/test_set_buku_iku.md       -> "Jawaban benar" + halaman kunci (semua soal)
- data/evaluation/test_inputs_hitung.json     -> angka kunci soal hitungan (H01-H30)
- data/evaluation/test_fakta_definisi.json    -> fakta kunci soal definisi & jebakan (D01-D14)

Pemeriksaan otomatis per soal:
- Hitungan : kalkulator dipanggil, hasil kalkulator = kunci, angka kunci muncul di jawaban,
             halaman sitasi/rumus cocok dengan halaman kunci
- Definisi : semua fakta kunci muncul di jawaban, halaman sitasi cocok dengan halaman kunci
- Jebakan  : D11 meluruskan ke IKU 2; D12 menolak (tidak mengarang) dan tidak perlu sitasi
Pemeriksaan otomatis hanya bantuan: baca juga jawaban lengkap di laporan.

Setiap soal memanggil LLM (biasanya 1-3 kali). Pada free tier, beri jeda antar-soal
agar tidak terkena batas pemakaian.

Run panjang yang terkena batas pemakaian:
- Laporan ditulis ulang setiap selesai satu soal, jadi hasil tidak hilang bila run terhenti.
- Batas PER MENIT (429): tunggu sesuai permintaan server, lalu soal yang sama diulang.
- Jatah HARIAN habis (429 per hari), 3 error berturut-turut, atau Ctrl+C: run langsung berhenti
  dan laporan disimpan. Lanjutkan sisanya (mis. besok) ke laporan yang SAMA dengan --lanjut.

Jalankan dari root project:
    python src/evaluation/run_answer_tests.py                     # semua 44 soal
    python src/evaluation/run_answer_tests.py --tipe hitung       # 30 soal hitungan saja
    python src/evaluation/run_answer_tests.py --tipe definisi     # 14 soal definisi & jebakan
    python src/evaluation/run_answer_tests.py --id H07,D11        # soal tertentu
    python src/evaluation/run_answer_tests.py --set inti          # kelompok soal (data/evaluation/test_sets.json)
    python src/evaluation/run_answer_tests.py --jeda 10           # jeda 10 detik antar-soal
    python src/evaluation/run_answer_tests.py --model qwen/qwen3.8-27b   # model lain, penyedia sama (.env)
    python src/evaluation/run_answer_tests.py --lanjut reports/evaluation/answer_test_<...>.json
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "evaluation"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "generation"))

from eval_retrieval import load_test_set, TEST_SET_FILE  # noqa: E402
from answer import Chatbot  # noqa: E402
from postproses import angka_muncul  # noqa: E402

INPUTS_HITUNG = PROJECT_ROOT / "data" / "evaluation" / "test_inputs_hitung.json"
FAKTA_DEFINISI = PROJECT_ROOT / "data" / "evaluation" / "test_fakta_definisi.json"
TEST_SETS = PROJECT_ROOT / "data" / "evaluation" / "test_sets.json"
RESULTS_DIR = PROJECT_ROOT / "reports" / "evaluation"
TOLERANCE = 0.01
BATAS_ERROR_BERUNTUN = 3
MAX_TUNGGU_429 = 4          # berapa kali satu soal boleh menunggu lalu diulang karena batas per menit
TUNGGU_429_DEFAULT = 30.0   # detik, bila pesan 429 tidak menyebut waktu tunggu
TUNGGU_429_MAKS = 180.0


def jatah_harian_habis(error: str) -> bool:
    """429 karena jatah HARIAN (token/request per hari) habis: menunggu sebentar tidak menolong,
    jadi run sebaiknya berhenti. Pesan Groq: '... on tokens per day (TPD) ...'."""
    return "429" in error and re.search(r"per day|\b[TR]PD\b|PerDay", error, re.I) is not None


def detik_tunggu(e: Exception) -> float:
    """Waktu tunggu yang diminta server: header retry-after, atau teks 'try again in 1m2.5s'."""
    response = getattr(e, "response", None)
    retry_after = response.headers.get("retry-after") if response is not None else None
    if retry_after:
        try:
            return float(retry_after)
        except ValueError:
            pass
    m = re.search(r"try again in ((?:\d+h)?(?:\d+m)?(?:[\d.]+s)?)", str(e))
    if m and m.group(1):
        jam, menit, detik = (re.search(rf"([\d.]+){s}", m.group(1)) for s in ("h", "m", "s"))
        return sum(float(x.group(1)) * k for x, k in ((jam, 3600), (menit, 60), (detik, 1)) if x)
    return TUNGGU_429_DEFAULT


def tanya(bot, pertanyaan: str) -> dict:
    """bot.ask() yang sabar: bila kena batas PER MENIT (429), tunggu sesuai permintaan server
    lalu ulangi soal yang sama. Batas per hari dan error lain langsung diteruskan."""
    for ke in range(MAX_TUNGGU_429 + 1):
        try:
            return bot.ask(pertanyaan)
        except Exception as e:
            teks = f"{type(e).__name__}: {e}"
            if "429" not in teks or jatah_harian_habis(teks) or ke == MAX_TUNGGU_429:
                raise
            tunggu = min(detik_tunggu(e), TUNGGU_429_MAKS) + 2
            print(f"(batas per menit, tunggu {tunggu:.0f} dtk) ", end="", flush=True)
            time.sleep(tunggu)


# ---------------------------------------------------------------------------
# Pemeriksaan
# ---------------------------------------------------------------------------

def sama(aktual, harapan) -> bool:
    if isinstance(harapan, dict):
        return isinstance(aktual, dict) and all(sama(aktual.get(k), v) for k, v in harapan.items())
    if isinstance(harapan, (int, float)) and isinstance(aktual, (int, float)):
        return abs(aktual - harapan) <= TOLERANCE
    return aktual == harapan


def nilai_kunci(harapan) -> list:
    return list(harapan.values()) if isinstance(harapan, dict) else [harapan]


def halaman_dikutip(hasil: dict) -> list[tuple[int, int]]:
    """Rentang halaman dari rujukan [n] yang valid di jawaban + dari sumber rumus kalkulator."""
    rentang = []
    chunks = hasil["chunks"]
    for n in {int(x) for x in re.findall(r"\[(\d+)\]", hasil["jawaban"])}:
        if 1 <= n <= len(chunks):
            rentang.append((chunks[n - 1]["page_start"], chunks[n - 1]["page_end"]))
    for sumber in hasil["sumber_rumus"]:
        for a, b in re.findall(r"hlm\.\s*(\d+)(?:\s*[–-]\s*(\d+))?", sumber):
            rentang.append((int(a), int(b or a)))
    return rentang


def cek_halaman(hasil: dict, halaman_kunci: list[int]) -> bool:
    return any(a <= p <= b for a, b in halaman_dikutip(hasil) for p in halaman_kunci)


def cek_hitungan(hasil: dict, kasus: dict, halaman_kunci: list[int]) -> dict:
    berhasil = [k for k in hasil["kalkulator"] if "error" not in k["hasil"]]
    harapan = kasus["harapan"]
    return {
        "kalkulator dipanggil": bool(berhasil),
        "hasil kalkulator = kunci": any(sama(k["hasil"]["hasil"], harapan) for k in berhasil),
        "angka kunci ada di jawaban": all(angka_muncul(x, hasil["jawaban"]) for x in nilai_kunci(harapan)),
        "halaman sitasi benar": cek_halaman(hasil, halaman_kunci),
    }


def cek_definisi(hasil: dict, kasus: dict, halaman_kunci: list[int]) -> dict:
    teks = hasil["jawaban"].lower()
    cek = {}
    for kelompok in kasus["fakta"]:
        cek[f"fakta: {' / '.join(kelompok)}"] = any(alt.lower() in teks for alt in kelompok)
    if kasus.get("tanpa_sitasi"):
        cek["tidak mengarang sitasi"] = not hasil["sitasi"]
    elif halaman_kunci:
        cek["halaman sitasi benar"] = cek_halaman(hasil, halaman_kunci)
    return cek


# ---------------------------------------------------------------------------
# Laporan
# ---------------------------------------------------------------------------

def fmt(nilai) -> str:
    if isinstance(nilai, dict):
        return ", ".join(f"{k} = {fmt(v)}" for k, v in nilai.items())
    if isinstance(nilai, float):
        return f"{nilai:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
    if isinstance(nilai, int) and not isinstance(nilai, bool):
        return f"{nilai:,}".replace(",", ".")
    return str(nilai)


def blok_soal(baris: dict) -> list[str]:
    status = "✅ LULUS" if baris["lulus"] else ("⚠️ ERROR" if baris.get("error") else "❌ PERLU DICEK")
    out = [
        f"### {baris['id']} — {status}",
        "",
        f"**Pertanyaan:** {baris['pertanyaan']}",
        "",
        "**Jawaban chatbot:**",
        "",
        "```text",
        baris.get("jawaban") or f"(tidak ada jawaban: {baris.get('error')})",
        "```",
        "",
    ]
    if baris.get("sitasi"):
        out += ["**Sitasi chatbot:**", ""] + [f"- {s}" for s in baris["sitasi"]] + [""]
    if baris.get("sumber_rumus"):
        out += ["**Sumber rumus (kalkulator):**", ""] + [f"- {s}" for s in baris["sumber_rumus"]] + [""]
    if baris.get("kalkulator"):
        out += ["**Panggilan kalkulator:**", ""]
        for k in baris["kalkulator"]:
            hasil = k["hasil"].get("hasil", k["hasil"].get("error"))
            out.append(f"- argumen `{k['argumen']}` → {fmt(hasil)}")
        out.append("")
    if baris.get("peringatan"):
        out += ["**Peringatan chatbot:**", ""] + [f"- {p}" for p in baris["peringatan"]] + [""]
    out += ["**Jawaban yang diharapkan:**", ""]
    if baris.get("harapan_angka") is not None:
        out.append(f"- Angka kunci: **{fmt(baris['harapan_angka'])}**")
    out += [f"- Halaman kunci: {', '.join(map(str, baris['halaman_kunci'])) or '-'}", "", baris["jawaban_benar"], ""]
    if baris.get("catatan"):
        out += [f"*Catatan soal:* {baris['catatan']}", ""]
    out += ["**Pemeriksaan otomatis:**", ""]
    out += [f"- {'✅' if ok else '❌'} {nama}" for nama, ok in baris.get("cek", {}).items()]
    out.append("")
    return out


def tulis_laporan(rows: list[dict], model: str, path: Path, total: int,
                  belum: list[str], berhenti: str | None, perintah_lanjut: str):
    n = len(rows)
    lulus = sum(r["lulus"] for r in rows)
    hitung = [r for r in rows if r["id"].startswith("H")]
    definisi = [r for r in rows if r["id"].startswith("D")]

    def rasio(daftar, kunci):
        relevan = [r for r in daftar if kunci in r.get("cek", {})]
        return f"{sum(r['cek'][kunci] for r in relevan)}/{len(relevan)}" if relevan else "-"

    lines = [
        "# Uji Jawaban Chatbot (retriever + LLM + kalkulator)",
        "",
        f"- Waktu: {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"- Model LLM: `{model}`",
        f"- Soal: {n} dari {total} dijalankan (hitungan {len(hitung)}, definisi & jebakan {len(definisi)})",
        f"- Status run: {'selesai' if not belum else 'berhenti: ' + (berhenti or 'sedang berjalan')}",
        "",
        "## Ringkasan",
        "",
        "| Metrik | Hasil |",
        "|---|---|",
        f"| Lulus semua pemeriksaan otomatis | **{lulus}/{n}** |",
        f"| Hitungan: kalkulator dipanggil | {rasio(hitung, 'kalkulator dipanggil')} |",
        f"| Hitungan: hasil kalkulator = kunci | {rasio(hitung, 'hasil kalkulator = kunci')} |",
        f"| Hitungan: angka kunci ada di jawaban | {rasio(hitung, 'angka kunci ada di jawaban')} |",
        f"| Halaman sitasi benar (hitungan) | {rasio(hitung, 'halaman sitasi benar')} |",
        f"| Halaman sitasi benar (definisi) | {rasio(definisi, 'halaman sitasi benar')} |",
        f"| Soal error (API/kuota) | {sum(1 for r in rows if r.get('error'))} |",
        f"| Jawaban dengan peringatan chatbot | {sum(1 for r in rows if r.get('peringatan'))} |",
        "",
        "| ID | Status | Pemeriksaan yang gagal |",
        "|---|---|---|",
    ]
    for r in rows:
        gagal = [k for k, ok in r.get("cek", {}).items() if not ok]
        status = "✅" if r["lulus"] else ("⚠️ error" if r.get("error") else "❌")
        lines.append(f"| {r['id']} | {status} | {'; '.join(gagal) or (r.get('error') or '-')} |")
    lines += ["", "Pemeriksaan otomatis hanya bantuan. Baca jawaban lengkap di bawah dan bandingkan "
              "dengan jawaban yang diharapkan.", ""]
    if belum:
        lines += ["## Soal yang belum selesai / perlu diulang", "",
                  f"{len(belum)} soal belum dijalankan atau berakhir error: {', '.join(belum)}. "
                  "Lanjutkan ke laporan ini dengan:", "",
                  "```powershell", perintah_lanjut, "```", ""]
    lines += ["## Detail per soal", ""]
    for r in rows:
        lines += blok_soal(r)
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Uji jawaban chatbot terhadap test set")
    parser.add_argument("--tipe", choices=["semua", "hitung", "definisi"], default="semua")
    parser.add_argument("--id", help="daftar ID dipisah koma, mis. H07,D11")
    sets = json.loads(TEST_SETS.read_text(encoding="utf-8"))["sets"]
    parser.add_argument("--set", choices=sorted(sets), help="kelompok soal dari data/evaluation/test_sets.json")
    parser.add_argument("--jeda", type=float, default=5.0,
                        help="jeda (detik) antar-soal agar tidak terkena batas free tier")
    parser.add_argument("--model", help="ganti LLM_MODEL untuk run ini saja (penyedia/base URL tetap dari .env)")
    parser.add_argument("--lanjut", type=Path,
                        help="file .json laporan yang terhenti; soal yang belum selesai dijalankan dan ditulis ke laporan itu")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    semua_soal = load_test_set(TEST_SET_FILE)
    kasus_hitung = {c["id"]: c for c in json.loads(INPUTS_HITUNG.read_text(encoding="utf-8"))["cases"]}
    kasus_definisi = json.loads(FAKTA_DEFINISI.read_text(encoding="utf-8"))["cases"]

    rows: list[dict] = []
    if args.lanjut:
        # melanjutkan run yang terhenti: pakai rencana soal, model, dan file laporan yang sama
        lama = json.loads(args.lanjut.read_text(encoding="utf-8"))
        rencana = lama.get("rencana") or [r["id"] for r in lama["results"]] + lama.get("belum_selesai", [])
        rows = [r for r in lama["results"] if not r.get("error")]  # soal error diulang
        args.model = args.model or lama["model"]
    elif args.id:
        dipilih = {x.strip().upper() for x in args.id.split(",")}
        rencana = [q["id"] for q in semua_soal if q["id"] in dipilih]
    elif args.set:
        dipilih = set(sets[args.set]["id"])
        rencana = [q["id"] for q in semua_soal if q["id"] in dipilih]
    else:
        awalan = {"hitung": "H", "definisi": "D"}.get(args.tipe, "")
        rencana = [q["id"] for q in semua_soal if q["id"].startswith(awalan)]

    if args.model:
        os.environ["LLM_MODEL"] = args.model  # dibaca get_client() saat Chatbot dibuat
    sudah = {r["id"] for r in rows}
    soal = [q for q in semua_soal if q["id"] in rencana and q["id"] not in sudah]
    if not soal:
        print("Tidak ada soal yang perlu dijalankan." if args.lanjut else "Tidak ada soal yang cocok dengan filter.")
        return

    print("Memuat retriever dan LLM...")
    bot = Chatbot()
    if args.lanjut and bot.model != lama["model"]:
        print(f"Model sekarang ({bot.model}) berbeda dengan laporan ({lama['model']}). "
              "Hasil dua model tidak boleh dicampur dalam satu laporan; jalankan run baru tanpa --lanjut.")
        return
    keterangan = f"lanjutan: {len(sudah)} soal sudah selesai" if args.lanjut else "run baru"
    print(f"Model: {bot.model} | {len(soal)} soal ({keterangan}) | jeda {args.jeda:g} detik\n")

    if args.lanjut:
        json_path = args.lanjut
        md_path = json_path.with_suffix(".md")
    else:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_slug = re.sub(r"[^A-Za-z0-9.-]+", "-", bot.model)
        md_path = RESULTS_DIR / f"answer_test_{model_slug}_{stamp}.md"
        json_path = md_path.with_suffix(".json")
    try:
        lokasi_json = json_path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        lokasi_json = str(json_path)
    perintah_lanjut = f"python src/evaluation/run_answer_tests.py --lanjut {lokasi_json} --jeda {args.jeda:g}"
    berhenti = None

    def simpan() -> list[str]:
        """Tulis ulang laporan dengan hasil sejauh ini; kembalikan ID yang belum selesai/error."""
        urutan = {i: n for n, i in enumerate(rencana)}
        rows.sort(key=lambda r: urutan.get(r["id"], len(urutan)))
        selesai = {r["id"] for r in rows if not r.get("error")}
        belum = [i for i in rencana if i not in selesai]
        if rows:
            tulis_laporan(rows, bot.model, md_path, len(rencana), belum, berhenti, perintah_lanjut)
            json_path.write_text(json.dumps({"model": bot.model, "status": berhenti if belum else "selesai",
                                             "rencana": rencana, "belum_selesai": belum, "results": rows},
                                            ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        return belum

    error_beruntun = 0
    try:
        for i, q in enumerate(soal, start=1):
            kasus = kasus_hitung.get(q["id"]) or kasus_definisi.get(q["id"]) or {}
            baris = {
                "id": q["id"],
                "pertanyaan": q["question"],
                "jawaban_benar": q["expected_answer"],
                "halaman_kunci": q["expected_pages"],
                "harapan_angka": kasus.get("harapan") if q["id"].startswith("H") else None,
                "catatan": kasus.get("catatan"),
                "lulus": False,
            }
            print(f"[{i}/{len(soal)}] {q['id']} ... ", end="", flush=True)
            try:
                hasil = tanya(bot, q["question"])
                if q["id"].startswith("H"):
                    cek = cek_hitungan(hasil, kasus, q["expected_pages"])
                else:
                    cek = cek_definisi(hasil, kasus, q["expected_pages"])
                baris.update({
                    "jawaban": hasil["jawaban"], "sitasi": hasil["sitasi"], "sumber_rumus": hasil["sumber_rumus"],
                    "kalkulator": hasil["kalkulator"], "peringatan": hasil["peringatan"], "cek": cek,
                    "lulus": bool(cek) and all(cek.values()),
                })
                gagal = [k for k, ok in cek.items() if not ok]
                print("LULUS" if baris["lulus"] else f"PERLU DICEK ({'; '.join(gagal)})")
            except Exception as e:  # satu soal gagal (mis. kuota) tidak langsung menghentikan run
                baris["error"] = f"{type(e).__name__}: {e}"
                # pesan 429 dicetak lengkap: di situ tertulis batas mana yang habis (per menit/per hari)
                print(f"ERROR {baris['error'] if '429' in baris['error'] else baris['error'][:200]}")
            rows[:] = [r for r in rows if r["id"] != baris["id"]] + [baris]
            simpan()

            if baris.get("error"):
                error_beruntun += 1
                if jatah_harian_habis(baris["error"]):
                    berhenti = "jatah harian LLM habis (429 per hari)"
                    break
                if error_beruntun >= BATAS_ERROR_BERUNTUN:
                    berhenti = f"{error_beruntun} error berturut-turut"
                    break
            else:
                error_beruntun = 0
            if i < len(soal):
                time.sleep(args.jeda)
    except KeyboardInterrupt:
        berhenti = "dihentikan pengguna (Ctrl+C)"

    belum = simpan()
    lulus = sum(r["lulus"] for r in rows)
    if berhenti and belum:
        print(f"\nRun BERHENTI: {berhenti}")
    print(f"\nLulus semua pemeriksaan otomatis: {lulus}/{len(rows)} (dari {len(rencana)} soal yang direncanakan)")
    if rows:
        print(f"Laporan : {md_path}")
        print(f"Detail  : {json_path}")
    if belum:
        print(f"\n{len(belum)} soal belum selesai/error: {', '.join(belum)}")
        print("Lanjutkan (mis. besok) ke laporan yang sama dengan:")
        print(perintah_lanjut)


if __name__ == "__main__":
    main()
