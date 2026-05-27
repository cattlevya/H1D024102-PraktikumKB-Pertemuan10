# Algoritma Genetika — Evaluasi Fitness (Pertemuan 10)
# Evaluasi fitness menghitung seberapa baik setiap individu (kromosom)
# dalam menyelesaikan Knapsack Problem.
# Fitness = total keuntungan barang yang dipilih, dengan syarat total ukuran ≤ kapasitas gudang.
# Jika total ukuran melebihi kapasitas, fitness = 0 (penalti).

# 1. Data barang (nama, keuntungan, ukuran) sesuai ketentuan
barang = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7)
]

kapasitas_gudang = 15  # Ukuran maksimal gudang

# 2. Fungsi untuk menghitung nilai fitness
def hitung_fitness(kromosom, barang, kapasitas_gudang):
    total_keuntungan = 0
    total_ukuran = 0

    for i in range(len(kromosom)):
        if kromosom[i] == 1:
            # Jika gen bernilai 1, barang ke-i dipilih
            total_keuntungan += barang[i][1]
            total_ukuran += barang[i][2]

    # Jika total ukuran melebihi kapasitas gudang, beri penalti (fitness = 0)
    if total_ukuran > kapasitas_gudang:
        return 0
    else:
        return total_keuntungan

# 3. Contoh penggunaan (hanya dijalankan jika file dieksekusi secara langsung)
if __name__ == "__main__":
    # Definisi contoh populasi awal
    populasi_awal = [
        [1, 0, 1, 0, 1],  # Total ukuran = 5 + 6 + 7 = 18 (> 15) -> Fitness = 0
        [0, 1, 0, 1, 0],  # Total ukuran = 4 + 3 = 7 (<= 15) -> Fitness = 40 + 50 = 90
        [1, 1, 0, 1, 0],  # Total ukuran = 5 + 4 + 3 = 12 (<= 15) -> Fitness = 10 + 40 + 50 = 100
        [0, 1, 0, 1, 1],  # Total ukuran = 4 + 3 + 7 = 14 (<= 15) -> Fitness = 40 + 50 + 35 = 125
    ]

    print("=" * 60)
    print("                EVALUASI NILAI FITNESS")
    print("=" * 60)
    
    # Hitung fitness untuk setiap individu
    for idx, individu in enumerate(populasi_awal):
        fitness = hitung_fitness(individu, barang, kapasitas_gudang)
        # Hitung ukuran asli untuk visualisasi di terminal
        ukuran_asli = sum(barang[i][2] for i in range(len(individu)) if individu[i] == 1)
        print(f"  Individu {idx+1}: {individu} | Ukuran: {ukuran_asli:2d} | Fitness: {fitness}")
        
    print("=" * 60)
