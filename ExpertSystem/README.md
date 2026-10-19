# AI-TE503: Kampus Navigation & Expert System

Proyek **AI-TE503** adalah sistem navigasi kampus cerdas yang menggabungkan dua pendekatan kecerdasan buatan (*Artificial Intelligence*):
1. **Search Algorithm (BFS)**: Menemukan jalur/rute terpendek antar gedung di lingkungan kampus.
2. **Expert System (Forward Chaining)**: Menentukan kategori tujuan dan memberikan rekomendasi/batasan rute berdasarkan kondisi tertentu (seperti cuaca, kebutuhan disabilitas, atau jam operasional).

---

## 👥 Tim Pengembang
* **Nizar** (`dev-nizar`): Modul Search Algorithm & Integrasi BFS
* **Sargi** (`dev-sargi`): Modul Peta & Graph Data Kampus
* **Raffi** (`dev-raffi`): Modul Expert System (Forward Chaining)

---

## 📁 Struktur Proyek

```text
AI-TE503/
├── main.py              # Entry point utama aplikasi
├── search_route.py      # Modul Algoritma BFS untuk pencarian rute
├── expert_system.py     # Modul Sistem Pakar dengan Forward Chaining
└── README.md            # Dokumentasi proyek
```

---

## 🚀 Fitur Utama

### 1. Modul Search Route (`search_route.py`)
* Menggunakan algoritma **Breadth-First Search (BFS)**.
* Mencari rute efisien antar lokasi/gedung di kampus berdasarkan graph keterhubungan gedung.

### 2. Modul Expert System (`expert_system.py`)
* Menggunakan teknik pencocokan aturan **Forward Chaining**.
* Memproses berbagai fakta input (contoh: `hujan`, `kursi_roda`, `jam_malam`, `butuh_makan`).
* Menghasilkan kategori lokasi tujuan beserta rekomendasi/saran khusus (contoh: mengutamakan jalur beratap atau menghindari tangga).

---

## 💻 Cara Menjalankan Project

### Prasyarat
* Python versi `3.10` atau yang lebih baru.

### Langkah-Langkah Running
1. **Clone Repository:**
   ```bash
   git clone https://github.com/rapitod/AI-TE503.git
   cd AI-TE503
   ```

2. **Jalankan Main Application:**
   ```bash
   python main.py
   ```

3. **Atau Jalankan Tes Modul Secara Terpisah:**
   * Tes pencarian rute:
     ```bash
     python search_route.py
     ```
   * Tes sistem pakar:
     ```bash
     python expert_system.py
     ```

---

## 📜 Contoh Hasil Aturan (Rule Base) Expert System

| Rule | Input Facts (Premis) | Kesimpulan / Rekomendasi |
| :--- | :--- | :--- |
| **R1** | `butuh_makan` | `kategori:makan` |
| **R8** | `hujan` | `rute:utamakan_beratap` |
| **R9** | `kursi_roda` | `rute:hindari_tangga` |
| **R11**| `jam_malam` | `saran:Banyak gedung sudah tutup` |

