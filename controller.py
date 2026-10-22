import tkinter as tk
from tkinter import messagebox

from model import LibraryDatabase, BookFactory
from view import LoginView, AdminDashboard, UserDashboard

class AppController:
    def __init__(self, root):
        self.root = root
        self.db = LibraryDatabase()
        self.login_view = LoginView(root, self)

    def cari_buku(self, keyword):
        return self.db.cari_buku(keyword)

    def handle_login(self, username, password):
        if username in self.db.akun_dummy and self.db.akun_dummy[username] == password:
            self.root.withdraw() 
            if username == "admin":
                messagebox.showinfo("Login", "Login Admin Berhasil!")
                AdminDashboard(self)
            else:
                if username not in self.db.buku_aktif_dipinjam:
                    self.db.buku_aktif_dipinjam[username] = []
                if username not in self.db.riwayat_baca_permanen:
                    self.db.riwayat_baca_permanen[username] = []
                    
                messagebox.showinfo("Login", f"Selamat Datang, {username}!")
                UserDashboard(self, username)
        else:
            messagebox.showerror("Error", "Username atau Password salah!")

    def handle_logout(self, window):
        window.destroy()
        self.login_view.entry_user.delete(0, tk.END)
        self.login_view.entry_pass.delete(0, tk.END)
        self.root.deiconify()

    def tambah_buku(self, jenis, judul, penulis, stok_str, genre_str, view):
        if not judul or not penulis or not stok_str or not genre_str:
            messagebox.showwarning("Peringatan", "Semua field (Judul, Penulis, Stok, Genre/Topik) wajib diisi!")
            return
        
        if not stok_str.isdigit():
            messagebox.showerror("Error", "Nilai Stok wajib berupa angka bilangan bulat!")
            return
            
        id_baru = self.db.generate_id()
        buku_baru = BookFactory.buat_buku(jenis, id_baru, judul, penulis, int(stok_str), genre_str)
        self.db.koleksi_buku.append(buku_baru)
        
        messagebox.showinfo("Sukses", f"Buku '{judul}' dirakit otomatis via Factory dengan ID: {id_baru}!")
        view.e_judul.delete(0, tk.END)
        view.e_penulis.delete(0, tk.END)
        view.e_stok.delete(0, tk.END)
        view.e_genre.delete(0, tk.END)
        
        # Mencegah state leak pada sistem edit
        view.edit_id_target.set("") 
        
        view.refresh_ui()

    def edit_buku(self, id_buku, judul_baru, penulis_baru, stok_baru, view):
        buku = self.db.get_buku_by_id(id_buku)
        if not buku: return

        if judul_baru.strip() != "":
            buku.judul = judul_baru.strip()
        if penulis_baru.strip() != "":
            buku.penulis = penulis_baru.strip()
        if stok_baru.strip() != "":
            if stok_baru.isdigit():
                buku.stok = int(stok_baru)
            else:
                messagebox.showwarning("Input Diabaikan", "Input stok bukan angka. Nilai stok lama dipertahankan.")

        messagebox.showinfo("Update Berhasil", f"Data untuk buku {id_buku} berhasil diperbarui!")
        view.refresh_ui()

    def hapus_buku(self, id_buku, view):
        if self.db.validasi_hapus(id_buku):
            self.db.koleksi_buku = [b for b in self.db.koleksi_buku if b.id_buku != id_buku]
            messagebox.showinfo("Sukses", f"Buku {id_buku} berhasil dihapus dari pangkalan data!")
            view.refresh_ui()
        else:
            messagebox.showerror("Gagal", f"Operasi Ditolak! Buku {id_buku} sedang dipinjam oleh User aktif.")

    def pinjam_buku(self, username, id_buku, view):
        buku = self.db.get_buku_by_id(id_buku)
        if buku and buku.stok > 0:
            buku.stok -= 1
            
            self.db.buku_aktif_dipinjam[username].append(id_buku)
            self.db.riwayat_baca_permanen[username].append(id_buku)
                
            messagebox.showinfo("Sukses", f"Buku '{buku.judul}' berhasil dipinjam!")
            view.refresh_ui()
        else:
            messagebox.showerror("Gagal", "Stok buku habis!")

    def kembalikan_buku(self, username, id_buku, view):
        buku = self.db.get_buku_by_id(id_buku)
        if buku and id_buku in self.db.buku_aktif_dipinjam[username]:
            buku.stok += 1
            self.db.buku_aktif_dipinjam[username].remove(id_buku)
            messagebox.showinfo("Sukses", f"Buku '{buku.judul}' berhasil dikembalikan!")
            view.refresh_ui()