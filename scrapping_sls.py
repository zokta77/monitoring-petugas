import pandas as pd
import requests
import os
import random
import tempfile
from datetime import datetime
import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config_se2026 import NAMA_KABUPATEN, BASE_PATH, LATEST_FILE, archive_filename

# ================= SETTINGS =================
URL_DATA = 'https://fasih-sm.bps.go.id/app/api/analytic/api/v2/assignment/report-progress-by-responsibility'
base_path = BASE_PATH

# ===== KONFIGURASI SELENIUM =====
# Cara cek path: buka chrome://version di profil yang sudah login FASIH
# lihat baris "Profile Path" → folder induknya = CHROME_PROFILE_DIR
CHROME_PROFILE_DIR  = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Profil 1"   # ganti sesuai profil (Default / Profile 1 / dst)
FASIH_HOME_URL      = "https://fasih-sm.bps.go.id/app/"
# ==========================================================

# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'TS00000000076': '0868f8be6fab280088ea33e7f4e92dcca8b4bdfe710e29bce79c77381a2574241963b5faa3bfc967b1e90c18e367a21c0800a994d309d00095bc1b31f40bc510452bf2f066bca3dcf43f96641822aa917095bdf2e06e8484892bddc9a38eb7942541c1ea8d1f5e85bc5c0f66438e6eba268cdee8825cf85b408c9c821b1d1695e3ffc8c2e59d3dd1a03c052a72c36f734b2c70e4eed41c9fd10ad8e270fc961b9a109786024c9c0724eb48c07b469ca7b1f7bffaa03204410c739edd446a38144bb40507adc1206edff31446bca42359708435cd5a14138092622cc7ec0796950821a0494388801b7413c7ed7cc476efd73d38718e070046b6808c45ef0b6e6cf47b95369d54f5cb',
    'TSPD_101_DID': '0868f8be6fab280088ea33e7f4e92dcca8b4bdfe710e29bce79c77381a2574241963b5faa3bfc967b1e90c18e367a21c0800a994d3063800b1265aa1fcc7ae37a9cf084a40c2a4e26583e1899df277ccf17c3ee67ed213abe8c03674dbd3557440e1441334617b6125c20aaf85d80eef',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'c7960ad8d07e0799751116f551e973f4',
    'TS011f2d1a': '01266d26d04fc242a0d137d86ffe148d1706891c1d383262eb1ae98853e2df3440be45c6cb55fd3e23c01b0e44f0c19c2da96f87a6',
    'TSPD_101': '0868f8be6fab28007ff2c939e9de289b8d95ab792eef642cd1ed5e7e013b758448a4d32f4d59c96e492b6eb42c1a8d5708746674d4051800eaee6811cecb23eb5ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': 'e3edfd3e-a10a-4dcb-ba4e-e374e6f269ff',
    'SESSION': 'f0bea322-c948-4389-9bcf-7b8019521be3',
    'f5avraaaaaaaaaaaaaaaa_session_': 'ONCJOOEPOFDDLDKLAIENDGPPBLBBKMCALHCHCHHLNIEFFLLCMJOPDHOAHDLCCNNDFFODNGFJKHDPGHLMKDJAPFJBPEPIFKMNGEIEFBDMKAEIJIINHGALEAEOHHJJLHEN',
    'f5avr0793127497aaaaaaaaaaaaaaaa_cspm_': 'LKMNPJMBMALEBPKHPENEMFDIHLJLKLGMBOABLLBECADECGLBMLALECBKCGFOFAELBEECLCCIPKEBBGDKOKCAJINGGMBBHOHHLKNGEBPDHGMHIJJJHABAJGIEGPEMLMJB',
    'TS5220f739077': '0868f8be6fab2800d2a7bc9c7f9551078071047c0de011799f91ffae313f10c3806473cf95e24c6d72202394d667939308f63fca24172000003fb7ed693b18b34f7547ea80146100e5b542b7d43a5c05f14fc025c0480ad4',
    'TS5220f739029': '0868f8be6fab2800702b96a6bdf5b4f602911e60a72d2506c7287c8b75bddc1947bb3ea73a8ccdc3ec6899d03e6327d6',
    'TSf1edb2d2027': '0868f8be6fab20005727805eb05ca1f706c98ac79542a331a086922414cf4bd39b2a1391d83a78550840c839e4113000be410e2f596d545c3084bf281140dd4d7abfd2516802a8822c71db1090cee19a9432ad294974e830635cf3acb3430395',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': 'e3edfd3e-a10a-4dcb-ba4e-e374e6f269ff',
    'cookie': 'TS00000000076=0868f8be6fab280088ea33e7f4e92dcca8b4bdfe710e29bce79c77381a2574241963b5faa3bfc967b1e90c18e367a21c0800a994d309d00095bc1b31f40bc510452bf2f066bca3dcf43f96641822aa917095bdf2e06e8484892bddc9a38eb7942541c1ea8d1f5e85bc5c0f66438e6eba268cdee8825cf85b408c9c821b1d1695e3ffc8c2e59d3dd1a03c052a72c36f734b2c70e4eed41c9fd10ad8e270fc961b9a109786024c9c0724eb48c07b469ca7b1f7bffaa03204410c739edd446a38144bb40507adc1206edff31446bca42359708435cd5a14138092622cc7ec0796950821a0494388801b7413c7ed7cc476efd73d38718e070046b6808c45ef0b6e6cf47b95369d54f5cb; TSPD_101_DID=0868f8be6fab280088ea33e7f4e92dcca8b4bdfe710e29bce79c77381a2574241963b5faa3bfc967b1e90c18e367a21c0800a994d3063800b1265aa1fcc7ae37a9cf084a40c2a4e26583e1899df277ccf17c3ee67ed213abe8c03674dbd3557440e1441334617b6125c20aaf85d80eef; db8ca2b43ed851cc93e71fd5fd72bff7=c7960ad8d07e0799751116f551e973f4; TS011f2d1a=01266d26d04fc242a0d137d86ffe148d1706891c1d383262eb1ae98853e2df3440be45c6cb55fd3e23c01b0e44f0c19c2da96f87a6; TSPD_101=0868f8be6fab28007ff2c939e9de289b8d95ab792eef642cd1ed5e7e013b758448a4d32f4d59c96e492b6eb42c1a8d5708746674d4051800eaee6811cecb23eb5ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=e3edfd3e-a10a-4dcb-ba4e-e374e6f269ff; SESSION=f0bea322-c948-4389-9bcf-7b8019521be3; f5avraaaaaaaaaaaaaaaa_session_=ONCJOOEPOFDDLDKLAIENDGPPBLBBKMCALHCHCHHLNIEFFLLCMJOPDHOAHDLCCNNDFFODNGFJKHDPGHLMKDJAPFJBPEPIFKMNGEIEFBDMKAEIJIINHGALEAEOHHJJLHEN; f5avr0793127497aaaaaaaaaaaaaaaa_cspm_=LKMNPJMBMALEBPKHPENEMFDIHLJLKLGMBOABLLBECADECGLBMLALECBKCGFOFAELBEECLCCIPKEBBGDKOKCAJINGGMBBHOHHLKNGEBPDHGMHIJJJHABAJGIEGPEMLMJB; TS5220f739077=0868f8be6fab2800d2a7bc9c7f9551078071047c0de011799f91ffae313f10c3806473cf95e24c6d72202394d667939308f63fca24172000003fb7ed693b18b34f7547ea80146100e5b542b7d43a5c05f14fc025c0480ad4; TS5220f739029=0868f8be6fab2800702b96a6bdf5b4f602911e60a72d2506c7287c8b75bddc1947bb3ea73a8ccdc3ec6899d03e6327d6; TSf1edb2d2027=0868f8be6fab20005727805eb05ca1f706c98ac79542a331a086922414cf4bd39b2a1391d83a78550840c839e4113000be410e2f596d545c3084bf281140dd4d7abfd2516802a8822c71db1090cee19a9432ad294974e830635cf3acb3430395',
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
 
 
def refresh_cookies():
    """
    Buka Chrome pakai profil yang sudah login SSO BPS, ambil cookies segar,
    lalu update variabel global cookies & headers secara otomatis.
    Dipanggil otomatis ketika session terdeteksi expired.
 
    Syarat:
    - VPN BPS sudah konek
    - Profil Chrome di CHROME_PROFILE_DIR/CHROME_PROFILE_NAME sudah pernah
      login manual ke FASIH minimal sekali
    - Tidak ada window Chrome lain yang sedang memakai profil yang sama
    """
    global cookies
 
    print("🔄 Session expired — membuka browser untuk ambil cookies segar...")
    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    options.add_argument(f"--profile-directory={CHROME_PROFILE_NAME}")
    # Aktifkan baris di bawah setelah yakin jalan (browser gak muncul di layar):
    # options.add_argument("--headless=new")
 
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(FASIH_HOME_URL)
        time.sleep(6)   # tunggu redirect SSO + halaman selesai load
 
        fresh = {c["name"]: c["value"] for c in driver.get_cookies()}
 
        if not fresh.get("SESSION") and not fresh.get("XSRF-TOKEN"):
            raise RuntimeError(
                "Cookies SESSION/XSRF-TOKEN tidak ditemukan. "
                "Buka Chrome dengan profil ini dan login manual ke FASIH dulu."
            )
 
        cookies.update(fresh)
        headers["x-xsrf-token"] = fresh.get("XSRF-TOKEN", headers["x-xsrf-token"])
        print(f"✅ Cookies segar berhasil diambil ({len(fresh)} cookie). Lanjut scraping...")
    finally:
        driver.quit()
 
 
def is_session_expired(response):
    """
    Deteksi apakah session sudah expired berdasarkan respons API.
    FASIH/Keycloak biasanya redirect ke halaman login (HTML) saat session habis —
    sehingga Content-Type bukan JSON, atau JSON-nya tidak punya field 'data'.
    """
    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type:
        return True
 
    try:
        body = response.json()
        # Kalau response JSON tapi field 'data' hilang dan ada pesan error auth
        if body.get("status") in (401, 403):
            return True
        if "login" in str(body).lower() or "unauthorized" in str(body).lower():
            return True
        return False
    except Exception:
        # Kalau response sama sekali gak bisa di-parse sebagai JSON → HTML login page
        return True
 
 
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
    max_refresh = 2          # maksimal berapa kali boleh refresh cookies dalam 1 run
    refresh_count = 0

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

        # ── Deteksi session expired → auto-refresh cookies lalu ulangi page ini ──
        if response.status_code in (200,) and is_session_expired(response) or \
           response.status_code in (302, 401):
            if refresh_count >= max_refresh:
                print(f"🛑 Session expired lagi setelah {max_refresh}x refresh. "
                      "Kemungkinan profil Chrome perlu login manual ulang.")
                break
            try:
                refresh_cookies()
                refresh_count += 1
                # Reset session agar cookies baru ikut terpakai
                session = requests.Session()
                print(f"↩️  Mengulang page {page} dengan cookies baru...")
                time.sleep(2)
                continue   # ulangi iterasi loop dengan page yang sama
            except Exception as e:
                print(f"🛑 Gagal refresh cookies: {e}")
                break

        if response.status_code != 200:
            print(f"❌ Error di page {page} | Status: {response.status_code}")
            print(response.text[:500])
            break

        try:
            json_res    = response.json()
        except Exception:
            print(f"❌ Response bukan JSON di page {page}. Kemungkinan session expired.")
            break

        data_block  = json_res.get("data", {})
        data        = data_block.get("content", [])
        is_last     = data_block.get("last", True)

        print(f"📄 Page {page} | data: {len(data)} | last: {is_last}")

        for user in data:
            for region in user.get("regionSummary", []):
                row = {
                    "userId":     user.get("userId"),
                    "username":   user.get("username"),
                    "email":      user.get("email"),
                    "role":       user.get("roleName"),
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
        time.sleep(random.uniform(1, 2))

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

    print("⏱️  Script berjalan otomatis setiap 1 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)