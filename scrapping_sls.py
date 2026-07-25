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
    'cf_clearance': 'eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg',
    '_ga': 'GA1.3.967752592.1784785844',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '6c22c8497050655f1bcec821b13a05e4',
    'XSRF-TOKEN': 'eb4a434a-9cd1-44df-be7d-d9eba018a9d8',
    'f5avraaaaaaaaaaaaaaaa_session_': 'GIJENACEBIMHHBAIDPHIGILNOOEGPFKEPJGNOOGCDMMLCKLMGHGDDAIMIHLDMEBKGNIDOMNIKEHOHLKPAKCANHFADBPOGKCFKCOBGOPCNABLGJHEEDLKBMDACPDJPBGO',
    'TS011f2d1a': '01266d26d068388fd8adf9321021adc5bea47a58be3da65e2008dbbe2799f7eae33db209c89d0b3e0022e66b80b8f1ce1f09bf9291',
    'f5avr1980069168aaaaaaaaaaaaaaaa_cspm_': 'JGHIGLIPLBNKIGJCOFLIGFOEDKJGJEFOEFEEKLNAGCGEKGIJLEEIGBMOCBLKJIEIIPICDMCOCNIJDELBKPIAFAFFAGMBLGPHLLHGDKAMHEIBLAGAJGOFPNAANDMHLBBF',
    'TS00000000076': '0868f8be6fab28008930784773dedec4f962e31b26ceeee4652ccb41c565a534184c1345185b9155b635089f41060eef0850b4ef1409d000b3993a1e6685e16e38e4f8afd368dc90daffeaec4c7bd7e1b36e2bef32d079af9b603aae875c3b4ef4c95dd3d7a1e6e519b0531c2861e5726056fe221b15ff449244d8630f247680d3ac02f2bd7edcb972ac24f40f4c0a6de70f9d162b2abf5c8c391b5ea0bf3df153ac4db2c35f57128e4780062e1823b577e5f234a42b066256039bad6f673f0181d905f376dc9205fe65472ba209bfc57309a5582e11d301b522caba61cc110108aa18a82d4d99be2b768e8cae9f302f67b2ca15ed55f7c1de36e9aa88061baa94848125d12ada5e',
    'TSPD_101_DID': '0868f8be6fab28008930784773dedec4f962e31b26ceeee4652ccb41c565a534184c1345185b9155b635089f41060eef0850b4ef140638009880c4d93441ff8f1328887f987bf7512f7e8112b86b8a7d410aa4fe01ed078475cff8fb93a286e7a212af4586350d78bb2427828265ec6a',
    'TSPD_101': '0868f8be6fab2800c491bcd437a160005a9793126fdf0bdb7c1e4fa00869e9a197a8e4b58ba1ba4172799979ba8248f108769609710518009e127c9846c90a2e5ca1732140a3428bba23ce13beb1c95e',
    'JSESSIONID': 'C1F630DC332F0A2D7821C306663E5056',
    'SESSION': '6ce15f8a-be35-4362-96ed-193574eae55c',
    'TS5220f739077': '0868f8be6fab280086befc9bed91bd08005b8e466881c89279e5935eaa3190c87a232564e5032e6f28a1b6b0b1b2e91908ecd2fe2617200028005403e911cb7bc850623ddd1f96d7017b6df5799ac7345c157e068cd81196',
    'TS5220f739029': '0868f8be6fab2800df31fd3b13875d34367dd624031147615dfa19085581f2de71185a24e360efda216c1e4fee1b7830',
    'TSf1edb2d2027': '0868f8be6fab20004b3c781f5ae49d81eae27aeafd53d42e844313fb05a0bf17c26859796b628a5e089d1a4c22113000f4f58b44b0caf4efba300e804ebb7921650731d2879b00fdf3af101eadbc4040849877853763095db146a579feb8f4ad',
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
    'x-xsrf-token': 'eb4a434a-9cd1-44df-be7d-d9eba018a9d8',
    'cookie': 'cf_clearance=eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg; _ga=GA1.3.967752592.1784785844; _ga_XXTTVXWHDB=GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=6c22c8497050655f1bcec821b13a05e4; XSRF-TOKEN=eb4a434a-9cd1-44df-be7d-d9eba018a9d8; f5avraaaaaaaaaaaaaaaa_session_=GIJENACEBIMHHBAIDPHIGILNOOEGPFKEPJGNOOGCDMMLCKLMGHGDDAIMIHLDMEBKGNIDOMNIKEHOHLKPAKCANHFADBPOGKCFKCOBGOPCNABLGJHEEDLKBMDACPDJPBGO; TS011f2d1a=01266d26d068388fd8adf9321021adc5bea47a58be3da65e2008dbbe2799f7eae33db209c89d0b3e0022e66b80b8f1ce1f09bf9291; f5avr1980069168aaaaaaaaaaaaaaaa_cspm_=JGHIGLIPLBNKIGJCOFLIGFOEDKJGJEFOEFEEKLNAGCGEKGIJLEEIGBMOCBLKJIEIIPICDMCOCNIJDELBKPIAFAFFAGMBLGPHLLHGDKAMHEIBLAGAJGOFPNAANDMHLBBF; TS00000000076=0868f8be6fab28008930784773dedec4f962e31b26ceeee4652ccb41c565a534184c1345185b9155b635089f41060eef0850b4ef1409d000b3993a1e6685e16e38e4f8afd368dc90daffeaec4c7bd7e1b36e2bef32d079af9b603aae875c3b4ef4c95dd3d7a1e6e519b0531c2861e5726056fe221b15ff449244d8630f247680d3ac02f2bd7edcb972ac24f40f4c0a6de70f9d162b2abf5c8c391b5ea0bf3df153ac4db2c35f57128e4780062e1823b577e5f234a42b066256039bad6f673f0181d905f376dc9205fe65472ba209bfc57309a5582e11d301b522caba61cc110108aa18a82d4d99be2b768e8cae9f302f67b2ca15ed55f7c1de36e9aa88061baa94848125d12ada5e; TSPD_101_DID=0868f8be6fab28008930784773dedec4f962e31b26ceeee4652ccb41c565a534184c1345185b9155b635089f41060eef0850b4ef140638009880c4d93441ff8f1328887f987bf7512f7e8112b86b8a7d410aa4fe01ed078475cff8fb93a286e7a212af4586350d78bb2427828265ec6a; TSPD_101=0868f8be6fab2800c491bcd437a160005a9793126fdf0bdb7c1e4fa00869e9a197a8e4b58ba1ba4172799979ba8248f108769609710518009e127c9846c90a2e5ca1732140a3428bba23ce13beb1c95e; JSESSIONID=C1F630DC332F0A2D7821C306663E5056; SESSION=6ce15f8a-be35-4362-96ed-193574eae55c; TS5220f739077=0868f8be6fab280086befc9bed91bd08005b8e466881c89279e5935eaa3190c87a232564e5032e6f28a1b6b0b1b2e91908ecd2fe2617200028005403e911cb7bc850623ddd1f96d7017b6df5799ac7345c157e068cd81196; TS5220f739029=0868f8be6fab2800df31fd3b13875d34367dd624031147615dfa19085581f2de71185a24e360efda216c1e4fee1b7830; TSf1edb2d2027=0868f8be6fab20004b3c781f5ae49d81eae27aeafd53d42e844313fb05a0bf17c26859796b628a5e089d1a4c22113000f4f58b44b0caf4efba300e804ebb7921650731d2879b00fdf3af101eadbc4040849877853763095db146a579feb8f4ad',
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