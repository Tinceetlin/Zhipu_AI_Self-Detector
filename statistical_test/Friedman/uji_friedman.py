import pandas as pd
from scipy.stats import friedmanchisquare
from tabulate import tabulate

# 1. Tentukan nama file Excel
file_excel = "uji_friedman.xlsx"

# Wadah untuk menyimpan baris data tabel hasil
hasil_tabel = []


def hitung_friedman(nama_sheet, nama_variabel):
    try:
        # 2. Baca data dari sheet
        df = pd.read_excel(file_excel, sheet_name=nama_sheet)

        # 3. Ambil data kelompok dan hapus baris yang kosong (dropna) untuk menjamin berpasangan sempurna
        grup_murni = df["Z.AI_Generate"].dropna()
        grup_rewrite = df["Z.AI_Rewrite"].dropna()
        grup_paraphrase = df["Z.AI_Paraphrase"].dropna()

        # Pastikan jumlah baris sama setelah dropna
        min_len = min(len(grup_murni), len(grup_rewrite), len(grup_paraphrase))
        grup_murni = grup_murni.iloc[:min_len]
        grup_rewrite = grup_rewrite.iloc[:min_len]
        grup_paraphrase = grup_paraphrase.iloc[:min_len]

        # 4. Hitung Median untuk masing-masing kelompok
        median_murni = grup_murni.median()
        median_rewrite = grup_rewrite.median()
        median_paraphrase = grup_paraphrase.median()

        # =========================================================================
        # FITUR TAMBAHAN: HITUNG PERSENTASE TIES (NILAI KEMBAR) PER BARIS
        # =========================================================================
        # Menggabungkan data secara horizontal untuk mendeteksi kesamaan nilai dalam satu subjek/baris
        df_gabung = pd.DataFrame(
            {
                "murni": grup_murni.values,
                "rewrite": grup_rewrite.values,
                "paraphrase": grup_paraphrase.values,
            }
        )

        # Hitung jumlah nilai unik per baris. Jika unik < 3, berarti ada nilai kembar (ties) pada baris tersebut.
        baris_ada_ties = df_gabung.apply(
            lambda x: x.nunique() < len(x), axis=1
        ).sum()
        persen_ties = (baris_ada_ties / len(df_gabung)) * 100
        # =========================================================================

        # 5. Jalankan Uji Friedman
        # (Catatan: scipy secara otomatis menerapkan Tie Correction matematis pada fungsi ini)
        stat, p_value = friedmanchisquare(
            grup_murni, grup_rewrite, grup_paraphrase
        )

        # 6. Hitung Derajat Kebebasan (df = jumlah kelompok - 1)
        df_value = 3 - 1

        # 7. Tentukan Kesimpulan (Alpha = 0.05)
        kesimpulan = "Signifikan" if p_value < 0.05 else "Tidak Signifikan"

        # 8. Masukkan data ke dalam baris tabel (dibulatkan 4 angka di belakang koma)
        # Menambahkan informasi persentase Ties ke dalam baris tabel
        hasil_tabel.append(
            [
                nama_variabel,
                f"{median_murni:.4f}",
                f"{median_rewrite:.4f}",
                f"{median_paraphrase:.4f}",
                f"{stat:.4f}",
                df_value,
                f"{p_value:.4f}" if p_value >= 0.0001 else "< 0.0001",
                f"{persen_ties:.1f}%",
                kesimpulan,
            ]
        )

    except FileNotFoundError:
        print(f"Error: File '{file_excel}' tidak ditemukan.")
        return False
    except KeyError as e:
        print(f"Error: Kolom {e} tidak ditemukan di sheet '{nama_sheet}'.")
        return False
    return True


# Jalankan fungsi untuk kedua variabel
sukses_1 = hitung_friedman("Confidence_Score", "Verbalized Confidence Score")
sukses_2 = hitung_friedman("Prediction_Entropy", "Prediction Entropy")

# 9. Cetak hasil akhir dalam bentuk tabel jika pembacaan data sukses
if sukses_1 and sukses_2:
    # Memperbarui header dengan kolom baru 'Intensitas Ties'
    header = [
        "Variabel Evaluasi",
        "Median\n(Murni AI)",
        "Median\n(AI-Rewrite)",
        "Median\n(AI-Paraphrase)",
        "Chi-Square\n(χ²)*",
        "df",
        "p-value",
        "Intensitas\nTies",
        "Kesimpulan",
    ]

    print("\n" + "=" * 80)
    print("TABEL HASIL UJI FRIEDMAN (DENGAN KOREKSI NILAI KEMBAR)")
    print("=" * 80)
    print(tabulate(hasil_tabel, headers=header, tablefmt="grid"))
    print("\n* Nilai Chi-Square (χ²) otomatis disesuaikan dengan Tie Correction.")
    print("* Signifikan jika p-value < 0.05")
    print(
        "* Intensitas Ties tinggi (>50%) mengindikasikan adanya Floor/Ceiling Effect berat."
    )
