import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.stats.multicomp as mc

def get_input_list(prompt):
    print(prompt)
    items = []
    while True:
        item = input("Masukkan item (atau ketik 'selesai' untuk berhenti): ")
        if item.lower() == 'selesai':
            break
        items.append(item)
    return items

def normalize_probabilities(proporsi_ratings):
    total = sum(proporsi_ratings.values())
    return {k: v / total for k, v in proporsi_ratings.items()}

def generate_ratings(size, proporsi_ratings, unggulkan=False):
    proporsi_ratings = normalize_probabilities(proporsi_ratings)
    ratings = []
    if unggulkan:
        # Jika diunggulkan, proporsi rating 5 ditingkatkan signifikan
        for rating, proporsi in proporsi_ratings.items():
            if rating == 5:
                ratings.extend([rating] * int(proporsi * size * 3))  # Gandakan proporsi untuk rating 5
            else:
                ratings.extend([rating] * int(proporsi * size * 0.5))  # Kurangi proporsi untuk rating lainnya
    else:
        for rating, proporsi in proporsi_ratings.items():
            ratings.extend([rating] * int(proporsi * size))
    ratings = np.array(ratings)
    if len(ratings) < size:
        ratings = np.append(ratings, np.random.choice(list(proporsi_ratings.keys()), size - len(ratings), p=list(proporsi_ratings.values())))
    np.random.shuffle(ratings)
    return ratings

def perform_anova(data, hal):
    formula = f'{hal} ~ C(Formulasi)'
    model = ols(formula, data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    return anova_table

def perform_duncan(data, hal):
    comp = mc.MultiComparison(data[hal], data['Formulasi'])
    duncan_result = comp.tukeyhsd(alpha=0.05)  # Tukey HSD sebagai pengganti Duncan
    return duncan_result.summary()

def main():
    # Meminta input dari pengguna
    jumlah_panelis = int(input("Masukkan jumlah panelis: "))
    jumlah_formulasi = int(input("Masukkan jumlah formulasi: "))
    hal_diuji = get_input_list("Masukkan hal yang diuji (contoh: Aroma, Rasa, Tekstur):")
    
    # Menanyakan apakah ingin ada pengaruh nyata
    ada_pengaruh = input("Apakah ingin ada pengaruh nyata pada hal yang diuji? (ya/tidak): ").lower()

    if ada_pengaruh == 'ya':
        hal_pengaruh = input("Hal yang diuji mana yang ingin diadakan pengaruh nyata?: ")
        formulasi_unggul = int(input("Formulasi mana yang ingin diunggulkan?: "))

    # Definisi proporsi ratings
    proporsi_ratings = {
        1: 0.009,
        2: 0.015,
        3: 0.190,
        4: 0.320,
        5: 0.314
    }
    
    # Membuat writer untuk menulis ke file Excel
    output_file = 'hasil_organoleptik.xlsx'
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for hal in hal_diuji:
            # Membuat DataFrame dengan kolom awal
            columns = ['Panelis', 'Formulasi', hal]
            data = []

            # Mengisi DataFrame dengan data
            for panelis in range(1, jumlah_panelis + 1):
                for formulasi in range(1, jumlah_formulasi + 1):
                    if ada_pengaruh == 'ya' and hal == hal_pengaruh and formulasi == formulasi_unggul:
                        rating = generate_ratings(1, proporsi_ratings, unggulkan=True)[0]
                    else:
                        rating = generate_ratings(1, proporsi_ratings)[0]
                    data.append([f'Panelis {panelis}', f'Formulasi {formulasi}', rating])

            df = pd.DataFrame(data, columns=columns)
            
            # Menyimpan DataFrame ke sheet yang berbeda
            df.to_excel(writer, sheet_name=hal, index=False)

            # Melakukan uji ANOVA
            anova_results = perform_anova(df, hal)
            anova_df = anova_results.reset_index()
            anova_df.to_excel(writer, sheet_name=f'ANOVA_{hal}', index=False)

            # Jika ada perbedaan nyata, lakukan uji Duncan
            if anova_results['PR(>F)'].iloc[0] < 0.05:
                duncan_results = perform_duncan(df, hal)
                duncan_df = pd.DataFrame(duncan_results.data[1:], columns=duncan_results.data[0])
                duncan_df.to_excel(writer, sheet_name=f'Duncan_{hal}', index=False)

    print(f"Data organoleptik telah disimpan ke {output_file}")

if __name__ == "__main__":
    main()
