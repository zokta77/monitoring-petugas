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
    'f5avraaaaaaaaaaaaaaaa_session_': 'OKMPPADFONKPIPMGIHJBJGGNNIDOFHGIGIEBJCJKBGBDBEONPGHPODPNFJCIAMODBECDDPDGOLPHLOECNCEAGCCFJMLJFIICEGBLDNCLNAEBDMJCMDKGBBJGHGMNCHPN',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'f5avraaaaaaaaaaaaaaaa_session_': 'DJKFNDCKNJONIPPCBBDANHDMJFHCFKIKMNGGNBKABEMPGKJMECDCHBJODECEEFNFDJCDOMNLACFHNMDMAPIABICLNMLFBLIMFGMDHGDILAHBKADJKBMCCGAFKDKPIIEA',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'b4510136b164f28477db8bdb9d53569d',
    'XSRF-TOKEN': '4ad720b4-5dc2-445a-8687-37f58ec13097',
    'SESSION': '08963849-222a-4c55-b080-738aa9fb312b',
    'TS018af012': '0167a1c8615074aaaf4d48b05738fbcfa25a78daf2ff562f24034f7e425f6acb736cb2e17b1789cbc2cd1731ed9d6dc87b43b60727f31f0c9dfa4bccd0de3e297dd6dc008a526aa6c2b5b6100ca0e92c30ee171358',
    'TS00000000076': '0868f8be6fab2800f3bfc05eec9eaa378e89b7f22a8d3470ee998ab6e9311d0627880a5c9cdafbe06cf3196de3a00cec082cd787c709d000908deef8be85bdf365554434a12cab45295a3ee130845aa11aff06d19ab76ed330fc37c4857be406730f4a0c708bbf52383eded43bd4e944a1f4d9056d67b9258ccb6cfcc9270c3071a2599321764461c1b4d40d1b79618f9e6a1d1af010bfb9f8cbbf915d20e533b6b35b99865663a414d6a60818c87d5e7e46256eb7eee3385e4d195c631b36ea50d9c02f57954f2756cd2ecf876e4babe5406f17677e7d82892fc1ba9ee14247908e2a7758a4b198900cadc56ed96429f532c1f862035cdf1237ad982e208162ff057c294ab02885',
    'TSPD_101_DID': '0868f8be6fab2800f3bfc05eec9eaa378e89b7f22a8d3470ee998ab6e9311d0627880a5c9cdafbe06cf3196de3a00cec082cd787c7063800edc5287dde8e414d5092c2d6e51896971f32ac11d2a1afb1e51789c28e3113dd870b9f555612711e751cefd7f27035c203598664adaa69b1',
    'TS011f2d1a': '01266d26d09e07713d21655d1f384afcba9bbca1b75cac0988348c2cbfb2faa37c35bafb24fa84153c44a0e1ddfb69494aee5cc5b8',
    'TSPD_101': '0868f8be6fab28005120314bc642ee1d05a3d10e189fd62ad9d83e991151b5dbdbb3b859679f6ce896e7727d9e83129a08ad6b34da0518008c6f5a6480eba1935ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800b4a171a891e04e073c050a93cad82ac7c6f29bc8d19226af4cc1acd0982828255940dad6573e8ac50869b92fac1720000c9352a2855f31e2f14c36bc7beb8fcfa3ddf43fae6fbd44d356bc6f1e124df2',
    'TS5220f739029': '0868f8be6fab28000598f78a25b23823c1ed7f5b67278eb00f92877546c5ec7b056b0540c4cc799748f3d4aeb69fa843',
    'TSf1edb2d2027': '0868f8be6fab20000c95f4451aa221b5ca54ab112c29553337f7331685674968b858faae687a85ee083e85fc1a1130008d810c1eefa0e6f587cde5b1916f353ff237ed9b60e9940399c3a57a6ba6a1c8ce51e38a6149a3cfd8712c55357acddd',
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
    'x-xsrf-token': '4ad720b4-5dc2-445a-8687-37f58ec13097',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=OKMPPADFONKPIPMGIHJBJGGNNIDOFHGIGIEBJCJKBGBDBEONPGHPODPNFJCIAMODBECDDPDGOLPHLOECNCEAGCCFJMLJFIICEGBLDNCLNAEBDMJCMDKGBBJGHGMNCHPN; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; f5avraaaaaaaaaaaaaaaa_session_=DJKFNDCKNJONIPPCBBDANHDMJFHCFKIKMNGGNBKABEMPGKJMECDCHBJODECEEFNFDJCDOMNLACFHNMDMAPIABICLNMLFBLIMFGMDHGDILAHBKADJKBMCCGAFKDKPIIEA; db8ca2b43ed851cc93e71fd5fd72bff7=b4510136b164f28477db8bdb9d53569d; XSRF-TOKEN=4ad720b4-5dc2-445a-8687-37f58ec13097; SESSION=08963849-222a-4c55-b080-738aa9fb312b; TS018af012=0167a1c8615074aaaf4d48b05738fbcfa25a78daf2ff562f24034f7e425f6acb736cb2e17b1789cbc2cd1731ed9d6dc87b43b60727f31f0c9dfa4bccd0de3e297dd6dc008a526aa6c2b5b6100ca0e92c30ee171358; TS00000000076=0868f8be6fab2800f3bfc05eec9eaa378e89b7f22a8d3470ee998ab6e9311d0627880a5c9cdafbe06cf3196de3a00cec082cd787c709d000908deef8be85bdf365554434a12cab45295a3ee130845aa11aff06d19ab76ed330fc37c4857be406730f4a0c708bbf52383eded43bd4e944a1f4d9056d67b9258ccb6cfcc9270c3071a2599321764461c1b4d40d1b79618f9e6a1d1af010bfb9f8cbbf915d20e533b6b35b99865663a414d6a60818c87d5e7e46256eb7eee3385e4d195c631b36ea50d9c02f57954f2756cd2ecf876e4babe5406f17677e7d82892fc1ba9ee14247908e2a7758a4b198900cadc56ed96429f532c1f862035cdf1237ad982e208162ff057c294ab02885; TSPD_101_DID=0868f8be6fab2800f3bfc05eec9eaa378e89b7f22a8d3470ee998ab6e9311d0627880a5c9cdafbe06cf3196de3a00cec082cd787c7063800edc5287dde8e414d5092c2d6e51896971f32ac11d2a1afb1e51789c28e3113dd870b9f555612711e751cefd7f27035c203598664adaa69b1; TS011f2d1a=01266d26d09e07713d21655d1f384afcba9bbca1b75cac0988348c2cbfb2faa37c35bafb24fa84153c44a0e1ddfb69494aee5cc5b8; TSPD_101=0868f8be6fab28005120314bc642ee1d05a3d10e189fd62ad9d83e991151b5dbdbb3b859679f6ce896e7727d9e83129a08ad6b34da0518008c6f5a6480eba1935ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800b4a171a891e04e073c050a93cad82ac7c6f29bc8d19226af4cc1acd0982828255940dad6573e8ac50869b92fac1720000c9352a2855f31e2f14c36bc7beb8fcfa3ddf43fae6fbd44d356bc6f1e124df2; TS5220f739029=0868f8be6fab28000598f78a25b23823c1ed7f5b67278eb00f92877546c5ec7b056b0540c4cc799748f3d4aeb69fa843; TSf1edb2d2027=0868f8be6fab20000c95f4451aa221b5ca54ab112c29553337f7331685674968b858faae687a85ee083e85fc1a1130008d810c1eefa0e6f587cde5b1916f353ff237ed9b60e9940399c3a57a6ba6a1c8ce51e38a6149a3cfd8712c55357acddd',
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