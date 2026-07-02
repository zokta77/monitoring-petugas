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
    'f5avraaaaaaaaaaaaaaaa_session_': 'ILELFNAAIPMDPMANGBJKKLGEFDJAECNAGDOKGAAMJEAKLHCMGBAKCLBDPCMPFDIMKCODDHAJJFEEOPHOGGCAFLCGICBPDKKFNFJPCBMCJNAOJAICEJCADBAIPKMCBCDP',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'fa562932fc28ca0b3fccefa0da837e6b',
    'XSRF-TOKEN': '897c433f-58c1-4253-90b1-7eb38362df83',
    'TS018af012': '0167a1c8614c8bf24ee2ab30c1e0f259b1ce18f2cf12da13a72d159674a5afa0fd35e41447b1c65c2668dddef87063b60572ff7fb77b4fec3e7fa51cd77084c5fb7503eef5',
    'JSESSIONID': '5DC74262F6F8C9E391AC5A56EFC8BC38',
    'SESSION': '4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b',
    'TS0151fc2b': '0167a1c8619d401425fd145d27f4bd481a96d70e57ac5c524e7f2d391d5ecd25771960f683496031ce906f214ad99c9e176f81ec40',
    'f5avraaaaaaaaaaaaaaaa_session_': 'IKKAECCGDKKKEPIEGIEMJILNMIJKGKDCJFBKAHIFCNIINOGNBNCDAFBIFKGGDMHBGNIDBHLKPFFOAIIPAKCABDFOHCNOCJAFPIEFEDMOOPBKGJJEDAFBKDACDABOMMPI',
    'TS00000000076': '0868f8be6fab28006fde858147f58a8880643fc4436dccca9682a521200dc355e015dd4736cb9e5c7681949333b9ec9308f12d9b2509d000aaaf4c55b6f7d7d2f0d671d1afd717f955785b4d344b90ed6010487c31f55c49d03bd1a1a6ae6c86a1f6f0b35719c53930361174e9ef631d49400f7be92013e425658569ca50d79fdd7bf3b09470ea7e7b1600e240c741586e9bf0a56ab6f19c7cef9f67516afc7e6e0cff5469b0e0985ca812243dd70f721274ecbd62e9b41fd45e7045ceb032a1424be6f6340f0cb35fbb7248fe34d9dc902e614d1bc93bd386e2bd325919349d2a7b6296b3decae4fd5c1bb5c4c71cf8f17a82d5871560a053ed544bb967658c69c11ae3d0443592',
    'TSPD_101_DID': '0868f8be6fab28006fde858147f58a8880643fc4436dccca9682a521200dc355e015dd4736cb9e5c7681949333b9ec9308f12d9b25063800ccb3b9c6bf6618ce5bbabdad7b921b1abf377f4a703c399e4e94526fa42e6144f26975c68f8804c8334038119a731bfb2bd21565f074614a',
    'TS011f2d1a': '01266d26d0201dcc42e2e7dba011c364f78a67d889f06e7ccc8b5a26bbd006dfdef2a5ba7af3dac620e597a4896eeccd4b05b5333d',
    'TSPD_101': '0868f8be6fab280033d70b1c5f877aab4ceff0dbcbddbbd86b92fea9e763abbebf34a30b81792642b23c0106598e2a0f085c116790051800694c6ad741e9c1e15ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab280075bfdf239677deb24414eebe92e4b4e78d633fb092f47e2fa86af77a9f26de1a0f3f46d6fbf565110880768cf81720003edd3513fd754a64656af93510352a6a4b6da57957850c235f97149a2d716fe6',
    'TS5220f739029': '0868f8be6fab280061799c052ccea813163a2e76774d6b18e6b1e7217526b24f55162d06102450815c53d5ef1d687024',
    'TSf1edb2d2027': '0868f8be6fab20001eb9c7cc7b5676fcfc4fddfea4aa0b136cc4aa97a806ff25f5547a529c81ecf508192eaed7113000137820842006b92d0c500b5e9802eeeb6c5969e3ff730b7df39260a605f562f33619964461a4762b473dde39fdddca6f',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': '897c433f-58c1-4253-90b1-7eb38362df83',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=ILELFNAAIPMDPMANGBJKKLGEFDJAECNAGDOKGAAMJEAKLHCMGBAKCLBDPCMPFDIMKCODDHAJJFEEOPHOGGCAFLCGICBPDKKFNFJPCBMCJNAOJAICEJCADBAIPKMCBCDP; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; db8ca2b43ed851cc93e71fd5fd72bff7=fa562932fc28ca0b3fccefa0da837e6b; XSRF-TOKEN=897c433f-58c1-4253-90b1-7eb38362df83; TS018af012=0167a1c8614c8bf24ee2ab30c1e0f259b1ce18f2cf12da13a72d159674a5afa0fd35e41447b1c65c2668dddef87063b60572ff7fb77b4fec3e7fa51cd77084c5fb7503eef5; JSESSIONID=5DC74262F6F8C9E391AC5A56EFC8BC38; SESSION=4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b; TS0151fc2b=0167a1c8619d401425fd145d27f4bd481a96d70e57ac5c524e7f2d391d5ecd25771960f683496031ce906f214ad99c9e176f81ec40; f5avraaaaaaaaaaaaaaaa_session_=IKKAECCGDKKKEPIEGIEMJILNMIJKGKDCJFBKAHIFCNIINOGNBNCDAFBIFKGGDMHBGNIDBHLKPFFOAIIPAKCABDFOHCNOCJAFPIEFEDMOOPBKGJJEDAFBKDACDABOMMPI; TS00000000076=0868f8be6fab28006fde858147f58a8880643fc4436dccca9682a521200dc355e015dd4736cb9e5c7681949333b9ec9308f12d9b2509d000aaaf4c55b6f7d7d2f0d671d1afd717f955785b4d344b90ed6010487c31f55c49d03bd1a1a6ae6c86a1f6f0b35719c53930361174e9ef631d49400f7be92013e425658569ca50d79fdd7bf3b09470ea7e7b1600e240c741586e9bf0a56ab6f19c7cef9f67516afc7e6e0cff5469b0e0985ca812243dd70f721274ecbd62e9b41fd45e7045ceb032a1424be6f6340f0cb35fbb7248fe34d9dc902e614d1bc93bd386e2bd325919349d2a7b6296b3decae4fd5c1bb5c4c71cf8f17a82d5871560a053ed544bb967658c69c11ae3d0443592; TSPD_101_DID=0868f8be6fab28006fde858147f58a8880643fc4436dccca9682a521200dc355e015dd4736cb9e5c7681949333b9ec9308f12d9b25063800ccb3b9c6bf6618ce5bbabdad7b921b1abf377f4a703c399e4e94526fa42e6144f26975c68f8804c8334038119a731bfb2bd21565f074614a; TS011f2d1a=01266d26d0201dcc42e2e7dba011c364f78a67d889f06e7ccc8b5a26bbd006dfdef2a5ba7af3dac620e597a4896eeccd4b05b5333d; TSPD_101=0868f8be6fab280033d70b1c5f877aab4ceff0dbcbddbbd86b92fea9e763abbebf34a30b81792642b23c0106598e2a0f085c116790051800694c6ad741e9c1e15ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab280075bfdf239677deb24414eebe92e4b4e78d633fb092f47e2fa86af77a9f26de1a0f3f46d6fbf565110880768cf81720003edd3513fd754a64656af93510352a6a4b6da57957850c235f97149a2d716fe6; TS5220f739029=0868f8be6fab280061799c052ccea813163a2e76774d6b18e6b1e7217526b24f55162d06102450815c53d5ef1d687024; TSf1edb2d2027=0868f8be6fab20001eb9c7cc7b5676fcfc4fddfea4aa0b136cc4aa97a806ff25f5547a529c81ecf508192eaed7113000137820842006b92d0c500b5e9802eeeb6c5969e3ff730b7df39260a605f562f33619964461a4762b473dde39fdddca6f',
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
    schedule.every(1).hours.do(job)

    print("⏱️  Script berjalan otomatis setiap 3 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)