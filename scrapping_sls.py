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
    'f5avraaaaaaaaaaaaaaaa_session_': 'NCNPHNIMOOLEFELKAHAONIEGGEGIONHJMGFNBKCCOOKCBDGCJNPACFOBPCMFNFEIAPODCHPBINGIMAPMHIOAMKFJBDCPMMIEBOBKLNKILMCHFDPCAEONPPOCJEHALFGM',
    'f5_cspm': '1234',
    'f5avraaaaaaaaaaaaaaaa_session_': 'KEPMJPMKLIILNEAPECACJCMDHINKGDBLGLJAOPJDLGKOLKIDFPNIGEENEGGEFDHGJMODMIIOIMPIJKKGMGAAHPAANDDPCHHKPAEKBAPONLAHEBOABFLAGEBPHHADLGGN',
    'cf_clearance': 'eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg',
    '_ga': 'GA1.3.967752592.1784785844',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0',
    'XSRF-TOKEN': '8a78cc84-f362-4d31-8e0f-bf746c0c91ff',
    'f5avr1315829136aaaaaaaaaaaaaaaa_cspm_': 'GBPBHHCIGGCFIKAMNLFHFEHIGFHLPMKDHAFHPCAOLAKOHELGIMAGLFKOLEBIEJDKFAMCIHMBDHEICEKNFJIALMLEAKDGFMCHGENPKNGABLBHHECHBAPEMFONGKPPJCGO',
    'TS018af012': '0167a1c86186272affaf91ef86db2482de6a980824412ecdd087177cff37b5bff5f44c264df4722924b9db421f5d03fd312ed62898b99a8bc6037d7e07d1d219da0598bd5009c97bec2a616ae0444aca20fe12524d',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'ba1da908ae31eae9d0b148382127fcf5',
    'JSESSIONID': 'FB85F31055F81A92C2157BAB0D532450',
    'TS00000000076': '0868f8be6fab28004ce0a95e44e1f3596cda6a5997d094d77515aa3d4c6421375da7edf67ff2f2d440ecbb766592f78908ff03bed909d00009b25e499543ba938e1b86d2929a1c467edda06c3394d3ecb55792d7b24ec9588ba5e150d6168c4060cbf0a9265b37e322dadca575f7681c09229d8a69255ed7f66a6f7c70ce59bbcf16f1bac60b0d3486b26b37a1badcbfb047d5c9f7eeb510a41633351e830c7b828ae84295cb6963a64007cdc4b8c8b21ace7c37c1cc847ab967addb1f21edf757f3701ea9eb5b016ff1a25bef12750686586c1dd38612b06e5fe0b5d14136cef8631936651de5ecca95b239dbd13d5cc462535eeba7e37dbe1285aa6ea337b3de609f6e7f885ec3',
    'TSPD_101_DID': '0868f8be6fab28004ce0a95e44e1f3596cda6a5997d094d77515aa3d4c6421375da7edf67ff2f2d440ecbb766592f78908ff03bed9063800d7f0c01d577f956e9fd891bbe04304c4737afcf0ada46ba9126763920dd086719528b2b4e91c9224bfe20f2bb6ee4405a62fcf8811b52c1c',
    'TS011f2d1a': '01266d26d0310e10989b2ffdce6042a8bfb5fbfd1febb34d04c9d613562abb3bcfd15c25f0a0a83f405c8df647cd829725e76ee57f',
    'TSPD_101': '0868f8be6fab2800f6b4e7db078daecab0ca6bddc053f770c304d28699343596a63e3cf9c232f7696226895f9d049b9908a1246769051800b3c18721b890ed775ca1732140a3428bba23ce13beb1c95e',
    'SESSION': '8e84b767-8739-40dd-8b56-9befc4784504',
    'f5avraaaaaaaaaaaaaaaa_session_': 'NABEGPBCFIGIBGPEHBOLIJAGJCLJFLIHMBGDLLNEHJPNIBAIIJMGNNAIENBEOMKDDMKDKGHAKMNCNAJGCHLABBPOODJAMDBIMILJMIFLKALNNBJKDOONCMIJKEKPCMMK',
    'TS0151fc2b': '0167a1c861dc6aa3955fc0e0710faec128841f5c3fc84ad45227bcc27bb699edec160277b959090f23c1d3f19b6a8d96a70007ad8c',
    'TS5220f739077': '0868f8be6fab2800c2aa77c7847bba0fafa59dc719f5fb5679d5bf411b100f4ef7700df928cda1134c58fae21aedc1fe0868ace9921720007b2b1cb077660230aa1d9d954177ac04a780d696019ae78e42fada37885c93ed',
    'TS5220f739029': '0868f8be6fab2800bbd9cc1eef06caf8e639a75e2900c2631f843492a1ce18c17965e54952af7c34e75cc02d711748c4',
    'TSf1edb2d2027': '0868f8be6fab200004bfd2a1999d4b47f3655ac8e13a136cd6af48df88659124168040542454f9b908734e37d111300087e1bbd615e889a5444ddff821564e271c85922b491e23edc63719179ab0c3c0e4b59c6110e42541cea938cf1b3b3f85',
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
    'x-xsrf-token': '8a78cc84-f362-4d31-8e0f-bf746c0c91ff',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=NCNPHNIMOOLEFELKAHAONIEGGEGIONHJMGFNBKCCOOKCBDGCJNPACFOBPCMFNFEIAPODCHPBINGIMAPMHIOAMKFJBDCPMMIEBOBKLNKILMCHFDPCAEONPPOCJEHALFGM; f5_cspm=1234; f5avraaaaaaaaaaaaaaaa_session_=KEPMJPMKLIILNEAPECACJCMDHINKGDBLGLJAOPJDLGKOLKIDFPNIGEENEGGEFDHGJMODMIIOIMPIJKKGMGAAHPAANDDPCHHKPAEKBAPONLAHEBOABFLAGEBPHHADLGGN; cf_clearance=eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg; _ga=GA1.3.967752592.1784785844; _ga_XXTTVXWHDB=GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0; XSRF-TOKEN=8a78cc84-f362-4d31-8e0f-bf746c0c91ff; f5avr1315829136aaaaaaaaaaaaaaaa_cspm_=GBPBHHCIGGCFIKAMNLFHFEHIGFHLPMKDHAFHPCAOLAKOHELGIMAGLFKOLEBIEJDKFAMCIHMBDHEICEKNFJIALMLEAKDGFMCHGENPKNGABLBHHECHBAPEMFONGKPPJCGO; TS018af012=0167a1c86186272affaf91ef86db2482de6a980824412ecdd087177cff37b5bff5f44c264df4722924b9db421f5d03fd312ed62898b99a8bc6037d7e07d1d219da0598bd5009c97bec2a616ae0444aca20fe12524d; db8ca2b43ed851cc93e71fd5fd72bff7=ba1da908ae31eae9d0b148382127fcf5; JSESSIONID=FB85F31055F81A92C2157BAB0D532450; TS00000000076=0868f8be6fab28004ce0a95e44e1f3596cda6a5997d094d77515aa3d4c6421375da7edf67ff2f2d440ecbb766592f78908ff03bed909d00009b25e499543ba938e1b86d2929a1c467edda06c3394d3ecb55792d7b24ec9588ba5e150d6168c4060cbf0a9265b37e322dadca575f7681c09229d8a69255ed7f66a6f7c70ce59bbcf16f1bac60b0d3486b26b37a1badcbfb047d5c9f7eeb510a41633351e830c7b828ae84295cb6963a64007cdc4b8c8b21ace7c37c1cc847ab967addb1f21edf757f3701ea9eb5b016ff1a25bef12750686586c1dd38612b06e5fe0b5d14136cef8631936651de5ecca95b239dbd13d5cc462535eeba7e37dbe1285aa6ea337b3de609f6e7f885ec3; TSPD_101_DID=0868f8be6fab28004ce0a95e44e1f3596cda6a5997d094d77515aa3d4c6421375da7edf67ff2f2d440ecbb766592f78908ff03bed9063800d7f0c01d577f956e9fd891bbe04304c4737afcf0ada46ba9126763920dd086719528b2b4e91c9224bfe20f2bb6ee4405a62fcf8811b52c1c; TS011f2d1a=01266d26d0310e10989b2ffdce6042a8bfb5fbfd1febb34d04c9d613562abb3bcfd15c25f0a0a83f405c8df647cd829725e76ee57f; TSPD_101=0868f8be6fab2800f6b4e7db078daecab0ca6bddc053f770c304d28699343596a63e3cf9c232f7696226895f9d049b9908a1246769051800b3c18721b890ed775ca1732140a3428bba23ce13beb1c95e; SESSION=8e84b767-8739-40dd-8b56-9befc4784504; f5avraaaaaaaaaaaaaaaa_session_=NABEGPBCFIGIBGPEHBOLIJAGJCLJFLIHMBGDLLNEHJPNIBAIIJMGNNAIENBEOMKDDMKDKGHAKMNCNAJGCHLABBPOODJAMDBIMILJMIFLKALNNBJKDOONCMIJKEKPCMMK; TS0151fc2b=0167a1c861dc6aa3955fc0e0710faec128841f5c3fc84ad45227bcc27bb699edec160277b959090f23c1d3f19b6a8d96a70007ad8c; TS5220f739077=0868f8be6fab2800c2aa77c7847bba0fafa59dc719f5fb5679d5bf411b100f4ef7700df928cda1134c58fae21aedc1fe0868ace9921720007b2b1cb077660230aa1d9d954177ac04a780d696019ae78e42fada37885c93ed; TS5220f739029=0868f8be6fab2800bbd9cc1eef06caf8e639a75e2900c2631f843492a1ce18c17965e54952af7c34e75cc02d711748c4; TSf1edb2d2027=0868f8be6fab200004bfd2a1999d4b47f3655ac8e13a136cd6af48df88659124168040542454f9b908734e37d111300087e1bbd615e889a5444ddff821564e271c85922b491e23edc63719179ab0c3c0e4b59c6110e42541cea938cf1b3b3f85',
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
    size = 5
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