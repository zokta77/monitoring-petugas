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
    'f5avraaaaaaaaaaaaaaaa_session_': 'GALOAKBIAHJADAJGIEFHLCGGCIJDLPCKFJCMBIKLLKNEPDNFDPMPLLCMKEDJGLEGKKMDKIFKFNOICNMLNBAAIEFKGMEOAMAIHOFKMKIPLGGHICEMFBHPKENKOFPANLLP',
    'f5avraaaaaaaaaaaaaaaa_session_': 'JCKPOFAACLNEOBKCBGBJJBNMFLNKIBMMDAGPLHNHFDKAKNBHCFJGGKEHOJFPDKMDCJEDGCEJKELFDCDLEPCAEFHIALMGHGIDGIONLJBJLMMGLEMGBFPDPDKMMNJEMKGN',
    'XSRF-TOKEN': '72456d4d-2ea5-4e9b-8bc4-b5451fecffdd',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'f9fc17aeaba01609e8011436627c1a78',
    'JSESSIONID': '4FB79866DC32E1568CB3D5794D2DAD45',
    'SESSION': 'd65f777e-22e5-4d18-8a77-37a871ac23fd',
    'TS018af012': '0167a1c8613e6c3a0317de952e7cfb2a242dc84e3dd679922d6a3d97f898b508301c7c8ab10ced4afbbea19997644af402d1febd26ae46832afae3d5a16c875c2c376014c7b665d1e2b4e7ea249c7c89a1d0aa669d8baf2687698f2d82667f1faee65b1bf3',
    'TS011f2d1a': '01266d26d03c181632fe457eb3e57ea0cce39ff0f03c8febafe726cfebfc8f2c38b3b1f5d3d78abac77c700c7122440f8b4b4564f1',
    'TS5220f739078': '0868f8be6fab2000e3357ca3c56113be89b3c275d119fc89c32e87657de7fef9e390a9a7090546a9080e1a59a818780110c7e0be1ee7898bb88257a58d981023a0bd243574d72034a820e2e853d54195dd65dbce0be7e33ee576cd4c2895c47c1655e4d31a7c833e2cb60306058906a9655313bee3e27f5c230d63ffc835d1547227a89bfe1c769eb79a27487a904abd39dbacdbb91853c502752ae3e0b228ab6daa78339d93166b6af311f8b5893426aaba6501e43696c563838c0c64767502c3041c96c27cd925c0613a86adb4bbc6137aaa04b0a823fa9fd76fde39acf5ec71c95c0872e50c8d697d060d22be4a65ea6083fd454a6483bef29ea386f9335e593ae45817d6f47b6031723894b60f72a7702607c2d1a5363d0d4232da04d6ad78ba0dbc8f3014f343ee201711c9d01efd807421f55450c3cd59f79fde9345625e1859ad89141633768f38b8c18343d8b0a7c0035e858831949c5660b68cabdaa144c09d8595eef20f2621b612d7ca4fe10169c9149138b25a4b138588a1b569957c47c4bc107ee6a7d2fe024067b217dc3e16be7693cfcfbcd970578a91e1fedde839f7e65a46bd',
    'TS00000000076': '0868f8be6fab28009a1931c13476578f61bfa19f4964680bc0bab17d165ec79b5d0325daa6d7222ff1180ba1ad9bcffd085410673d09d000775af4daa568f11e0f354c764602e63e10dbc9a39c7228955d0b510c8bd815097a901df03117e8a6e38b12a0bc383efbc630c278e39b461f51852acdac74897c3ae421e35a97c6ed7825f85ba0ee011d45b1d71fedbb2c54fe56ebc66ef2af700f24ab3af11bbb87635255451b43171224b64933b1f5454a1dede75c6b45330d46d32b9debc0b80f8c05dfb7b9ac3ca5ad837e0fad508621ef1070b5a483afa3d186947867839e210a45118d95f02db83d39b0a30f0ee9bdb49d050b74e83434a33d51adb55800532fa934b1528a8727',
    'TSPD_101_DID': '0868f8be6fab28009a1931c13476578f61bfa19f4964680bc0bab17d165ec79b5d0325daa6d7222ff1180ba1ad9bcffd085410673d06380037c6528df05c80447cd7d1cdb7eead37070c9cb4080a9032f3cdd0548ddc7ad5afddb11bb463c2dc12f7004ca19917d8bbed303d1e8b1674',
    'TSPD_101': '0868f8be6fab28005d459b19ef52c7ba019872d2a3111928e763719b9d9c8ce5ee2d552699694617346765517248473f085438b8d30518004053c4934f8db14e5ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800827155ab89a4947a6ac3db6463825f0f3771ab5ee76799e7f9bd7f9c46553517cdf85334df06f28308d934adb817200006e27cbfd315e633c15fd91b4545528735c64c18b45a8279af5c1a675934e320',
    'TS5220f739029': '0868f8be6fab2800a8e4e129dc7a9bb32f2a25bf341f43cb93766406f9d572533544da8b36639c1edb1387b7db5f7da8',
    'TSf1edb2d2027': '0868f8be6fab20001a1bba1be2f64e5014364964241fbda0b2f1df89e85a3bd3a961631495a9cd59085ed00df91130008aeeb7613025c0a4671f64f0f1b12d666cf7d16744b46c40ad59456766e25151d424001904fc15c4753f4752167fd771',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'referer': 'https://fasih-sm.bps.go.id/app/surveys/a0429e96-51a5-477b-a415-485f9c153004/fd68e454-ba45-4b85-8205-f3bf777ded24',
    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': '72456d4d-2ea5-4e9b-8bc4-b5451fecffdd',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=GALOAKBIAHJADAJGIEFHLCGGCIJDLPCKFJCMBIKLLKNEPDNFDPMPLLCMKEDJGLEGKKMDKIFKFNOICNMLNBAAIEFKGMEOAMAIHOFKMKIPLGGHICEMFBHPKENKOFPANLLP; f5avraaaaaaaaaaaaaaaa_session_=JCKPOFAACLNEOBKCBGBJJBNMFLNKIBMMDAGPLHNHFDKAKNBHCFJGGKEHOJFPDKMDCJEDGCEJKELFDCDLEPCAEFHIALMGHGIDGIONLJBJLMMGLEMGBFPDPDKMMNJEMKGN; XSRF-TOKEN=72456d4d-2ea5-4e9b-8bc4-b5451fecffdd; db8ca2b43ed851cc93e71fd5fd72bff7=f9fc17aeaba01609e8011436627c1a78; JSESSIONID=4FB79866DC32E1568CB3D5794D2DAD45; SESSION=d65f777e-22e5-4d18-8a77-37a871ac23fd; TS018af012=0167a1c8613e6c3a0317de952e7cfb2a242dc84e3dd679922d6a3d97f898b508301c7c8ab10ced4afbbea19997644af402d1febd26ae46832afae3d5a16c875c2c376014c7b665d1e2b4e7ea249c7c89a1d0aa669d8baf2687698f2d82667f1faee65b1bf3; TS011f2d1a=01266d26d03c181632fe457eb3e57ea0cce39ff0f03c8febafe726cfebfc8f2c38b3b1f5d3d78abac77c700c7122440f8b4b4564f1; TS5220f739078=0868f8be6fab2000e3357ca3c56113be89b3c275d119fc89c32e87657de7fef9e390a9a7090546a9080e1a59a818780110c7e0be1ee7898bb88257a58d981023a0bd243574d72034a820e2e853d54195dd65dbce0be7e33ee576cd4c2895c47c1655e4d31a7c833e2cb60306058906a9655313bee3e27f5c230d63ffc835d1547227a89bfe1c769eb79a27487a904abd39dbacdbb91853c502752ae3e0b228ab6daa78339d93166b6af311f8b5893426aaba6501e43696c563838c0c64767502c3041c96c27cd925c0613a86adb4bbc6137aaa04b0a823fa9fd76fde39acf5ec71c95c0872e50c8d697d060d22be4a65ea6083fd454a6483bef29ea386f9335e593ae45817d6f47b6031723894b60f72a7702607c2d1a5363d0d4232da04d6ad78ba0dbc8f3014f343ee201711c9d01efd807421f55450c3cd59f79fde9345625e1859ad89141633768f38b8c18343d8b0a7c0035e858831949c5660b68cabdaa144c09d8595eef20f2621b612d7ca4fe10169c9149138b25a4b138588a1b569957c47c4bc107ee6a7d2fe024067b217dc3e16be7693cfcfbcd970578a91e1fedde839f7e65a46bd; TS00000000076=0868f8be6fab28009a1931c13476578f61bfa19f4964680bc0bab17d165ec79b5d0325daa6d7222ff1180ba1ad9bcffd085410673d09d000775af4daa568f11e0f354c764602e63e10dbc9a39c7228955d0b510c8bd815097a901df03117e8a6e38b12a0bc383efbc630c278e39b461f51852acdac74897c3ae421e35a97c6ed7825f85ba0ee011d45b1d71fedbb2c54fe56ebc66ef2af700f24ab3af11bbb87635255451b43171224b64933b1f5454a1dede75c6b45330d46d32b9debc0b80f8c05dfb7b9ac3ca5ad837e0fad508621ef1070b5a483afa3d186947867839e210a45118d95f02db83d39b0a30f0ee9bdb49d050b74e83434a33d51adb55800532fa934b1528a8727; TSPD_101_DID=0868f8be6fab28009a1931c13476578f61bfa19f4964680bc0bab17d165ec79b5d0325daa6d7222ff1180ba1ad9bcffd085410673d06380037c6528df05c80447cd7d1cdb7eead37070c9cb4080a9032f3cdd0548ddc7ad5afddb11bb463c2dc12f7004ca19917d8bbed303d1e8b1674; TSPD_101=0868f8be6fab28005d459b19ef52c7ba019872d2a3111928e763719b9d9c8ce5ee2d552699694617346765517248473f085438b8d30518004053c4934f8db14e5ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800827155ab89a4947a6ac3db6463825f0f3771ab5ee76799e7f9bd7f9c46553517cdf85334df06f28308d934adb817200006e27cbfd315e633c15fd91b4545528735c64c18b45a8279af5c1a675934e320; TS5220f739029=0868f8be6fab2800a8e4e129dc7a9bb32f2a25bf341f43cb93766406f9d572533544da8b36639c1edb1387b7db5f7da8; TSf1edb2d2027=0868f8be6fab20001a1bba1be2f64e5014364964241fbda0b2f1df89e85a3bd3a961631495a9cd59085ed00df91130008aeeb7613025c0a4671f64f0f1b12d666cf7d16744b46c40ad59456766e25151d424001904fc15c4753f4752167fd771',
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