import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Smart Digital Library - Login")
        self.root.geometry("350x200")

        style = ttk.Style()
        style.theme_use('clam')

        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(frame, text="Username:", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=10, sticky="w")
        self.entry_user = ttk.Entry(frame, width=25)
        self.entry_user.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(frame, text="Password:", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=10, sticky="w")
        self.entry_pass = ttk.Entry(frame, width=25, show="*")
        self.entry_pass.grid(row=1, column=1, pady=10, padx=10)

        ttk.Button(frame, text="Login", command=self.proses_login).grid(row=2, column=0, columnspan=2, pady=15)

    def proses_login(self):
        self.controller.handle_login(self.entry_user.get(), self.entry_pass.get())


class AdminDashboard(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Admin Dashboard - Manajemen Pustaka")
        self.geometry("750x520")
        self.protocol("WM_DELETE_WINDOW", lambda: self.controller.handle_logout(self))

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tab_kelola = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_kelola, text="Kelola Buku & Stok")

        ttk.Label(self.tab_kelola, text="Judul:").grid(row=0, column=0, padx=5, pady=5)
        self.e_judul = ttk.Entry(self.tab_kelola)
        self.e_judul.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.tab_kelola, text="Penulis:").grid(row=0, column=2, padx=5, pady=5)
        self.e_penulis = ttk.Entry(self.tab_kelola)
        self.e_penulis.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.tab_kelola, text="Stok Baru:").grid(row=1, column=0, padx=5, pady=5)
        self.e_stok = ttk.Entry(self.tab_kelola)
        self.e_stok.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.tab_kelola, text="Genre/Topik:").grid(row=1, column=2, padx=5, pady=5)
        self.e_genre = ttk.Entry(self.tab_kelola)
        self.e_genre.grid(row=1, column=3, padx=5, pady=5)
        
        self.edit_id_target = tk.StringVar() 

        ttk.Button(self.tab_kelola, text="+ Tambah Fiksi", command=lambda: self.controller.tambah_buku("Fiksi", self.e_judul.get(), self.e_penulis.get(), self.e_stok.get(), self.e_genre.get(), self)).grid(row=2, column=0, pady=5)
        ttk.Button(self.tab_kelola, text="+ Tambah Non-Fiksi", command=lambda: self.controller.tambah_buku("Non-Fiksi", self.e_judul.get(), self.e_penulis.get(), self.e_stok.get(), self.e_genre.get(), self)).grid(row=2, column=1, pady=5)
        ttk.Button(self.tab_kelola, text="💾 Simpan Hasil Edit", command=self.simpan_edit_ui).grid(row=2, column=2, columnspan=2, pady=5, sticky="ew", padx=5)

        ttk.Label(self.tab_kelola, text="Cari (Keyword):").grid(row=3, column=0, padx=5, pady=5)
        self.e_cari = ttk.Entry(self.tab_kelola)
        self.e_cari.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.tab_kelola, text="🔍 Cari Buku", command=self.cari_buku_ui).grid(row=3, column=2, pady=5)
        ttk.Button(self.tab_kelola, text="🔄 Reset Tabel", command=self.refresh_ui).grid(row=3, column=3, pady=5)

        self.listbox = tk.Listbox(self.tab_kelola, width=100, height=10)
        self.listbox.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        ttk.Button(self.tab_kelola, text="Hapus Terpilih", command=self.hapus).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(self.tab_kelola, text="✏️ Muat Data ke Form Edit", command=self.muat_edit_ui).grid(row=5, column=2, columnspan=2, pady=5)

        self.tab_pinjam = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pinjam, text="Data Peminjaman")
        self.list_pinjam = tk.Listbox(self.tab_pinjam, width=80, height=15)
        self.list_pinjam.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(self, text="Logout", command=lambda: self.controller.handle_logout(self)).grid(row=1, column=0, pady=5)
        self.refresh_ui()

    def cari_buku_ui(self):
        keyword = self.e_cari.get()
        if keyword:
            hasil = self.controller.cari_buku(keyword)
            if not hasil:
                messagebox.showinfo("Info", "Buku tidak ditemukan!")
            self.perbarui_listbox(hasil)

    def muat_edit_ui(self):
        pilihan = self.listbox.curselection()
        if pilihan:
            id_buku = self.listbox.get(pilihan).split(" | ")[0]
            buku = self.controller.db.get_buku_by_id(id_buku)
            if buku:
                self.e_judul.delete(0, tk.END)
                self.e_penulis.delete(0, tk.END)
                self.e_stok.delete(0, tk.END)
                self.e_genre.delete(0, tk.END)
                
                self.e_judul.insert(0, buku.judul)
                self.e_penulis.insert(0, buku.penulis)
                self.e_stok.insert(0, str(buku.stok))
                
                # Memanggil metode polimorfik murni alih-alih mengintip via getattr
                self.e_genre.insert(0, buku.get_nilai_spesifik())
                
                self.edit_id_target.set(buku.id_buku)
                messagebox.showinfo("Mode Edit Aktif", f"Data buku {buku.id_buku} dimuat. Kosongkan field yang tidak ingin diubah.")

    def simpan_edit_ui(self):
        id_buku = self.edit_id_target.get()
        if not id_buku:
            messagebox.showwarning("Peringatan", "Pilih buku dan klik 'Muat Data ke Form Edit' terlebih dahulu!")
            return
        
        self.controller.edit_buku(id_buku, self.e_judul.get(), self.e_penulis.get(), self.e_stok.get(), self)
        self.edit_id_target.set("") 
        self.e_judul.delete(0, tk.END)
        self.e_penulis.delete(0, tk.END)
        self.e_stok.delete(0, tk.END)
        self.e_genre.delete(0, tk.END)

    def refresh_ui(self):
        self.e_cari.delete(0, tk.END)
        self.perbarui_listbox(self.controller.db.koleksi_buku)

        self.list_pinjam.delete(0, tk.END)
        for user, dipinjam in self.controller.db.buku_aktif_dipinjam.items():
            if dipinjam:
                self.list_pinjam.insert(tk.END, f"User: '{user}' sedang meminjam ID: {dipinjam}")

    def perbarui_listbox(self, daftar_buku):
        self.listbox.delete(0, tk.END)
        for b in daftar_buku:
            self.listbox.insert(tk.END, f"{b.id_buku} | {b.judul} | Penulis: {b.penulis} | Kat: {b.kategori} | Stok: {b.stok}{b.get_spesifikasi()}")

    def hapus(self):
        pilihan = self.listbox.curselection()
        if pilihan:
            id_buku = self.listbox.get(pilihan).split(" | ")[0]
            self.controller.hapus_buku(id_buku, self)


class UserDashboard(tk.Toplevel):
    def __init__(self, controller, username):
        super().__init__()
        self.controller = controller
        self.username = username
        self.title(f"Dashboard - {username}")
        self.geometry("750x520")
        self.protocol("WM_DELETE_WINDOW", lambda: self.controller.handle_logout(self))

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tab_katalog = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_katalog, text="Katalog & Pinjam")
        
        ttk.Label(self.tab_katalog, text="Cari:").grid(row=0, column=0, padx=5, pady=5)
        self.e_cari = ttk.Entry(self.tab_katalog)
        self.e_cari.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.tab_katalog, text="🔍 Cari", command=self.cari_buku_ui).grid(row=0, column=2, pady=5)
        ttk.Button(self.tab_katalog, text="🔄 Reset", command=self.refresh_ui).grid(row=0, column=3, pady=5)

        self.list_katalog = tk.Listbox(self.tab_katalog, width=100, height=10)
        self.list_katalog.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        ttk.Button(self.tab_katalog, text="Pinjam Buku Terpilih", command=self.pinjam).grid(row=2, column=0, columnspan=4, pady=5)

        self.tab_saya = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_saya, text="Buku Saya (Aktif)")
        self.list_saya = tk.Listbox(self.tab_saya, width=100, height=12)
        self.list_saya.grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(self.tab_saya, text="Kembalikan Buku", command=self.kembali).grid(row=1, column=0, pady=5)

        self.tab_riwayat = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_riwayat, text="Riwayat Peminjaman")
        self.list_riwayat = tk.Listbox(self.tab_riwayat, width=100, height=14)
        self.list_riwayat.grid(row=0, column=0, padx=10, pady=10)

        self.tab_rekomendasi = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rekomendasi, text="⭐ Rekomendasi Untukmu ⭐")
        self.list_rekomendasi = tk.Listbox(self.tab_rekomendasi, width=100, height=12)
        self.list_rekomendasi.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(self, text="Logout", command=lambda: self.controller.handle_logout(self)).grid(row=1, column=0, pady=5)
        self.refresh_ui()

    def cari_buku_ui(self):
        keyword = self.e_cari.get()
        if keyword:
            hasil = self.controller.cari_buku(keyword)
            if not hasil:
                messagebox.showinfo("Info", "Buku tidak ditemukan!")
            
            self.list_katalog.delete(0, tk.END)
            for b in hasil:
                self.list_katalog.insert(tk.END, f"{b.id_buku} | {b.judul} | Kategori: {b.kategori} | Stok: {b.stok}{b.get_spesifikasi()}")

    def refresh_ui(self):
        self.e_cari.delete(0, tk.END)
        db = self.controller.db

        self.list_katalog.delete(0, tk.END)
        for b in db.koleksi_buku:
            self.list_katalog.insert(tk.END, f"{b.id_buku} | {b.judul} | Kategori: {b.kategori} | Stok: {b.stok}{b.get_spesifikasi()}")

        self.list_saya.delete(0, tk.END)
        for id_buku in db.buku_aktif_dipinjam.get(self.username, []):
            buku = db.get_buku_by_id(id_buku)
            if buku:
                self.list_saya.insert(tk.END, f"{buku.id_buku} | {buku.judul}{buku.get_spesifikasi()}")

        self.list_riwayat.delete(0, tk.END)
        for id_buku in db.riwayat_baca_permanen.get(self.username, []):
            buku = db.get_buku_by_id(id_buku)
            if buku:
                self.list_riwayat.insert(tk.END, f"{buku.id_buku} | {buku.judul} | Kategori: {buku.kategori}{buku.get_spesifikasi()}")
            else:
                self.list_riwayat.insert(tk.END, f"{id_buku} | (Data buku telah dihapus sistem)")

        self.list_rekomendasi.delete(0, tk.END)
        rekomendasi = db.dapatkan_rekomendasi(self.username)
        for b in rekomendasi:
            self.list_rekomendasi.insert(tk.END, f"📌 {b.id_buku} | {b.judul} | Kategori: {b.kategori}{b.get_spesifikasi()}")

    def pinjam(self):
        pilihan = self.list_katalog.curselection()
        if pilihan:
            id_buku = self.list_katalog.get(pilihan).split(" | ")[0]
            self.controller.pinjam_buku(self.username, id_buku, self)

    def kembali(self):
        pilihan = self.list_saya.curselection()
        if pilihan:
            id_buku = self.list_saya.get(pilihan).split(" | ")[0]
            self.controller.kembalikan_buku(self.username, id_buku, self)