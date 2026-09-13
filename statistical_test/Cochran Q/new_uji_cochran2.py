import pandas as pd
from statsmodels.stats.contingency_tables import cochrans_q

def jalankan_analisis_statistik(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"❌ Gagal membaca file: {e}")
        return

    # !!! PERBAIKAN: Tentukan nama kolom label asli/ground truth di Excel Anda !!!
    kolom_label_asli = 'LABEL_GROUND_TRUTH' 
    
    if kolom_label_asli not in df.columns:
        print(f"❌ Kolom ground truth '{kolom_label_asli}' tidak ditemukan. Pastikan nama kolom sudah sesuai.")
        return

    pemetaan_model = {
        'LABEL_Paraphrase': 'AI-Paraphrase',
        'LABEL_Rewrite': 'AI-Rewrite',
        'LABEL_Generate': 'AI-Generated'
    }
    
    kolom_skenario = list(pemetaan_model.keys())
    
    for col in kolom_skenario:
        if col not in df.columns:
            print(f"❌ Kolom '{col}' tidak ditemukan di Excel Anda.")
            return

    # !!! PERBAIKAN: Buat DataFrame baru khusus untuk evaluasi ketepatan tebakan (Benar=1, Salah=0) !!!
    df_evaluasi = pd.DataFrame()
    for col in kolom_skenario:
        # Jika nilai prediksi sama dengan label asli, maka dinilai 1 (Sukses/Benar), jika beda dinilai 0 (Gagal/Salah)
        df_evaluasi[col] = (df[col] == df[kolom_label_asli]).astype(int)

    # 2. Menghitung Uji Cochran's Q menggunakan data evaluasi yang sudah valid
    hasil_q = cochrans_q(df_evaluasi[kolom_skenario])
    
    p_value_str = f"< 0.005" if hasil_q.pvalue < 0.005 else f"{hasil_q.pvalue:.4f}"

    # 3. Membuat dan Menampilkan Header Tabel
    header = f"{'Model':<15}\t{'Jumlah Sample (N)':<17}\t{'Sukses (1)':<10}\t{'Gagal (0)':<9}\t{'Akurasi (%)':<11}\t{'Cochran’s Q':<12}\t{'Degree Of Freedom (df)':<23}\t{'Sig. (p-value)'}"
    print(header)
    
    # 4. Melakukan Iterasi Baris untuk Setiap Model menggunakan df_evaluasi
    for i, (kolom_asli, nama_tampilan) in enumerate(pemetaan_model.items()):
        n_sample = len(df_evaluasi[kolom_asli])
        sukses = int((df_evaluasi[kolom_asli] == 1).sum()) # Menghitung total tebakan yang BENAR
        gagal = int((df_evaluasi[kolom_asli] == 0).sum())  # Menghitung total tebakan yang SALAH
        akurasi = (sukses / n_sample) * 100
        
        if i == 0:
            print(f"{nama_tampilan:<15}\t{n_sample:<17}\t{sukses:<10}\t{gagal:<9}\t{akurasi:<11.2f}\t{hasil_q.statistic:<12.2f}\t{hasil_q.df:<23}\t{p_value_str}")
        else:
            print(f"{nama_tampilan:<15}\t{n_sample:<17}\t{sukses:<10}\t{gagal:<9}\t{akurasi:<11.2f}\t{'':<12}\t{'':<23}\t{''}")

# Jalankan fungsi
jalankan_analisis_statistik("uji_cochran.xlsx")
