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
    'f5avraaaaaaaaaaaaaaaa_session_': 'FIGDOMENMBEIADNOGFIPNJFFMMGBMFNDFBPGNNENIFOENDCHNPCKBAFNAKADNANIDDIDJGBDCPPCPBJEPDOACCAAIJINMCDKGIJDNNDBPNJLNCNEOEKFLJFBIDOGEHJG',
    'TS01acc472': '01266d26d0c9d72de48952d80b8df57617e791726bfb52e6fee4269dd9290dcc004302967a82a91d9e9026ba6f26d032d56b5cc2ae9c088e5349c621a5238ddc77157a9b1726f6c20b86992c50d8aaed1cd7922d7025d14f52451e5d913e0367777d193f4fbac58b37984082f4b4bb491b262b9de1',
    'cf_clearance': 'vCS7GWnD90EGCzme5SvnFiHTh87CAXni6KKq.n7F9R0-1784673476-1.2.1.1-kgazhBTNZLwLJgZ1kTaNAIuLqKXJWGfWo6ASyRzDBD19JlyzolDBjUHMerM.ihkb8PSTnORzJSgCnWFqg3w4vqSILmYwJrpcKasX6mdboa.rm8KaGmUg_D7K_QPPQNS9nTgWoTmoQQIifn3eutv3MrkKFYBrswUxG3sMDzD36ZTzqQw7JLRcdlYjoodLZXg_sSYwGuj5NcioJa93CnD98qANFv1QaVN_RyZSfB77ba9d2NPkd2qjUOmXSiknUUH.1wExIdrGwHtwZhxHC6O1VucGL8ssDXQic423cfPg7nT3imW8gAcARK.ZHXNUubFX57ZTAcgrSgu2cIBEh5pw9g',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'f5a9d9c05b9b6dce00d74c156e302bc4',
    'XSRF-TOKEN': 'ce256d00-8d4b-4ee3-bd55-ef243e4c533a',
    'TS0151fc2b': '0167a1c861a0927865d5ca499c2daa2eba8d1f332262a49daadf054ddeab4d185bd1d0102c0e393771a0b31d59f79b1843c130245b',
    'TS018af012': '0167a1c861918a56a26aa60d37adecae9a6131301b006535769affe10529b6398c39d85675c4c6a678898e3771e4761a45c8bf5af6f75f71f0f3bc52ff6f6e381afda9bf39ed17d6f73ae2f8c141deb4544dfe4b11',
    'f5avraaaaaaaaaaaaaaaa_session_': 'HKKHCDBHMPKEIIGABDDFCJPJKFPDPKGJPENLAOCOPJFEGGABOEFIDFLIBANJODCACACDNFLMFPMLONBPKPLAGDMPFJBJJLLGPNEBHNHLKIINICJFBFLMOLHEMOLDADKA',
    'TS00000000076': '0868f8be6fab2800eda68b18555a6d2a270a16c2d22820754cc7e2be19dad34fc53336dd56f2a7a4eace64f345174c25088217daf709d0000df697c6af19a09622bd34193c5825627aade6c50bb3d64ed1b92d334ced44c325446b6bed141959534a621cb91502e62c7f9fc8032e2a62f5b868f1590f6d083b0c90440afb18744f56ab6ad36d808d540dda8143296d7c3a667ddfcd943559c29c1a4c01cf32da8d141eee6847d544af5bec3dffe091737fe5cb584bc03539ec38e6271d9558a29848447d3710432e99d1a9896cd3ccb905392c3f7344fe3a20fdcd2420dc663436b0260f1993ff518c51c2d411e029150109b8476c208763e28f3054ad003c5a8a0159b6227a08d6',
    'TSPD_101_DID': '0868f8be6fab2800eda68b18555a6d2a270a16c2d22820754cc7e2be19dad34fc53336dd56f2a7a4eace64f345174c25088217daf7063800d713129e6f309b0668f910f68b6128676bf8ba2f2707ca143e30a7165f08c4eeccabf6d451cac9e91f287359f7877f3acccbc195fc04cef3',
    'TS011f2d1a': '01266d26d0b06ab65fc601d7c6819dbd3e72e3d8eea89104e37eefad9a359fe69f27a877c4ac2ada5490555712f993a305891960ae',
    'TSPD_101': '0868f8be6fab28009049a88d63a27089fe3a44aeb97532ab1ffede9f589fa0a5b86e0ac0a11547ace88e85faaa7900fe08fe4f27b20518006806f04897a9636d5ca1732140a3428bba23ce13beb1c95e',
    'JSESSIONID': 'DEFA2DBC86DD1EDDA4B341EB32178864',
    'SESSION': 'd7eb608e-08ce-4bf3-8002-9e3d47da51f1',
    'TS5220f739077': '0868f8be6fab280030dff9c5362528861689a1e3620675fe959e17ef8a0cdfdf62e3f1744364e8997edc9c09c4ba8cee08e50d999b1720001727477ff2687ce5df7dbbcec42cb3c411c6b49268f50202e46cda1ab4a33a07',
    'TS5220f739029': '0868f8be6fab28006a05d4c6660a31f290aeeee60ba4209cae9c8794c68aa67676df01647fe2332a3db73b33f1c0439b',
    'TSf1edb2d2027': '0868f8be6fab20001f274b998a3494ab6ac29e632345e833118b88eca9770ecc8e10c419b19d12f908113dc6f4113000d3ba9021ef887896c067ac0c3a9b09e71f082ee8020f6ebc8b6798fd9070153bb4ddd4db955b6ff53c773989a65bbc32',
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
    'x-xsrf-token': 'ce256d00-8d4b-4ee3-bd55-ef243e4c533a',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=FIGDOMENMBEIADNOGFIPNJFFMMGBMFNDFBPGNNENIFOENDCHNPCKBAFNAKADNANIDDIDJGBDCPPCPBJEPDOACCAAIJINMCDKGIJDNNDBPNJLNCNEOEKFLJFBIDOGEHJG; TS01acc472=01266d26d0c9d72de48952d80b8df57617e791726bfb52e6fee4269dd9290dcc004302967a82a91d9e9026ba6f26d032d56b5cc2ae9c088e5349c621a5238ddc77157a9b1726f6c20b86992c50d8aaed1cd7922d7025d14f52451e5d913e0367777d193f4fbac58b37984082f4b4bb491b262b9de1; cf_clearance=vCS7GWnD90EGCzme5SvnFiHTh87CAXni6KKq.n7F9R0-1784673476-1.2.1.1-kgazhBTNZLwLJgZ1kTaNAIuLqKXJWGfWo6ASyRzDBD19JlyzolDBjUHMerM.ihkb8PSTnORzJSgCnWFqg3w4vqSILmYwJrpcKasX6mdboa.rm8KaGmUg_D7K_QPPQNS9nTgWoTmoQQIifn3eutv3MrkKFYBrswUxG3sMDzD36ZTzqQw7JLRcdlYjoodLZXg_sSYwGuj5NcioJa93CnD98qANFv1QaVN_RyZSfB77ba9d2NPkd2qjUOmXSiknUUH.1wExIdrGwHtwZhxHC6O1VucGL8ssDXQic423cfPg7nT3imW8gAcARK.ZHXNUubFX57ZTAcgrSgu2cIBEh5pw9g; db8ca2b43ed851cc93e71fd5fd72bff7=f5a9d9c05b9b6dce00d74c156e302bc4; XSRF-TOKEN=ce256d00-8d4b-4ee3-bd55-ef243e4c533a; TS0151fc2b=0167a1c861a0927865d5ca499c2daa2eba8d1f332262a49daadf054ddeab4d185bd1d0102c0e393771a0b31d59f79b1843c130245b; TS018af012=0167a1c861918a56a26aa60d37adecae9a6131301b006535769affe10529b6398c39d85675c4c6a678898e3771e4761a45c8bf5af6f75f71f0f3bc52ff6f6e381afda9bf39ed17d6f73ae2f8c141deb4544dfe4b11; f5avraaaaaaaaaaaaaaaa_session_=HKKHCDBHMPKEIIGABDDFCJPJKFPDPKGJPENLAOCOPJFEGGABOEFIDFLIBANJODCACACDNFLMFPMLONBPKPLAGDMPFJBJJLLGPNEBHNHLKIINICJFBFLMOLHEMOLDADKA; TS00000000076=0868f8be6fab2800eda68b18555a6d2a270a16c2d22820754cc7e2be19dad34fc53336dd56f2a7a4eace64f345174c25088217daf709d0000df697c6af19a09622bd34193c5825627aade6c50bb3d64ed1b92d334ced44c325446b6bed141959534a621cb91502e62c7f9fc8032e2a62f5b868f1590f6d083b0c90440afb18744f56ab6ad36d808d540dda8143296d7c3a667ddfcd943559c29c1a4c01cf32da8d141eee6847d544af5bec3dffe091737fe5cb584bc03539ec38e6271d9558a29848447d3710432e99d1a9896cd3ccb905392c3f7344fe3a20fdcd2420dc663436b0260f1993ff518c51c2d411e029150109b8476c208763e28f3054ad003c5a8a0159b6227a08d6; TSPD_101_DID=0868f8be6fab2800eda68b18555a6d2a270a16c2d22820754cc7e2be19dad34fc53336dd56f2a7a4eace64f345174c25088217daf7063800d713129e6f309b0668f910f68b6128676bf8ba2f2707ca143e30a7165f08c4eeccabf6d451cac9e91f287359f7877f3acccbc195fc04cef3; TS011f2d1a=01266d26d0b06ab65fc601d7c6819dbd3e72e3d8eea89104e37eefad9a359fe69f27a877c4ac2ada5490555712f993a305891960ae; TSPD_101=0868f8be6fab28009049a88d63a27089fe3a44aeb97532ab1ffede9f589fa0a5b86e0ac0a11547ace88e85faaa7900fe08fe4f27b20518006806f04897a9636d5ca1732140a3428bba23ce13beb1c95e; JSESSIONID=DEFA2DBC86DD1EDDA4B341EB32178864; SESSION=d7eb608e-08ce-4bf3-8002-9e3d47da51f1; TS5220f739077=0868f8be6fab280030dff9c5362528861689a1e3620675fe959e17ef8a0cdfdf62e3f1744364e8997edc9c09c4ba8cee08e50d999b1720001727477ff2687ce5df7dbbcec42cb3c411c6b49268f50202e46cda1ab4a33a07; TS5220f739029=0868f8be6fab28006a05d4c6660a31f290aeeee60ba4209cae9c8794c68aa67676df01647fe2332a3db73b33f1c0439b; TSf1edb2d2027=0868f8be6fab20001f274b998a3494ab6ac29e632345e833118b88eca9770ecc8e10c419b19d12f908113dc6f4113000d3ba9021ef887896c067ac0c3a9b09e71f082ee8020f6ebc8b6798fd9070153bb4ddd4db955b6ff53c773989a65bbc32',
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