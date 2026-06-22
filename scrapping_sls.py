import pandas as pd
import requests
import os
import tempfile
from datetime import datetime
import schedule
import time
from config_se2026 import NAMA_KABUPATEN, BASE_PATH, LATEST_FILE, archive_filename

# ================= SETTINGS =================
URL_DATA = 'https://fasih-sm.bps.go.id/app/api/analytic/api/v2/assignment/report-progress-by-responsibility' 
base_path = BASE_PATH                #FOLDER UNTUK MENYIMPAN DATA HASIL SCRAPPING
# ==========================================================


# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'f5avraaaaaaaaaaaaaaaa_session_': 'LFDPGNJFEFCMILPCADINAPJAGINBKGHHLMJCIHBNPAAKGNAMPNLFPNMOJNDACGOEBFMDDKJHHBBEHNEPDJKADCJEGMMGHPHCAJBHPHHMGLONJNOACEEGNJALGJALECIJ',
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '15faddc55339961e726413df06a9e1dc',
    'TS011f2d1a': '01266d26d0b996c03a5dfbd65137b5d128bd325664197c59277a7d09240f8f2d8831fc618dbf602b454ddd7387ed56a79b275763de',
    'XSRF-TOKEN': '25b8a3be-18d1-4c74-8ccc-8449a0b283ad',
    'SESSION': '966f7717-3add-44df-a084-8d6128567125',
    'TSPD_101': '0868f8be6fab28000b85d959311ad778e5013bc0861c02893564b7e101f59bfbddd574e13696d5974183f610c2a3064008d1b7fd170518005e94aa11420487a35ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'FFGJMNPDCKBHPABFBAKHPEGHCICCNLMBGGLCHFEADNMIFMMBHEFHMEDHFINEMIGPBCGDGLIELAADGCEFEJEAPAOOOMJGGFKPBFKCOKBDINPBACJALMGNEKFLMAMIPAPM',
    'TS5220f739077': '0868f8be6fab2800bcc5c142fc403ffa0dcf833c5305c7d945e2c2ae973229bb56c83de93b16acf16260896e4cd0fa5e0876a03233172000c5ba3368147f2a5df7bf71eb08220160b387923598e2df968fdb7c5333e4ba5a',
    'TS5220f739029': '0868f8be6fab28002c1baf71f59497a55d03e84e5902d56cfabfb30403528780a69f54c7fa40a05a973ff20fbe3bc7b1',
    'TSf1edb2d2027': '0868f8be6fab20000a63fb45a8f8bf93fcad126366da030f83d1d3a4f2b70285149814c5a8fffd1608cad65ef6113000710884bcf60a50d6e4566bc48e68919c80c4304cb7d0877e0791a69875372ec103f53f09866776bf77d5693815172ed4',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://fasih-sm.bps.go.id',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
    'X-XSRF-TOKEN': '25b8a3be-18d1-4c74-8ccc-8449a0b283ad',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=LFDPGNJFEFCMILPCADINAPJAGINBKGHHLMJCIHBNPAAKGNAMPNLFPNMOJNDACGOEBFMDDKJHHBBEHNEPDJKADCJEGMMGHPHCAJBHPHHMGLONJNOACEEGNJALGJALECIJ; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=15faddc55339961e726413df06a9e1dc; TS011f2d1a=01266d26d0b996c03a5dfbd65137b5d128bd325664197c59277a7d09240f8f2d8831fc618dbf602b454ddd7387ed56a79b275763de; XSRF-TOKEN=25b8a3be-18d1-4c74-8ccc-8449a0b283ad; SESSION=966f7717-3add-44df-a084-8d6128567125; TSPD_101=0868f8be6fab28000b85d959311ad778e5013bc0861c02893564b7e101f59bfbddd574e13696d5974183f610c2a3064008d1b7fd170518005e94aa11420487a35ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=FFGJMNPDCKBHPABFBAKHPEGHCICCNLMBGGLCHFEADNMIFMMBHEFHMEDHFINEMIGPBCGDGLIELAADGCEFEJEAPAOOOMJGGFKPBFKCOKBDINPBACJALMGNEKFLMAMIPAPM; TS5220f739077=0868f8be6fab2800bcc5c142fc403ffa0dcf833c5305c7d945e2c2ae973229bb56c83de93b16acf16260896e4cd0fa5e0876a03233172000c5ba3368147f2a5df7bf71eb08220160b387923598e2df968fdb7c5333e4ba5a; TS5220f739029=0868f8be6fab28002c1baf71f59497a55d03e84e5902d56cfabfb30403528780a69f54c7fa40a05a973ff20fbe3bc7b1; TSf1edb2d2027=0868f8be6fab20000a63fb45a8f8bf93fcad126366da030f83d1d3a4f2b70285149814c5a8fffd1608cad65ef6113000710884bcf60a50d6e4566bc48e68919c80c4304cb7d0877e0791a69875372ec103f53f09866776bf77d5693815172ed4',
}

json_data = {
    'surveyPeriodId': 'fd68e454-ba45-4b85-8205-f3bf777ded24',
    'surveyRoleId': '6d7d919a-45e5-4779-bb87-2905b49fd31a',
    'size': 5,
    'page': 0,
    'search': '',
    'target': 'TARGET_ONLY',
    'region': {
        'region1Id': None,
        'region2Id': None,
        'region3Id': None,
        'region4Id': None,
        'region5Id': None,
        'region6Id': None,
        'region7Id': None,
        'region8Id': None,
        'region9Id': None,
        'region10Id': None,
    },
    'regionSummaryLevel': 6,
}

# ================================================================

if not os.path.exists(base_path):
    os.makedirs(base_path)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = archive_filename(timestamp)  # arsip histori, 1 file per kali scraping


def save_and_merge(new_data):
    """Simpan ke file arsip (histori, append) DAN ke file LATEST (overwrite, untuk dashboard)"""
    if not new_data:
        return

    df_new = pd.DataFrame(new_data)
    df_new["scraped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1) Arsip histori - tetap ditambah (append), supaya bisa lihat tren dari waktu ke waktu
    if os.path.exists(backup_file):
        df_old = pd.read_excel(backup_file)
        df_archive = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_archive = df_new
    df_archive.to_excel(backup_file, index=False)

    # 2) File LATEST - SELALU ditimpa dengan snapshot terbaru saja (dibaca dashboard)
    _atomic_write_excel(df_new, LATEST_FILE)
    print(f"💾 Snapshot terbaru disimpan ke: {LATEST_FILE}")


def _atomic_write_excel(df, path):
    """Tulis Excel dengan aman: tulis ke file sementara dulu, baru rename.
    Mencegah dashboard membaca file yang setengah jadi/korup saat scraping sedang menulis."""
    folder = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(suffix=".xlsx", dir=folder)
    os.close(fd)
    try:
        df.to_excel(tmp_path, index=False)
        os.replace(tmp_path, path)  # atomic di OS yang sama (Windows/Linux)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise

def fetch_data():
    all_rows = []
    page = 0
    size = 10

    while True:
        json_data['page'] = page
        json_data['size'] = size

        response = requests.post(
            URL_DATA,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        if response.status_code != 200:
            print(f"❌ Error di page {page}")
            print(f"Status Code: {response.status_code}")
            print(response.text[:1000])
            break

        json_res = response.json()
        data_block = json_res.get("data", {})
        data = data_block.get("content", [])
        is_last = data_block.get("last", True)

        print(f"📄 Page {page} | jumlah data: {len(data)} | last: {is_last}")

        # 🔽 Flatten
        for user in data:
            for region in user.get("regionSummary", []):
                row = {
                    "userId": user.get("userId"),
                    "username": user.get("username"),
                    "email": user.get("email"),
                    "role": user.get("roleName"),
                    "regionCode": region.get("regionCode"),
                    "total_data": region.get("total"),
                }

                for status in region.get("statusBreakdown", []):
                    row[status.get("status")] = status.get("count")

                all_rows.append(row)

        if is_last:
            print("✅ Sudah sampai halaman terakhir")
            break

        page += 1

    if all_rows:
        save_and_merge(all_rows)

    print("🎉 Semua data berhasil disimpan!")


def job():
    print(f"\n[+] Memulai proses scraping pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_data()

if __name__ == "__main__":
    # Menjadwalkan job setiap 1 jam
    schedule.every(1).hours.do(job)

    print("⏱️  Script berjalan otomatis setiap 1 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)