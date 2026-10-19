# AI-TE503: Smart Campus Building & Energy Management (Multi-Agent System)

Proyek ini merupakan implementasi **Multi-Agent System (MAS)** untuk pengelolaan fasilitas, efisiensi energi listrik, dan keselamatan gedung kampus secara otonom. Setiap agen memiliki peran spesifik dan saling berkomunikasi melalui mekanisme *Message Bus* untuk mengambil keputusan kolektif.

## Tim Pengembang
* **Sargi** (`dev1-gara`): Modul Lingkungan Simulasi & Arsitektur Komunikasi (*Message Bus*)
* **Nizar** (`dev2-nizar`): Modul Agen Otonom (*Monitor, Room Control, Energy, Security*) & Simulasi Skenario
* **Raffi** (`rapitod`): Perancangan Arsitektur Multi-Agent, Dokumentasi, & Integrasi Repository

## Struktur Proyek
```text
Multi Agent System/
├── main.py            # Entry point utama simulasi skenario Multi-Agent
├── environment.py     # Modul lingkungan gedung kampus & Message Bus antar agen
├── agents.py          # Implementasi 4 agen otonom
└── README.md          # Dokumentasi proyek Multi-Agent System
