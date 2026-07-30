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

# ===== PENGATURAN REQUEST YANG RAMAH SERVER =====
# Ukuran halaman lebih besar mengurangi jumlah request total.
# Jika server menolak ukuran 20, turunkan menjadi 10.
PAGE_SIZE = 10

# Jeda normal antarpages. Jangan dibuat terlalu kecil.
PAGE_DELAY_MIN = 5.0
PAGE_DELAY_MAX = 8.0

# Istirahat tambahan secara berkala agar request tidak terus-menerus.
COOLDOWN_EVERY_PAGES = 15
COOLDOWN_MIN_SECONDS = 45
COOLDOWN_MAX_SECONDS = 75

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
    'f5avraaaaaaaaaaaaaaaa_session_': 'CLECFKODDBOAMLBDMMPIJJKMGBFGMKLAAKIMOMFMDPDGIALKJJAJPHNFJMLFBEPFELKDEIMMDKJNBAONDAAAKFNNDDKPBKFNOFKCBCFDJBIBEEJJNDMBNNCMAENJNAKC',
    'cf_clearance': 'eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg',
    'XSRF-TOKEN': '54012588-9cc7-41b6-91fd-cc551293aa35',
    'TS018af012': '0167a1c8619ac5534d42f78c2d37660a69bda420d55ec6e7af18b175045b1f6836c2e5c1ae7df470ccaf8a517508b7575aae66b52012d0e6aca3b14a6e0333e06eaffde041f300e8aadc176005508d5a742d7d8649',
    'TS0151fc2b': '0167a1c861cb0a46e61076c914e6a0273ba95ed1b101f85af74662792f4ad34fdfefba479c5b672b35a30380356477d59073e3d537',
    'JSESSIONID': '44F1FBC4480409676311AABD4F0EC9A7',
    'TS00000000076': '0868f8be6fab2800c1bf8311bbe80d930fd27196ae877510725647d6eab04ad98dced47b6e6029f72ec28a6b0fa3e737089dfd02f309d000c28526a4715540c9969c409aaba01aa7c3cccc5d2f0b49306d3983260ecc61d5878544ff3c6f0319e5a62e045ab13032d1bc2a5661278c8e5a2999b1fd94cf054829dd2ecc86d9cdbbba0fcdcee736f2c7b6dad58a4784fc8ca0d6d71060372d3d6e4d7dc98df66e5c85e9ff5d3810e9e2f76df5981e65fc565839e5c2194bc8eb6c47cf195c34389894d5508fc7314f6a7383479d2be0e980be1ba14d58ed6e1788f57cee2a16cf4a938286a20b751eca29f4db8b664061bf77b403cd092da38537cbaf6048425ab9285b9d8b3a1688',
    'TSPD_101_DID': '0868f8be6fab2800c1bf8311bbe80d930fd27196ae877510725647d6eab04ad98dced47b6e6029f72ec28a6b0fa3e737089dfd02f30638002b24cb372049f33e84eb0cfe8eb309639d62590b3bce0e40c6c59e46d2282ab2b7b62087b38e452c6781feaaf3eda0620b9ee9fa925ca093',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '28ef3e24cd5e67a902b6836328610c60',
    'TS011f2d1a': '01266d26d04e49b8fa13a339268d4d68bbe458c80e488258d657d225f80e0f89cc2eb078527a6c10bffa1945983426529f5c3900f6',
    'TSPD_101': '0868f8be6fab2800a02721a522f1aad3c2151160bb9c79a2c5ce3cb5c332d2f36baae27c963e82b2b4875761e5e8624508a753635d051800cc712a6efd8e035f5ca1732140a3428bba23ce13beb1c95e',
    'SESSION': 'b06e5b48-0ca5-4e7d-91b6-640d224ceaa5',
    'f5avraaaaaaaaaaaaaaaa_session_': 'LHPBMBIMEJGCMIBHNJGABHFEEJMHEAMLIPBBJHJAAAGNPJJCGLGIPBKPOEMPEEJICMADBMALOKNNHHAGPOEAMPLOBDJJIJLKBNBCHEIBFLHFGIAGEJJHMKMAFNCDBJKL',
    'TS5220f739077': '0868f8be6fab28002a7479dd711d3277abbfda4ff72aabf938fb956a72f928803b8d6a613c3c8af0b927fa28bd5281d908de8ab7c3172000701a3931dc113cdee835b30a9697419109ed88e4bf8bb5dace761af85c005c66',
    'TS5220f739029': '0868f8be6fab2800b2aec8acf51ae79072b52f7fce0bd1f2319608dcc5177438b08cea2f9113c6822e160f5273462335',
    'TSf1edb2d2027': '0868f8be6fab2000dd8055319e4e708e87c7abe157d7f5b262b72b14e103cb8a997ff40ee3e2114c082b9d1ce8113000103fb1026cb3d2d6a8b0509ec24733860a59b868e55f34db7bb939139c057d78cd1e8c37458c1cc74fa56f4d6f392f64',
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
    'x-xsrf-token': '54012588-9cc7-41b6-91fd-cc551293aa35',
     'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=CLECFKODDBOAMLBDMMPIJJKMGBFGMKLAAKIMOMFMDPDGIALKJJAJPHNFJMLFBEPFELKDEIMMDKJNBAONDAAAKFNNDDKPBKFNOFKCBCFDJBIBEEJJNDMBNNCMAENJNAKC; cf_clearance=eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg; XSRF-TOKEN=54012588-9cc7-41b6-91fd-cc551293aa35; TS018af012=0167a1c8619ac5534d42f78c2d37660a69bda420d55ec6e7af18b175045b1f6836c2e5c1ae7df470ccaf8a517508b7575aae66b52012d0e6aca3b14a6e0333e06eaffde041f300e8aadc176005508d5a742d7d8649; TS0151fc2b=0167a1c861cb0a46e61076c914e6a0273ba95ed1b101f85af74662792f4ad34fdfefba479c5b672b35a30380356477d59073e3d537; JSESSIONID=44F1FBC4480409676311AABD4F0EC9A7; TS00000000076=0868f8be6fab2800c1bf8311bbe80d930fd27196ae877510725647d6eab04ad98dced47b6e6029f72ec28a6b0fa3e737089dfd02f309d000c28526a4715540c9969c409aaba01aa7c3cccc5d2f0b49306d3983260ecc61d5878544ff3c6f0319e5a62e045ab13032d1bc2a5661278c8e5a2999b1fd94cf054829dd2ecc86d9cdbbba0fcdcee736f2c7b6dad58a4784fc8ca0d6d71060372d3d6e4d7dc98df66e5c85e9ff5d3810e9e2f76df5981e65fc565839e5c2194bc8eb6c47cf195c34389894d5508fc7314f6a7383479d2be0e980be1ba14d58ed6e1788f57cee2a16cf4a938286a20b751eca29f4db8b664061bf77b403cd092da38537cbaf6048425ab9285b9d8b3a1688; TSPD_101_DID=0868f8be6fab2800c1bf8311bbe80d930fd27196ae877510725647d6eab04ad98dced47b6e6029f72ec28a6b0fa3e737089dfd02f30638002b24cb372049f33e84eb0cfe8eb309639d62590b3bce0e40c6c59e46d2282ab2b7b62087b38e452c6781feaaf3eda0620b9ee9fa925ca093; db8ca2b43ed851cc93e71fd5fd72bff7=28ef3e24cd5e67a902b6836328610c60; TS011f2d1a=01266d26d04e49b8fa13a339268d4d68bbe458c80e488258d657d225f80e0f89cc2eb078527a6c10bffa1945983426529f5c3900f6; TSPD_101=0868f8be6fab2800a02721a522f1aad3c2151160bb9c79a2c5ce3cb5c332d2f36baae27c963e82b2b4875761e5e8624508a753635d051800cc712a6efd8e035f5ca1732140a3428bba23ce13beb1c95e; SESSION=b06e5b48-0ca5-4e7d-91b6-640d224ceaa5; f5avraaaaaaaaaaaaaaaa_session_=LHPBMBIMEJGCMIBHNJGABHFEEJMHEAMLIPBBJHJAAAGNPJJCGLGIPBKPOEMPEEJICMADBMALOKNNHHAGPOEAMPLOBDJJIJLKBNBCHEIBFLHFGIAGEJJHMKMAFNCDBJKL; TS5220f739077=0868f8be6fab28002a7479dd711d3277abbfda4ff72aabf938fb956a72f928803b8d6a613c3c8af0b927fa28bd5281d908de8ab7c3172000701a3931dc113cdee835b30a9697419109ed88e4bf8bb5dace761af85c005c66; TS5220f739029=0868f8be6fab2800b2aec8acf51ae79072b52f7fce0bd1f2319608dcc5177438b08cea2f9113c6822e160f5273462335; TSf1edb2d2027=0868f8be6fab2000dd8055319e4e708e87c7abe157d7f5b262b72b14e103cb8a997ff40ee3e2114c082b9d1ce8113000103fb1026cb3d2d6a8b0509ec24733860a59b868e55f34db7bb939139c057d78cd1e8c37458c1cc74fa56f4d6f392f64',
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
    """
    Request yang menghormati rate limit server.

    Ini tidak mencoba melewati proteksi server. Saat menerima 429, fungsi akan
    mengikuti Retry-After atau menunggu dengan exponential backoff + jitter.
    """
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