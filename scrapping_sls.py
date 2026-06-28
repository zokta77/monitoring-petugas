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
    'db8ca2b43ed851cc93e71fd5fd72bff7': '37ffe750940d1049f405b1ce71f018c1',
    'XSRF-TOKEN': '716574e4-67b7-4789-839f-53ba5b624044',
    'SESSION': 'f7234d66-2978-4347-9c26-44de8a232609',
    'f5avraaaaaaaaaaaaaaaa_session_': 'JBKAIMOBJFKLKIDIHFJKGJILPFHIOEAFMDGNKFFOABHEJKIEDJKHIPJLPNPHNCHNONEDDEHJOJEDCDGBPEKANBEHBCPNBPKDEKNLELJODLCILLHAHLHKGDEEJMHGMIBJ',
    'TS00000000076': '0868f8be6fab2800cd7f829202932e1a543f434c7a5ae9594b62c543343b97ccfb2fafe4c7522eb44841dbcd3f60e2140832590f3709d0001ab82c7e11c88c8d12d5ad03a97d642f1ce42ee4fa3ee72980af9fdbc1a287ca4566fbe24d909f82c63ebd4c330f26ee6c660f71f5bf766912a4972a75ca29d61744e5ff669cd1aaf9f5efa33598785e6e87c4c712b366a8f13adaf6fdd8f9cc969d1d9da78a5d93a74770e81d9d66a33c40de925ab91e850e19130d29de29b5f19efa61675ff45a110dd8b600fa63dc4e6df9af68391bfb2b26c4f77a472750612a301884059ffb339d2cfeba17651b976c82a779d4d49cd180e618937945341886fe4d8339f82859cc08c75a6f1989',
    'TSPD_101_DID': '0868f8be6fab2800cd7f829202932e1a543f434c7a5ae9594b62c543343b97ccfb2fafe4c7522eb44841dbcd3f60e2140832590f37063800b2b9f8bf6ec289339437e223a234b7ccce64a09990fef1fd6c9c846730e7a8c92e0a3db27536e07701fff72270f2fec4c9ad3e335fa23c06',
    'TS011f2d1a': '01266d26d0716fbbab73caae1142b66a521e2ec61a014350a9d3591f63cb3308b4e509a2656af1a589a0bca83096c0aaeb5692272f',
    'TSPD_101': '0868f8be6fab280099f059f5e8a982118f118537d8c03c9f4156d0aba175186db680a853b62e79d1a2fbfe6ab92136190841f4c4b0051800a4b91bd68a42b81e5ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800aece851d37e0a6089f28cba65aa12fdeeea54ed1589062415dadd1bdcf8f252041d83ebbc6f83faa08b099041f172000ccd06a01c322b672bb5b5f7774084ddc1a15fb5253b09ece93de66b7c988e44a',
    'TS5220f739029': '0868f8be6fab2800ed17f28b5ccf9c9349955148e51bf3acfc1a50e148d79b28d7262dd4f9376374a8b00fa677890f25',
    'TSf1edb2d2027': '0868f8be6fab2000362adf97fe2e810777d643585e373ea95b53c0c10dbdabc4bfb78074b11baebd082e60de5d113000dd4f1a5158d75fb0c376e2f5df14b4d46ec29fb4ef71a6e34f72202deaa2c275079108f1ff16d2a28111d0e390d944e5',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
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
    'x-xsrf-token': '716574e4-67b7-4789-839f-53ba5b624044',
    'cookie': 'db8ca2b43ed851cc93e71fd5fd72bff7=37ffe750940d1049f405b1ce71f018c1; XSRF-TOKEN=716574e4-67b7-4789-839f-53ba5b624044; SESSION=f7234d66-2978-4347-9c26-44de8a232609; f5avraaaaaaaaaaaaaaaa_session_=JBKAIMOBJFKLKIDIHFJKGJILPFHIOEAFMDGNKFFOABHEJKIEDJKHIPJLPNPHNCHNONEDDEHJOJEDCDGBPEKANBEHBCPNBPKDEKNLELJODLCILLHAHLHKGDEEJMHGMIBJ; TS00000000076=0868f8be6fab2800cd7f829202932e1a543f434c7a5ae9594b62c543343b97ccfb2fafe4c7522eb44841dbcd3f60e2140832590f3709d0001ab82c7e11c88c8d12d5ad03a97d642f1ce42ee4fa3ee72980af9fdbc1a287ca4566fbe24d909f82c63ebd4c330f26ee6c660f71f5bf766912a4972a75ca29d61744e5ff669cd1aaf9f5efa33598785e6e87c4c712b366a8f13adaf6fdd8f9cc969d1d9da78a5d93a74770e81d9d66a33c40de925ab91e850e19130d29de29b5f19efa61675ff45a110dd8b600fa63dc4e6df9af68391bfb2b26c4f77a472750612a301884059ffb339d2cfeba17651b976c82a779d4d49cd180e618937945341886fe4d8339f82859cc08c75a6f1989; TSPD_101_DID=0868f8be6fab2800cd7f829202932e1a543f434c7a5ae9594b62c543343b97ccfb2fafe4c7522eb44841dbcd3f60e2140832590f37063800b2b9f8bf6ec289339437e223a234b7ccce64a09990fef1fd6c9c846730e7a8c92e0a3db27536e07701fff72270f2fec4c9ad3e335fa23c06; TS011f2d1a=01266d26d0716fbbab73caae1142b66a521e2ec61a014350a9d3591f63cb3308b4e509a2656af1a589a0bca83096c0aaeb5692272f; TSPD_101=0868f8be6fab280099f059f5e8a982118f118537d8c03c9f4156d0aba175186db680a853b62e79d1a2fbfe6ab92136190841f4c4b0051800a4b91bd68a42b81e5ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800aece851d37e0a6089f28cba65aa12fdeeea54ed1589062415dadd1bdcf8f252041d83ebbc6f83faa08b099041f172000ccd06a01c322b672bb5b5f7774084ddc1a15fb5253b09ece93de66b7c988e44a; TS5220f739029=0868f8be6fab2800ed17f28b5ccf9c9349955148e51bf3acfc1a50e148d79b28d7262dd4f9376374a8b00fa677890f25; TSf1edb2d2027=0868f8be6fab2000362adf97fe2e810777d643585e373ea95b53c0c10dbdabc4bfb78074b11baebd082e60de5d113000dd4f1a5158d75fb0c376e2f5df14b4d46ec29fb4ef71a6e34f72202deaa2c275079108f1ff16d2a28111d0e390d944e5',
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
 
 
def request_with_backoff(session, method, url, max_retries=3, **kwargs):
    """Request dengan retry + exponential backoff untuk error sementara (network/5xx).

    Kalau dapat 403/429 berulang sampai max_retries, INI BUKAN dianggap 'masih bisa dicoba
    cara lain' - melainkan sinyal untuk berhenti (circuit breaker). Sengaja TIDAK mencoba
    menyamarkan request lebih jauh; tujuannya cuma menghindari nge-hantam endpoint yang sama
    berkali-kali dalam waktu singkat saat ada gangguan sesaat.
    """
    delay = 2
    response = None
    for attempt in range(1, max_retries + 1):
        try:
            response = session.request(method, url, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Network error (percobaan {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise
            time.sleep(delay)
            delay *= 2
            continue

        if response.status_code == 200:
            return response

        if response.status_code in (403, 429):
            print(f"⚠️  Status {response.status_code} (percobaan {attempt}/{max_retries}) - "
                  f"kemungkinan rate-limited/diblokir sementara.")
            if attempt == max_retries:
                raise RuntimeError(
                    f"Berhenti: status {response.status_code} berulang {max_retries}x. "
                    "Sistem sepertinya menahan request ini - cek manual lewat browser, "
                    "atau koordinasi ke admin FASIH, sebelum mencoba lagi."
                )
            time.sleep(delay)
            delay *= 2
            continue

        # status error lain (5xx, dll) - anggap transient, retry juga
        if attempt < max_retries:
            time.sleep(delay)
            delay *= 2
            continue
        return response  # serahkan ke pemanggil untuk dilog seperti biasa

    return response


def fetch_data():
    all_rows = []
    page = 0
    size = 10
    session = requests.Session()

    while True:
        json_data['page'] = page
        json_data['size'] = size

        try:
            response = request_with_backoff(
                session, "POST", URL_DATA,
                cookies=cookies, headers=headers, json=json_data,
            )
        except (RuntimeError, requests.exceptions.RequestException) as e:
            print(f"🛑 Berhenti scraping: {e}")
            break

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
        time.sleep(random.uniform(1, 2))  # delay acak 1-3 detik antar request

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

    print("⏱️  Script berjalan otomatis setiap 3 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)