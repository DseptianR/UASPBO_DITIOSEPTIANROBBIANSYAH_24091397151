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

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math

# Matplotlib for embedded charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ------------------------
# Business logic (OOP)
# ------------------------

class Person:
    def __init__(self, nama: str, umur: int):
        self._nama = nama
        self._umur = umur

    def get_nama(self):
        return self._nama

    def get_umur(self):
        return self._umur

    def get_info(self):
        return f"{self._nama}, {self._umur} tahun"

class Mahasiswa(Person):
    def __init__(self, nama: str, umur: int, nim: str, prodi: str):
        super().__init__(nama, umur)
        self._nim = nim
        self._prodi = prodi
        self._data_aktivitas = []

    def get_info(self):
        return f"Mahasiswa: {self._nama} ({self._nim}) - {self._prodi}"

    def get_nim(self):
        return self._nim

    def get_prodi(self):
        return self._prodi

    def tambah_aktivitas(self, aktivitas):
        self._data_aktivitas.append(aktivitas)

    def get_data_aktivitas(self):
        return self._data_aktivitas

class AktivitasMahasiswa:
    def __init__(self, jamBelajar, kehadiran, tugasSelesai, jamTidur, jamMain):
        self._jamBelajar = jamBelajar
        self._kehadiran = kehadiran
        self._tugasSelesai = tugasSelesai
        self._jamTidur = jamTidur
        self._jamMain = jamMain

    def getJamBelajar(self): return self._jamBelajar
    def getKehadiran(self): return self._kehadiran
    def getTugasSelesai(self): return self._tugasSelesai
    def getJamTidur(self): return self._jamTidur
    def getJamMain(self): return self._jamMain

    def hitungSkor(self):
        skor = 0
        skor += self._jamBelajar * 10
        skor += self._kehadiran * 5
        skor += self._tugasSelesai * 15
        skor -= self._jamMain * 5
        skor += 20 if (6 <= self._jamTidur <= 8) else 0
        return skor

class PrediktorKemalasan:
    def prediksi(self, aktivitas: AktivitasMahasiswa):
        raise NotImplementedError()

class SimplePrediktor(PrediktorKemalasan):
    def prediksi(self, aktivitas: AktivitasMahasiswa):
        skor = aktivitas.hitungSkor()
        if skor >= 150: return {"tingkat":"Sangat Rajin","warna":"#22c55e","persentase":100}
        if skor >= 100: return {"tingkat":"Rajin","warna":"#3b82f6","persentase":75}
        if skor >= 50: return {"tingkat":"Cukup Rajin","warna":"#f59e0b","persentase":50}
        if skor >= 20: return {"tingkat":"Malas","warna":"#ef4444","persentase":25}
        return {"tingkat":"Sangat Malas","warna":"#dc2626","persentase":10}

class AdvancedPrediktor(PrediktorKemalasan):
    def prediksi(self, aktivitas: AktivitasMahasiswa):
        skor = 0
        skor += aktivitas.getJamBelajar() * 12
        skor += aktivitas.getKehadiran() * 6
        skor += aktivitas.getTugasSelesai() * 18
        skor -= aktivitas.getJamMain() * 8
        tidur = aktivitas.getJamTidur()
        if 7 <= tidur <= 8: skor += 25
        elif 6 <= tidur < 7: skor += 15

        if skor >= 180: return {"tingkat":"Sangat Rajin","warna":"#22c55e","persentase":100}
        if skor >= 120: return {"tingkat":"Rajin","warna":"#3b82f6","persentase":75}
        if skor >= 60: return {"tingkat":"Cukup Rajin","warna":"#f59e0b","persentase":50}
        if skor >= 30: return {"tingkat":"Malas","warna":"#ef4444","persentase":25}
        return {"tingkat":"Sangat Malas","warna":"#dc2626","persentase":10}

# ------------------------
# GUI Application
# ------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Prediksi Tingkat Kemalasan Mahasiswa")
        self.geometry("1100x780")
        self.configure(bg="#eef2ff")  # soft background

        # State
        self.mahasiswa = None
        self.riwayat = []  # list of result dicts

        # Form data default
        self.form = {
            "nama": tk.StringVar(),
            "umur": tk.IntVar(value=20),
            "nim": tk.StringVar(),
            "prodi": tk.StringVar(),
            "jamBelajar": tk.IntVar(value=0),
            "kehadiran": tk.IntVar(value=0),
            "tugasSelesai": tk.IntVar(value=0),
            "jamTidur": tk.IntVar(value=7),
            "jamMain": tk.IntVar(value=0),
            "algoritma": tk.StringVar(value="simple")
        }

        self.hasil = None  # last result dict

        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=16, pady=12)

        # Header
        header = ttk.Frame(container)
        header.pack(fill="x", pady=(0,10))
        ttk.Label(header, text="Sistem Prediksi Tingkat Kemalasan Mahasiswa", font=("Inter", 20, "bold")).pack(side="left")
        ttk.Label(header, text="Analisis Produktivitas Berbasis OOP - UAS PBO 2025", foreground="#555").pack(side="left", padx=12)

        # Main grid: left column = inputs, right column = outputs
        main = ttk.Frame(container)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=2)

        # Left: Data Mahasiswa Card
        self._build_mahasiswa_card(left)
        # Left: Aktivitas Card
        self._build_aktivitas_card(left)

        # Right: hasil, rekomendasi, charts
        self._build_hasil_card(right)
        self._build_visual_card(right)
        self._build_history_card(right)

    def _build_mahasiswa_card(self, parent):
        card = ttk.LabelFrame(parent, text="Data Mahasiswa")
        card.pack(fill="x", pady=(0,8))

        frm = ttk.Frame(card)
        frm.pack(fill="x", padx=8, pady=8)

        ttk.Label(frm, text="Nama Lengkap").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.form["nama"]).grid(row=1, column=0, sticky="ew", padx=(0,8))
        frm.columnconfigure(0, weight=1)

        sub = ttk.Frame(card)
        sub.pack(fill="x", padx=8, pady=(0,8))
        ttk.Label(sub, text="Umur").grid(row=0, column=0, sticky="w")
        ttk.Entry(sub, textvariable=self.form["umur"]).grid(row=1, column=0, sticky="ew", padx=(0,8))
        ttk.Label(sub, text="NIM").grid(row=0, column=1, sticky="w")
        ttk.Entry(sub, textvariable=self.form["nim"]).grid(row=1, column=1, sticky="ew", padx=(8,0))
        ttk.Label(sub, text="Program Studi").grid(row=2, column=0, sticky="w", pady=(8,0))
        ttk.Entry(sub, textvariable=self.form["prodi"]).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,8))

        btn = ttk.Button(card, text="Buat Data Mahasiswa", command=self.buat_mahasiswa)
        btn.pack(fill="x", padx=8, pady=(0,8))

        self.label_mahasiswa_info = ttk.Label(card, text="", foreground="#066f2d")
        self.label_mahasiswa_info.pack(fill="x", padx=8, pady=(0,8))

    def _build_aktivitas_card(self, parent):
        card = ttk.LabelFrame(parent, text="Data Aktivitas Harian")
        card.pack(fill="both", expand=False, pady=(0,8))

        def slider_row(label_text, var, min_, max_, row):
            ttk.Label(card, text=label_text).grid(row=row*2, column=0, sticky="w", padx=8, pady=(6,0))
            s = ttk.Scale(card, from_=min_, to=max_, orient="horizontal", variable=var, command=lambda e: self._on_slider_change())
            s.grid(row=row*2+1, column=0, sticky="ew", padx=8)
            val_lbl = ttk.Label(card, textvariable=var)
            val_lbl.grid(row=row*2+1, column=1, sticky="w", padx=6)

        slider_row("Jam Belajar/Hari:", self.form["jamBelajar"], 0, 12, 0)
        slider_row("Persentase Kehadiran (%):", self.form["kehadiran"], 0, 100, 1)
        slider_row("Tugas Diselesaikan (%):", self.form["tugasSelesai"], 0, 100, 2)
        slider_row("Jam Tidur/Hari:", self.form["jamTidur"], 0, 12, 3)
        slider_row("Jam Bermain/Hari:", self.form["jamMain"], 0, 12, 4)

        # Algoritma select
        ttk.Label(card, text="Algoritma Prediksi").grid(row=10, column=0, sticky="w", padx=8, pady=(8,0))
        algo_box = ttk.Combobox(card, textvariable=self.form["algoritma"], values=["simple", "advanced"], state="readonly")
        algo_box.grid(row=11, column=0, sticky="ew", padx=8, pady=(0,8))
        algo_box.bind("<<ComboboxSelected>>", lambda e: None)

        btn = ttk.Button(card, text="🔍 Analisis Tingkat Kemalasan", command=self.analisis_kemalasan)
        btn.grid(row=12, column=0, columnspan=2, sticky="ew", padx=8, pady=(0,8))

    def _on_slider_change(self):
        # Called while sliding; update charts live if desired. For now, do nothing.
        pass

    def _build_hasil_card(self, parent):
        card = ttk.LabelFrame(parent, text="Hasil Analisis")
        card.pack(fill="x", pady=(0,8))

        top = ttk.Frame(card)
        top.pack(fill="x", padx=8, pady=8)

        self.label_tingkat = ttk.Label(top, text="Tingkat: -", font=("Inter", 16, "bold"))
        self.label_tingkat.grid(row=0, column=0, sticky="w")
        self.label_skor = ttk.Label(top, text="Skor: -")
        self.label_skor.grid(row=1, column=0, sticky="w")
        self.label_persen = ttk.Label(top, text="Persentase: -")
        self.label_persen.grid(row=2, column=0, sticky="w")

        self.label_alg = ttk.Label(top, text="Algoritma: -")
        self.label_alg.grid(row=0, column=1, sticky="e", padx=12)
        self.label_timestamp = ttk.Label(top, text="Waktu: -")
        self.label_timestamp.grid(row=1, column=1, sticky="e", padx=12)

        # Rekomendasi area
        rec_card = ttk.LabelFrame(parent, text="Rekomendasi Peningkatan")
        rec_card.pack(fill="x", pady=(0,8))
        self.rekom_listbox = tk.Listbox(rec_card, height=5)
        self.rekom_listbox.pack(fill="both", padx=8, pady=8)

    def _build_visual_card(self, parent):
        card = ttk.Frame(parent)
        card.pack(fill="both", expand=True, pady=(0,8))

        # Bar chart frame
        bar_frame = ttk.LabelFrame(card, text="Grafik Aktivitas vs Target")
        bar_frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.fig_bar, self.ax_bar = plt.subplots(figsize=(5,2.7))
        plt.tight_layout()
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, master=bar_frame)
        self.canvas_bar.get_tk_widget().pack(fill="both", expand=True)

        # Pie chart frame
        pie_frame = ttk.LabelFrame(card, text="Distribusi Tingkat Produktivitas")
        pie_frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.fig_pie, self.ax_pie = plt.subplots(figsize=(5,2.7))
        plt.tight_layout()
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, master=pie_frame)
        self.canvas_pie.get_tk_widget().pack(fill="both", expand=True)

        self._redraw_charts()

    def _build_history_card(self, parent):
        card = ttk.LabelFrame(parent, text="Riwayat Analisis")
        card.pack(fill="both", expand=True)

        cols = ("No","Waktu","Tingkat","Skor","Persentase")
        self.tree = ttk.Treeview(card, columns=cols, show="headings", selectmode="browse", height=6)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    # ----------------------
    # Actions
    # ----------------------

    def buat_mahasiswa(self):
        nama = self.form["nama"].get().strip()
        nim = self.form["nim"].get().strip()
        prodi = self.form["prodi"].get().strip()
        umur = self.form["umur"].get()

        if not nama or not nim or not prodi:
            messagebox.showwarning("Data kurang", "Mohon isi nama, NIM, dan program studi.")
            return
        self.mahasiswa = Mahasiswa(nama, umur, nim, prodi)
        self.label_mahasiswa_info.config(text=self.mahasiswa.get_info())
        messagebox.showinfo("Berhasil", "Data mahasiswa berhasil dibuat!")

    def analisis_kemalasan(self):
        if not self.mahasiswa:
            messagebox.showwarning("Mahasiswa belum dibuat", "Buat data mahasiswa terlebih dahulu!")
            return

        aktivitas = AktivitasMahasiswa(
            self.form["jamBelajar"].get(),
            self.form["kehadiran"].get(),
            self.form["tugasSelesai"].get(),
            self.form["jamTidur"].get(),
            self.form["jamMain"].get()
        )

        self.mahasiswa.tambah_aktivitas(aktivitas)

        prediktor = SimplePrediktor() if self.form["algoritma"].get()=="simple" else AdvancedPrediktor()
        hasil_pred = prediktor.prediksi(aktivitas)
        skor = aktivitas.hitungSkor()
        rekom = self.generate_rekomendasi(aktivitas, hasil_pred)
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        hasil_analisis = {
            "mahasiswa": self.mahasiswa.get_info(),
            "tingkat": hasil_pred["tingkat"],
            "warna": hasil_pred["warna"],
            "persentase": hasil_pred["persentase"],
            "skor": skor,
            "rekomendasi": rekom,
            "timestamp": timestamp,
            "algoritma": self.form["algoritma"].get()
        }
        self.hasil = hasil_analisis
        self.riwayat.append(hasil_analisis)
        self._update_ui_after_analysis()

    def generate_rekomendasi(self, aktivitas: AktivitasMahasiswa, hasil):
        rekomendasi = []
        if aktivitas.getJamBelajar() < 3:
            rekomendasi.append("⚠️ Tingkatkan jam belajar minimal 3 jam/hari")
        if aktivitas.getKehadiran() < 80:
            rekomendasi.append("📚 Tingkatkan kehadiran kuliah minimal 80%")
        if aktivitas.getTugasSelesai() < 70:
            rekomendasi.append("✍️ Selesaikan tugas minimal 70%")
        if aktivitas.getJamMain() > 4:
            rekomendasi.append("🎮 Kurangi waktu bermain, maksimal 3 jam/hari")
        if aktivitas.getJamTidur() < 6 or aktivitas.getJamTidur() > 9:
            rekomendasi.append("😴 Atur pola tidur 7-8 jam/hari untuk produktivitas optimal")
        if not rekomendasi:
            rekomendasi.append("🌟 Pertahankan pola belajar yang sudah baik!")
        return rekomendasi

    def _update_ui_after_analysis(self):
        h = self.hasil
        if not h: return
        # update labels
        self.label_tingkat.config(text=f"Tingkat: {h['tingkat']}", foreground=h["warna"])
        self.label_skor.config(text=f"Skor: {h['skor']}")
        self.label_persen.config(text=f"Persentase: {h['persentase']}%")
        self.label_alg.config(text=f"Algoritma: {h.get('algoritma','-')}")
        self.label_timestamp.config(text=f"Waktu: {h['timestamp']}")

        # rekom
        self.rekom_listbox.delete(0, tk.END)
        for r in h["rekomendasi"]:
            self.rekom_listbox.insert(tk.END, r)

        # update history tree
        self.tree.insert("", "end", values=(len(self.riwayat), h["timestamp"], h["tingkat"], h["skor"], f"{h['persentase']}%"))
        # redraw charts
        self._redraw_charts()

    def _redraw_charts(self):
        # Bar chart: show current form input vs targets
        chart_data_names = ['Jam Belajar', 'Kehadiran %', 'Tugas %', 'Jam Tidur', 'Jam Main']
        chart_values = [
            self.form["jamBelajar"].get(),
            self.form["kehadiran"].get(),
            self.form["tugasSelesai"].get(),
            self.form["jamTidur"].get(),
            self.form["jamMain"].get()
        ]
        chart_targets = [5, 90, 90, 8, 2]

        self.ax_bar.clear()
        indices = range(len(chart_data_names))
        width = 0.35
        self.ax_bar.bar([i - width/2 for i in indices], chart_values, width=width, label="Aktual")
        self.ax_bar.bar([i + width/2 for i in indices], chart_targets, width=width, label="Target")
        self.ax_bar.set_xticks(indices)
        self.ax_bar.set_xticklabels(chart_data_names, rotation=25, ha="right")
        self.ax_bar.legend()
        self.ax_bar.set_ylabel("Nilai")
        self.fig_bar.tight_layout()
        self.canvas_bar.draw()

        # Pie chart: distribution dari riwayat
        self.ax_pie.clear()
        labels = []
        counts = []
        for item in self.riwayat:
            found = False
            for i, l in enumerate(labels):
                if l == item["tingkat"]:
                    counts[i] += 1
                    found = True
                    break
            if not found:
                labels.append(item["tingkat"])
                counts.append(1)
        if counts:
            colors_map = {
                "Sangat Rajin":"#22c55e","Rajin":"#3b82f6","Cukup Rajin":"#f59e0b","Malas":"#ef4444","Sangat Malas":"#dc2626"
            }
            colors = [colors_map.get(lbl, "#8884d8") for lbl in labels]
            self.ax_pie.pie(counts, labels=[f"{l} ({c})" for l,c in zip(labels,counts)], autopct=lambda p: f'{p:.0f}%', colors=colors)
        else:
            # empty state
            self.ax_pie.text(0.5, 0.5, "Belum ada riwayat analisis", ha="center", va="center")
        self.fig_pie.tight_layout()
        self.canvas_pie.draw()

# ------------------------
# Run the app
# ------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()
