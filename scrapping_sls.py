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
    '_ga_FMZTHHQN2K': 'GS2.1.s1778035370$o1$g1$t1778035723$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1778035727$o1$g1$t1778035852$j60$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1778314369$o1$g1$t1778314389$j40$l0$h0',
    '_ga_9E7L2XJ89Y': 'GS2.1.s1778465304$o1$g0$t1778465307$j57$l0$h0',
    'cf_clearance': 'CwLXIaLV3mmGpRwuhuAC30Uco3Pjb_tz_1ZEbXnsvlo-1780364611-1.2.1.1-JeJaibKrj6XS4kPV4Ip25uQkYHC0SxIs56rfZupCrrK8yP_H6zi1dSFcMZnahwgzur4pRIS8XT8t.FS4e5IZD.l09FvOnFaWnw1eLG9FQpfiCb6rGNDUqraHwu0yGtfqjoATjtiW8VgnuTu7I13XGK8qcdi5YicZDzmWAEfbg0GfAms1zt6a3TtivoUKuPHm91832sMMPQ4eCQ77uVHVtMj8thYLEZbhWlQGGd8TE3ZqmJ1dIjlbGtBIMzKCS9YrdI3BX4QMqGMRNKdCVHFpJhQyO3yvQt5ZK3mFh83hjYJJSLZJnszvXzwkM5Q._LIPvYpMzOE_zhyRpUg2Nrd2rA',
    '_ga': 'GA1.3.337823039.1778035336',
    '_ga_XXTTVXWHDB': 'GS2.3.s1780364612$o4$g1$t1780364813$j60$l0$h0',
    'f5avraaaaaaaaaaaaaaaa_session_': 'CMECEJPFCIBDPLEJEGAIMGAJLHMOAJNGJIAONHIGAJGJCGMELDNHDCJABKMCKKONMNMDNLAPPDFJKCLPILCAPHLKLDMGDFDKPMDMDLDDFJMHPJNOJDENGNOHIKJCEINI',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '30a373b9a6355c4bf200c2f6c2137823',
    'XSRF-TOKEN': '4ea052d8-5020-4528-883f-0ad5069d1089',
    'SESSION': 'be9566ae-1340-44fb-ba11-b6d2a7308eb4',
    'TS00000000076': '0868f8be6fab2800bca30dbf21101e8959ed8a9f2cde6d765d67cc6688a1f43dc441692c73f292d0183d4908317cc29a08d7a2c75609d0001d76b06b37ed33750a612d50d8a538d2bfb359f88a917806b4525922cd2968ba8105f920e816cb6fde43b59d132050eec82eb3cd6b04664182f32d22b37d056f4678d39eadcb02d75b53c7708945bff311c8496e95a4cc812612f9db6200a253c86eaa55fb1560e0bcff0543dee7ce9c94d1f1fb6fa2278d93e3cd4f3708983cc4c3d79f9d1797fd30295a5b0dbd6666370026c392546661abb445ae64b47e82573dadb567f24128ede03ebaec74d4c58f43d79fc53cc55b9c8fdcda999e9d4832d01badd5a947bfb607fc99ddee7071',
    'TSPD_101_DID': '0868f8be6fab2800bca30dbf21101e8959ed8a9f2cde6d765d67cc6688a1f43dc441692c73f292d0183d4908317cc29a08d7a2c75606380049bef8a4163485dece4c1e20e5ad8e28b0ed5913e06a5d941141b14821b113c5daa365795300ef7703886f8a3b4c436cde8421d2ae56b499',
    'TS011f2d1a': '01266d26d05f15bf8cfb6dddcbccae76ef2e94feb84897774ac69b102f37e8a6d2b02859a7f60e26545317f94d61d8acd75a562a3a',
    'TSPD_101': '0868f8be6fab2800b36136a82b0622409c14ed003fbb5aedd1da9bf3a93c520c9768ff3ed4fec76438925d817c9eacb2080b89d049051800b992fe4680e349c85ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab28006aa140c3760ced5f422cc3ffd5b7ee1ad069f2fd83b6c2f4004947a830ecb00f6ccfc15aef8aa634085607cf80172000676c4270b94fdfe525cea4b6d1f4a045dfb119d610207b70ac0616474db222c7',
    'TS5220f739029': '0868f8be6fab28001e750eaa460748f00e2387cc0b3c726f654c9a70aeee0ada2ee7d7e32051c829bfb3c93a21cea8f0',
    'TSf1edb2d2027': '0868f8be6fab200000fe135621e375c48a3bdafac996b7bb3d29c05acc89322f8b4818b0b19dab3408a1dd488e1130008f6f6b20a9cf4da55ce8db0fad717eb4d4de41bcd2e50a7dd12103d7e3bebd455355ea3e60abd3512a4032a16626072e',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8,sv;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Microsoft Edge";v="150"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': '4ea052d8-5020-4528-883f-0ad5069d1089',
    'cookie': '_ga_FMZTHHQN2K=GS2.1.s1778035370$o1$g1$t1778035723$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1778035727$o1$g1$t1778035852$j60$l0$h0; _ga_K98R6MSKRH=GS2.1.s1778314369$o1$g1$t1778314389$j40$l0$h0; _ga_9E7L2XJ89Y=GS2.1.s1778465304$o1$g0$t1778465307$j57$l0$h0; cf_clearance=CwLXIaLV3mmGpRwuhuAC30Uco3Pjb_tz_1ZEbXnsvlo-1780364611-1.2.1.1-JeJaibKrj6XS4kPV4Ip25uQkYHC0SxIs56rfZupCrrK8yP_H6zi1dSFcMZnahwgzur4pRIS8XT8t.FS4e5IZD.l09FvOnFaWnw1eLG9FQpfiCb6rGNDUqraHwu0yGtfqjoATjtiW8VgnuTu7I13XGK8qcdi5YicZDzmWAEfbg0GfAms1zt6a3TtivoUKuPHm91832sMMPQ4eCQ77uVHVtMj8thYLEZbhWlQGGd8TE3ZqmJ1dIjlbGtBIMzKCS9YrdI3BX4QMqGMRNKdCVHFpJhQyO3yvQt5ZK3mFh83hjYJJSLZJnszvXzwkM5Q._LIPvYpMzOE_zhyRpUg2Nrd2rA; _ga=GA1.3.337823039.1778035336; _ga_XXTTVXWHDB=GS2.3.s1780364612$o4$g1$t1780364813$j60$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=CMECEJPFCIBDPLEJEGAIMGAJLHMOAJNGJIAONHIGAJGJCGMELDNHDCJABKMCKKONMNMDNLAPPDFJKCLPILCAPHLKLDMGDFDKPMDMDLDDFJMHPJNOJDENGNOHIKJCEINI; db8ca2b43ed851cc93e71fd5fd72bff7=30a373b9a6355c4bf200c2f6c2137823; XSRF-TOKEN=4ea052d8-5020-4528-883f-0ad5069d1089; SESSION=be9566ae-1340-44fb-ba11-b6d2a7308eb4; TS00000000076=0868f8be6fab2800bca30dbf21101e8959ed8a9f2cde6d765d67cc6688a1f43dc441692c73f292d0183d4908317cc29a08d7a2c75609d0001d76b06b37ed33750a612d50d8a538d2bfb359f88a917806b4525922cd2968ba8105f920e816cb6fde43b59d132050eec82eb3cd6b04664182f32d22b37d056f4678d39eadcb02d75b53c7708945bff311c8496e95a4cc812612f9db6200a253c86eaa55fb1560e0bcff0543dee7ce9c94d1f1fb6fa2278d93e3cd4f3708983cc4c3d79f9d1797fd30295a5b0dbd6666370026c392546661abb445ae64b47e82573dadb567f24128ede03ebaec74d4c58f43d79fc53cc55b9c8fdcda999e9d4832d01badd5a947bfb607fc99ddee7071; TSPD_101_DID=0868f8be6fab2800bca30dbf21101e8959ed8a9f2cde6d765d67cc6688a1f43dc441692c73f292d0183d4908317cc29a08d7a2c75606380049bef8a4163485dece4c1e20e5ad8e28b0ed5913e06a5d941141b14821b113c5daa365795300ef7703886f8a3b4c436cde8421d2ae56b499; TS011f2d1a=01266d26d05f15bf8cfb6dddcbccae76ef2e94feb84897774ac69b102f37e8a6d2b02859a7f60e26545317f94d61d8acd75a562a3a; TSPD_101=0868f8be6fab2800b36136a82b0622409c14ed003fbb5aedd1da9bf3a93c520c9768ff3ed4fec76438925d817c9eacb2080b89d049051800b992fe4680e349c85ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab28006aa140c3760ced5f422cc3ffd5b7ee1ad069f2fd83b6c2f4004947a830ecb00f6ccfc15aef8aa634085607cf80172000676c4270b94fdfe525cea4b6d1f4a045dfb119d610207b70ac0616474db222c7; TS5220f739029=0868f8be6fab28001e750eaa460748f00e2387cc0b3c726f654c9a70aeee0ada2ee7d7e32051c829bfb3c93a21cea8f0; TSf1edb2d2027=0868f8be6fab200000fe135621e375c48a3bdafac996b7bb3d29c05acc89322f8b4818b0b19dab3408a1dd488e1130008f6f6b20a9cf4da55ce8db0fad717eb4d4de41bcd2e50a7dd12103d7e3bebd455355ea3e60abd3512a4032a16626072e',
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