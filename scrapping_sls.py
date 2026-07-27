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
    'f5avraaaaaaaaaaaaaaaa_session_': 'GHPDOCLAPHNIAIPONHFLPIPJDEHCLJAPBPPMDDENLNMPFFOLFHKFCOOBAMFGNEBIMHKDBOCDFJDLDDFMDPGAIODIBKDDIMJPKGNBGICPCMDNMHIBKMIOKAMOOGIFEJNI',
    'cf_clearance': 'eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg',
    '_ga': 'GA1.3.967752592.1784785844',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'f6e66949c4c269f37a1f439f46e2c296',
    'XSRF-TOKEN': 'bd5fa6dc-a329-4869-9b39-adf1f9646e70',
    'JSESSIONID': '23F056BED26F3DD0756475FE7B52D56E',
    'SESSION': '77dcc3d3-be66-41d9-a3e8-e24fc508606e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'BCALDIOHDKEPFFLPGPJIPLMLFPOLJDMKGGKFOAJFEBGAGPALFJKBHINNLLGLBCBCDFKDGLLHBOPMDACKGEAAODODHIIOJJGNDLFGMBMILDPOJFNANLEAMONKMGKLJHOH',
    'TS018af012': '0167a1c8617c00e58a8943dd004beb6e285853be505af59bf90a38c906a27bbd78346860b3810a526fce79148bb5ad43d1ad3e5f9877ea0cf368dee24c7dbd0642b7924e2d7a44cd199946d7b0ce3eaad326b27999',
    'TS011f2d1a': '01266d26d02c023abeba583e350413dd80c97533a06d841d1a3dfdcc7b5d599153a20802fcaca0d61c84ad2de33cd19066da38860a',
    'TS00000000076': '0868f8be6fab2800018b4314e60604db80737c5b979d08058dd31c1e5c0aec44a271dee3ca6da8249852e084f7283f3c087345e88e09d000efb49a508586a911ba56b8378c6f014d0f9567fa5eeb58401f8c7ef8f2c43d8e5e6109fd09865b5f81ee0afba34be0fd77db3b0389aa715f6b5dd779970db5616c895671aefa9a7dc3cacb7da22ea9340c6618687584ebd5d11457a49cf6baa75d2f5dd0cabe1ff9561ca4fc736d2ecb41ce65e17ce0f84f9a36f36fb78fc4611b3e83426390a8af84506b7b33ab69ed46e1be89edf238443985b168e831adc17f7cdab282c677ce02498691aff1c646e86ec5b67017245187a400b56ab509325aa3c10d4223426329b57c5f4a4388ea',
    'TSPD_101_DID': '0868f8be6fab2800018b4314e60604db80737c5b979d08058dd31c1e5c0aec44a271dee3ca6da8249852e084f7283f3c087345e88e06380058ee5138f717cc6cf71d9d9d8195c3edee2c9a3e391fc3bc4207c240581fe720f0b58973279db2f42e50ba35a8ac7ced83c8294325924ce0',
    'TSPD_101': '0868f8be6fab2800b171e773fa90e8fcc0c1cea71507b94ff193f0948b0539fafa699a4a234d368eeb2bc2685ecdc7b30873e00d4d0518001cbc44eec7e423385ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800e799ff69c6301fbe60314dd02adc2d44e099d5de11e832343a3e58707c88ac5aee325f946e2b0f6008d18abfee1720003d2b08ded078faa8c1327fed30a82a26cbc76cf12adc73cce9ac52e8bbcd1dd7',
    'TS5220f739029': '0868f8be6fab2800e92188cf4b2fb41ff2a0aa9ed9cda83a4203f81cc5f239b52b0b88e98a986aff6de9df53e308d16d',
    'TSf1edb2d2027': '0868f8be6fab2000b878961ea89f0662058981aa260188fb8bfb4c9a193fc18272d899ea04e0d82808938eec07113000e01693106011093e90d660206feac5a083bc5490e3f29b3da8d5955c0fb12702b0078e77b6336b30545224bb46bc9837',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'referer': 'https://fasih-sm.bps.go.id/app/surveys/a0429e96-51a5-477b-a415-485f9c153004/fd68e454-ba45-4b85-8205-f3bf777ded24',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': 'bd5fa6dc-a329-4869-9b39-adf1f9646e70',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=GHPDOCLAPHNIAIPONHFLPIPJDEHCLJAPBPPMDDENLNMPFFOLFHKFCOOBAMFGNEBIMHKDBOCDFJDLDDFMDPGAIODIBKDDIMJPKGNBGICPCMDNMHIBKMIOKAMOOGIFEJNI; cf_clearance=eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg; _ga=GA1.3.967752592.1784785844; _ga_XXTTVXWHDB=GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=f6e66949c4c269f37a1f439f46e2c296; XSRF-TOKEN=bd5fa6dc-a329-4869-9b39-adf1f9646e70; JSESSIONID=23F056BED26F3DD0756475FE7B52D56E; SESSION=77dcc3d3-be66-41d9-a3e8-e24fc508606e; f5avraaaaaaaaaaaaaaaa_session_=BCALDIOHDKEPFFLPGPJIPLMLFPOLJDMKGGKFOAJFEBGAGPALFJKBHINNLLGLBCBCDFKDGLLHBOPMDACKGEAAODODHIIOJJGNDLFGMBMILDPOJFNANLEAMONKMGKLJHOH; TS018af012=0167a1c8617c00e58a8943dd004beb6e285853be505af59bf90a38c906a27bbd78346860b3810a526fce79148bb5ad43d1ad3e5f9877ea0cf368dee24c7dbd0642b7924e2d7a44cd199946d7b0ce3eaad326b27999; TS011f2d1a=01266d26d02c023abeba583e350413dd80c97533a06d841d1a3dfdcc7b5d599153a20802fcaca0d61c84ad2de33cd19066da38860a; TS00000000076=0868f8be6fab2800018b4314e60604db80737c5b979d08058dd31c1e5c0aec44a271dee3ca6da8249852e084f7283f3c087345e88e09d000efb49a508586a911ba56b8378c6f014d0f9567fa5eeb58401f8c7ef8f2c43d8e5e6109fd09865b5f81ee0afba34be0fd77db3b0389aa715f6b5dd779970db5616c895671aefa9a7dc3cacb7da22ea9340c6618687584ebd5d11457a49cf6baa75d2f5dd0cabe1ff9561ca4fc736d2ecb41ce65e17ce0f84f9a36f36fb78fc4611b3e83426390a8af84506b7b33ab69ed46e1be89edf238443985b168e831adc17f7cdab282c677ce02498691aff1c646e86ec5b67017245187a400b56ab509325aa3c10d4223426329b57c5f4a4388ea; TSPD_101_DID=0868f8be6fab2800018b4314e60604db80737c5b979d08058dd31c1e5c0aec44a271dee3ca6da8249852e084f7283f3c087345e88e06380058ee5138f717cc6cf71d9d9d8195c3edee2c9a3e391fc3bc4207c240581fe720f0b58973279db2f42e50ba35a8ac7ced83c8294325924ce0; TSPD_101=0868f8be6fab2800b171e773fa90e8fcc0c1cea71507b94ff193f0948b0539fafa699a4a234d368eeb2bc2685ecdc7b30873e00d4d0518001cbc44eec7e423385ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800e799ff69c6301fbe60314dd02adc2d44e099d5de11e832343a3e58707c88ac5aee325f946e2b0f6008d18abfee1720003d2b08ded078faa8c1327fed30a82a26cbc76cf12adc73cce9ac52e8bbcd1dd7; TS5220f739029=0868f8be6fab2800e92188cf4b2fb41ff2a0aa9ed9cda83a4203f81cc5f239b52b0b88e98a986aff6de9df53e308d16d; TSf1edb2d2027=0868f8be6fab2000b878961ea89f0662058981aa260188fb8bfb4c9a193fc18272d899ea04e0d82808938eec07113000e01693106011093e90d660206feac5a083bc5490e3f29b3da8d5955c0fb12702b0078e77b6336b30545224bb46bc9837',
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
                "nama_pml",
                "jumlah_prelist_awal"
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