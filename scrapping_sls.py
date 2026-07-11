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
    'f5avraaaaaaaaaaaaaaaa_session_': 'KEJEACDEGNPODCOIGJCDINBMEEJGHLKMGLCBPNNNEJNICNEEMAKDLMBNNPKAFCOAFNADHKGHMJCHEFPJLIGAMPHAJCGLNIHCJNOBBONNNGEJFIPKAGGJKIHKMEKMGCNH',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '996cc6b582f6b00b6e85a9049ecc17e3',
    'XSRF-TOKEN': '0bdd09c4-9a81-4754-86dc-0b99b0d75bb7',
    'f5avr0793127497aaaaaaaaaaaaaaaa_cspm_': 'HMJFNFDOGBOFFMDFNIPCHKDPBMLBDKHDEBMABNPDGGNOBMLCBFHDBFNBGCPPIKGHNCGCDHJJBMCLCBKJMNNADJKDAOMBKGDFIBAAJDCJNFFIOOACLBNGKOPKBGKFMFPF',
    'JSESSIONID': '33361E4B0D139E9210959D9D5B6D1F0D',
    'f5avraaaaaaaaaaaaaaaa_session_': 'KKJEILLPNDHBGGHLDEEGDGFDFAEGEKDIIJKMAEPPKKNNGLDKHGHOCMGLCANMJOCCONGDCBNFAJEJJKOBGKBAMKCAACNPMOBKOBEHFGOIBFKBIDIDNIOKGCEFGGBJDDCP',
    'SESSION': 'b31a14b8-02c0-4e36-b785-82832a716af8',
    'TS00000000076': '0868f8be6fab2800efe9a1f74778bd140bb25411b61a2b56f721531010b9588d6c900f60fe8ca19deced50f544a27f92082bda589b09d0005299fad99ba40287eab3198368e5abf6740013cb84a6e06bd3875f5438a31c5576923c3b079a8073187d5c9f283274f6e9e175b339e3452ebde7d7dc379647b2b9dd89f80f4d1d05c27330036c625fbc5ed471f185355e6ee9c7265bd386dc192d62a88ada535ed991efe5340fd8cd8e0e3bf5a46a84f129e57361cf341276e393197cd2cc016c2dbca1a10dbef0876e660b03cd8f4f46528fa75f40225619551e86a583699f22ecdaae26531c279cbcc3740aafe1908788c75e29fecd79350fc9546a7f4cb107e45a3f890bf1402a46',
    'TSPD_101_DID': '0868f8be6fab2800efe9a1f74778bd140bb25411b61a2b56f721531010b9588d6c900f60fe8ca19deced50f544a27f92082bda589b06380074b90d11ca1e382b91205f5a5baea64957211226bbfe62545f5fe5be6749eed5665e2f324cc51f323b8f2312ce54cbe5b1042c65337b1706',
    'TS011f2d1a': '01266d26d0ad0800ef0058616e2ecb1e4f91512e1d9c2004ae4543f9ef854bf199005e15cb8d8886007a91967d290d453c0e9904cb',
    'TSPD_101': '0868f8be6fab28004ca2f6fea18f433fb7629d0e9fd19771d25cb9c7d78e8ef2e25785c7a480d978e0275b29f3306f910886b7cc4a0518008e8028d38562a9085ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab28002dd3cf1806d2be240f88e0c294317d1b9375b828c7455a7384d5cf43ac051f60f4a8594995cb159a0837a5977c172000d9524bb6c8a98a533d5350522de6d2e2d2a3a0f2e95fbc2189c076f5b9cb05e4',
    'TS5220f739029': '0868f8be6fab28004609f517d0fd8cfff8d0128bf4734406d4f506b443cab30a44dfe9beeb0d4c864c316116d67412f8',
    'TSf1edb2d2027': '0868f8be6fab2000bc18cfbd24fe6ed5fc3c3670f8e627faf33a7749805dd896b3a30c1f9e2ea59f083c20fc31113000f8fc1fe2dcf5c199343daf30e546982aafbe47119e98f66e1161502ca10900122e56c86c3192c5e3df1d95d22fd5788a',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
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
    'x-xsrf-token': '0bdd09c4-9a81-4754-86dc-0b99b0d75bb7',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=KEJEACDEGNPODCOIGJCDINBMEEJGHLKMGLCBPNNNEJNICNEEMAKDLMBNNPKAFCOAFNADHKGHMJCHEFPJLIGAMPHAJCGLNIHCJNOBBONNNGEJFIPKAGGJKIHKMEKMGCNH; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; db8ca2b43ed851cc93e71fd5fd72bff7=996cc6b582f6b00b6e85a9049ecc17e3; XSRF-TOKEN=0bdd09c4-9a81-4754-86dc-0b99b0d75bb7; f5avr0793127497aaaaaaaaaaaaaaaa_cspm_=HMJFNFDOGBOFFMDFNIPCHKDPBMLBDKHDEBMABNPDGGNOBMLCBFHDBFNBGCPPIKGHNCGCDHJJBMCLCBKJMNNADJKDAOMBKGDFIBAAJDCJNFFIOOACLBNGKOPKBGKFMFPF; JSESSIONID=33361E4B0D139E9210959D9D5B6D1F0D; f5avraaaaaaaaaaaaaaaa_session_=KKJEILLPNDHBGGHLDEEGDGFDFAEGEKDIIJKMAEPPKKNNGLDKHGHOCMGLCANMJOCCONGDCBNFAJEJJKOBGKBAMKCAACNPMOBKOBEHFGOIBFKBIDIDNIOKGCEFGGBJDDCP; SESSION=b31a14b8-02c0-4e36-b785-82832a716af8; TS00000000076=0868f8be6fab2800efe9a1f74778bd140bb25411b61a2b56f721531010b9588d6c900f60fe8ca19deced50f544a27f92082bda589b09d0005299fad99ba40287eab3198368e5abf6740013cb84a6e06bd3875f5438a31c5576923c3b079a8073187d5c9f283274f6e9e175b339e3452ebde7d7dc379647b2b9dd89f80f4d1d05c27330036c625fbc5ed471f185355e6ee9c7265bd386dc192d62a88ada535ed991efe5340fd8cd8e0e3bf5a46a84f129e57361cf341276e393197cd2cc016c2dbca1a10dbef0876e660b03cd8f4f46528fa75f40225619551e86a583699f22ecdaae26531c279cbcc3740aafe1908788c75e29fecd79350fc9546a7f4cb107e45a3f890bf1402a46; TSPD_101_DID=0868f8be6fab2800efe9a1f74778bd140bb25411b61a2b56f721531010b9588d6c900f60fe8ca19deced50f544a27f92082bda589b06380074b90d11ca1e382b91205f5a5baea64957211226bbfe62545f5fe5be6749eed5665e2f324cc51f323b8f2312ce54cbe5b1042c65337b1706; TS011f2d1a=01266d26d0ad0800ef0058616e2ecb1e4f91512e1d9c2004ae4543f9ef854bf199005e15cb8d8886007a91967d290d453c0e9904cb; TSPD_101=0868f8be6fab28004ca2f6fea18f433fb7629d0e9fd19771d25cb9c7d78e8ef2e25785c7a480d978e0275b29f3306f910886b7cc4a0518008e8028d38562a9085ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab28002dd3cf1806d2be240f88e0c294317d1b9375b828c7455a7384d5cf43ac051f60f4a8594995cb159a0837a5977c172000d9524bb6c8a98a533d5350522de6d2e2d2a3a0f2e95fbc2189c076f5b9cb05e4; TS5220f739029=0868f8be6fab28004609f517d0fd8cfff8d0128bf4734406d4f506b443cab30a44dfe9beeb0d4c864c316116d67412f8; TSf1edb2d2027=0868f8be6fab2000bc18cfbd24fe6ed5fc3c3670f8e627faf33a7749805dd896b3a30c1f9e2ea59f083c20fc31113000f8fc1fe2dcf5c199343daf30e546982aafbe47119e98f66e1161502ca10900122e56c86c3192c5e3df1d95d22fd5788a',
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