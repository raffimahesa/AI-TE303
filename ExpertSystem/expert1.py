# ==========================================
# FILE: ExpertSystem/main.py
# ==========================================

# 1. Mendefinisikan 'Mesin' Sistem Pakar (Rules)
def rekomendasi_kantin(uang_saku, cuaca):
    print("=== Sistem Pakar Rekomendasi Makan Mahasiswa ===")
    print(f"Status yang masuk -> Uang: Rp{uang_saku}, Cuaca: {cuaca}\n")
    
    # KUNCI BUG FIX: Bersihkan input cuaca dari spasi gaib dan paksa jadi huruf kecil
    cuaca_bersih = cuaca.strip().lower()

    # Rule 1: Uang mepet dan cuaca hujan
    if uang_saku <= 15000 and cuaca_bersih == "hujan":
        return "Rekomendasi: Makan indomie rebus di Warung Podomoro aja, murah dan anget pas hujan!"
        
    # Rule 2: Uang mepet tapi cuaca cerah
    elif uang_saku <= 15000 and cuaca_bersih == "cerah":
        return "Rekomendasi: Jalan ke Kantin Mulya Rasa, menu hemat dan ngenyangin."
        
    # Rule 3: Uang lebih dari 15000 (apapun cuacanya)
    else:
        return "Rekomendasi: Uang aman, bebas milih mau makan di mana aja di sekitar kampus!"

# 2. Mengambil Input Langsung dari Terminal
print("\n--- Masukkan Data Mahasiswa ---")

# int() maksa apapun yang diketik jadi tipe data angka bulat, bukan teks.
uang_mahasiswa = int(input("Berapa sisa uang saku kamu? (Ketik angka saja, misal 10000): "))

# Ambil input cuaca teks biasa
cuaca_hari_ini = input("Bagaimana cuaca hari ini? (Ketik Hujan/Cerah): ")

# 3. Menjalankan Mesin & Mencetak Keputusan
print("\n--- Hasil Analisis Expert System ---")
keputusan = rekomendasi_kantin(uang_mahasiswa, cuaca_hari_ini)
print(keputusan)