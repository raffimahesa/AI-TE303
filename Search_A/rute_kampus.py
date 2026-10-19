import math
import heapq
import webbrowser
import os
import requests
import folium
from folium.plugins import LocateControl

KOORDINAT = {
    "Universitas Telkom": (-6.9733, 107.6304),
    "Simpang Sukabirus": (-6.9765, 107.6328),
    "Simpang Sukapura": (-6.9695, 107.6345),
    "Podomoro Park Buah Batu": (-6.9680, 107.6382),
    "Transmart Buah Batu": (-6.9628, 107.6386),
    "Gerbang Tol Buah Batu": (-6.9602, 107.6391),
    "Simpang Buah Batu Soekarno Hatta": (-6.9482, 107.6335),
    "Simpang Turangga": (-6.9355, 107.6258),
    "Simpang Lengkong Besar": (-6.9268, 107.6145),
    "Alun-Alun Bandung": (-6.9218, 107.6071)
}

GRAF = {
    "Universitas Telkom": ["Simpang Sukabirus", "Simpang Sukapura", "Podomoro Park Buah Batu"],
    "Simpang Sukabirus": ["Universitas Telkom", "Podomoro Park Buah Batu"],
    "Simpang Sukapura": ["Universitas Telkom", "Podomoro Park Buah Batu", "Transmart Buah Batu"],
    "Podomoro Park Buah Batu": ["Universitas Telkom", "Simpang Sukabirus", "Simpang Sukapura", "Transmart Buah Batu"],
    "Transmart Buah Batu": ["Simpang Sukapura", "Podomoro Park Buah Batu", "Gerbang Tol Buah Batu"],
    "Gerbang Tol Buah Batu": ["Transmart Buah Batu", "Simpang Buah Batu Soekarno Hatta"],
    "Simpang Buah Batu Soekarno Hatta": ["Gerbang Tol Buah Batu", "Simpang Turangga"],
    "Simpang Turangga": ["Simpang Buah Batu Soekarno Hatta", "Simpang Lengkong Besar"],
    "Simpang Lengkong Besar": ["Simpang Turangga", "Alun-Alun Bandung"],
    "Alun-Alun Bandung": ["Simpang Lengkong Besar"]
}

def haversine(k1, k2):
    R = 6371.0
    lat1, lon1 = math.radians(k1[0]), math.radians(k1[1])
    lat2, lon2 = math.radians(k2[0]), math.radians(k2[1])
    a = math.sin((lat2 - lat1) / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def deteksi_lokasi():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=4).json()
        lat, lon = map(float, r["loc"].split(","))
        if haversine((lat, lon), KOORDINAT["Universitas Telkom"]) <= 30:
            return (lat, lon)
    except Exception:
        pass
    return (-6.9742, 107.6315)

def hubungkan_ke_graf(koord_user):
    nama = "Lokasi Saya"
    KOORDINAT[nama] = koord_user
    terdekat = [n for _, n in sorted((haversine(koord_user, k), n) for n, k in KOORDINAT.items() if n != nama)[:2]]
    GRAF[nama] = terdekat
    for t in terdekat:
        if nama not in GRAF[t]:
            GRAF[t].append(nama)
    return nama

def a_star(awal, tujuan):
    antrean = [(0.0, [awal])]
    g_score = {awal: 0.0}
    while antrean:
        _, jalur = heapq.heappop(antrean)
        curr = jalur[-1]
        if curr == tujuan:
            return jalur, g_score[tujuan]
        for tetangga in GRAF.get(curr, []):
            g_baru = g_score[curr] + haversine(KOORDINAT[curr], KOORDINAT[tetangga])
            if tetangga not in g_score or g_baru < g_score[tetangga]:
                g_score[tetangga] = g_baru
                f_score = g_baru + haversine(KOORDINAT[tetangga], KOORDINAT[tujuan])
                heapq.heappush(antrean, (f_score, jalur + [tetangga]))
    return None, 0.0

def rute_jalan_osrm(koord_list):
    try:
        s = ";".join([f"{lon},{lat}" for lat, lon in koord_list])
        url = f"http://router.project-osrm.org/route/v1/driving/{s}?overview=full&geometries=geojson"
        r = requests.get(url, timeout=5).json()
        if r.get("routes"):
             rute_data = r["routes"][0]
             garis = [(lat, lon) for lon, lat in rute_data["geometry"]["coordinates"]]
             return garis, rute_data["distance"] / 1000.0
    except Exception:
        pass
    return koord_list, None

def render_peta(rute, jarak_km):
    peta = folium.Map(location=KOORDINAT[rute[0]], zoom_start=14, control_scale=True)
    LocateControl(auto_start=False).add_to(peta)

    garis, jarak_osrm = rute_jalan_osrm([KOORDINAT[n] for n in rute])
    if jarak_osrm:
        jarak_km = jarak_osrm

    t_motor = max(1, round((jarak_km / 30.0) * 60))
    t_mobil = max(1, round((jarak_km / 20.0) * 60))

    folium.PolyLine(garis, color="#1a73e8", weight=6, opacity=0.85).add_to(peta)

    for i, nama in enumerate(rute):
        warna = "green" if i == 0 else ("red" if i == len(rute) - 1 else "blue")
        folium.Marker(
            location=KOORDINAT[nama],
            tooltip=f"{nama} ({jarak_km:.2f} km)" if i == len(rute) - 1 else nama,
            icon=folium.Icon(color=warna, icon="info-sign")
        ).add_to(peta)

    file_out = os.path.join(os.path.dirname(__file__), "peta_rute.html")
    peta.save(file_out)
    return os.path.abspath(file_out), jarak_km, t_motor, t_mobil

if __name__ == "__main__":
    daftar = list(KOORDINAT.keys())
    koord_awal = deteksi_lokasi()
    awal = hubungkan_ke_graf(koord_awal)
    print(f"Lokasi Anda Terdeteksi: {koord_awal}\n")
    for i, n in enumerate(daftar, 1):
        print(f"{i}. {n}")
    try:
        tujuan = daftar[int(input("\nPilih nomor tujuan: ")) - 1]
    except Exception:
        tujuan = "Alun-Alun Bandung"

    rute, jarak = a_star(awal, tujuan)
    if rute:
        file_peta, jarak_akhir, motor, mobil = render_peta(rute, jarak)
        print(f"\nRute Terpendek : {' -> '.join(rute)}")
        print(f"Estimasi Jarak : {jarak_akhir:.2f} km")
        print(f"Estimasi Waktu : ~{motor} menit (Motor) | ~{mobil} menit (Mobil)")
        webbrowser.open(f"file://{file_peta}")