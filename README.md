# AI-TE103 

Tugas Mata Kuliah Kecerdasan Buatan – Implementasi Search Algorithm dan Expert System.

## Introduction

Program ini membantu mahasiswa menemukan rute terbaik antar gedung di kampus.
1. **Search Algorithm (A\* dan BFS)**
   Kampus dimodelkan sebagai graf: gedung sebagai node, jalur sebagai edge. A\* mencari rute dengan biaya terendah ke setiap gedung yang sesuai dan sedang buka, lalu memilih yang terbaik. Heuristiknya adalah jarak Euclidean. BFS dipakai sebagai pembanding jumlah node yang dieksplorasi.

2. **Expert System (Forward Chaining)**
   Menerima input berupa kebutuhan pengguna (makan, ibadah, membaca, administrasi, olahraga, praktikum komputer, kuliah) dan kondisi (hujan, jam, kebutuhan kursi roda). Dari fakta tersebut, sistem menurunkan kategori tujuan, batasan rute, dan saran melalui aturan (rule) IF-THEN. Jejak penalarannya ditampilkan ke pengguna.

**Batasan yang diperhitungkan saat pencarian:**
- Saat hujan, jalur tanpa atap diberi biaya lebih besar (x2).
- Jika pengguna butuh akses kursi roda, jalur dengan tangga dilewati.
- Gedung yang tutup pada jam tersebut tidak dijadikan tujuan.

### Anggota Kelompok

| Nama | NIM | Peran | Branch |
|---|---|---|---|
| Raffi Mahesa | 101022400065 | Manager | `main` |
| Sargi Sagara | 101022400203 | Developer 1 | `dev1-gara` |
| Nizar Zulpikar | 101022400272 | Developer 2 | `dev2-nizar` |

### Struktur Repository

```
AI-TE103/
├── README.md
├── requirements.txt
├── main.py              # program utama 
├── search.py            # A* dan BFS
├── expert_system.py     # rule base dan forward chaining
├── data/
│   └── campus.json      # data gedung dan jalur kampus
└── screenshots/
    └── running.png
```

## Requirements

- Python 3.10 
- Tidak ada library eksternal (hanya library standar Python: `json`, `math`, `heapq`, `collections`, `datetime`)

Cek versi Python:

```bash
python --version
```

## How to Use

1. Clone repository:
   ```bash
   git clone https://github.com/<username>/AI-TE103.git
   cd AI-TE103
   ```
2. (Opsional) Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan program:
   ```bash
   python main.py
   ```
4. Ikuti instruksi di terminal:
   - Pilih nomor lokasi awal
   - Pilih nomor kebutuhan
   - Masukkan jam (0-23), atau kosongkan untuk memakai jam sekarang
   - Jawab `y` atau `n` untuk kondisi hujan dan kebutuhan kursi roda
5. Program menampilkan penalaran expert system, tujuan terbaik, rute, biaya rute, dan perbandingan dengan BFS.

### Mengubah Data Kampus

Edit `data/campus.json`:
- `nodes`: nama gedung, koordinat `x`/`y` (meter), `kategori`, dan `jam_buka`
- `edges`: `[gedung_a, gedung_b, beratap, ramah_kursi_roda]`
