"""
spreadsheet_calc.py
Pre-calculator deterministik untuk seluruh tabel spreadsheet IKU (IKU 1, 2, 3, 5, 7, 9).
Menjalankan fungsi resmi di iku_formulas.py di sisi server Python sehingga LLM hanya
perlu dipanggil 1 kali (tanpa loop tool-calling yang boros token).
"""

from collections import defaultdict
import iku_formulas as calc


def _to_float(val) -> float:
    if val is None:
        return 0.0
    s = str(val).strip().replace("%", "")
    if not s or s == "-":
        return 0.0
    try:
        return calc._angka_id(s)
    except Exception:
        try:
            return float(s)
        except Exception:
            return 0.0


def _to_int(val) -> int:
    return int(round(_to_float(val)))


def precalculate_spreadsheet(spreadsheet_context: str) -> tuple[str, list[dict]]:
    """
    Menerima string spreadsheet_context dari Next.js (format pipa '|'),
    mendeteksi jenis IKU dari kolom header, menjalankan perhitungan resmi calc,
    dan mengembalikan (teks_konteks_matang, daftar_hasil_alat).
    """
    lines = [line.strip() for line in spreadsheet_context.splitlines() if line.strip()]

    header_idx = -1
    raw_headers = []
    headers = []
    for i, line in enumerate(lines):
        if "|" in line and any(k in line.lower() for k in ("tahun", "fakultas", "prodi")):
            header_idx = i
            raw_headers = [h.strip() for h in line.split("|")]
            headers = [h.lower() for h in raw_headers]
            break

    if header_idx == -1 or not headers:
        return spreadsheet_context, []

    rows = []
    for line in lines[header_idx + 1:]:
        if "|" not in line:
            continue
        vals = [v.strip() for v in line.split("|")]
        if len(vals) == len(headers):
            rows.append(dict(zip(headers, vals)))

    if not rows:
        return spreadsheet_context, []

    col_set = set(headers)

    # -----------------------------------------------------------------------
    # 1. DETEKSI IKU 001 (lulus_tepat_waktu & mahasiswa_aktif)
    # -----------------------------------------------------------------------
    if "lulus_tepat_waktu" in col_set and "mahasiswa_aktif" in col_set:
        return _calc_iku1(rows)

    # -----------------------------------------------------------------------
    # 2. DETEKSI IKU 002 (responden ts & bekerja / lanjut studi / wirausaha)
    # -----------------------------------------------------------------------
    if "responden ts" in col_set or "total lulusan" in col_set:
        return _calc_iku2(rows)

    # -----------------------------------------------------------------------
    # 3. DETEKSI IKU 003 (mahasiswa memenuhi iku 003)
    # -----------------------------------------------------------------------
    if "mahasiswa memenuhi iku 003" in col_set:
        return _calc_rasio_umum(
            rows=rows,
            iku_label="IKU 3 (Mahasiswa Berkegiatan/Berprestasi di Luar Prodi)",
            kode_rumus="iku3",
            col_pembilang="mahasiswa memenuhi iku 003",
            col_penyebut="mahasiswa aktif",
            raw_headers=raw_headers,
            headers=headers,
        )

    # -----------------------------------------------------------------------
    # 4. DETEKSI IKU 005 (total_dosen & total_luaran)
    # -----------------------------------------------------------------------
    if "total_dosen" in col_set and "total_luaran" in col_set:
        return _calc_rasio_umum(
            rows=rows,
            iku_label="IKU 5 (Rasio Luaran Hasil Kerja Sama terhadap Total Dosen)",
            kode_rumus="iku5",
            col_pembilang="total_luaran",
            col_penyebut="total_dosen",
            raw_headers=raw_headers,
            headers=headers,
        )

    # -----------------------------------------------------------------------
    # 5. DETEKSI IKU 007 (program_memenuhi_iku & total_program_tridharma)
    # -----------------------------------------------------------------------
    if "program_memenuhi_iku" in col_set and "total_program_tridharma" in col_set:
        return _calc_rasio_umum(
            rows=rows,
            iku_label="IKU 7 (Keterlibatan dalam SDGs)",
            kode_rumus="iku7",
            col_pembilang="program_memenuhi_iku",
            col_penyebut="total_program_tridharma",
            raw_headers=raw_headers,
            headers=headers,
        )

    # -----------------------------------------------------------------------
    # 6. DETEKSI IKU 009 (total_non_mahasiswa & total_pendapatan)
    # -----------------------------------------------------------------------
    if "total_non_mahasiswa" in col_set and "total_pendapatan" in col_set:
        return _calc_iku9(rows, raw_headers, headers)

    return spreadsheet_context, []


def _calc_iku1(rows: list[dict]) -> tuple[str, list[dict]]:
    hasil_alat = []
    by_year = defaultdict(list)
    by_year_fac = defaultdict(list)
    by_year_deg = defaultdict(list)
    detail_lines = []

    sumber_resmi = calc._keluaran("iku1_aee_pt", 0, "%", [])["sumber"]

    for r in rows:
        thn = r.get("tahun", "-")
        fak = r.get("fakultas", "-")
        prodi = r.get("prodi", "-")
        jenjang = r.get("jenjang", "S1").upper()
        masuk = _to_int(r.get("mahasiswa_masuk", 0))
        lulus = _to_int(r.get("lulus_tepat_waktu", 0))
        do_mhs = _to_int(r.get("mahasiswa_do", 0))
        pindah = _to_int(r.get("mahasiswa_pindah", 0))
        aktif = _to_int(r.get("mahasiswa_aktif", 0))

        # Di spreadsheet kampus, mahasiswa_aktif sudah merupakan basis (masuk - DO - pindah).
        # Gunakan fungsi resmi calc.iku1_aee_prodi dengan total_mahasiswa = aktif.
        try:
            res_prodi = calc.iku1_aee_prodi(
                jenjang=jenjang,
                lulus_tepat_waktu=lulus,
                total_mahasiswa=aktif,
            )
            aee_real = res_prodi["hasil"]["aee_realisasi_pct"]
            capaian = res_prodi["hasil"]["tingkat_pencapaian_pct"]
            sumber_resmi = res_prodi["sumber"]
        except Exception:
            ideal = calc.AEE_IDEAL.get(jenjang, 25.0)
            aee_real = round(lulus / aktif * 100, 2) if aktif > 0 else 0.0
            capaian = round(aee_real / ideal * 100, 2) if ideal > 0 else 0.0

        ideal_val = calc.AEE_IDEAL.get(jenjang, 25)
        by_year[thn].append(capaian)
        by_year_fac[(thn, fak)].append(capaian)
        by_year_deg[(thn, jenjang)].append(capaian)

        detail_lines.append(
            f"{thn} | {fak} | {prodi} | {jenjang} | {masuk} | {lulus} | {do_mhs} | {pindah} | {aktif} | "
            f"{aee_real:.2f}% | {ideal_val}% | {capaian:.2f}%"
        )

    out = ["=== HASIL PERHITUNGAN RESMI KALKULATOR IKU 1 (AEE PT) ==="]
    out.append(f"Sumber Rumus: {sumber_resmi}")
    out.append("\n1. Rekap Capaian IKU 1 (Rata-rata Tingkat Pencapaian AEE PT) per Tahun:")
    for thn, vals in sorted(by_year.items()):
        avg_v = round(sum(vals) / len(vals), 2)
        sum_v = round(sum(vals), 2)
        out.append(f"   - Tahun {thn}: {avg_v:.2f}% (Jumlah Tingkat Pencapaian = {sum_v:.2f}% dibagi {len(vals)} prodi)")
        hasil_alat.append({
            "alat": "hitung_iku",
            "argumen": {"fungsi": "iku1_aee_pt", "tahun": thn},
            "hasil": {"hasil": avg_v, "satuan": "%", "sumber": sumber_resmi},
        })

    out.append("\n2. Rekap Capaian IKU 1 per Tahun & Fakultas:")
    for (thn, fak), vals in sorted(by_year_fac.items()):
        avg_f = round(sum(vals) / len(vals), 2)
        out.append(f"   - {thn} | Fakultas {fak}: {avg_f:.2f}% ({len(vals)} prodi)")
        hasil_alat.append({
            "alat": "hitung_iku",
            "argumen": {"fungsi": "iku1_aee_pt", "tahun": thn, "fakultas": fak},
            "hasil": {"hasil": avg_f, "satuan": "%", "sumber": sumber_resmi},
        })

    out.append("\n3. Rekap Capaian IKU 1 per Tahun & Jenjang:")
    for (thn, jnj), vals in sorted(by_year_deg.items()):
        avg_j = round(sum(vals) / len(vals), 2)
        out.append(f"   - {thn} | Jenjang {jnj}: {avg_j:.2f}% ({len(vals)} prodi)")

    out.append("\n=== TABEL DATA & PERHITUNGAN PER PRODI ===")
    out.append("tahun | fakultas | prodi | jenjang | mhs_masuk | lulus_tepat | mhs_do | mhs_pindah | mhs_aktif | AEE_realisasi | AEE_ideal | tingkat_pencapaian")
    out.extend(detail_lines)

    return "\n".join(out), hasil_alat


def _calc_iku2(rows: list[dict]) -> tuple[str, list[dict]]:
    hasil_alat = []
    by_year = defaultdict(lambda: defaultdict(int))
    by_year_fac = defaultdict(lambda: defaultdict(int))
    detail_lines = []

    sumber_resmi = calc._keluaran("iku2", 0, "%", [])["sumber"]

    for r in rows:
        thn = r.get("tahun", "-")
        fak = r.get("fakultas", "-")
        prodi = r.get("prodi", "-")
        jnj = r.get("jenjang", "-")

        lulusan = _to_int(r.get("total lulusan", 0))
        resp = _to_int(r.get("responden ts", 0))
        b_6_12 = _to_int(r.get("bekerja <6 bln >1.2 ump", 0))
        b_12_12 = _to_int(r.get("bekerja <1 thn >1.2 ump", 0))
        b_12_kurang = _to_int(r.get("bekerja <1 thn <1.2 ump", 0))
        studi = _to_int(r.get("lanjut studi", 0))
        wira = _to_int(r.get("wirausaha", 0))
        belum = _to_int(r.get("belum bekerja", 0))
        tidak_lacak = _to_int(r.get("tidak terlacak", 0))

        # Petakan ke kunci resmi BOBOT_IKU2 di spec
        # Bobot standar IKU 2: bekerja <=6 bln >1.2 UMP (1.0), lanjut studi (1.0),
        # bekerja <=1 thn >1.2 UMP (0.8), wirausaha (0.8 / 1.2 sesuai spec), bekerja <1.2 UMP (0.5)
        skor_baris = (b_6_12 * 1.0) + (studi * 1.0) + (b_12_12 * 0.8) + (wira * 0.8) + (b_12_kurang * 0.5)
        capaian_prodi = round(skor_baris / resp * 100, 2) if resp > 0 else 0.0

        for grp in (by_year[thn], by_year_fac[(thn, fak)]):
            grp["lulusan"] += lulusan
            grp["resp"] += resp
            grp["skor_x100"] += int(round(skor_baris * 100))

        detail_lines.append(
            f"{thn} | {fak} | {prodi} | {jnj} | {lulusan} | {resp} | {b_6_12} | {b_12_12} | "
            f"{b_12_kurang} | {studi} | {wira} | {belum} | {tidak_lacak} | {capaian_prodi:.2f}%"
        )

    out = ["=== HASIL PERHITUNGAN RESMI KALKULATOR IKU 2 ==="]
    out.append(f"Sumber Rumus: {sumber_resmi}")
    out.append("\n1. Rekap Capaian IKU 2 & Slovin Responden Minimum per Tahun:")
    for thn, g in sorted(by_year.items()):
        skor_tot = g["skor_x100"] / 100.0
        cap_thn = round(skor_tot / g["resp"] * 100, 2) if g["resp"] > 0 else 0.0
        slovin = calc.iku2_responden_minimum(g["lulusan"])["hasil"] if g["lulusan"] > 0 else 0
        out.append(
            f"   - Tahun {thn}: Capaian IKU 2 = {cap_thn:.2f}% "
            f"(Total Skor Berbobot = {skor_tot:.2f} dari {g['resp']} responden; "
            f"Total Lulusan = {g['lulusan']}, Responden Minimum Slovin = {slovin})"
        )
        hasil_alat.append({
            "alat": "hitung_iku",
            "argumen": {"fungsi": "iku2", "tahun": thn},
            "hasil": {"hasil": cap_thn, "satuan": "%", "sumber": sumber_resmi},
        })

    out.append("\n2. Rekap Capaian IKU 2 per Tahun & Fakultas:")
    for (thn, fak), g in sorted(by_year_fac.items()):
        skor_tot = g["skor_x100"] / 100.0
        cap_fak = round(skor_tot / g["resp"] * 100, 2) if g["resp"] > 0 else 0.0
        out.append(f"   - {thn} | Fakultas {fak}: {cap_fak:.2f}% (Responden: {g['resp']}, Lulusan: {g['lulusan']})")

    out.append("\n=== TABEL DATA & CAPAIAN IKU 2 PER PRODI ===")
    out.append("Tahun | Fakultas | Prodi | Jenjang | Total_Lulusan | Responden_TS | Bekerja_<6bln_>1.2UMP | Bekerja_<1thn_>1.2UMP | Bekerja_<1thn_<1.2UMP | Lanjut_Studi | Wirausaha | Belum_Bekerja | Tidak_Terlacak | Capaian_IKU2")
    out.extend(detail_lines)

    return "\n".join(out), hasil_alat


def _calc_rasio_umum(
    rows: list[dict],
    iku_label: str,
    kode_rumus: str,
    col_pembilang: str,
    col_penyebut: str,
    raw_headers: list[str],
    headers: list[str],
) -> tuple[str, list[dict]]:
    hasil_alat = []
    by_year = defaultdict(lambda: [0.0, 0.0, []])
    by_year_fac = defaultdict(lambda: [0.0, 0.0, []])

    sumber_resmi = (
        calc._keluaran(kode_rumus, 0, "%", [])["sumber"]
        if kode_rumus in calc.RUMUS
        else f"{calc.BUKU}"
    )

    for r in rows:
        thn = r.get("tahun", "-")
        fak = r.get("fakultas", "-")
        a = _to_float(r.get(col_pembilang, 0))
        b = _to_float(r.get(col_penyebut, 0))
        pct_row = (a / b * 100.0) if b > 0 else 0.0

        by_year[thn][0] += a
        by_year[thn][1] += b
        by_year[thn][2].append(pct_row)

        by_year_fac[(thn, fak)][0] += a
        by_year_fac[(thn, fak)][1] += b
        by_year_fac[(thn, fak)][2].append(pct_row)

    out = [f"=== HASIL PERHITUNGAN RESMI KALKULATOR {iku_label} ==="]
    out.append(f"Sumber Rumus: {sumber_resmi}")
    out.append("\n1. Rekap Capaian per Tahun:")
    for thn, (tot_a, tot_b, pcts) in sorted(by_year.items()):
        rasio_tot = round(tot_a / tot_b * 100, 2) if tot_b > 0 else 0.0
        avg_prodi = round(sum(pcts) / len(pcts), 2) if pcts else 0.0
        out.append(
            f"   - Tahun {thn}: Rasio Agregat Kampus = {rasio_tot:.2f}% "
            f"(Total {col_pembilang} = {tot_a:g} / Total {col_penyebut} = {tot_b:g} × 100%) | "
            f"Rata-rata Persentase Prodi = {avg_prodi:.2f}% ({len(pcts)} baris)"
        )
        hasil_alat.append({
            "alat": "hitung_iku",
            "argumen": {"fungsi": kode_rumus, "tahun": thn},
            "hasil": {"hasil": rasio_tot, "satuan": "%", "sumber": sumber_resmi},
        })

    out.append("\n2. Rekap Capaian per Tahun & Fakultas:")
    for (thn, fak), (tot_a, tot_b, pcts) in sorted(by_year_fac.items()):
        rasio_f = round(tot_a / tot_b * 100, 2) if tot_b > 0 else 0.0
        avg_f = round(sum(pcts) / len(pcts), 2) if pcts else 0.0
        out.append(
            f"   - {thn} | Fakultas {fak}: Rasio = {rasio_f:.2f}% "
            f"({tot_a:g} / {tot_b:g}) | Rata-rata Prodi = {avg_f:.2f}%"
        )

    out.append("\n=== TABEL DATA DETAIL ===")
    out.append(" | ".join(raw_headers))
    for r in rows:
        out.append(" | ".join(str(r.get(h, "")) for h in headers))

    return "\n".join(out), hasil_alat


def _calc_iku9(rows: list[dict], raw_headers: list[str], headers: list[str]) -> tuple[str, list[dict]]:
    hasil_alat = []
    by_year = defaultdict(lambda: [0.0, 0.0, 0.0, []])
    sumber_resmi = calc._keluaran("iku9", 0, "%", [])["sumber"]

    for r in rows:
        thn = r.get("tahun", "-")
        non_mhs = _to_float(r.get("total_non_mahasiswa", 0))
        ukt = _to_float(r.get("pendapatan_ukt", 0))
        tot = _to_float(r.get("total_pendapatan", 0))
        pct_row = _to_float(r.get("iku009", 0)) or ((non_mhs / tot * 100.0) if tot > 0 else 0.0)

        by_year[thn][0] += non_mhs
        by_year[thn][1] += ukt
        by_year[thn][2] += tot
        by_year[thn][3].append(pct_row)

    out = ["=== HASIL PERHITUNGAN RESMI KALKULATOR IKU 9 (Pendapatan Non-Mahasiswa/UKT) ==="]
    out.append(f"Sumber Rumus: {sumber_resmi}")
    out.append("\n1. Rekap Capaian IKU 9 per Tahun:")
    for thn, (non_mhs, ukt, tot, pcts) in sorted(by_year.items()):
        rasio_tot = round(non_mhs / tot * 100, 2) if tot > 0 else 0.0
        avg_fak = round(sum(pcts) / len(pcts), 2) if pcts else 0.0
        out.append(
            f"   - Tahun {thn}: Capaian Agregat Kampus = {rasio_tot:.2f}% "
            f"(Total Non-Mahasiswa = {calc._fmt(non_mhs)} / Total Pendapatan = {calc._fmt(tot)}, "
            f"Pendapatan UKT [tidak dihitung] = {calc._fmt(ukt)}) | "
            f"Rata-rata Fakultas = {avg_fak:.2f}%"
        )
        hasil_alat.append({
            "alat": "hitung_iku",
            "argumen": {"fungsi": "iku9", "tahun": thn},
            "hasil": {"hasil": rasio_tot, "satuan": "%", "sumber": sumber_resmi},
        })

    out.append("\n=== TABEL DATA DETAIL PER FAKULTAS ===")
    out.append(" | ".join(raw_headers))
    for r in rows:
        out.append(" | ".join(str(r.get(h, "")) for h in headers))

    return "\n".join(out), hasil_alat