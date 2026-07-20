import json
import os
import random
import re
import tempfile
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

import pandas as pd
import requests
import schedule
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from config_se2026 import NAMA_KABUPATEN, BASE_PATH, LATEST_FILE, archive_filename

# ================= SETTINGS =================
URL_DATA = "https://fasih-sm.bps.go.id/app/api/analytic/api/v2/assignment/report-progress-by-responsibility"
FASIH_HOME_URL = "https://fasih-sm.bps.go.id/app/"
FASIH_LOGIN_URL = "https://fasih-sm.bps.go.id/oauth_login.html"
SSO_BUTTON_SELECTOR = '[href="/oauth2/authorization/ics"]'
base_path = BASE_PATH

BASE_DIR = Path(__file__).resolve().parent
AUTH_DIR = BASE_DIR / ".auth"
STATE_FILE = AUTH_DIR / "fasih_state.json"
ENV_FILE = BASE_DIR / ".env"
AUTH_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Cookie tidak lagi ditulis manual. Nilainya diisi dari Playwright/state file.
cookies = {}

# Header dibuat minimal. Header Cookie akan dibentuk otomatis oleh requests
# dari parameter cookies=..., sehingga tidak ada cookie kedaluwarsa yang tertinggal.
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "origin": "https://fasih-sm.bps.go.id",
    "referer": "https://fasih-sm.bps.go.id/app/surveys/a0429e96-51a5-477b-a415-485f9c153004/fd68e454-ba45-4b85-8205-f3bf777ded24",
    "user-agent": DEFAULT_USER_AGENT,
}


def load_env():
    """Membaca file .env tanpa package python-dotenv."""
    env = {}
    if not ENV_FILE.exists():
        return env

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = re.match(r"^\s*([\w.-]+)\s*=\s*(.*?)\s*$", line)
        if not match:
            continue

        key = match.group(1)
        value = match.group(2) or ""
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        env[key] = value

    return env


def env_bool(value, default=True):
    if value is None:
        return default
    return str(value).strip().lower() not in {"false", "no", "0", "off", "tidak"}


def ask_otp():
    return input("Masukkan kode OTP: ").strip()


def is_app_url(url):
    parsed = urlparse(url)
    return (
        parsed.hostname == "fasih-sm.bps.go.id"
        and (
            parsed.path.startswith("/app")
            or parsed.path.startswith("/survey-collection")
        )
    )


def safe_wait_network_idle(page, timeout=15000):
    """Networkidle dapat timeout jika aplikasi terus melakukan polling."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass


def wait_for_app_or_otp(page, use_otp=True, timeout_seconds=15):
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if is_app_url(page.url):
            return "app"

        if use_otp:
            try:
                if page.locator('input[name="otp"]').first.is_visible():
                    return "otp"
            except Exception:
                pass

        time.sleep(0.5)
    return "timeout"


def update_runtime_cookies(fresh_cookies):
    """Sinkronkan cookie Playwright ke requests dan perbarui XSRF header."""
    global cookies

    cookies = {
        item["name"]: item["value"]
        for item in fresh_cookies
        if item.get("name") and item.get("value") is not None
    }

    xsrf_token = cookies.get("XSRF-TOKEN")
    if xsrf_token:
        headers["x-xsrf-token"] = unquote(xsrf_token)
    else:
        headers.pop("x-xsrf-token", None)


def load_cookies_from_state():
    """Muat cookie dari storage state tanpa membuka browser."""
    if not STATE_FILE.exists():
        return False

    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        state_cookies = state.get("cookies", [])
        if not state_cookies:
            return False

        update_runtime_cookies(state_cookies)
        return bool(cookies)
    except (OSError, json.JSONDecodeError, TypeError) as e:
        print(f"⚠️ State login tidak valid dan akan dihapus: {e}")
        STATE_FILE.unlink(missing_ok=True)
        return False


def login_with_sso(
    username="",
    password="",
    otp_code=None,
    use_otp=True,
    executable_path="",
    headless=True,
):
    """
    Buka FASIH dengan Playwright, gunakan storage state jika masih valid,
    dan lakukan login SSO ketika session sudah kedaluwarsa.

    Return: list cookie Playwright yang siap dipakai requests.
    """
    launch_options = {"headless": headless}
    if executable_path and Path(executable_path).is_file():
        launch_options["executable_path"] = executable_path

    context_options = {
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": headers["user-agent"],
    }

    if STATE_FILE.exists():
        try:
            json.loads(STATE_FILE.read_text(encoding="utf-8"))
            context_options["storage_state"] = str(STATE_FILE)
        except (OSError, json.JSONDecodeError):
            STATE_FILE.unlink(missing_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**launch_options)
        context = browser.new_context(**context_options)
        page = context.new_page()

        try:
            # 1. Coba session yang sudah tersimpan.
            if STATE_FILE.exists():
                print("🔎 Memeriksa session Playwright yang tersimpan...")
                try:
                    page.goto(FASIH_HOME_URL, wait_until="domcontentloaded", timeout=30000)
                    safe_wait_network_idle(page)
                    if is_app_url(page.url):
                        print("✅ Session tersimpan masih valid.")
                        context.storage_state(path=str(STATE_FILE))
                        return context.cookies()
                except Exception as e:
                    print(f"⚠️ Session tersimpan tidak dapat digunakan: {e}")

                STATE_FILE.unlink(missing_ok=True)
                context.clear_cookies()

            # 2. Session tidak tersedia/kedaluwarsa, lakukan login SSO.
            if not username or not password:
                raise RuntimeError(
                    "Session sudah tidak valid, tetapi username/password belum tersedia. "
                    "Isi file .env terlebih dahulu."
                )

            print("🔐 Login ulang melalui SSO BPS menggunakan Playwright...")
            page.goto(FASIH_LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
            safe_wait_network_idle(page)

            page.locator(SSO_BUTTON_SELECTOR).click(timeout=60000)
            page.wait_for_load_state("domcontentloaded", timeout=60000)

            page.locator('input[name="username"]').fill(username, timeout=60000)
            page.locator('input[name="password"]').fill(password, timeout=60000)
            page.locator('input[type="submit"]').click(timeout=60000)
            safe_wait_network_idle(page)

            state = wait_for_app_or_otp(page, use_otp=use_otp, timeout_seconds=15)

            if use_otp:
                otp_input = page.locator('input[name="otp"]').first
                otp_visible = False
                try:
                    otp_visible = otp_input.is_visible()
                except Exception:
                    pass

                if state == "otp" or otp_visible:
                    print("🔢 OTP diperlukan. Periksa aplikasi Authenticator.")
                    otp_value = otp_code or ask_otp()
                    if not otp_value:
                        raise RuntimeError("Kode OTP tidak boleh kosong.")

                    otp_input.fill(otp_value)
                    page.locator('input[type="submit"]').click(timeout=60000)
                    safe_wait_network_idle(page)

            # 3. Tunggu sampai kembali ke aplikasi FASIH.
            deadline = time.monotonic() + 60
            while time.monotonic() < deadline and not is_app_url(page.url):
                time.sleep(0.5)

            if "survey-collection" in page.url:
                page.goto(FASIH_HOME_URL, wait_until="domcontentloaded", timeout=30000)
                safe_wait_network_idle(page)

            if not is_app_url(page.url):
                raise RuntimeError(f"Login gagal. URL terakhir: {page.url}")

            context.storage_state(path=str(STATE_FILE))
            fresh_cookies = context.cookies()

            if not any(c.get("name") in {"SESSION", "XSRF-TOKEN"} for c in fresh_cookies):
                raise RuntimeError(
                    "Login tampak berhasil, tetapi cookie SESSION/XSRF-TOKEN tidak ditemukan."
                )

            print(f"✅ Login berhasil. State disimpan ke {STATE_FILE}")
            return fresh_cookies

        finally:
            browser.close()


def refresh_cookies():
    """Login/refresh session dengan Playwright, lalu kirim cookie ke requests."""
    env = load_env()

    username = env.get("username") or env.get("USERNAME") or ""
    password = env.get("password") or env.get("PASSWORD") or ""
    use_otp = env_bool(env.get("use_otp") or env.get("USE_OTP"), default=True)
    headless = env_bool(env.get("HEADLESS") or env.get("headless"), default=True)
    executable_path = (
        env.get("CHROME_EXECUTABLE_PATH")
        or env.get("chrome_executable_path")
        or ""
    )

    fresh = login_with_sso(
        username=username,
        password=password,
        otp_code=None,
        use_otp=use_otp,
        executable_path=executable_path,
        headless=headless,
    )
    update_runtime_cookies(fresh)
    print(f"🍪 {len(cookies)} cookie aktif siap dipakai oleh requests.")


def ensure_cookies():
    """Gunakan state tersimpan terlebih dahulu; login jika belum tersedia."""
    if cookies:
        return

    if load_cookies_from_state():
        print(f"🍪 Memuat {len(cookies)} cookie dari {STATE_FILE}")
        return

    refresh_cookies()


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

        # 401/403 dikembalikan langsung agar fetch_data() dapat melakukan
        # refresh session Playwright, bukan mengulang request dengan cookie lama.
        if response.status_code in (401, 403):
            return response

        if response.status_code == 429:
            print(
                f"⚠️  Status 429 (percobaan {attempt}/{max_retries}) - "
                "request dibatasi sementara."
            )
            if attempt == max_retries:
                raise RuntimeError(
                    f"Berhenti: status 429 berulang {max_retries}x. "
                    "Tunggu sebelum mencoba lagi atau koordinasi ke admin FASIH."
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

    # Ambil cookie dari state Playwright. Jika belum ada, login SSO otomatis.
    try:
        ensure_cookies()
    except Exception as e:
        print(f"🛑 Tidak dapat menyiapkan session FASIH: {e}")
        return

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
        if (
            (response.status_code == 200 and is_session_expired(response))
            or response.status_code in (302, 401, 403)
        ):
            if refresh_count >= max_refresh:
                print(
                    f"🛑 Session expired lagi setelah {max_refresh}x refresh. "
                    "Periksa username/password, OTP, VPN, atau akses akun FASIH."
                )
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