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

# ===== PENGATURAN REQUEST SERVER =====
# Ukuran halaman lebih besar mengurangi jumlah request total.
# Jika server menolak ukuran 20, turunkan menjadi 10.
PAGE_SIZE = 10

# Jeda normal antarpages.
PAGE_DELAY_MIN = 5.0
PAGE_DELAY_MAX = 8.0

# Istirahat tambahan secara berkala agar request tidak terus-menerus.
COOLDOWN_EVERY_PAGES = 15
COOLDOWN_MIN_SECONDS = 20
COOLDOWN_MAX_SECONDS = 30

# Penanganan 429. Jika server memberi Retry-After, nilai server diprioritaskan.
MAX_REQUEST_RETRIES = 5
DEFAULT_429_WAIT_SECONDS = 60
MAX_429_WAIT_SECONDS = 15 * 60

# Timeout koneksi dan pembacaan respons.
REQUEST_TIMEOUT = (20, 120)

# ===== KONFIGURASI SELENIUM =====
# Cara cek path: buka chrome://version di profil yang sudah login FASIH
# lihat baris "Profile Path" → folder induknya = CHROME_PROFILE_DIR
CHROME_PROFILE_DIR  = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Profil 1"   # ganti sesuai profil (Default / Profile 1 / dst)
FASIH_HOME_URL      = "https://fasih-sm.bps.go.id/app/"

# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'XSRF-TOKEN': '24edea92-7716-4849-9495-dde155cc7f14',
    'JSESSIONID': '7569813F6CDC982EF6ED07A356DA8975',
    'TS5220f739078': '0868f8be6fab20000453e2d2c5c37f3ea103d59e39c28e69a3d4cddca67fc349571bf51c58c6907d08c665df5b18380169ce068f5e46d1947680be95e867d78e9b5be480bf14b0e2f7c6fcfd3306bf7b631dbc123d87c7a1d7d00169ab0238ca7ee9c39fe74aba20b942dcfd89e3ee0310fbdc6f55d8c73c8178e037c606a0af0a3b6f41491431883f2c8ebf5fb1bb1b78ae543d9541b1a028f5fdb3ab82298feddf79e5cb5962b8353b9ae7b75a32bc39b271e5739bf714e8a5b6ab66e39b504d065f15699441c3a69b294a86a39c456edd93f3c5dc1632fe5c424c8df19afee0a017e8b7abf81e72e65bf73a420b968a9093b135737e6e180642451f05bf5cdec6a6df3c49383e5220310a9189fc33d3c5b2ac43f5a241a070f32b12e0937ced5a50dcd919b81074f2a67568ba40c829fdb626d2b9457060f4c1c6186d5a04950f3fc71758adbf187b6f77c76fa4d299dceb71618ee3f3bf3d51c9271daea88ea088b3d85835d1',
    'TS00000000076': '0868f8be6fab280086cf23681cc9b9388bb51100691f08ff3cb14bb2c919b348e28ef35bd4142d5e975dca6a128969cd08bd57900709d000b5fe6c15b3bbcb8d79009ba83079f84348034875cef69eb691a2f10eb6f4720bfb253206498f76a658da1ee42d4f05db0f7ca1daa0a57de9446e31b74e17ad13b75a95be7e7821e0a18a7dae607f647ae9ca62cd4891fd73b538df818d02bc69d516a3cc01756359088b8c1ac65f160211c32ea67848b51d084d7ac612ca6d581a96794b7654690a18a43fb75bc2f02654482e6e623f8e6f97ee96c1bdcdf69e08d69f659cf752fb9f3cf053c99e2fd734b63934691972fee1f84e22d1ca0d501760274d62d52a073c2b27bffb29d7d2',
    'TSPD_101_DID': '0868f8be6fab280086cf23681cc9b9388bb51100691f08ff3cb14bb2c919b348e28ef35bd4142d5e975dca6a128969cd08bd579007063800a3c839d13dea11af7c6db72024333f4f6c6452167697b7acd1ad0492385481755bd92c8eb5b59482bab6e87565fdb22c80d3d94d1dc1ac0f',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '138ec005feeb4d65933b176c6116e1a7',
    'TS011f2d1a': '01266d26d0bc86914b70a28884cc6b686e408ad39ae2183064d507a7d7551a4f18f0ae7a3d72bf40461b3064aa4233fdac962c1682',
    'TSPD_101': '0868f8be6fab28008a912a6d178a675c6ecb5353289fc6a677387bd83a61213da9fa40c5a80487e143798693aad5600408d3b5c428051800fd19f6004aa4cce65ca1732140a3428bba23ce13beb1c95e',
    'SESSION': 'e7c9c89a-2273-4198-81f4-18303602260e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'EMFOGGALFOOMJKNCONGOJEKDOEENMNFFCIHBAKHJJKCOHBDHAGCGGEDFBKJJCNMHHOMDLCHAFNBDMFHIPHDAJJCIMCMMGJGDCDDCNLMGFOEMAHMECCLIGONIJGCLEOGC',
    'TS5220f739077': '0868f8be6fab28008dc2a3087aee7f18b0f893ab78a5c19963fc27bf72d6add882b1432e9438eea462251c724a4d7da00832706cd81720002dd0232b0db49293a3fa2327247b01f0dfe678f195f2b7220e31d235439f4d96',
    'TS5220f739029': '0868f8be6fab28000067a4af0891256ffdc6d212d777214ab88f07e8aadae40a561f1c077c4ee956d99b125e04f6ca0e',
    'TSf1edb2d2027': '0868f8be6fab2000a6c27182bbfa3c3e3199a82b3e20815bcc797d2bc853b2e1db59cecfd22e88520806ab41271130009aa17ec173246a923d50d9c71915709a3c4d8e7ee2eac0744fbf83a9230b96214516c92160ea9307fa4507c2cfe3da88',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'referer': 'https://fasih-sm.bps.go.id/app/surveys/a0429e96-51a5-477b-a415-485f9c153004/fd68e454-ba45-4b85-8205-f3bf777ded24',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': '24edea92-7716-4849-9495-dde155cc7f14',
    'cookie': 'XSRF-TOKEN=24edea92-7716-4849-9495-dde155cc7f14; JSESSIONID=7569813F6CDC982EF6ED07A356DA8975; TS5220f739078=0868f8be6fab20000453e2d2c5c37f3ea103d59e39c28e69a3d4cddca67fc349571bf51c58c6907d08c665df5b18380169ce068f5e46d1947680be95e867d78e9b5be480bf14b0e2f7c6fcfd3306bf7b631dbc123d87c7a1d7d00169ab0238ca7ee9c39fe74aba20b942dcfd89e3ee0310fbdc6f55d8c73c8178e037c606a0af0a3b6f41491431883f2c8ebf5fb1bb1b78ae543d9541b1a028f5fdb3ab82298feddf79e5cb5962b8353b9ae7b75a32bc39b271e5739bf714e8a5b6ab66e39b504d065f15699441c3a69b294a86a39c456edd93f3c5dc1632fe5c424c8df19afee0a017e8b7abf81e72e65bf73a420b968a9093b135737e6e180642451f05bf5cdec6a6df3c49383e5220310a9189fc33d3c5b2ac43f5a241a070f32b12e0937ced5a50dcd919b81074f2a67568ba40c829fdb626d2b9457060f4c1c6186d5a04950f3fc71758adbf187b6f77c76fa4d299dceb71618ee3f3bf3d51c9271daea88ea088b3d85835d1; TS00000000076=0868f8be6fab280086cf23681cc9b9388bb51100691f08ff3cb14bb2c919b348e28ef35bd4142d5e975dca6a128969cd08bd57900709d000b5fe6c15b3bbcb8d79009ba83079f84348034875cef69eb691a2f10eb6f4720bfb253206498f76a658da1ee42d4f05db0f7ca1daa0a57de9446e31b74e17ad13b75a95be7e7821e0a18a7dae607f647ae9ca62cd4891fd73b538df818d02bc69d516a3cc01756359088b8c1ac65f160211c32ea67848b51d084d7ac612ca6d581a96794b7654690a18a43fb75bc2f02654482e6e623f8e6f97ee96c1bdcdf69e08d69f659cf752fb9f3cf053c99e2fd734b63934691972fee1f84e22d1ca0d501760274d62d52a073c2b27bffb29d7d2; TSPD_101_DID=0868f8be6fab280086cf23681cc9b9388bb51100691f08ff3cb14bb2c919b348e28ef35bd4142d5e975dca6a128969cd08bd579007063800a3c839d13dea11af7c6db72024333f4f6c6452167697b7acd1ad0492385481755bd92c8eb5b59482bab6e87565fdb22c80d3d94d1dc1ac0f; db8ca2b43ed851cc93e71fd5fd72bff7=138ec005feeb4d65933b176c6116e1a7; TS011f2d1a=01266d26d0bc86914b70a28884cc6b686e408ad39ae2183064d507a7d7551a4f18f0ae7a3d72bf40461b3064aa4233fdac962c1682; TSPD_101=0868f8be6fab28008a912a6d178a675c6ecb5353289fc6a677387bd83a61213da9fa40c5a80487e143798693aad5600408d3b5c428051800fd19f6004aa4cce65ca1732140a3428bba23ce13beb1c95e; SESSION=e7c9c89a-2273-4198-81f4-18303602260e; f5avraaaaaaaaaaaaaaaa_session_=EMFOGGALFOOMJKNCONGOJEKDOEENMNFFCIHBAKHJJKCOHBDHAGCGGEDFBKJJCNMHHOMDLCHAFNBDMFHIPHDAJJCIMCMMGJGDCDDCNLMGFOEMAHMECCLIGONIJGCLEOGC; TS5220f739077=0868f8be6fab28008dc2a3087aee7f18b0f893ab78a5c19963fc27bf72d6add882b1432e9438eea462251c724a4d7da00832706cd81720002dd0232b0db49293a3fa2327247b01f0dfe678f195f2b7220e31d235439f4d96; TS5220f739029=0868f8be6fab28000067a4af0891256ffdc6d212d777214ab88f07e8aadae40a561f1c077c4ee956d99b125e04f6ca0e; TSf1edb2d2027=0868f8be6fab2000a6c27182bbfa3c3e3199a82b3e20815bcc797d2bc853b2e1db59cecfd22e88520806ab41271130009aa17ec173246a923d50d9c71915709a3c4d8e7ee2eac0744fbf83a9230b96214516c92160ea9307fa4507c2cfe3da88',
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
# ================================================================
if not os.path.exists(base_path):
    os.makedirs(base_path)


def _atomic_write_excel(df, path):
    """Tulis Excel secara atomik agar file tidak terbaca setengah jadi."""
    folder = os.path.dirname(path) or "."
    os.makedirs(folder, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(suffix=".xlsx", dir=folder)
    os.close(fd)
    try:
        df.to_excel(tmp_path, index=False)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def save_and_merge(new_data):
    """
    Simpan satu snapshot yang sudah selesai.

    - Tepat satu baris dipertahankan untuk setiap userId + regionCode.
    - Satu proses scraping sukses menghasilkan satu file history baru.
    - File history tidak di-append dengan snapshot sebelumnya.
    - LATEST selalu ditimpa snapshot sukses terbaru.
    """
    if not new_data:
        return False

    df_new = pd.DataFrame(new_data)

    required_keys = ["userId", "regionCode"]
    missing_keys = [c for c in required_keys if c not in df_new.columns]
    if missing_keys:
        raise ValueError(f"Kolom kunci tidak ditemukan: {missing_keys}")

    before_dedupe = len(df_new)
    df_new["userId"] = df_new["userId"].astype(str).str.strip()
    df_new["regionCode"] = df_new["regionCode"].astype(str).str.strip()

    # Bukan menghapus semua key yang kembar: tetap simpan tepat satu baris,
    # dan pertahankan kemunculan terakhir sebagai nilai terbaru.
    df_new = df_new.drop_duplicates(
        subset=["userId", "regionCode"],
        keep="last",
    ).reset_index(drop=True)

    duplicate_extra = before_dedupe - len(df_new)
    if duplicate_extra:
        print(
            f"🧹 Ditemukan {duplicate_extra:,} kemunculan tambahan untuk "
            "userId + regionCode. Tepat satu baris per key tetap disimpan."
        )

    scraped_at = datetime.now()
    df_new["scraped_at"] = scraped_at.strftime("%Y-%m-%d %H:%M:%S")

    master = pd.read_excel("data/master_data.xlsx")
    master["pencacah"] = master["pencacah"].astype(str).str.strip().str.lower()
    master["regionCode"] = master["regionCode"].astype(str).str.strip()

    # Cegah merge master menggandakan hasil scraping.
    master_before = len(master)
    master = master.drop_duplicates(
        subset=["pencacah", "regionCode"],
        keep="last",
    ).copy()
    master_dup = master_before - len(master)
    if master_dup:
        print(
            f"⚠️  Master data memiliki {master_dup:,} baris key pencacah + "
            "regionCode yang berulang. Hanya satu baris per key dipakai saat merge."
        )

    df_new["email"] = df_new["email"].astype(str).str.strip().str.lower()

    master_cols = [
        "regionCode", "nmkab", "nmkec", "nmdesa", "nmsls", "nmsubsls",
        "pengawas", "pencacah", "nama_pcl", "nama_pml",
        "jumlah_prelist_awal",
    ]
    missing_master = [c for c in master_cols if c not in master.columns]
    if missing_master:
        raise ValueError(f"Kolom master_data.xlsx belum lengkap: {missing_master}")

    rows_before_merge = len(df_new)
    df_new = df_new.merge(
        master[master_cols],
        left_on=["email", "regionCode"],
        right_on=["pencacah", "regionCode"],
        how="left",
        validate="many_to_one",
    )
    if len(df_new) != rows_before_merge:
        raise RuntimeError(
            "Jumlah baris berubah setelah merge master. Snapshot dibatalkan untuk "
            "mencegah data ganda."
        )

    timestamp = scraped_at.strftime("%Y%m%d_%H%M%S")
    backup_file = archive_filename(timestamp)

    _atomic_write_excel(df_new, backup_file)
    _atomic_write_excel(df_new, LATEST_FILE)

    print(f"🗂️  History tersimpan: {backup_file}")
    print(f"💾 Snapshot terbaru tersimpan: {LATEST_FILE}")
    print(f"✅ Jumlah baris unik: {len(df_new):,}")
    return True


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
 
 
def _retry_after_seconds(response, fallback_seconds):
    """Ambil waktu tunggu dari header Retry-After jika tersedia."""
    raw = response.headers.get("Retry-After")
    if raw:
        try:
            return max(float(raw), 1.0)
        except (TypeError, ValueError):
            pass
    return fallback_seconds


def request_with_backoff(
    session,
    method,
    url,
    max_retries=MAX_REQUEST_RETRIES,
    **kwargs,
):

    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    network_delay = 10.0
    response = None

    for attempt in range(1, max_retries + 1):
        try:
            response = session.request(method, url, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Network error (percobaan {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise

            wait_seconds = min(
                network_delay + random.uniform(1, 5),
                MAX_429_WAIT_SECONDS,
            )
            print(f"⏳ Menunggu {wait_seconds:.0f} detik sebelum mencoba lagi...")
            time.sleep(wait_seconds)
            network_delay *= 2
            continue

        if response.status_code == 200:
            return response

        if response.status_code == 429:
            fallback = min(
                DEFAULT_429_WAIT_SECONDS * (2 ** (attempt - 1)),
                MAX_429_WAIT_SECONDS,
            )
            wait_seconds = _retry_after_seconds(response, fallback)
            wait_seconds = min(
                wait_seconds + random.uniform(5, 15),
                MAX_429_WAIT_SECONDS,
            )

            print(
                f"⚠️  Status 429 (percobaan {attempt}/{max_retries}). "
                f"Server meminta request diperlambat; tunggu {wait_seconds:.0f} detik."
            )

            if attempt == max_retries:
                raise RuntimeError(
                    "Rate limit 429 masih aktif setelah seluruh percobaan. "
                    "Snapshot tidak disimpan. Jalankan kembali setelah masa cooldown."
                )

            time.sleep(wait_seconds)
            continue

        # Jangan menghantam ulang 401/403. Serahkan ke fetch_data untuk refresh session.
        if response.status_code in (302, 401, 403):
            return response

        # Gangguan server sementara.
        if 500 <= response.status_code < 600 and attempt < max_retries:
            wait_seconds = min(
                15 * (2 ** (attempt - 1)) + random.uniform(1, 5),
                180,
            )
            print(
                f"⚠️  Status {response.status_code}. "
                f"Menunggu {wait_seconds:.0f} detik sebelum retry..."
            )
            time.sleep(wait_seconds)
            continue

        return response

    return response


def fetch_data():
    # Dictionary memastikan satu userId + regionCode hanya memiliki satu baris.
    rows_by_key = {}
    page = 0
    session = requests.Session()
    max_refresh = 2
    refresh_count = 0
    reached_last_page = False

    while True:
        payload = dict(json_data)
        payload["page"] = page
        payload["size"] = PAGE_SIZE

        try:
            response = request_with_backoff(
                session,
                "POST",
                URL_DATA,
                cookies=cookies,
                headers=headers,
                json=payload,
            )
        except (RuntimeError, requests.exceptions.RequestException) as e:
            print(f"🛑 Berhenti scraping: {e}")
            return False

        session_expired = (
            (response.status_code == 200 and is_session_expired(response))
            or response.status_code in (302, 401, 403)
        )
        if session_expired:
            if refresh_count >= max_refresh:
                print(
                    f"🛑 Session expired lagi setelah {max_refresh}x refresh. "
                    "Kemungkinan profil Chrome perlu login manual ulang."
                )
                return False

            try:
                refresh_cookies()
                refresh_count += 1
                session.close()
                session = requests.Session()
                wait_seconds = random.uniform(10, 20)
                print(
                    f"↩️  Mengulang page {page} dengan cookies baru setelah "
                    f"jeda {wait_seconds:.0f} detik..."
                )
                time.sleep(wait_seconds)
                continue
            except Exception as e:
                print(f"🛑 Gagal refresh cookies: {e}")
                return False

        if response.status_code != 200:
            print(f"❌ Error di page {page} | Status: {response.status_code}")
            print(response.text[:500])
            return False

        try:
            json_res = response.json()
        except Exception:
            print(f"❌ Response bukan JSON di page {page}.")
            return False

        data_block = json_res.get("data", {})
        data = data_block.get("content", [])
        is_last = bool(data_block.get("last", True))

        print(
            f"📄 Page {page} | user: {len(data)} | "
            f"key unik sementara: {len(rows_by_key):,} | last: {is_last}"
        )

        duplicate_on_page = 0
        for user in data:
            user_id = str(user.get("userId") or "").strip()
            for region in user.get("regionSummary", []):
                region_code = str(region.get("regionCode") or "").strip()
                key = (user_id, region_code)

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

                if key in rows_by_key:
                    duplicate_on_page += 1

                # Tetap simpan satu baris; kemunculan terakhir mengganti yang sebelumnya.
                rows_by_key[key] = row

        if duplicate_on_page:
            print(
                f"🧹 Page {page}: {duplicate_on_page:,} kemunculan tambahan "
                "userId + regionCode ditemukan; satu baris per key tetap disimpan."
            )

        if is_last:
            reached_last_page = True
            print("✅ Sudah sampai halaman terakhir.")
            break

        page += 1

        # Jeda normal antarpages.
        delay = random.uniform(PAGE_DELAY_MIN, PAGE_DELAY_MAX)
        print(f"⏳ Jeda {delay:.1f} detik sebelum page {page}...")
        time.sleep(delay)

        # Istirahat berkala untuk menurunkan burst request panjang.
        if page > 0 and page % COOLDOWN_EVERY_PAGES == 0:
            cooldown = random.uniform(
                COOLDOWN_MIN_SECONDS,
                COOLDOWN_MAX_SECONDS,
            )
            print(
                f"🧊 Cooldown setelah {page} page: "
                f"menunggu {cooldown:.0f} detik..."
            )
            time.sleep(cooldown)

    if not reached_last_page:
        print("🛑 Halaman terakhir belum tercapai. Snapshot parsial tidak disimpan.")
        return False

    if not rows_by_key:
        print("⚠️  Tidak ada data yang diperoleh.")
        return False

    try:
        return save_and_merge(list(rows_by_key.values()))
    except Exception as e:
        print(f"🛑 Gagal menyimpan snapshot: {e}")
        return False


def job():
    print(
        f"\n[+] Memulai proses scraping pada "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    success = fetch_data()
    if success:
        print("🎉 Scraping lengkap berhasil disimpan.")
        auto_push_github()
    else:
        print("⏭️ Push GitHub dilewati karena scraping tidak berhasil lengkap.")


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