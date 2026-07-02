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
    'f5avraaaaaaaaaaaaaaaa_session_': 'FMEINPFFFJKKFJJLBCEKGEGONCBFGDGIKENNPEPADCBJDMCGJPMMGENPNJMBABEHHKEDAJJFLJLLKNPAEDNAHEOPAOOMKLFDOFMDJHMJPIFKBOKOOEJBBLIJEFALINNO',
    'f5_cspm': '1234',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '9a32fc3ce04039d14660c4f4c4ac4aa2',
    'XSRF-TOKEN': '8ad306c3-4d47-4be0-8bc0-3b9abf8efbf4',
    'f5avr1980069168aaaaaaaaaaaaaaaa_cspm_': 'CJIOMLELKNECBAJAKCJPJDIGADDOJPDLDGEGMIBNBIOBNJKDMFEHEACHPAGMDGDOHDOCIKOBJFDBFOEOONCAIECCAPAAPKLLOCFGODIBBHLPAFJIKPFEFGKFGACJHGAK',
    'SESSION': '1838a08b-9f92-4edf-b3fd-67162f028672',
    'TS00000000076': '0868f8be6fab2800687d07c48d7959bfaae4cbb6c4c4e37a4cdcdb848ba1d519be89546098983bdb6b7973db280576da086250011a09d0008860960bf622be4951a8fe159d4b78cc5943b27125027a9074dfce8e81b0b53f1f281731ee486fb0331984e73ed333971f702cd8ca4955c93db115816f4ef2d568a42b0c5922a180f5e0648a746f7c4f6f4b7fefb51aef3a8a73e498e0b08f1f0d647c1bd766819320da938b53cf5b13815b3d02b5804da4cac8bdfaf20dff958e586cfd1b6e1fd5cf264d090cae4ab54098f8bc8457fea60a6f3e587ce0fd0a0be2e03e74d531ade5d5c2585a8f5fb388d03ef74011bcf9b7e8e22388f055504e2d800e1f22ef7e3aa42aae7353b7ea',
    'TSPD_101_DID': '0868f8be6fab2800687d07c48d7959bfaae4cbb6c4c4e37a4cdcdb848ba1d519be89546098983bdb6b7973db280576da086250011a063800eacc834937df8d92ee609728481a3fd035e87be869ecbc0fc4a461dd921946243329d3443429a56cc369835a2454df88ac62184bb290f4a2',
    'TS011f2d1a': '01266d26d06b158d40f39281c58309dd9473115b38177cd0c7083781d30fd7e040027aa80367acdc64591c83dba5d03dfbab3a657c',
    'TSPD_101': '0868f8be6fab28007e1739b433797b5f717c88ea2c83999ccbb06e3f45c7f149177d23bd0663cfb121bf8b731f250427084b8bef4a0518008538e012fd03fa535ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'FPGKMEJJCGHGFKMBPKPEEAMDDHIMLAFHKBCPNIFIGCFLAKJCEALLBFHPGPBMLJCGGFMDFBABNJGBNCOJCFCANFLNCOPAHFBBLMNIFHPDFIILCLCMCNGLLMCBFAKNMKJI',
    'TS5220f739077': '0868f8be6fab280028352a7a896789c60afa1e85600a55669909b89bead0f743cff6ee02cfd948217939e959a8955c1b083594f6e61720005eda8dcd9b12d4bfbd4733dfce892c45468f51cd89b9b71cc40c7f63043325a4',
    'TS5220f739029': '0868f8be6fab2800f178b06a27e385ddab875846f0c9e83aa03fb08ba52f1c577ce4c098ddb62661eb5cdb3ab25398f5',
    'TSf1edb2d2027': '0868f8be6fab20009ef17a24eb7035f09a55ac5e4c36f230cc27761bb362683227a0353d15f73f390879030bed1130003bffae554efd20ae48dba6a53bba32ebc9c614988c888ebd85fbbe111732860a98cf568d8598fe6b0e8a1ffe1aaf4356',
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
    'x-xsrf-token': '8ad306c3-4d47-4be0-8bc0-3b9abf8efbf4',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=FMEINPFFFJKKFJJLBCEKGEGONCBFGDGIKENNPEPADCBJDMCGJPMMGENPNJMBABEHHKEDAJJFLJLLKNPAEDNAHEOPAOOMKLFDOFMDJHMJPIFKBOKOOEJBBLIJEFALINNO; f5_cspm=1234; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; db8ca2b43ed851cc93e71fd5fd72bff7=9a32fc3ce04039d14660c4f4c4ac4aa2; XSRF-TOKEN=8ad306c3-4d47-4be0-8bc0-3b9abf8efbf4; f5avr1980069168aaaaaaaaaaaaaaaa_cspm_=CJIOMLELKNECBAJAKCJPJDIGADDOJPDLDGEGMIBNBIOBNJKDMFEHEACHPAGMDGDOHDOCIKOBJFDBFOEOONCAIECCAPAAPKLLOCFGODIBBHLPAFJIKPFEFGKFGACJHGAK; SESSION=1838a08b-9f92-4edf-b3fd-67162f028672; TS00000000076=0868f8be6fab2800687d07c48d7959bfaae4cbb6c4c4e37a4cdcdb848ba1d519be89546098983bdb6b7973db280576da086250011a09d0008860960bf622be4951a8fe159d4b78cc5943b27125027a9074dfce8e81b0b53f1f281731ee486fb0331984e73ed333971f702cd8ca4955c93db115816f4ef2d568a42b0c5922a180f5e0648a746f7c4f6f4b7fefb51aef3a8a73e498e0b08f1f0d647c1bd766819320da938b53cf5b13815b3d02b5804da4cac8bdfaf20dff958e586cfd1b6e1fd5cf264d090cae4ab54098f8bc8457fea60a6f3e587ce0fd0a0be2e03e74d531ade5d5c2585a8f5fb388d03ef74011bcf9b7e8e22388f055504e2d800e1f22ef7e3aa42aae7353b7ea; TSPD_101_DID=0868f8be6fab2800687d07c48d7959bfaae4cbb6c4c4e37a4cdcdb848ba1d519be89546098983bdb6b7973db280576da086250011a063800eacc834937df8d92ee609728481a3fd035e87be869ecbc0fc4a461dd921946243329d3443429a56cc369835a2454df88ac62184bb290f4a2; TS011f2d1a=01266d26d06b158d40f39281c58309dd9473115b38177cd0c7083781d30fd7e040027aa80367acdc64591c83dba5d03dfbab3a657c; TSPD_101=0868f8be6fab28007e1739b433797b5f717c88ea2c83999ccbb06e3f45c7f149177d23bd0663cfb121bf8b731f250427084b8bef4a0518008538e012fd03fa535ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=FPGKMEJJCGHGFKMBPKPEEAMDDHIMLAFHKBCPNIFIGCFLAKJCEALLBFHPGPBMLJCGGFMDFBABNJGBNCOJCFCANFLNCOPAHFBBLMNIFHPDFIILCLCMCNGLLMCBFAKNMKJI; TS5220f739077=0868f8be6fab280028352a7a896789c60afa1e85600a55669909b89bead0f743cff6ee02cfd948217939e959a8955c1b083594f6e61720005eda8dcd9b12d4bfbd4733dfce892c45468f51cd89b9b71cc40c7f63043325a4; TS5220f739029=0868f8be6fab2800f178b06a27e385ddab875846f0c9e83aa03fb08ba52f1c577ce4c098ddb62661eb5cdb3ab25398f5; TSf1edb2d2027=0868f8be6fab20009ef17a24eb7035f09a55ac5e4c36f230cc27761bb362683227a0353d15f73f390879030bed1130003bffae554efd20ae48dba6a53bba32ebc9c614988c888ebd85fbbe111732860a98cf568d8598fe6b0e8a1ffe1aaf4356',
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