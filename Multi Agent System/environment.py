"""Modul Environment & Message Bus untuk komunikasi Multi-Agent System. (Dev: Sargi)"""


class Message:
    """Representasi pesan yang dikirim antar agen di dalam sistem."""

    def __init__(self, sender, receiver, topic, content):
        self.sender = sender
        self.receiver = receiver  # Nama agen tujuan atau 'ALL' untuk broadcast
        self.topic = topic
        self.content = content

    def __repr__(self):
        return f"[{self.sender} -> {self.receiver}] ({self.topic}): {self.content}"


class CampusEnvironment:
    """
    Lingkungan simulasi gedung kampus tempat agen berinteraksi.
    Menyimpan data kondisi ruangan serta antrean pesan (Message Bus).
    """

    def __init__(self):
        self.rooms = {
            "Lab Komputer": {
                "jumlah_orang": 0,
                "suhu_c": 26.0,
                "ac_menyala": False,
                "lampu_menyala": False,
                "asap_terdeteksi": False,
                "daya_kw": 0.5,
            },
            "Ruang Kuliah A": {
                "jumlah_orang": 0,
                "suhu_c": 27.0,
                "ac_menyala": False,
                "lampu_menyala": False,
                "asap_terdeteksi": False,
                "daya_kw": 0.2,
            },
            "Perpustakaan": {
                "jumlah_orang": 0,
                "suhu_c": 25.0,
                "ac_menyala": False,
                "lampu_menyala": False,
                "asap_terdeteksi": False,
                "daya_kw": 0.4,
            },
        }
        self.batas_daya_maks_kw = 12.0
        self.mode_darurat = False
        self.message_queue = []
        self.logs = []

    def update_room_condition(self, room_name, **kwargs):
        """Perbarui kondisi fisik ruangan (misal perubahan jumlah orang, suhu, atau sensor asap)."""
        if room_name in self.rooms:
            for key, value in kwargs.items():
                if key in self.rooms[room_name]:
                    self.rooms[room_name][key] = value

    def send_message(self, sender, receiver, topic, content):
        """Kirim pesan ke Message Bus."""
        msg = Message(sender, receiver, topic, content)
        self.message_queue.append(msg)
        self.logs.append(str(msg))

    def get_messages_for(self, agent_name):
        """Ambil semua pesan yang ditujukan untuk agen tertentu atau broadcast ('ALL')."""
        return [
            m for m in self.message_queue
            if m.receiver == agent_name or m.receiver == "ALL"
        ]

    def clear_messages(self):
        """Bersihkan antrean pesan setelah satu siklus eksekusi selesai."""
        self.message_queue.clear()

    def get_total_power(self):
        """Hitung total konsumsi daya listrik seluruh ruangan (kW)."""
        return round(sum(r["daya_kw"] for r in self.rooms.values()), 2)


if __name__ == "__main__":
    print("=== TES MODUL ENVIRONMENT & MESSAGE BUS ===")
    env = CampusEnvironment()
    env.update_room_condition("Lab Komputer", jumlah_orang=35, suhu_c=30.5)
    env.send_message("SensorAgent", "EnergyAgent", "SUHU_TINGGI", {"ruang": "Lab Komputer", "suhu": 30.5})

    print(f"Kondisi Lab Komputer : {env.rooms['Lab Komputer']}")
    print(f"Total Daya Awal      : {env.get_total_power()} kW")
    print(f"Pesan untuk Energy   : {env.get_messages_for('EnergyAgent')}")
