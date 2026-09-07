import pandas as pd
import numpy as np
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests

# ==========================================
# 1. MEMBACA FILE EXCEL
# ==========================================
file_name = "mcnemar.xlsx"
df = pd.read_excel(file_name)

# Definisikan nama kolom model yang ada di Excel
# Skrip ini otomatis mendeteksi semua kombinasi berpasangan antar model ini
nama_model = ["AI-Generated", "AI-Rewrite", "AI-Paraphrase"]
# model A = AI-Generated
# model B = AI-Rewrite
# model C = AI-Paraphrase

# ==========================================
# 2. PROSES PAIRWISE MCNEMAR TEST
# ==========================================

pasangan_uji = []
p_values_mentah = []
chi2_stats = []

# Melakukan perbandingan berpasangan (A vs B, A vs C, B vs C)
for i in range(len(nama_model)):
    for j in range(i + 1, len(nama_model)):
        model_1 = nama_model[i]
        model_2 = nama_model[j]

        # Membuat tabel kontingensi 2x2 (Cross-tabulation)
        # Baris/Kolom 0 = Salah, Baris/Kolom 1 = Benar
        tabel_kontingensi = pd.crosstab(df[model_1], df[model_2])

        # Memastikan tabel berukuran 2x2 penuh meski ada kategori yang kosong
        tabel_kontingensi = tabel_kontingensi.reindex(
            index=[0, 1], columns=[0, 1], fill_value=0
        )

        # Menjalankan Uji McNemar
        # exact=True digunakan jika ada sel dengan frekuensi rendah (< 25)
        # correction=True menggunakan koreksi kontinuitas Edwards untuk sampel besar
        hasil_mcnemar = mcnemar(tabel_kontingensi, exact=False, correction=True)

        # Simpan hasil sementara
        pasangan_uji.append(f"{model_1} vs {model_2}")
        p_values_mentah.append(hasil_mcnemar.pvalue)
        chi2_stats.append(hasil_mcnemar.statistic)


# ==========================================
# 3. MENERAPKAN KOREKSI HOLM
# ==========================================
# multipletests akan mengurutkan p-value dan mengoreksinya berdasarkan metode Holm
tolak_h0, p_values_terkoreksi, _, _ = multipletests(
    p_values_mentah, alpha=0.05, method="holm"
)


# ==========================================
# 4. MENAMPILKAN HASIL AKHIR (TABEL)
# ==========================================
df_hasil = pd.DataFrame(
    {
        "Perbandingan Pasangan": pasangan_uji,
        "Chi-Square Stat": chi2_stats,
        "p-value Mentah": p_values_mentah,
        "p-value (Koreksi Holm)": p_values_terkoreksi,
        "Signifikan (Alpha 0.05)?": [
            "YA (Tolak H0)" if x else "TIDAK (Terima H0)" for x in tolak_h0
        ],
    }
)

print("\n====================================================================")
print("     HASIL UJI LANJUT: PAIRWISE MCNEMAR TEST & KOREKSI HOLM")
print("====================================================================")
print(df_hasil.to_string(index=False))
print("====================================================================\n")

# Opsional: Menyimpan hasil analisis langsung ke file Excel baru
df_hasil.to_excel("hasil_post_hoc_mcnemar.xlsx", index=False)
print("Hasil analisis telah disimpan ke dalam file 'hasil_post_hoc_mcnemar.xlsx'")
