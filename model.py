from collections import Counter

class Koleksi:
    def __init__(self, id_buku, judul, penulis, kategori, stok):
        self.id_buku = id_buku
        self.judul = judul
        self.penulis = penulis
        self.kategori = kategori
        self.stok = int(stok)

    # P5: Fondasi Polimorfisme - Menampilkan string detail di Listbox
    def get_spesifikasi(self):
        return ""

    # POLISH: Ekstraksi nilai spesifik tanpa melanggar Open/Closed Principle
    def get_nilai_spesifik(self):
        return ""

# P2: Penerapan Inheritance (Pewarisan)
class BukuFiksi(Koleksi):
    def __init__(self, id_buku, judul, penulis, kategori, stok, genre):
        super().__init__(id_buku, judul, penulis, kategori, stok)
        self.genre = genre

    def get_spesifikasi(self):
        return f" | Genre: {self.genre}"

    def get_nilai_spesifik(self):
        return self.genre

class BukuNonFiksi(Koleksi):
    def __init__(self, id_buku, judul, penulis, kategori, stok, topik):
        super().__init__(id_buku, judul, penulis, kategori, stok)
        self.topik = topik

    def get_spesifikasi(self):
        return f" | Topik: {self.topik}"

    def get_nilai_spesifik(self):
        return self.topik

# P7 & P9: Penerapan Factory Pattern dengan Static Method
class BookFactory:
    @staticmethod
    def buat_buku(jenis, id_buku, judul, penulis, stok, spesifik):
        if jenis == "Fiksi":
            return BukuFiksi(id_buku, judul, penulis, "Fiksi", stok, spesifik)
        elif jenis == "Non-Fiksi":
            return BukuNonFiksi(id_buku, judul, penulis, "Non-Fiksi", stok, spesifik)
        else:
            raise ValueError("Jenis buku tidak valid.")

# P9: Penerapan Singleton Pattern
class LibraryDatabase:
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self.koleksi_buku = []
            self.akun_dummy = {
                "admin": "admin", 
                "daffa": "123",
                "budi": "123"
            }

            # Pemisahan riwayat untuk mencegah User Amnesia
            self.buku_aktif_dipinjam = {"daffa": ["BK001", "BK003"], "budi": []}
            self.riwayat_baca_permanen = {"daffa": ["BK001", "BK003"], "budi": []}

            self._seed_data()
            LibraryDatabase._is_initialized = True

    def _seed_data(self):
        self.koleksi_buku.extend([
            BookFactory.buat_buku("Fiksi", "BK001", "Bumi Manusia", "Pramoedya", 3, "Sastra"),
            BookFactory.buat_buku("Non-Fiksi", "BK002", "Sapiens", "Yuval N. H.", 5, "Sejarah"),
            BookFactory.buat_buku("Fiksi", "BK003", "Laskar Pelangi", "Andrea Hirata", 2, "Drama"),
            BookFactory.buat_buku("Non-Fiksi", "BK004", "Atomic Habits", "James Clear", 4, "Psikologi"),
            BookFactory.buat_buku("Fiksi", "BK005", "Cantik Itu Luka", "Eka Kurniawan", 3, "Sastra")
        ])

    def generate_id(self):
        next_id = len(self.koleksi_buku) + 1
        return f"BK{next_id:03d}"

    def get_buku_by_id(self, id_buku):
        for buku in self.koleksi_buku:
            if buku.id_buku == id_buku:
                return buku
        return None

    def cari_buku(self, keyword):
        keyword = keyword.lower()
        hasil = []
        for buku in self.koleksi_buku:
            if keyword in buku.id_buku.lower() or keyword in buku.judul.lower() or keyword in buku.penulis.lower():
                hasil.append(buku)
        return hasil

    def validasi_hapus(self, id_buku):
        for pinjaman in self.buku_aktif_dipinjam.values():
            if id_buku in pinjaman:
                return False
        return True

    def dapatkan_rekomendasi(self, username):
        riwayat = self.riwayat_baca_permanen.get(username, [])

        if not riwayat:
            return self.koleksi_buku[-3:]

        kategori_dipinjam = []
        for id_buku in riwayat:
            buku = self.get_buku_by_id(id_buku)
            if buku:
                kategori_dipinjam.append(buku.kategori)

        if not kategori_dipinjam:
            return self.koleksi_buku[-3:]

        kategori_favorit = Counter(kategori_dipinjam).most_common(1)[0][0]

        rekomendasi = [b for b in self.koleksi_buku if b.kategori == kategori_favorit and b.id_buku not in riwayat]
        return rekomendasi if rekomendasi else self.koleksi_buku[-3:]