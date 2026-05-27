# Algoritma Genetika — Main Program (Pertemuan 10)
# Program utama untuk menyelesaikan 0-1 Knapsack Problem menggunakan Algoritma Genetika
# dengan spesifikasi metode sesuai NIM H1D024102:
# - Seleksi: Roulette Wheel Selection (RWS)
# - Crossover: Uniform Crossover
# - Mutasi: Uniform Mutation (Bit Flip)

# 1. Import Library dan Modul Pendukung
import os
import random
import matplotlib.pyplot as plt
from InisiasiPopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness, barang, kapasitas_gudang
from selection import roulette_wheel_selection
from crossover import uniform_crossover
from mutation import uniform_mutation

# 2. Parameter Algoritma Genetika
JUMLAH_POPULASI  = 20    # Ukuran populasi
CROSSOVER_RATE   = 0.8   # Probabilitas kawin silang
MUTATION_RATE    = 0.1   # Probabilitas mutasi gen
JUMLAH_GENERASI  = 50    # Jumlah iterasi generasi
ELITISME_SIZE    = 2     # Jumlah individu terbaik yang langsung disalin ke generasi berikutnya

# 3. Fungsi Utama Algoritma Genetika
def run_genetic_algorithm():
    # Inisialisasi populasi awal secara acak
    jumlah_gen = len(barang)
    populasi = inisialisasi_populasi(JUMLAH_POPULASI, jumlah_gen)
    
    # List untuk menyimpan statistik perkembangan fitness untuk visualisasi grafik
    history_best_fitness = []
    history_avg_fitness = []
    
    global_best_individual = None
    global_best_fitness = -1

    print("=" * 60)
    print("                PROSES ITERASI ALGORITMA GENETIKA")
    print("=" * 60)

    for gen in range(JUMLAH_GENERASI):
        # Hitung fitness untuk setiap individu di populasi saat ini
        fitness_populasi = [hitung_fitness(ind, barang, kapasitas_gudang) for ind in populasi]
        
        # Temukan individu terbaik pada generasi saat ini
        best_fitness_current = max(fitness_populasi)
        best_idx = fitness_populasi.index(best_fitness_current)
        best_individual_current = populasi[best_idx]
        
        # Hitung rata-rata fitness pada generasi saat ini
        avg_fitness_current = sum(fitness_populasi) / JUMLAH_POPULASI
        
        # Simpan ke history untuk keperluan plotting
        history_best_fitness.append(best_fitness_current)
        history_avg_fitness.append(avg_fitness_current)
        
        # Update solusi terbaik global jika ditemukan yang lebih baik
        if best_fitness_current > global_best_fitness:
            global_best_fitness = best_fitness_current
            global_best_individual = best_individual_current.copy()
            
        # Tampilkan informasi log per generasi
        print(f"  Generasi {gen+1:02d}: Fitness Terbaik = {best_fitness_current:3d} | Rata-rata Fitness = {avg_fitness_current:5.1f} | Kromosom Terbaik = {best_individual_current}")
        
        # Membuat populasi baru (generasi berikutnya)
        populasi_baru = []
        
        # --- Penerapan Elitisme ---
        # Mengurutkan populasi saat ini berdasarkan fitness secara menurun
        populasi_urut = [x for _, x in sorted(zip(fitness_populasi, populasi), key=lambda pair: pair[0], reverse=True)]
        for i in range(ELITISME_SIZE):
            populasi_baru.append(populasi_urut[i].copy())
            
        # --- Seleksi, Crossover, dan Mutasi ---
        while len(populasi_baru) < JUMLAH_POPULASI:
            # Seleksi parent 1 dan parent 2 menggunakan Roulette Wheel Selection (RWS)
            parent1, _ = roulette_wheel_selection(populasi, fitness_populasi)
            parent2, _ = roulette_wheel_selection(populasi, fitness_populasi)
            
            # Crossover (kawin silang) menggunakan Uniform Crossover
            child1, child2 = uniform_crossover(parent1, parent2, CROSSOVER_RATE)
            
            # Mutasi menggunakan Uniform Mutation (Bit Flip)
            child1 = uniform_mutation(child1, MUTATION_RATE)
            child2 = uniform_mutation(child2, MUTATION_RATE)
            
            # Masukkan ke populasi baru
            populasi_baru.append(child1)
            if len(populasi_baru) < JUMLAH_POPULASI:
                populasi_baru.append(child2)
                
        # Perbarui populasi lama dengan populasi baru untuk generasi selanjutnya
        populasi = populasi_baru

    print("=" * 60)
    print("                HASIL OPTIMASI AKHIR")
    print("=" * 60)
    
    # Mengidentifikasi barang-barang yang dipilih berdasarkan solusi terbaik
    barang_terpilih = []
    total_ukuran = 0
    for idx, gen in enumerate(global_best_individual):
        if gen == 1:
            barang_terpilih.append(barang[idx])
            total_ukuran += barang[idx][2]
            
    print(f"  Kromosom Terbaik Global : {global_best_individual}")
    print(f"  Total Keuntungan (Max)  : {global_best_fitness}")
    print(f"  Total Ukuran Gudang     : {total_ukuran} (Kapasitas Maksimum: {kapasitas_gudang})")
    print("\n  Daftar Barang yang Harus Dibeli:")
    for b in barang_terpilih:
        print(f"    - {b[0]} (Keuntungan: {b[1]}, Ukuran: {b[2]})")
    print("=" * 60)
    
    # 4. Visualisasi Grafik Menggunakan Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, JUMLAH_GENERASI + 1), history_best_fitness, label='Fitness Terbaik', color='blue', linewidth=2)
    plt.plot(range(1, JUMLAH_GENERASI + 1), history_avg_fitness, label='Rata-rata Fitness', color='orange', linestyle='--', linewidth=1.5)
    
    plt.title('Grafik Perkembangan Nilai Fitness Setiap Generasi\n(RWS, Uniform Crossover, Uniform Mutation)', fontsize=12, fontweight='bold')
    plt.xlabel('Generasi', fontsize=10)
    plt.ylabel('Nilai Fitness (Total Keuntungan)', fontsize=10)
    plt.legend(loc='lower right')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Simpan grafik
    grafik_path = 'grafik_fitness.png'
    plt.savefig(grafik_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Grafik perkembangan fitness disimpan sebagai '{grafik_path}'")
    print("=" * 60)

if __name__ == "__main__":
    # Mengatur seed random agar hasil replikatif jika diperlukan (opsional)
    # random.seed(42)
    run_genetic_algorithm()
