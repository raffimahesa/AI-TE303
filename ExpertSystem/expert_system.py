"""Expert System: forward chaining untuk menentukan tujuan & batasan rute. (Dev: Raffi)"""

# Setiap rule: (nama, set premis, kesimpulan)
RULES = [
    # Aturan penentuan kategori dari kebutuhan user
    ("R1", {"butuh_makan"},         "kategori:makan"),
    ("R2", {"butuh_ibadah"},        "kategori:ibadah"),
    ("R3", {"butuh_baca"},          "kategori:baca"),
    ("R4", {"butuh_administrasi"},  "kategori:administrasi"),
    ("R5", {"butuh_olahraga"},      "kategori:olahraga"),
    ("R6", {"butuh_komputer"},      "kategori:komputer"),
    ("R7", {"butuh_kuliah"},        "kategori:kuliah"),

    # Aturan batasan rute & saran kondisi
    ("R8", {"hujan"},               "rute:utamakan_beratap"),
    ("R9", {"kursi_roda"},          "rute:hindari_tangga"),
    ("R10", {"hujan", "kursi_roda"}, "saran:Rute dipilih dengan dua batasan sekaligus (atap + akses disabilitas)"),
    ("R11", {"jam_malam"},          "saran:Banyak gedung sudah tutup, hanya gedung 24 jam yang pasti buka"),
    ("R12", {"jam_malam", "kategori:makan"}, "saran:Kantin tutup pukul 20.00, pastikan masih sempat"),

    # Aturan lanjutan (Forward Chaining tahap 2): Kategori -> Rekomendasi Gedung Tujuan
    ("R13", {"kategori:makan"},        "tujuan:Kantin Kampus"),
    ("R14", {"kategori:ibadah"},       "tujuan:Masjid Kampus"),
    ("R15", {"kategori:baca"},         "tujuan:Perpustakaan"),
    ("R16", {"kategori:administrasi"}, "tujuan:Gedung Rektorat"),
    ("R17", {"kategori:olahraga"},     "tujuan:Student Center"),
    ("R18", {"kategori:komputer"},     "tujuan:Lab Komputer"),
    ("R19", {"kategori:kuliah"},       "tujuan:Gedung Kuliah Umum"),

    # Aturan peringatan jam malam untuk gedung tertentu
    ("R20", {"jam_malam", "kategori:administrasi"}, "saran:Layanan administrasi Gedung Rektorat tutup pada malam hari"),
    ("R21", {"jam_malam", "kategori:baca"},         "saran:Perpustakaan tutup pukul 21.00, gunakan area baca 24 jam"),
]


def forward_chaining(facts):
    """Terapkan rule berulang sampai tidak ada fakta baru. Return (fakta_akhir, trace)."""
    facts = set(facts)
    trace = []
    changed = True
    while changed:
        changed = False
        for name, premises, conclusion in RULES:
            if premises <= facts and conclusion not in facts:
                facts.add(conclusion)
                trace.append(f"{name}: {sorted(premises)} -> {conclusion}")
                changed = True
    return facts, trace


def get_conclusions(facts, prefix):
    """Ambil nilai kesimpulan berdasarkan prefix (kategori, tujuan, rute, saran)."""
    return [f.split(":", 1)[1] for f in sorted(facts) if f.startswith(prefix + ":")]


def analyze_user_needs(input_facts):
    """Fungsi pembantu untuk merangkum hasil inferensi Expert System."""
    final_facts, trace = forward_chaining(input_facts)
    return {
        "input_facts": list(input_facts),
        "kategori": get_conclusions(final_facts, "kategori"),
        "tujuan": get_conclusions(final_facts, "tujuan"),
        "batasan_rute": get_conclusions(final_facts, "rute"),
        "saran": get_conclusions(final_facts, "saran"),
        "trace": trace,
    }


if __name__ == "__main__":
    print("=== TES MODUL EXPERT SYSTEM (FORWARD CHAINING) ===")
    contoh_fakta = ["butuh_makan", "hujan", "kursi_roda", "jam_malam"]
    print(f"Fakta Awal : {contoh_fakta}\n")

    hasil = analyze_user_needs(contoh_fakta)

    print("Jeja Inferensi (Trace):")
    for langkah in hasil["trace"]:
        print(f"  - {langkah}")

    print("\nHasil Rekomendasi:")
    print(f"  - Kategori Tujuan : {hasil['kategori']}")
    print(f"  - Gedung Tujuan   : {hasil['tujuan']}")
    print(f"  - Batasan Rute    : {hasil['batasan_rute']}")
    print("  - Saran Khusus    :")
    for s in hasil["saran"]:
        print(f"    * {s}")
