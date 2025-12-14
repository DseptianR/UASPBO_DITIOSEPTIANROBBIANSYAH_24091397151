"""
prediksi_kemalasan.py
Aplikasi GUI (Tkinter) versi Python dari Sistem Prediksi Tingkat Kemalasan Mahasiswa.
Fitur:
- OOP classes: Person, Mahasiswa, AktivitasMahasiswa, Prediktor (Simple & Advanced)
- Input mahasiswa (nama, umur, nim, prodi)
- Slider input aktivitas (jam belajar, kehadiran, tugas selesai, jam tidur, jam main)
- Pilihan algoritma (simple / advanced)
- Analisis -> hasil (tingkat, warna, persentase, skor), rekomendasi, timestamp
- Riwayat analisis (Treeview)
- Visualisasi Bar Chart (aktivitas vs target) & Pie Chart (distribusi hasil)
"""

# ===== IMPORT LIBRARY =====
import tkinter as tk  # Library utama untuk membuat GUI
from tkinter import ttk, messagebox  # ttk untuk widget modern, messagebox untuk dialog
from datetime import datetime  # Untuk mendapatkan timestamp analisis
import math  # Library matematika (tidak digunakan dalam kode ini)

# Matplotlib for embedded charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Untuk embed chart matplotlib ke tkinter
import matplotlib.pyplot as plt  # Untuk membuat visualisasi grafik

# ========================
# BAGIAN 1: BUSINESS LOGIC (OOP)
# ========================

# ----- Class Person (Parent/Superclass) -----
class Person:
    """
    Class dasar yang merepresentasikan seseorang dengan atribut nama dan umur.
    Ini adalah parent class yang akan diwarisi oleh class Mahasiswa.
    Konsep OOP: Encapsulation (data disimpan sebagai private dengan underscore)
    """
    def __init__(self, nama: str, umur: int):
        # Constructor: method yang dipanggil saat objek dibuat
        self._nama = nama      # Atribut private (underscore = protected)
        self._umur = umur      # Menyimpan umur

    def get_nama(self):
        """Getter method untuk mengakses nama (encapsulation)"""
        return self._nama

    def get_umur(self):
        """Getter method untuk mengakses umur"""
        return self._umur

    def get_info(self):
        """Method untuk menampilkan informasi dasar person"""
        return f"{self._nama}, {self._umur} tahun"


# ----- Class Mahasiswa (Child class dari Person) -----
class Mahasiswa(Person):
    """
    Class turunan dari Person yang spesifik untuk mahasiswa.
    Konsep OOP: Inheritance (mewarisi dari Person)
    Menambahkan atribut NIM, Prodi, dan data aktivitas
    """
    def __init__(self, nama: str, umur: int, nim: str, prodi: str):
        super().__init__(nama, umur)  # Memanggil constructor parent class
        self._nim = nim               # Atribut tambahan: NIM
        self._prodi = prodi           # Atribut tambahan: Program Studi
        self._data_aktivitas = []     # List untuk menyimpan riwayat aktivitas

    def get_info(self):
        """
        Override method dari parent class
        Konsep OOP: Polymorphism (method dengan nama sama tapi implementasi berbeda)
        """
        return f"Mahasiswa: {self._nama} ({self._nim}) - {self._prodi}"

    def get_nim(self):
        """Getter untuk NIM"""
        return self._nim

    def get_prodi(self):
        """Getter untuk Program Studi"""
        return self._prodi

    def tambah_aktivitas(self, aktivitas):
        """Method untuk menambahkan data aktivitas ke riwayat"""
        self._data_aktivitas.append(aktivitas)

    def get_data_aktivitas(self):
        """Getter untuk mengambil semua data aktivitas"""
        return self._data_aktivitas


# ----- Class AktivitasMahasiswa -----
class AktivitasMahasiswa:
    """
    Class yang merepresentasikan aktivitas harian mahasiswa.
    Menyimpan 5 parameter: jam belajar, kehadiran, tugas selesai, jam tidur, jam main
    """
    def __init__(self, jamBelajar, kehadiran, tugasSelesai, jamTidur, jamMain):
        # Menyimpan semua parameter aktivitas sebagai atribut private
        self._jamBelajar = jamBelajar        # Jam belajar per hari (0-12)
        self._kehadiran = kehadiran          # Persentase kehadiran (0-100)
        self._tugasSelesai = tugasSelesai    # Persentase tugas diselesaikan (0-100)
        self._jamTidur = jamTidur            # Jam tidur per hari (0-12)
        self._jamMain = jamMain              # Jam bermain per hari (0-12)

    # ----- Getter methods untuk setiap atribut -----
    def getJamBelajar(self): 
        return self._jamBelajar
    
    def getKehadiran(self): 
        return self._kehadiran
    
    def getTugasSelesai(self): 
        return self._tugasSelesai
    
    def getJamTidur(self): 
        return self._jamTidur
    
    def getJamMain(self): 
        return self._jamMain

    def hitungSkor(self):
        """
        Method untuk menghitung skor kerajinan berdasarkan aktivitas.
        Formula:
        - Jam belajar: +10 per jam (semakin banyak semakin baik)
        - Kehadiran: +5 per persen (semakin tinggi semakin baik)
        - Tugas selesai: +15 per persen (bobot tertinggi)
        - Jam main: -5 per jam (mengurangi skor, karena mengganggu produktivitas)
        - Jam tidur ideal (6-8 jam): +20 bonus (tidur cukup = produktif)
        """
        skor = 0
        skor += self._jamBelajar * 10      # Kontribusi positif dari belajar
        skor += self._kehadiran * 5        # Kontribusi dari kehadiran
        skor += self._tugasSelesai * 15    # Kontribusi terbesar dari penyelesaian tugas
        skor -= self._jamMain * 5          # Penalti dari waktu bermain
        skor += 20 if (6 <= self._jamTidur <= 8) else 0  # Bonus tidur ideal
        return skor


# ----- Class PrediktorKemalasan (Abstract/Base Class) -----
class PrediktorKemalasan:
    """
    Abstract base class untuk prediktor.
    Konsep OOP: Abstraction (class yang harus diimplementasikan oleh subclass)
    Mendefinisikan interface yang harus diikuti oleh semua prediktor
    """
    def prediksi(self, aktivitas: AktivitasMahasiswa):
        """
        Method yang harus diimplementasikan oleh child class.
        Jika dipanggil langsung akan error.
        """
        raise NotImplementedError()


# ----- Class SimplePrediktor -----
class SimplePrediktor(PrediktorKemalasan):
    """
    Implementasi sederhana dari prediktor.
    Konsep OOP: Inheritance dan Polymorphism
    Menggunakan threshold skor yang lebih rendah
    """
    def prediksi(self, aktivitas: AktivitasMahasiswa):
        """
        Memprediksi tingkat kemalasan berdasarkan skor aktivitas.
        Threshold Simple:
        - ≥150: Sangat Rajin (100%)
        - ≥100: Rajin (75%)
        - ≥50: Cukup Rajin (50%)
        - ≥20: Malas (25%)
        - <20: Sangat Malas (10%)
        """
        skor = aktivitas.hitungSkor()  # Ambil skor dari method hitungSkor()
        
        # Return dictionary berisi hasil prediksi
        if skor >= 150: 
            return {"tingkat":"Sangat Rajin", "warna":"#22c55e", "persentase":100}
        if skor >= 100: 
            return {"tingkat":"Rajin", "warna":"#3b82f6", "persentase":75}
        if skor >= 50: 
            return {"tingkat":"Cukup Rajin", "warna":"#f59e0b", "persentase":50}
        if skor >= 20: 
            return {"tingkat":"Malas", "warna":"#ef4444", "persentase":25}
        return {"tingkat":"Sangat Malas", "warna":"#dc2626", "persentase":10}


# ----- Class AdvancedPrediktor -----
class AdvancedPrediktor(PrediktorKemalasan):
    """
    Implementasi advanced dari prediktor.
    Menggunakan formula perhitungan skor yang berbeda dan threshold lebih tinggi.
    Lebih ketat dalam menilai kerajinan mahasiswa.
    """
    def prediksi(self, aktivitas: AktivitasMahasiswa):
        """
        Formula Advanced (bobot lebih besar):
        - Jam belajar: +12 per jam (naik dari 10)
        - Kehadiran: +6 per persen (naik dari 5)
        - Tugas selesai: +18 per persen (naik dari 15)
        - Jam main: -8 per jam (penalti lebih besar dari -5)
        - Tidur ideal 7-8 jam: +25, tidur cukup 6-7 jam: +15
        
        Threshold Advanced (lebih tinggi):
        - ≥180: Sangat Rajin
        - ≥120: Rajin
        - ≥60: Cukup Rajin
        - ≥30: Malas
        - <30: Sangat Malas
        """
        skor = 0
        # Perhitungan dengan bobot lebih tinggi
        skor += aktivitas.getJamBelajar() * 12
        skor += aktivitas.getKehadiran() * 6
        skor += aktivitas.getTugasSelesai() * 18
        skor -= aktivitas.getJamMain() * 8
        
        # Bonus tidur dengan kriteria lebih spesifik
        tidur = aktivitas.getJamTidur()
        if 7 <= tidur <= 8: 
            skor += 25      # Tidur sangat ideal
        elif 6 <= tidur < 7: 
            skor += 15      # Tidur cukup

        # Klasifikasi dengan threshold lebih tinggi
        if skor >= 180: 
            return {"tingkat":"Sangat Rajin", "warna":"#22c55e", "persentase":100}
        if skor >= 120: 
            return {"tingkat":"Rajin", "warna":"#3b82f6", "persentase":75}
        if skor >= 60: 
            return {"tingkat":"Cukup Rajin", "warna":"#f59e0b", "persentase":50}
        if skor >= 30: 
            return {"tingkat":"Malas", "warna":"#ef4444", "persentase":25}
        return {"tingkat":"Sangat Malas", "warna":"#dc2626", "persentase":10}


# ========================
# BAGIAN 2: GUI APPLICATION
# ========================

class App(tk.Tk):
    """
    Main application class yang mewarisi dari tk.Tk (window utama Tkinter).
    Menggabungkan semua class business logic dengan interface GUI.
    """
    def __init__(self):
        """Constructor untuk inisialisasi aplikasi"""
        super().__init__()  # Inisialisasi parent class (tk.Tk)
        
        # ----- Konfigurasi Window -----
        self.title("Sistem Prediksi Tingkat Kemalasan Mahasiswa")
        self.geometry("1100x780")  # Ukuran window: lebar x tinggi
        self.configure(bg="#eef2ff")  # Background color soft blue

        # ----- State Management -----
        self.mahasiswa = None  # Objek Mahasiswa yang sedang aktif
        self.riwayat = []      # List untuk menyimpan semua hasil analisis

        # ----- Form Data dengan Tkinter Variables -----
        # StringVar dan IntVar adalah variabel Tkinter yang bisa di-bind ke widget
        self.form = {
            "nama": tk.StringVar(),              # Nama mahasiswa
            "umur": tk.IntVar(value=20),         # Umur default 20
            "nim": tk.StringVar(),               # NIM mahasiswa
            "prodi": tk.StringVar(),             # Program studi
            "jamBelajar": tk.IntVar(value=0),    # Jam belajar (slider)
            "kehadiran": tk.IntVar(value=0),     # Persentase kehadiran (slider)
            "tugasSelesai": tk.IntVar(value=0),  # Persentase tugas (slider)
            "jamTidur": tk.IntVar(value=7),      # Jam tidur default 7
            "jamMain": tk.IntVar(value=0),       # Jam bermain (slider)
            "algoritma": tk.StringVar(value="simple")  # Pilihan algoritma
        }

        self.hasil = None  # Dictionary untuk menyimpan hasil analisis terakhir

        # Panggil method untuk membangun UI
        self._build_ui()

    def _build_ui(self):
        """
        Method utama untuk membangun seluruh interface.
        Struktur: Header -> Main Grid (Left: Input | Right: Output)
        """
        # ----- Container Utama -----
        container = ttk.Frame(self)  # Frame container untuk semua widget
        container.pack(fill="both", expand=True, padx=16, pady=12)

        # ----- Header Section -----
        header = ttk.Frame(container)
        header.pack(fill="x", pady=(0,10))
        # Judul aplikasi dengan font besar dan bold
        ttk.Label(header, text="Sistem Prediksi Tingkat Kemalasan Mahasiswa", 
                  font=("Inter", 20, "bold")).pack(side="left")
        # Subtitle dengan warna abu-abu
        ttk.Label(header, text="Analisis Produktivitas Berbasis OOP - UAS PBO 2025", 
                  foreground="#555").pack(side="left", padx=12)

        # ----- Main Grid Layout -----
        # Grid dengan 2 kolom: kiri untuk input, kanan untuk output
        main = ttk.Frame(container)
        main.pack(fill="both", expand=True)

        # Kolom kiri (input forms)
        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        
        # Kolom kanan (hasil, charts, history)
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        
        # Konfigurasi grid weight (kolom kanan lebih lebar)
        main.columnconfigure(0, weight=1)  # Kolom kiri weight=1
        main.columnconfigure(1, weight=2)  # Kolom kanan weight=2 (2x lebih lebar)

        # ----- Membangun Cards di Kolom Kiri -----
        self._build_mahasiswa_card(left)   # Card untuk data mahasiswa
        self._build_aktivitas_card(left)   # Card untuk input aktivitas

        # ----- Membangun Cards di Kolom Kanan -----
        self._build_hasil_card(right)      # Card untuk hasil analisis
        self._build_visual_card(right)     # Card untuk visualisasi grafik
        self._build_history_card(right)    # Card untuk riwayat analisis

    def _build_mahasiswa_card(self, parent):
        """
        Membangun card untuk input data mahasiswa.
        Berisi: Form input (Nama, Umur, NIM, Prodi) + Tombol "Buat Data Mahasiswa"
        """
        # LabelFrame = Frame dengan border dan judul
        card = ttk.LabelFrame(parent, text="Data Mahasiswa")
        card.pack(fill="x", pady=(0,8))

        # ----- Form Nama -----
        frm = ttk.Frame(card)
        frm.pack(fill="x", padx=8, pady=8)
        ttk.Label(frm, text="Nama Lengkap").grid(row=0, column=0, sticky="w")
        # Entry widget di-bind dengan StringVar untuk 2-way binding
        ttk.Entry(frm, textvariable=self.form["nama"]).grid(row=1, column=0, sticky="ew", padx=(0,8))
        frm.columnconfigure(0, weight=1)  # Agar entry mengisi lebar

        # ----- Form Umur, NIM, Prodi -----
        sub = ttk.Frame(card)
        sub.pack(fill="x", padx=8, pady=(0,8))
        
        # Umur (kolom 0)
        ttk.Label(sub, text="Umur").grid(row=0, column=0, sticky="w")
        ttk.Entry(sub, textvariable=self.form["umur"]).grid(row=1, column=0, sticky="ew", padx=(0,8))
        
        # NIM (kolom 1)
        ttk.Label(sub, text="NIM").grid(row=0, column=1, sticky="w")
        ttk.Entry(sub, textvariable=self.form["nim"]).grid(row=1, column=1, sticky="ew", padx=(8,0))
        
        # Program Studi (span 2 kolom)
        ttk.Label(sub, text="Program Studi").grid(row=2, column=0, sticky="w", pady=(8,0))
        ttk.Entry(sub, textvariable=self.form["prodi"]).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,8))

        # ----- Tombol Buat Mahasiswa -----
        # command= menghubungkan tombol dengan method buat_mahasiswa
        btn = ttk.Button(card, text="Buat Data Mahasiswa", command=self.buat_mahasiswa)
        btn.pack(fill="x", padx=8, pady=(0,8))

        # Label untuk menampilkan info mahasiswa setelah dibuat
        self.label_mahasiswa_info = ttk.Label(card, text="", foreground="#066f2d")
        self.label_mahasiswa_info.pack(fill="x", padx=8, pady=(0,8))

    def _build_aktivitas_card(self, parent):
        """
        Membangun card untuk input aktivitas harian menggunakan slider.
        Berisi: 5 slider (Jam Belajar, Kehadiran, Tugas, Tidur, Main) + Combobox Algoritma + Tombol Analisis
        """
        card = ttk.LabelFrame(parent, text="Data Aktivitas Harian")
        card.pack(fill="both", expand=False, pady=(0,8))

        def slider_row(label_text, var, min_, max_, row):
            """
            Helper function untuk membuat baris slider.
            Parameter:
            - label_text: teks label
            - var: IntVar yang di-bind
            - min_, max_: range nilai slider
            - row: nomor baris untuk grid placement
            """
            # Label di atas slider
            ttk.Label(card, text=label_text).grid(row=row*2, column=0, sticky="w", padx=8, pady=(6,0))
            
            # Scale widget (slider) dengan orientation horizontal
            s = ttk.Scale(card, from_=min_, to=max_, orient="horizontal", variable=var, 
                          command=lambda e: self._on_slider_change())
            s.grid(row=row*2+1, column=0, sticky="ew", padx=8)
            
            # Label untuk menampilkan nilai slider secara real-time
            val_lbl = ttk.Label(card, textvariable=var)
            val_lbl.grid(row=row*2+1, column=1, sticky="w", padx=6)

        # ----- Membuat 5 Slider -----
        slider_row("Jam Belajar/Hari:", self.form["jamBelajar"], 0, 12, 0)
        slider_row("Persentase Kehadiran (%):", self.form["kehadiran"], 0, 100, 1)
        slider_row("Tugas Diselesaikan (%):", self.form["tugasSelesai"], 0, 100, 2)
        slider_row("Jam Tidur/Hari:", self.form["jamTidur"], 0, 12, 3)
        slider_row("Jam Bermain/Hari:", self.form["jamMain"], 0, 12, 4)

        # ----- Combobox Pemilihan Algoritma -----
        ttk.Label(card, text="Algoritma Prediksi").grid(row=10, column=0, sticky="w", padx=8, pady=(8,0))
        algo_box = ttk.Combobox(card, textvariable=self.form["algoritma"], 
                                values=["simple", "advanced"], state="readonly")
        algo_box.grid(row=11, column=0, sticky="ew", padx=8, pady=(0,8))
        algo_box.bind("<<ComboboxSelected>>", lambda e: None)  # Event handler (saat ini kosong)

        # ----- Tombol Analisis -----
        # Emoji 🔍 di tombol untuk visual appeal
        btn = ttk.Button(card, text="🔍 Analisis Tingkat Kemalasan", command=self.analisis_kemalasan)
        btn.grid(row=12, column=0, columnspan=2, sticky="ew", padx=8, pady=(0,8))

    def _on_slider_change(self):
        """
        Event handler yang dipanggil saat slider digeser.
        Bisa digunakan untuk update chart secara real-time (saat ini kosong).
        """
        pass  # Placeholder untuk future enhancement

    def _build_hasil_card(self, parent):
        """
        Membangun card untuk menampilkan hasil analisis.
        Berisi: Tingkat kemalasan, skor, persentase, algoritma, timestamp, dan rekomendasi
        """
        # ----- Card Hasil Analisis -----
        card = ttk.LabelFrame(parent, text="Hasil Analisis")
        card.pack(fill="x", pady=(0,8))

        top = ttk.Frame(card)
        top.pack(fill="x", padx=8, pady=8)

        # ----- Labels untuk Hasil (Kiri) -----
        # Label tingkat dengan font besar dan bold
        self.label_tingkat = ttk.Label(top, text="Tingkat: -", font=("Inter", 16, "bold"))
        self.label_tingkat.grid(row=0, column=0, sticky="w")
        
        self.label_skor = ttk.Label(top, text="Skor: -")
        self.label_skor.grid(row=1, column=0, sticky="w")
        
        self.label_persen = ttk.Label(top, text="Persentase: -")
        self.label_persen.grid(row=2, column=0, sticky="w")

        # ----- Labels untuk Info (Kanan) -----
        self.label_alg = ttk.Label(top, text="Algoritma: -")
        self.label_alg.grid(row=0, column=1, sticky="e", padx=12)
        
        self.label_timestamp = ttk.Label(top, text="Waktu: -")
        self.label_timestamp.grid(row=1, column=1, sticky="e", padx=12)

        # ----- Card Rekomendasi -----
        rec_card = ttk.LabelFrame(parent, text="Rekomendasi Peningkatan")
        rec_card.pack(fill="x", pady=(0,8))
        
        # Listbox untuk menampilkan list rekomendasi
        self.rekom_listbox = tk.Listbox(rec_card, height=5)
        self.rekom_listbox.pack(fill="both", padx=8, pady=8)

    def _build_visual_card(self, parent):
        """
        Membangun card untuk visualisasi grafik.
        Berisi: Bar Chart (Aktivitas vs Target) dan Pie Chart (Distribusi Tingkat)
        """
        card = ttk.Frame(parent)
        card.pack(fill="both", expand=True, pady=(0,8))

        # ----- Bar Chart Frame -----
        bar_frame = ttk.LabelFrame(card, text="Grafik Aktivitas vs Target")
        bar_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Membuat figure matplotlib dengan ukuran 5x2.7 inch
        self.fig_bar, self.ax_bar = plt.subplots(figsize=(5,2.7))
        plt.tight_layout()  # Agar tidak ada whitespace berlebih
        
        # Embed matplotlib ke tkinter menggunakan FigureCanvasTkAgg
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, master=bar_frame)
        self.canvas_bar.get_tk_widget().pack(fill="both", expand=True)

        # ----- Pie Chart Frame -----
        pie_frame = ttk.LabelFrame(card, text="Distribusi Tingkat Produktivitas")
        pie_frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.fig_pie, self.ax_pie = plt.subplots(figsize=(5,2.7))
        plt.tight_layout()
        
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, master=pie_frame)
        self.canvas_pie.get_tk_widget().pack(fill="both", expand=True)

        # Gambar chart pertama kali (masih kosong)
        self._redraw_charts()

    def _build_history_card(self, parent):
        """
        Membangun card untuk menampilkan riwayat analisis dalam bentuk tabel.
        Menggunakan Treeview widget (seperti table/spreadsheet)
        """
        card = ttk.LabelFrame(parent, text="Riwayat Analisis")
        card.pack(fill="both", expand=True)

        # Definisi kolom tabel
        cols = ("No","Waktu","Tingkat","Skor","Persentase")
        
        # Treeview dengan show="headings" agar tidak ada kolom kosong di awal
        self.tree = ttk.Treeview(card, columns=cols, show="headings", 
                                 selectmode="browse", height=6)
        
        # Set heading dan format untuk setiap kolom
        for c in cols:
            self.tree.heading(c, text=c)      # Header text
            self.tree.column(c, anchor="w")   # Align left
            
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    # ========================
    # BAGIAN 3: ACTION HANDLERS
    # ========================

    def buat_mahasiswa(self):
        """
        Handler untuk tombol "Buat Data Mahasiswa".
        Validasi input -> Buat objek Mahasiswa -> Simpan ke self.mahasiswa
        """
        # Ambil nilai dari form
        nama = self.form["nama"].get().strip()   # strip() untuk hapus whitespace
        nim = self.form["nim"].get().strip()
        prodi = self.form["prodi"].get().strip()
        umur = self.form["umur"].get()

        # ----- Validasi Input -----
        if not nama or not nim or not prodi:
            # Jika ada field kosong, tampilkan warning
            messagebox.showwarning("Data kurang", "Mohon isi nama, NIM, dan program studi.")
            return
        
        # ----- Buat Objek Mahasiswa -----
        self.mahasiswa = Mahasiswa(nama, umur, nim, prodi)
        
        # Update label info menggunakan method get_info() dari class Mahasiswa
        self.label_mahasiswa_info.config(text=self.mahasiswa.get_info())
        
        # Tampilkan dialog sukses
        messagebox.showinfo("Berhasil", "Data mahasiswa berhasil dibuat!")

    def analisis_kemalasan(self):
        """
        Handler untuk tombol "Analisis Tingkat Kemalasan".
        Flow:
        1. Validasi mahasiswa sudah dibuat
        2. Buat objek AktivitasMahasiswa dari input slider
        3. Pilih prediktor (Simple/Advanced)
        4. Jalankan prediksi
        5. Generate rekomendasi
        6. Simpan hasil ke riwayat
        7. Update UI
        """
        # ----- Validasi Mahasiswa -----
        if not self.mahasiswa:
            messagebox.showwarning("Mahasiswa belum dibuat", 
                                   "Buat data mahasiswa terlebih dahulu!")
            return

        # ----- Buat Objek AktivitasMahasiswa -----
        aktivitas = AktivitasMahasiswa(
            self.form["jamBelajar"].get(),
            self.form["kehadiran"].get(),
            self.form["tugasSelesai"].get(),
            self.form["jamTidur"].get(),
            self.form["jamMain"].get()
        )

        # Tambahkan aktivitas ke data mahasiswa
        self.mahasiswa.tambah_aktivitas(aktivitas)

        # ----- Pilih dan Jalankan Prediktor -----
        # Polymorphism: bisa Simple atau Advanced, tapi interface sama (prediksi())
        if self.form["algoritma"].get() == "simple
