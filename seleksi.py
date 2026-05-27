# Algoritma Genetika — Proses Seleksi (Pertemuan 10)
# Seleksi memilih individu-individu terbaik sebagai orang tua (parent)
# untuk menghasilkan generasi berikutnya melalui crossover dan mutasi.
# Berdasarkan NIM H1D024102, metode seleksi utama yang digunakan adalah:
# - Roulette Wheel Selection (RWS) (karena digit pertama dari dua digit terakhir NIM = 0)

# 1. Import Library
import random

# 2. Fungsi untuk Roulette Wheel Selection
# Individu dengan fitness lebih tinggi memiliki peluang lebih besar untuk dipilih
def roulette_wheel_selection(populasi, fitness_populasi):
    total_fitness = sum(fitness_populasi)

    # Jika semua fitness = 0, pilih individu secara acak
    if total_fitness == 0:
        idx = random.randrange(len(populasi))
        return populasi[idx], idx

    # Hitung probabilitas seleksi setiap individu
    probabilitas = [fitness / total_fitness for fitness in fitness_populasi]

    # Hitung probabilitas kumulatif
    kumulatif_prob = []
    kumulatif = 0
    for p in probabilitas:
        kumulatif += p
        kumulatif_prob.append(kumulatif)

    # Bangkitkan bilangan acak dan tentukan individu yang terpilih
    r = random.random()
    for i, kum_prob in enumerate(kumulatif_prob):
        if r <= kum_prob:
            return populasi[i], i

    # Fallback: kembalikan individu terakhir jika tidak ada yang memenuhi
    return populasi[-1], len(populasi) - 1

# 3. Fungsi untuk Tournament Selection (sebagai pembanding/alternatif)
def tournament_selection(populasi, fitness_populasi, k=3):
    if len(populasi) < k:
        k = len(populasi)

    # Pilih k peserta secara acak
    peserta_indices = random.sample(range(len(populasi)), k)
    peserta = [(populasi[i], fitness_populasi[i], i) for i in peserta_indices]

    # Urutkan berdasarkan fitness secara menurun, pilih yang tertinggi
    peserta.sort(key=lambda x: x[1], reverse=True)
    return peserta[0][0], peserta[0][2]

# 4. Contoh penggunaan (hanya dijalankan jika file dieksekusi secara langsung)
if __name__ == "__main__":
    populasi_awal    = [[1, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 1, 0, 1, 0], [0, 0, 1, 1, 1]]
    fitness_populasi = [60, 70, 100, 0]

    print("=" * 60)
    print("                 PROSES SELEKSI (PARENT)")
    print("=" * 60)
    print("Populasi:")
    for idx, (ind, fit) in enumerate(zip(populasi_awal, fitness_populasi)):
        print(f"  Individu {idx+1}: {ind} | Fitness: {fit}")
    print("-" * 60)

    # Memilih Parent menggunakan Roulette Wheel Selection
    parent1, idx1 = roulette_wheel_selection(populasi_awal, fitness_populasi)
    print(f"  Parent 1 (RWS) Terpilih : Individu {idx1+1} -> {parent1}")

    # Memilih Parent 2 menggunakan Tournament Selection
    parent2, idx2 = tournament_selection(populasi_awal, fitness_populasi)
    print(f"  Parent 2 (TS) Terpilih  : Individu {idx2+1} -> {parent2}")
    print("=" * 60)
