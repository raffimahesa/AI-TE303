"""Modul Peta Graph Kampus & Algoritma BFS untuk pencarian rute. (Dev: Sargi & Nizar)"""

from collections import deque

# Graph keterhubungan antar gedung di lingkungan kampus
# Setiap jalur memiliki atribut: beratap (bool) dan bebas_tangga (bool)
CAMPUS_GRAPH = {
    "Gerbang Utama": [
        {"ke": "Gedung Rektorat", "beratap": True, "bebas_tangga": True},
        {"ke": "Gedung Kuliah Umum", "beratap": False, "bebas_tangga": True},
        {"ke": "Masjid Kampus", "beratap": True, "bebas_tangga": True},
    ],
    "Gedung Rektorat": [
        {"ke": "Gerbang Utama", "beratap": True, "bebas_tangga": True},
        {"ke": "Perpustakaan", "beratap": True, "bebas_tangga": True},
        {"ke": "Gedung Kuliah Umum", "beratap": True, "bebas_tangga": False},
    ],
    "Gedung Kuliah Umum": [
        {"ke": "Gerbang Utama", "beratap": False, "bebas_tangga": True},
        {"ke": "Gedung Rektorat", "beratap": True, "bebas_tangga": False},
        {"ke": "Lab Komputer", "beratap": True, "bebas_tangga": True},
        {"ke": "Kantin Kampus", "beratap": False, "bebas_tangga": False},
    ],
    "Perpustakaan": [
        {"ke": "Gedung Rektorat", "beratap": True, "bebas_tangga": True},
        {"ke": "Lab Komputer", "beratap": True, "bebas_tangga": True},
        {"ke": "Kantin Kampus", "beratap": True, "bebas_tangga": True},
    ],
    "Lab Komputer": [
        {"ke": "Gedung Kuliah Umum", "beratap": True, "bebas_tangga": True},
        {"ke": "Perpustakaan", "beratap": True, "bebas_tangga": True},
        {"ke": "Student Center", "beratap": False, "bebas_tangga": True},
    ],
    "Masjid Kampus": [
        {"ke": "Gerbang Utama", "beratap": True, "bebas_tangga": True},
        {"ke": "Kantin Kampus", "beratap": True, "bebas_tangga": True},
        {"ke": "Student Center", "beratap": False, "bebas_tangga": True},
    ],
    "Kantin Kampus": [
        {"ke": "Gedung Kuliah Umum", "beratap": False, "bebas_tangga": False},
        {"ke": "Perpustakaan", "beratap": True, "bebas_tangga": True},
        {"ke": "Masjid Kampus", "beratap": True, "bebas_tangga": True},
        {"ke": "Student Center", "beratap": True, "bebas_tangga": True},
    ],
    "Student Center": [
        {"ke": "Lab Komputer", "beratap": False, "bebas_tangga": True},
        {"ke": "Masjid Kampus", "beratap": False, "bebas_tangga": True},
        {"ke": "Kantin Kampus", "beratap": True, "bebas_tangga": True},
    ],
}


def is_edge_valid(edge, constraints):
    """Periksa apakah jalur memenuhi batasan rute dari Expert System."""
    if "utamakan_beratap" in constraints and not edge["beratap"]:
        return False
    if "hindari_tangga" in constraints and not edge["bebas_tangga"]:
        return False
    return True


def bfs_shortest_path(start, goal, constraints=None):
    """
    Mencari rute terpendek dari start ke goal menggunakan Breadth-First Search (BFS).
    Jika dengan batasan ketat tidak ditemukan jalur, otomatis mencari jalur alternatif.
    """
    if constraints is None:
        constraints = []

    if start not in CAMPUS_GRAPH or goal not in CAMPUS_GRAPH:
        return None, "Lokasi awal atau tujuan tidak ditemukan di peta kampus."

    if start == goal:
        return [start], "Sudah berada di lokasi tujuan."

    # Pencarian BFS dengan memperhatikan batasan (constraints)
    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        current_node = path[-1]

        for edge in CAMPUS_GRAPH.get(current_node, []):
            next_node = edge["ke"]
            if next_node not in visited and is_edge_valid(edge, constraints):
                new_path = path + [next_node]
                if next_node == goal:
                    return new_path, "Rute optimal ditemukan sesuai seluruh batasan kondisi."
                visited.add(next_node)
                queue.append(new_path)

    # Fallback: Jika batasan terlalu ketat sehingga tidak ada jalur, cari jalur BFS biasa
    if constraints:
        fallback_path, _ = bfs_shortest_path(start, goal, constraints=[])
        if fallback_path:
            return fallback_path, "Peringatan: Tidak ada jalur yang memenuhi semua batasan, menampilkan rute standar terpendek."

    return None, "Tidak ada jalur yang menghubungkan kedua lokasi tersebut."


def get_all_locations():
    """Mengembalikan daftar seluruh lokasi di kampus."""
    return list(CAMPUS_GRAPH.keys())


if __name__ == "__main__":
    print("=== TES MODUL SEARCH ROUTE (BFS) ===")
    awal = "Gerbang Utama"
    tujuan = "Kantin Kampus"

    rute_biasa, info1 = bfs_shortest_path(awal, tujuan)
    print(f"1. Rute Standar ({awal} -> {tujuan}):")
    print(f"   Jalur : {' -> '.join(rute_biasa)}")
    print(f"   Info  : {info1}\n")

    batasan = ["utamakan_beratap", "hindari_tangga"]
    rute_khusus, info2 = bfs_shortest_path(awal, tujuan, constraints=batasan)
    print(f"2. Rute dengan Batasan {batasan}:")
    print(f"   Jalur : {' -> '.join(rute_khusus)}")
    print(f"   Info  : {info2}")
