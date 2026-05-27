# Algoritma Genetika — Proses Mutasi (Pertemuan 10)
# Mutasi memperkenalkan variasi genetik acak ke dalam populasi untuk mencegah
# konvergensi dini (terjebak di lokal optimum).
# Berdasarkan NIM H1D024102:
# - Jumlah dua digit terakhir NIM: 0 + 2 = 2.
# - Digit terakhir hasil penjumlahan: 2.
# - Metode mutasi utama yang digunakan adalah: Uniform Mutation (Bit Flip Mutation).

# 1. Import Library
import random

# 2. Fungsi untuk Uniform Mutation (Bit Flip Mutation)
# Setiap gen pada individu diperiksa satu per satu. Dengan probabilitas tertentu (mutation_rate),
# gen tersebut akan diubah nilainya (dalam biner: 0 -> 1 atau 1 -> 0).
def uniform_mutation(kromosom, mutation_rate=0.1):
    mutasi_kromosom = kromosom.copy()
    for i in range(len(mutasi_kromosom)):
        if random.random() < mutation_rate:
            # Flip bit (0 menjadi 1, atau 1 menjadi 0)
            mutasi_kromosom[i] = 1 - mutasi_kromosom[i]
    return mutasi_kromosom

# 3. Fungsi untuk Swap Mutation (alternatif)
# Memilih dua gen secara acak, lalu menukar posisinya
def swap_mutation(kromosom, mutation_rate=0.1):
    mutasi_kromosom = kromosom.copy()
    if random.random() < mutation_rate:
        # Pilih dua indeks acak berbeda
        idx1, idx2 = random.sample(range(len(kromosom)), 2)
        # Tukar nilainya
        mutasi_kromosom[idx1], mutasi_kromosom[idx2] = mutasi_kromosom[idx2], mutasi_kromosom[idx1]
    return mutasi_kromosom

# 4. Fungsi untuk Inversion Mutation (alternatif)
# Memilih dua titik secara acak, lalu membalik (reverse) urutan gen di antaranya
def inversion_mutation(kromosom, mutation_rate=0.1):
    mutasi_kromosom = kromosom.copy()
    if random.random() < mutation_rate:
        # Pilih dua titik acak
        titik1 = random.randint(0, len(kromosom) - 2)
        titik2 = random.randint(titik1 + 1, len(kromosom) - 1)
        # Balikkan urutan sublist di antara titik1 dan titik2
        sublist_reversed = mutasi_kromosom[titik1:titik2+1][::-1]
        mutasi_kromosom[titik1:titik2+1] = sublist_reversed
    return mutasi_kromosom

# 5. Contoh penggunaan (hanya dijalankan jika file dieksekusi secara langsung)
if __name__ == "__main__":
    kro = [1, 1, 0, 0, 1]
    mr = 0.5  # Probabilitas tinggi untuk mempermudah demonstrasi mutasi

    print("=" * 60)
    print("                 PROSES MUTASI (GENETIC VARIATION)")
    print("=" * 60)
    print(f"  Kromosom Asal      : {kro}")
    print("-" * 60)

    # Uji Uniform Mutation (Bit Flip)
    random.seed(42)  # Menyetel seed agar hasil konsisten untuk demo
    print(f"  Uniform Mutation   -> {uniform_mutation(kro, mr)}")
    
    # Uji Swap Mutation
    print(f"  Swap Mutation      -> {swap_mutation(kro, mr)}")

    # Uji Inversion Mutation
    print(f"  Inversion Mutation -> {inversion_mutation(kro, mr)}")
    print("=" * 60)
