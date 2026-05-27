# Algoritma Genetika — Inisiasi Populasi (Pertemuan 10)
# Langkah pertama dalam Algoritma Genetika adalah membangkitkan populasi awal
# secara acak, di mana setiap individu merepresentasikan solusi potensial (kromosom)

# 1. Import Library
import random

# 2. Fungsi untuk inisialisasi populasi
# Setiap kromosom direpresentasikan sebagai array biner:
# gen = 1 → barang dipilih, gen = 0 → barang tidak dipilih
def inisialisasi_populasi(jumlah_populasi, jumlah_gen):
    populasi = []
    for i in range(jumlah_populasi):
        # Membuat kromosom dengan gen biner secara acak
        kromosom = [random.randint(0, 1) for _ in range(jumlah_gen)]
        populasi.append(kromosom)
    return populasi

# 3. Contoh penggunaan (hanya dijalankan jika file dieksekusi secara langsung)
if __name__ == "__main__":
    jumlah_populasi = 10  # Jumlah individu dalam populasi
    jumlah_gen      = 5   # Jumlah barang (gen) dalam kromosom

    populasi_awal = inisialisasi_populasi(jumlah_populasi, jumlah_gen)

    # Menampilkan populasi awal
    print("=" * 60)
    print("                 INISIASI POPULASI AWAL")
    print("=" * 60)
    for idx, individu in enumerate(populasi_awal):
        print(f"  Individu {idx+1:2d}: {individu}")
    print("=" * 60)
