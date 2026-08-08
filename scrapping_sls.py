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
    'f5avraaaaaaaaaaaaaaaa_session_': 'ANEGAIALAOAFPBHGFLCDNAJDJLKBJEDKLGCJDCGAFKEMHDLJGKMJFDEEHOBCEMCEPAGDJMPGBKJICOFFBCHAHMFIJIGBMCOAOEPMEPNLEEBIAHALNFKDNFPGNEOJCIAA',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '5d057ac0efc961de02bd3d22869bf5a7',
    'XSRF-TOKEN': '1fffd967-94e0-400e-8f13-b765f9cb8fb6',
    'JSESSIONID': 'B6121CADBC756A894276DB04EA2B848D',
    'SESSION': 'cf527e17-3af7-4e7c-81a8-2a0645d49711',
    'f5avraaaaaaaaaaaaaaaa_session_': 'HFPONFENDAGOLJPGDDLJCNLPAKIAFOPHOKMMGKBKPKPMGLNDHPLLAHJGIHHFDJFNJEGDHBGMBIGHFKDHCFPAKIMCDICMHPBIALHKHNMBAENIHGAOLANCKJADOPJMGGKN',
    'TS00000000076': '0868f8be6fab2800fd3d0a6fbfc97343eda19c497a46255fe3c3148f27eaac8a9b4699a7b5c23ba649f70e26930b8565084127508909d000f96c30bdfafbb3ab528bcc5887f7925346abc031c1dca73de8593461fec7f89dbb9b5ae940b38d348f382adf8d811c78cd35cfc9a4f519a6d13ad3f0201dc66545044cb9a09ad914a3619a9997fb1e62f5324f01b16d5256404d36b704fca5d1f92d63ec8eb4702c7e183dfc3f4daf1199444e45feb65e6ff9f81faa1770292bc5f638ec7e70b8efa6859d27ad9b70e23571d66a6365c5e936f40a46b8da2dc7780cb52d7be326e0f8b9496053a31ff6d12f6dc16ef49df3e785dc8e13fdc00e13e0b19c02edd0f033482929c5586387',
    'TSPD_101_DID': '0868f8be6fab2800fd3d0a6fbfc97343eda19c497a46255fe3c3148f27eaac8a9b4699a7b5c23ba649f70e26930b85650841275089063800f8e10d24d358e4dbfee0aafc740d6bc3abd93a7bd9e60c944ebb24bd7706dbdfb7f820d9ab16f0dab4b3123db56ea87a1b0050af7ec45aaf',
    'TS011f2d1a': '01266d26d026531a816ea72f546ede451bad5a36155a41b2f8de92659d908a94d2066d768f50fe3b9b89f2c330f9cea09277d9aef7',
    'TSPD_101': '0868f8be6fab28005ef4f34c5b859f493294aae2af3471698dad0c595e873a56e027f57cb03742ba97b36f0c3e0ee2e708f19d8ab1051800f083cef0dad59d595ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab28003115bbba5f87eb40514093280893e2987735eb55c79937b2ff63e057786db83515f76fb1fabb549508af52e97817200095bb9f1fe4c23abe6c597633a047b472064180b5e75f4d442a1b8d89ed7cd6a4',
    'TS5220f739029': '0868f8be6fab280042ff9c0845e70b913df6b2fd82f06451b297bf51583a7d0e4ec98e72960c1c8c1291368f9aa56e50',
    'TSf1edb2d2027': '0868f8be6fab200097d75e1c7468a396e06e80d6cbbbc05792e7a655b815b34cb832973c035a60f308070fbe2211300090fd26b428c7769c0bfaf1d7bc540657b0bddd4411329f5c1629d06b3daea4b4b1391c1bdb1bd22c74a70f6edadaae62',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
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
    'x-xsrf-token': '1fffd967-94e0-400e-8f13-b765f9cb8fb6',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=ANEGAIALAOAFPBHGFLCDNAJDJLKBJEDKLGCJDCGAFKEMHDLJGKMJFDEEHOBCEMCEPAGDJMPGBKJICOFFBCHAHMFIJIGBMCOAOEPMEPNLEEBIAHALNFKDNFPGNEOJCIAA; db8ca2b43ed851cc93e71fd5fd72bff7=5d057ac0efc961de02bd3d22869bf5a7; XSRF-TOKEN=1fffd967-94e0-400e-8f13-b765f9cb8fb6; JSESSIONID=B6121CADBC756A894276DB04EA2B848D; SESSION=cf527e17-3af7-4e7c-81a8-2a0645d49711; f5avraaaaaaaaaaaaaaaa_session_=HFPONFENDAGOLJPGDDLJCNLPAKIAFOPHOKMMGKBKPKPMGLNDHPLLAHJGIHHFDJFNJEGDHBGMBIGHFKDHCFPAKIMCDICMHPBIALHKHNMBAENIHGAOLANCKJADOPJMGGKN; TS00000000076=0868f8be6fab2800fd3d0a6fbfc97343eda19c497a46255fe3c3148f27eaac8a9b4699a7b5c23ba649f70e26930b8565084127508909d000f96c30bdfafbb3ab528bcc5887f7925346abc031c1dca73de8593461fec7f89dbb9b5ae940b38d348f382adf8d811c78cd35cfc9a4f519a6d13ad3f0201dc66545044cb9a09ad914a3619a9997fb1e62f5324f01b16d5256404d36b704fca5d1f92d63ec8eb4702c7e183dfc3f4daf1199444e45feb65e6ff9f81faa1770292bc5f638ec7e70b8efa6859d27ad9b70e23571d66a6365c5e936f40a46b8da2dc7780cb52d7be326e0f8b9496053a31ff6d12f6dc16ef49df3e785dc8e13fdc00e13e0b19c02edd0f033482929c5586387; TSPD_101_DID=0868f8be6fab2800fd3d0a6fbfc97343eda19c497a46255fe3c3148f27eaac8a9b4699a7b5c23ba649f70e26930b85650841275089063800f8e10d24d358e4dbfee0aafc740d6bc3abd93a7bd9e60c944ebb24bd7706dbdfb7f820d9ab16f0dab4b3123db56ea87a1b0050af7ec45aaf; TS011f2d1a=01266d26d026531a816ea72f546ede451bad5a36155a41b2f8de92659d908a94d2066d768f50fe3b9b89f2c330f9cea09277d9aef7; TSPD_101=0868f8be6fab28005ef4f34c5b859f493294aae2af3471698dad0c595e873a56e027f57cb03742ba97b36f0c3e0ee2e708f19d8ab1051800f083cef0dad59d595ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab28003115bbba5f87eb40514093280893e2987735eb55c79937b2ff63e057786db83515f76fb1fabb549508af52e97817200095bb9f1fe4c23abe6c597633a047b472064180b5e75f4d442a1b8d89ed7cd6a4; TS5220f739029=0868f8be6fab280042ff9c0845e70b913df6b2fd82f06451b297bf51583a7d0e4ec98e72960c1c8c1291368f9aa56e50; TSf1edb2d2027=0868f8be6fab200097d75e1c7468a396e06e80d6cbbbc05792e7a655b815b34cb832973c035a60f308070fbe2211300090fd26b428c7769c0bfaf1d7bc540657b0bddd4411329f5c1629d06b3daea4b4b1391c1bdb1bd22c74a70f6edadaae62',
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