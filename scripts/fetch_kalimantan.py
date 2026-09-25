import requests
import csv
import os
from datetime import datetime, timezone

TOKEN = os.environ["AQICN_TOKEN"]  

STASIUN = {
    "Palangka Raya": 8342,
    "Banjarbaru": 8292,
    "Samarinda": 8293,
}

OUTPUT_FILE = "data/kalimantan_ispu.csv"

def ambil_data(nama_kota, uid):
    url = f"https://api.waqi.info/feed/@{uid}/?token={TOKEN}"
    res = requests.get(url).json()

    if res["status"] != "ok":
        print(f"Gagal ambil data {nama_kota}: {res}")
        return None

    data = res["data"]
    return {
        "tanggal_ambil": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "kota": nama_kota,
        "uid": uid,
        "aqi": data.get("aqi", ""),
        "pm25": data.get("iaqi", {}).get("pm25", {}).get("v", ""),
        "waktu_update_stasiun": data.get("time", {}).get("s", ""),
    }

def simpan_ke_csv(baris_baru):
    file_sudah_ada = os.path.isfile(OUTPUT_FILE)
    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=baris_baru[0].keys())
        if not file_sudah_ada:
            writer.writeheader()
        writer.writerows(baris_baru)

if __name__ == "__main__":
    hasil = []
    for kota, uid in STASIUN.items():
        data = ambil_data(kota, uid)
        if data:
            hasil.append(data)

    if hasil:
        simpan_ke_csv(hasil)
        print(f"Berhasil simpan {len(hasil)} baris data baru.")
    else:
        print("Tidak ada data yang berhasil diambil hari ini.")