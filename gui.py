# Algoritma Genetika — GUI Program (Pertemuan 10)
# Aplikasi berbasis GUI menggunakan Tkinter dan Matplotlib untuk mensimulasikan
# Algoritma Genetika pada 0-1 Knapsack Problem sesuai NIM H1D024102.

# 1. Import Library
import tkinter as tk
from tkinter import ttk, messagebox
import random

# Integrasi Matplotlib ke dalam Tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Import Modul Algoritma Genetika Lokal
from InisiasiPopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness, barang, kapasitas_gudang
from selection import roulette_wheel_selection
from crossover import uniform_crossover
from mutation import uniform_mutation

# 2. Definisi Kelas Aplikasi GUI Utama
class GAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Pengaturan Jendela Utama
        self.title("Algoritma Genetika 2 — 0/1 Knapsack Problem (NIM: H1D024102)")
        self.geometry("1100x650")
        self.configure(bg="#f4f6f9")
        
        # Mengatur Tema Gaya (Style)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(".", font=("Helvetica", 10))
        self.style.configure("TLabel", bg="#f4f6f9")
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), foreground="#2c3e50")
        self.style.configure("SubHeader.TLabel", font=("Helvetica", 11, "bold"), foreground="#34495e")
        self.style.configure("Card.TFrame", background="#ffffff", relief="flat", borderwidth=1)
        self.style.configure("Accent.TButton", font=("Helvetica", 10, "bold"), background="#3498db", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#2980b9")])
        
        self.create_widgets()
        self.run_ga()  # Jalankan sekali saat startup untuk inisialisasi visual

    def create_widgets(self):
        # ------------------ HEADER ------------------
        header_frame = ttk.Frame(self, padding=10)
        header_frame.pack(fill="x", side="top")
        
        title_label = ttk.Label(
            header_frame, 
            text="OPTIMASI KNAPSACK PROBLEM MENGGUNAKAN ALGORITMA GENETIKA", 
            style="Header.TLabel"
        )
        title_label.pack(anchor="w")
        
        nim_label = ttk.Label(
            header_frame, 
            text="NIM: H1D024102 | Seleksi: RWS | Crossover: Uniform | Mutasi: Uniform (Bit Flip)", 
            font=("Helvetica", 10, "italic"),
            foreground="#7f8c8d"
        )
        nim_label.pack(anchor="w")
        
        # ------------------ KONTEN UTAMA ------------------
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Kiri: Parameter & Tabel Barang
        left_frame = ttk.Frame(main_frame, width=400)
        left_frame.pack(side="left", fill="both", padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Kanan: Hasil & Grafik
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # ------------------ PANEL PARAMETER (KIRI) ------------------
        param_card = ttk.Frame(left_frame, style="Card.TFrame", padding=15)
        param_card.pack(fill="x", pady=(0, 10))
        
        ttk.Label(param_card, text="PARAMETER ALGORITMA GENETIKA", style="SubHeader.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Input - Ukuran Populasi
        ttk.Label(param_card, text="Jumlah Populasi:").grid(row=1, column=0, sticky="w", pady=5)
        self.pop_size_var = tk.IntVar(value=20)
        self.pop_size_entry = ttk.Entry(param_card, textvariable=self.pop_size_var, width=10)
        self.pop_size_entry.grid(row=1, column=1, sticky="e", pady=5)
        
        # Input - Crossover Rate
        ttk.Label(param_card, text="Crossover Rate (Pc):").grid(row=2, column=0, sticky="w", pady=5)
        self.cx_rate_var = tk.DoubleVar(value=0.8)
        self.cx_rate_entry = ttk.Entry(param_card, textvariable=self.cx_rate_var, width=10)
        self.cx_rate_entry.grid(row=2, column=1, sticky="e", pady=5)
        
        # Input - Mutation Rate
        ttk.Label(param_card, text="Mutation Rate (Pm):").grid(row=3, column=0, sticky="w", pady=5)
        self.mut_rate_var = tk.DoubleVar(value=0.1)
        self.mut_rate_entry = ttk.Entry(param_card, textvariable=self.mut_rate_var, width=10)
        self.mut_rate_entry.grid(row=3, column=1, sticky="e", pady=5)
        
        # Input - Jumlah Generasi
        ttk.Label(param_card, text="Jumlah Generasi:").grid(row=4, column=0, sticky="w", pady=5)
        self.generations_var = tk.IntVar(value=50)
        self.generations_entry = ttk.Entry(param_card, textvariable=self.generations_var, width=10)
        self.generations_entry.grid(row=4, column=1, sticky="e", pady=5)
        
        # Input - Elitisme Size
        ttk.Label(param_card, text="Elitisme Size:").grid(row=5, column=0, sticky="w", pady=5)
        self.elitism_var = tk.IntVar(value=2)
        self.elitism_entry = ttk.Entry(param_card, textvariable=self.elitism_var, width=10)
        self.elitism_entry.grid(row=5, column=1, sticky="e", pady=5)
        
        # Tombol Run
        self.run_button = ttk.Button(
            param_card, 
            text="JALANKAN GA", 
            style="Accent.TButton",
            command=self.run_ga
        )
        self.run_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        
        # ------------------ PANEL TABEL BARANG (KIRI) ------------------
        items_card = ttk.Frame(left_frame, style="Card.TFrame", padding=15)
        items_card.pack(fill="both", expand=True)
        
        ttk.Label(items_card, text="DAFTAR BARANG & KETENTUAN", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(items_card, text=f"Kapasitas Maksimal Gudang = {kapasitas_gudang}", font=("Helvetica", 9, "bold"), foreground="#e74c3c").pack(anchor="w", pady=(0, 10))
        
        # Definisikan Table View
        self.tree = ttk.Treeview(items_card, columns=("Nama", "Keuntungan", "Ukuran"), show="headings", height=6)
        self.tree.heading("Nama", text="Barang")
        self.tree.heading("Keuntungan", text="Keuntungan")
        self.tree.heading("Ukuran", text="Ukuran")
        self.tree.column("Nama", width=100, anchor="center")
        self.tree.column("Keuntungan", width=120, anchor="center")
        self.tree.column("Ukuran", width=100, anchor="center")
        
        for item in barang:
            self.tree.insert("", "end", values=(item[0], item[1], item[2]))
        self.tree.pack(fill="both", expand=True)
        
        # ------------------ PANEL HASIL (KANAN) ------------------
        result_card = ttk.Frame(right_frame, style="Card.TFrame", padding=15)
        result_card.pack(fill="x", pady=(0, 10))
        
        ttk.Label(result_card, text="SOLUSI TERBAIK DITEMUKAN", style="SubHeader.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Label Hasil 1: Kromosom Terbaik
        ttk.Label(result_card, text="Kromosom Terbaik:").grid(row=1, column=0, sticky="w", pady=2)
        self.result_chrom_label = ttk.Label(result_card, text="-", font=("Courier", 10, "bold"), foreground="#2c3e50")
        self.result_chrom_label.grid(row=1, column=1, sticky="w", pady=2, padx=10)
        
        # Label Hasil 2: Total Keuntungan
        ttk.Label(result_card, text="Total Keuntungan:").grid(row=2, column=0, sticky="w", pady=2)
        self.result_profit_label = ttk.Label(result_card, text="-", font=("Helvetica", 10, "bold"), foreground="#27ae60")
        self.result_profit_label.grid(row=2, column=1, sticky="w", pady=2, padx=10)
        
        # Label Hasil 3: Total Ukuran
        ttk.Label(result_card, text="Total Ukuran:").grid(row=3, column=0, sticky="w", pady=2)
        self.result_weight_label = ttk.Label(result_card, text="-", font=("Helvetica", 10, "bold"), foreground="#e67e22")
        self.result_weight_label.grid(row=3, column=1, sticky="w", pady=2, padx=10)
        
        # Label Hasil 4: Barang yang Dipilih
        ttk.Label(result_card, text="Barang Terpilih:").grid(row=4, column=0, sticky="nw", pady=2)
        self.result_items_label = ttk.Label(result_card, text="-", wraplength=500, justify="left", font=("Helvetica", 9))
        self.result_items_label.grid(row=4, column=1, sticky="w", pady=2, padx=10)
        
        # ------------------ PANEL GRAFIK (KANAN) ------------------
        chart_card = ttk.Frame(right_frame, style="Card.TFrame", padding=10)
        chart_card.pack(fill="both", expand=True)
        
        # Inisialisasi matplotlib figure
        self.fig = Figure(figsize=(5, 3.2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor("#ffffff")
        self.ax.set_facecolor("#f9f9f9")
        
        # Canvas tempat merender grafik di Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_card)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def run_ga(self):
        try:
            # Validasi input parameter
            pop_size = self.pop_size_var.get()
            cx_rate = self.cx_rate_var.get()
            mut_rate = self.mut_rate_var.get()
            generations = self.generations_var.get()
            elitism_size = self.elitism_var.get()
            
            if pop_size <= 0 or generations <= 0 or elitism_size < 0:
                raise ValueError("Nilai numerik integer harus positif.")
            if not (0.0 <= cx_rate <= 1.0) or not (0.0 <= mut_rate <= 1.0):
                raise ValueError("Crossover & Mutation rate harus berada dalam rentang [0.0, 1.0].")
            if elitism_size > pop_size:
                raise ValueError("Elitism size tidak boleh melebihi jumlah populasi.")
        except Exception as e:
            messagebox.showerror("Kesalahan Input", f"Harap periksa kembali input parameter!\nDetail: {e}")
            return

        # Eksekusi Algoritma Genetika
        jumlah_gen = len(barang)
        populasi = inisialisasi_populasi(pop_size, jumlah_gen)
        
        history_best_fitness = []
        history_avg_fitness = []
        
        global_best_individual = None
        global_best_fitness = -1

        for gen in range(generations):
            fitness_populasi = [hitung_fitness(ind, barang, kapasitas_gudang) for ind in populasi]
            
            best_fitness_current = max(fitness_populasi)
            best_idx = fitness_populasi.index(best_fitness_current)
            best_individual_current = populasi[best_idx]
            avg_fitness_current = sum(fitness_populasi) / pop_size
            
            history_best_fitness.append(best_fitness_current)
            history_avg_fitness.append(avg_fitness_current)
            
            if best_fitness_current > global_best_fitness:
                global_best_fitness = best_fitness_current
                global_best_individual = best_individual_current.copy()
                
            # Membuat populasi baru
            populasi_baru = []
            
            # Elitisme
            populasi_urut = [x for _, x in sorted(zip(fitness_populasi, populasi), key=lambda pair: pair[0], reverse=True)]
            for i in range(min(elitism_size, len(populasi_urut))):
                populasi_baru.append(populasi_urut[i].copy())
                
            # Crossover & Mutasi
            while len(populasi_baru) < pop_size:
                parent1, _ = roulette_wheel_selection(populasi, fitness_populasi)
                parent2, _ = roulette_wheel_selection(populasi, fitness_populasi)
                
                child1, child2 = uniform_crossover(parent1, parent2, cx_rate)
                
                child1 = uniform_mutation(child1, mut_rate)
                child2 = uniform_mutation(child2, mut_rate)
                
                populasi_baru.append(child1)
                if len(populasi_baru) < pop_size:
                    populasi_baru.append(child2)
                    
            populasi = populasi_baru

        # Perbarui Hasil UI
        self.result_chrom_label.config(text=f"{global_best_individual}")
        self.result_profit_label.config(text=f"{global_best_fitness} (Keuntungan)")
        
        # Hitung berat/ukuran total barang terpilih
        total_ukuran = 0
        barang_terpilih_str_list = []
        for idx, g in enumerate(global_best_individual):
            if g == 1:
                total_ukuran += barang[idx][2]
                barang_terpilih_str_list.append(f"{barang[idx][0]} (Untung: {barang[idx][1]}, Ukuran: {barang[idx][2]})")
                
        self.result_weight_label.config(text=f"{total_ukuran} / {kapasitas_gudang}")
        if barang_terpilih_str_list:
            self.result_items_label.config(text=",  ".join(barang_terpilih_str_list))
        else:
            self.result_items_label.config(text="Tidak ada barang yang terpilih (Total Ukuran = 0)")

        # Render Grafik Matplotlib
        self.ax.clear()
        self.ax.plot(range(1, generations + 1), history_best_fitness, label='Fitness Terbaik', color='#3498db', linewidth=2)
        self.ax.plot(range(1, generations + 1), history_avg_fitness, label='Rata-rata Fitness', color='#e67e22', linestyle='--', linewidth=1.5)
        
        self.ax.set_title('Grafik Perkembangan Nilai Fitness Setiap Generasi', fontsize=10, fontweight='bold', pad=10)
        self.ax.set_xlabel('Generasi', fontsize=8)
        self.ax.set_ylabel('Nilai Fitness (Keuntungan)', fontsize=8)
        self.ax.legend(loc='lower right', fontsize=8)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.fig.tight_layout()
        
        self.canvas.draw()

# 3. Menjalankan Aplikasi GUI
if __name__ == "__main__":
    app = GAApp()
    app.mainloop()
