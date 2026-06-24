import pandas as pd
import requests
import os
import random
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
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'f5avraaaaaaaaaaaaaaaa_session_': 'EDPLKIACMMAGJGPENGEIOBHAKJELAAJNCHCJBFOJGEHLMAJILJCDGDAMKBPHIIICPFODCGJPFPJGDEMLDNPACNPMIFLBMEGJLDLMIJFOOMJKNCMPLHCBKDOEENMNFFBE',
    'XSRF-TOKEN': 'e4fd2cac-4c84-46a3-ad35-0642e8c8be23',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '9167d391c996d1ee03a563e7bdb935d3',
    'JSESSIONID': 'E64F9E8024307DF79D5F2AD8C74F57B1',
    'SESSION': '2b7b563f-7cb0-46b1-901d-3ca68d3e66de',
    'TS00000000076': '0868f8be6fab28002661b990d4ccdc045bb3aa3c763c3bdde99c3ef0acba9774438baec2da9d5c75a3640bddc98590f5089961cd7c09d000b726dbb9138715d13f879d59145fc847a3ffde9a22959323da36d52a3d203aeebe16a7cc408efc38d236e7d7d85b6a55e13a347bd1ee8470c0548ed34e479ff9532b36b5b0101be41ca51bc61970c76ef291c67b14bbe31a8efcea61f62acdf96c89c062d04241a6706c4c49720a3f0e88fc4f74742b81342cd901b9bacf0c04994a1d41ce9b8ef504435f5d91f3d4c15150a94b34edd622626e37698a73f87553d9005211b83a26d6c6defc08a990b1887e927303df70bb03a8e17cfc6a36e67215261bb1038d5fc24e299d979c9cf0',
    'TSPD_101_DID': '0868f8be6fab28002661b990d4ccdc045bb3aa3c763c3bdde99c3ef0acba9774438baec2da9d5c75a3640bddc98590f5089961cd7c063800ff219f99b8a57a4dffc33de49c578176fc29f2efebd60374f7d433ec7faeb1b215ab40fc009e4d9d37301c8d248d3baad1b196e217f7f4a8',
    'TS011f2d1a': '01266d26d01d589d69a639fcdc006a85d215634798eb1e41c3a26f575e6b6d6263f7371cd21fbf2ed321fc8e9a83835e122981efc5',
    'TSPD_101': '0868f8be6fab280032d002a6a0e6afd56d852d5c8a57dc619f8459707bb7db749c0b7c65d8ab84423bc94eaa94b7bf5b08d6d3ddd20518003ccb222b1a3e88e65ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800b5a6add9a64b33f44fc46a7a0716468580cf5159b01016b656a1fa849788b59d329c6b3eb858c605081b198e37172000ba4402b850a425394db55d62d1227c2ff2ae7704fab64883e621e890b9059982',
    'TS5220f739029': '0868f8be6fab28008c9bf43af199faaf3121d3fe91740590a99a3bcaa5c8d048ca35a95ebeb2cbce0422d9712eb2eb02',
    'TSf1edb2d2027': '0868f8be6fab2000aabc96f87603845681b271896a18fbc8af380d7cbb30222840bbf61df88b4979089586986a113000d56f3e877be3a87cd1bc2a1bd37923c788ddf5b091573d08e549f36f2a4619b7f4da5566afca53ffe2bbbe9ee6083215',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"iOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
    'x-xsrf-token': 'e4fd2cac-4c84-46a3-ad35-0642e8c8be23',
    'cookie': '_ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=EDPLKIACMMAGJGPENGEIOBHAKJELAAJNCHCJBFOJGEHLMAJILJCDGDAMKBPHIIICPFODCGJPFPJGDEMLDNPACNPMIFLBMEGJLDLMIJFOOMJKNCMPLHCBKDOEENMNFFBE; XSRF-TOKEN=e4fd2cac-4c84-46a3-ad35-0642e8c8be23; db8ca2b43ed851cc93e71fd5fd72bff7=9167d391c996d1ee03a563e7bdb935d3; JSESSIONID=E64F9E8024307DF79D5F2AD8C74F57B1; SESSION=2b7b563f-7cb0-46b1-901d-3ca68d3e66de; TS00000000076=0868f8be6fab28002661b990d4ccdc045bb3aa3c763c3bdde99c3ef0acba9774438baec2da9d5c75a3640bddc98590f5089961cd7c09d000b726dbb9138715d13f879d59145fc847a3ffde9a22959323da36d52a3d203aeebe16a7cc408efc38d236e7d7d85b6a55e13a347bd1ee8470c0548ed34e479ff9532b36b5b0101be41ca51bc61970c76ef291c67b14bbe31a8efcea61f62acdf96c89c062d04241a6706c4c49720a3f0e88fc4f74742b81342cd901b9bacf0c04994a1d41ce9b8ef504435f5d91f3d4c15150a94b34edd622626e37698a73f87553d9005211b83a26d6c6defc08a990b1887e927303df70bb03a8e17cfc6a36e67215261bb1038d5fc24e299d979c9cf0; TSPD_101_DID=0868f8be6fab28002661b990d4ccdc045bb3aa3c763c3bdde99c3ef0acba9774438baec2da9d5c75a3640bddc98590f5089961cd7c063800ff219f99b8a57a4dffc33de49c578176fc29f2efebd60374f7d433ec7faeb1b215ab40fc009e4d9d37301c8d248d3baad1b196e217f7f4a8; TS011f2d1a=01266d26d01d589d69a639fcdc006a85d215634798eb1e41c3a26f575e6b6d6263f7371cd21fbf2ed321fc8e9a83835e122981efc5; TSPD_101=0868f8be6fab280032d002a6a0e6afd56d852d5c8a57dc619f8459707bb7db749c0b7c65d8ab84423bc94eaa94b7bf5b08d6d3ddd20518003ccb222b1a3e88e65ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800b5a6add9a64b33f44fc46a7a0716468580cf5159b01016b656a1fa849788b59d329c6b3eb858c605081b198e37172000ba4402b850a425394db55d62d1227c2ff2ae7704fab64883e621e890b9059982; TS5220f739029=0868f8be6fab28008c9bf43af199faaf3121d3fe91740590a99a3bcaa5c8d048ca35a95ebeb2cbce0422d9712eb2eb02; TSf1edb2d2027=0868f8be6fab2000aabc96f87603845681b271896a18fbc8af380d7cbb30222840bbf61df88b4979089586986a113000d56f3e877be3a87cd1bc2a1bd37923c788ddf5b091573d08e549f36f2a4619b7f4da5566afca53ffe2bbbe9ee6083215',
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
    master = pd.read_excel("data/master_data.xlsx")

    master["pencacah"] = (
        master["pencacah"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df_new["email"] = (
        df_new["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    master["regionCode"] = master["regionCode"].astype(str)
    df_new["regionCode"] = df_new["regionCode"].astype(str)

    df_new = df_new.merge(
        master[
            [
                "regionCode",
                "nmkab",
                "nmkec",
                "nmdesa",
                "nmsls",
                "nmsubsls",
                "pengawas",
                "pencacah",
                "nama_pcl",
                "nama_pml"
            ]
        ],
        left_on=["email", "regionCode"],
        right_on=["pencacah", "regionCode"],
        how="left"
    )

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

def auto_push_github():
    import subprocess

    try:
        subprocess.run(
            ["git", "add", "data/"],
            check=True
        )

        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )

        if not status.stdout.strip():
            print("📌 Tidak ada perubahan")
            return

        subprocess.run(
            ["git", "commit", "-m", "Update hasil scraping"],
            check=True
        )

        # sinkron dulu dengan GitHub
        subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"],
            check=True
        )

        subprocess.run(
            ["git", "push", "origin", "main"],
            check=True
        )

        print("✅ Data berhasil dipush ke GitHub")

    except Exception as e:
        print(f"❌ Error push GitHub: {e}")
 
 
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
        time.sleep(random.uniform(1, 3))  # delay acak 1-3 detik antar request

    if all_rows:
        save_and_merge(all_rows)

    print("🎉 Semua data berhasil disimpan!")


def job():
    print(f"\n[+] Memulai proses scraping pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_data()
    auto_push_github()

if __name__ == "__main__":
    # Menjadwalkan job setiap 1 jam
    schedule.every(3).hours.do(job)

    print("⏱️  Script berjalan otomatis setiap 1 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)