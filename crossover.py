# Algoritma Genetika — Proses Crossover (Pertemuan 10)
# Crossover (kawin silang) mengombinasikan gen dari dua parent untuk
# menghasilkan keturunan (offspring) baru.
# Berdasarkan NIM H1D024102, metode crossover utama yang digunakan adalah:
# - Uniform Crossover (karena digit kedua dari dua digit terakhir NIM = 2)

# 1. Import Library
import random

# 2. Fungsi untuk Uniform Crossover
# Setiap gen pada anak dipilih secara acak (biasanya peluang 50%) dari salah satu orang tua
def uniform_crossover(parent1, parent2, crossover_rate=0.8):
    # Pastikan panjang kedua parent sama
    assert len(parent1) == len(parent2)
    
    # Crossover terjadi jika bilangan acak kurang dari crossover_rate
    if random.random() < crossover_rate:
        child1 = []
        child2 = []
        for i in range(len(parent1)):
            # Lakukan penentuan asal gen dengan probabilitas 50%
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return child1, child2
    else:
        # Jika tidak terjadi crossover, anak mewarisi persis seperti parent masing-masing
        return parent1.copy(), parent2.copy()

# 3. Fungsi untuk One Point Crossover (alternatif)
def one_point_crossover(parent1, parent2, crossover_rate=0.8):
    assert len(parent1) == len(parent2)
    if random.random() < crossover_rate:
        # Pilih satu titik potong secara acak (antara index 1 sampai len - 1)
        titik_potong = random.randint(1, len(parent1) - 1)
        child1 = parent1[:titik_potong] + parent2[titik_potong:]
        child2 = parent2[:titik_potong] + parent1[titik_potong:]
        return child1, child2
    else:
        return parent1.copy(), parent2.copy()

# 4. Fungsi untuk Two Point Crossover (alternatif)
def two_point_crossover(parent1, parent2, crossover_rate=0.8):
    assert len(parent1) == len(parent2)
    if random.random() < crossover_rate:
        # Pilih dua titik potong secara acak
        titik1 = random.randint(1, len(parent1) - 2)
        titik2 = random.randint(titik1 + 1, len(parent1) - 1)
        
        child1 = parent1[:titik1] + parent2[titik1:titik2] + parent1[titik2:]
        child2 = parent2[:titik1] + parent1[titik1:titik2] + parent2[titik2:]
        return child1, child2
    else:
        return parent1.copy(), parent2.copy()

# 5. Contoh penggunaan (hanya dijalankan jika file dieksekusi secara langsung)
if __name__ == "__main__":
    p1 = [1, 1, 1, 1, 1]
    p2 = [0, 0, 0, 0, 0]
    cr = 1.0  # Dipaksa selalu terjadi crossover untuk pengujian

    print("=" * 60)
    print("                 PROSES CROSSOVER (KAWIN SILANG)")
    print("=" * 60)
    print(f"  Parent 1: {p1}")
    print(f"  Parent 2: {p2}")
    print("-" * 60)

    # Uji Uniform Crossover
    c1_uni, c2_uni = uniform_crossover(p1, p2, cr)
    print(f"  Uniform Crossover   -> Child 1: {c1_uni} | Child 2: {c2_uni}")

    # Uji One Point Crossover
    c1_one, c2_one = one_point_crossover(p1, p2, cr)
    print(f"  One Point Crossover -> Child 1: {c1_one} | Child 2: {c2_one}")

    # Uji Two Point Crossover
    c1_two, c2_two = two_point_crossover(p1, p2, cr)
    print(f"  Two Point Crossover -> Child 1: {c1_two} | Child 2: {c2_two}")
    print("=" * 60)
