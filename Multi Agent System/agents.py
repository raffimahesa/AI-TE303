"""Main Application: Simulasi Kolaborasi Multi-Agent System Kampus Pintar."""

from environment import CampusEnvironment
from agents import (
    OccupancyMonitorAgent,
    RoomControlAgent,
    EnergyCoordinatorAgent,
    SecuritySafetyAgent,
)


def print_environment_summary(env):
    print("\nStatus Akhir Ruangan:")
    for name, data in env.rooms.items():
        status_ac = "ON" if data["ac_menyala"] else "OFF"
        status_lampu = "ON" if data["lampu_menyala"] else "OFF"
        print(
            f"  - {name:<15} | Orang: {data['jumlah_orang']:<3} | Suhu: {data['suhu_c']} C "
            f"| AC: {status_ac:<3} | Lampu: {status_lampu:<3} | Daya: {data['daya_kw']} kW"
        )
    print(f"Total Konsumsi Daya Gedung: {env.get_total_power()} kW (Batas Maksimal: {env.batas_daya_maks_kw} kW)")
    print(f"Status Mode Darurat       : {'AKTIF' if env.mode_darurat else 'TIDAK AKTIF'}")


def run_cycle(title, env, agents):
    print("=" * 75)
    print(f"SKENARIO: {title}")
    print("=" * 75)

    env.clear_messages()

    # Siklus eksekusi berurutan agar pesan dari sensor diproses oleh agen pengontrol & koordinator
    for agent in agents:
        actions = agent.step(env)
        print(f"[{agent.name}]")
        for act in actions:
            print(f"  -> {act}")

    # Jika ada sinyal darurat dari SecurityAgent, beri kesempatan RoomControlAgent merespons langsung
    if env.mode_darurat:
        for agent in agents:
            if agent.name == "RoomControlAgent":
                emergency_actions = agent.step(env)
                print(f"[{agent.name} - Respons Darurat]")
                for act in emergency_actions:
                    print(f"  -> {act}")

    print_environment_summary(env)
    print()


if __name__ == "__main__":
    env = CampusEnvironment()
    agents = [
        OccupancyMonitorAgent(),
        SecuritySafetyAgent(),
        RoomControlAgent(),
        EnergyCoordinatorAgent(),
    ]

    # Skenario 1: Jam kuliah pagi (2 ruangan terisi, 1 ruangan kosong)
    env.update_room_condition("Lab Komputer", jumlah_orang=30, suhu_c=28.5, asap_terdeteksi=False)
    env.update_room_condition("Ruang Kuliah A", jumlah_orang=40, suhu_c=29.0, asap_terdeteksi=False)
    env.update_room_condition("Perpustakaan", jumlah_orang=0, suhu_c=25.0, asap_terdeteksi=False)
    run_cycle("1. Aktivitas Perkuliahan Normal", env, agents)

    # Skenario 2: Semua ruangan penuh dan panas -> Memicu Load Balancing dari EnergyAgent
    env.update_room_condition("Perpustakaan", jumlah_orang=12, suhu_c=28.0, asap_terdeteksi=False)
    run_cycle("2. Semua Ruangan Aktif (Uji Koordinasi Beban Listrik)", env, agents)

    # Skenario 3: Terdeteksi asap di Lab Komputer -> SecurityAgent mengambil alih protokol gedung
    env.update_room_condition("Lab Komputer", jumlah_orang=30, suhu_c=35.0, asap_terdeteksi=True)
    run_cycle("3. Deteksi Asap & Protokol Evakuasi Darurat", env, agents)
