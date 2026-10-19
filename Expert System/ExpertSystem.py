"""Expert System: forward chaining untuk menentukan tujuan & batasan rute. (Dev 2)"""

# Setiap rule: (nama, set premis, kesimpulan)
RULES = [
    ("R1", {"butuh_makan"},         "kategori:makan"),
    ("R2", {"butuh_ibadah"},        "kategori:ibadah"),
    ("R3", {"butuh_baca"},          "kategori:baca"),
    ("R4", {"butuh_administrasi"},  "kategori:administrasi"),
    ("R5", {"butuh_olahraga"},      "kategori:olahraga"),
    ("R6", {"butuh_komputer"},      "kategori:komputer"),
    ("R7", {"butuh_kuliah"},        "kategori:kuliah"),
    ("R8", {"hujan"},               "rute:utamakan_beratap"),
    ("R9", {"kursi_roda"},          "rute:hindari_tangga"),
    ("R10", {"hujan", "kursi_roda"}, "saran:Rute dipilih dengan dua batasan sekaligus (atap + akses disabilitas)"),
    ("R11", {"jam_malam"},          "saran:Banyak gedung sudah tutup, hanya gedung 24 jam yang pasti buka"),
    ("R12", {"jam_malam", "kategori:makan"}, "saran:Kantin tutup pukul 20.00, pastikan masih sempat"),
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
    return [f.split(":", 1)[1] for f in facts if f.startswith(prefix + ":")]
