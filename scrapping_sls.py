import pandas as pd
import requests
import os
import random
import tempfile
from datetime import datetime
import schedule
import time
from config_se2026 import NAMA_KABUPATEN, BASE_PATH, LATEST_FILE, archive_filename

# ================= SETTINGS =================
URL_DATA = 'https://fasih-sm.bps.go.id/app/api/analytic/api/v2/assignment/report-progress-by-responsibility' 
base_path = BASE_PATH                #FOLDER UNTUK MENYIMPAN DATA HASIL SCRAPPING
# ==========================================================


# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'f5avraaaaaaaaaaaaaaaa_session_': 'MBGBALOKOFDMNLELNBFHEEIKHGPMNOJCACKDPFCBLOPAMGNMJADDDCGBNLHELCGDMCEDDBBDOLANOIHLHNHAMIILFNGHALJGBPKENBHOEMLNOPFBNAEKLCGJKHJPHBAF',
    'TS00000000076': '0868f8be6fab28000ca79d12b10422ecae283c124851187e347398037176a29412dd4f9af96dfcda3eb0559739d5cdbe0899e111d109d000179748731780df09527e13340b663ca55a07f38713c83c5c8be24486273ba53617968c12afc549bd3426883a18839a2dec96514c286b9e4962347eaf5e36a2dc328b825e18b559d7db83ab6cb0aeb897093d77ee0c29579c2463f0a2943b8157606cc1d2b9e73fc312189319205caa58c3f88feaaa6b843b17880e1389a6b2a0f35645e1c621d4c1d188274c1335972091f36acd51085610a6f2e42dfff8d1f7f64bc5fc0e489f54bbaa5e967a813d0afe0efcd919555498217d67faa0cb800cfbf7ec76518aa4384c2b47eb6a40e696',
    'TSPD_101_DID': '0868f8be6fab28000ca79d12b10422ecae283c124851187e347398037176a29412dd4f9af96dfcda3eb0559739d5cdbe0899e111d10638002c56ee381fdf265ee1e98224d826027f45059ecc95754bad318dd0f637386e381c3d3d79314c9a539e0fbc274a4ad26ab089ef0cb38bde72',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '44048ff20d1e9ce712c2ca49f2efeaa9',
    'TS011f2d1a': '01266d26d00f64d0188fb347b6094e7aca60759f926b57810d16d6d5944faf8eb0221f71bd2d7378cceaa19bec86f2fd85be12b01a',
    'TSPD_101': '0868f8be6fab2800c6c2b570fd95a3189f1a0688625847f3f017140b9c787ebf36fee27d72edf116dc858690a303d87808f7f568ac05180077e1cff193fb1dff5ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': '45a57c9f-83c3-4d63-b155-22a0af102542',
    'SESSION': '77738260-4ddb-40a5-bbec-72820e64acc5',
    'TS5220f739077': '0868f8be6fab2800e8ad6ed23ee60ffab011307cc11a386c5dab00720c8cbf9920a352e4f7dc5eeaa25aece3c2b58bd008ea09f86b172000fc71d45a9d572741c3c8117b7376d457e14e4c39308cc475d4bbd34cb5b72b46',
    'TS5220f739029': '0868f8be6fab2800374560a75ee7b06d66a0eab16d2e473715760a41e17bd9cfeb73f0c0c08e7b3f64a3dc5beaa4ff9f',
    'TSf1edb2d2027': '0868f8be6fab2000dab56672a4f40ca2d336de5e50f2d0807685f854d4bea259ddbe014947c13b4508103d110111300024c77cb089abdd03eaf193b11d33d67a3b30d86d3b71db0a081f69bcf06412dea691dafdf99c84b09ef682e4a0a23fc9',
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
    'x-xsrf-token': '45a57c9f-83c3-4d63-b155-22a0af102542',
    # 'cookie': 'cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; f5avraaaaaaaaaaaaaaaa_session_=MBGBALOKOFDMNLELNBFHEEIKHGPMNOJCACKDPFCBLOPAMGNMJADDDCGBNLHELCGDMCEDDBBDOLANOIHLHNHAMIILFNGHALJGBPKENBHOEMLNOPFBNAEKLCGJKHJPHBAF; TS00000000076=0868f8be6fab28000ca79d12b10422ecae283c124851187e347398037176a29412dd4f9af96dfcda3eb0559739d5cdbe0899e111d109d000179748731780df09527e13340b663ca55a07f38713c83c5c8be24486273ba53617968c12afc549bd3426883a18839a2dec96514c286b9e4962347eaf5e36a2dc328b825e18b559d7db83ab6cb0aeb897093d77ee0c29579c2463f0a2943b8157606cc1d2b9e73fc312189319205caa58c3f88feaaa6b843b17880e1389a6b2a0f35645e1c621d4c1d188274c1335972091f36acd51085610a6f2e42dfff8d1f7f64bc5fc0e489f54bbaa5e967a813d0afe0efcd919555498217d67faa0cb800cfbf7ec76518aa4384c2b47eb6a40e696; TSPD_101_DID=0868f8be6fab28000ca79d12b10422ecae283c124851187e347398037176a29412dd4f9af96dfcda3eb0559739d5cdbe0899e111d10638002c56ee381fdf265ee1e98224d826027f45059ecc95754bad318dd0f637386e381c3d3d79314c9a539e0fbc274a4ad26ab089ef0cb38bde72; db8ca2b43ed851cc93e71fd5fd72bff7=44048ff20d1e9ce712c2ca49f2efeaa9; TS011f2d1a=01266d26d00f64d0188fb347b6094e7aca60759f926b57810d16d6d5944faf8eb0221f71bd2d7378cceaa19bec86f2fd85be12b01a; TSPD_101=0868f8be6fab2800c6c2b570fd95a3189f1a0688625847f3f017140b9c787ebf36fee27d72edf116dc858690a303d87808f7f568ac05180077e1cff193fb1dff5ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=45a57c9f-83c3-4d63-b155-22a0af102542; SESSION=77738260-4ddb-40a5-bbec-72820e64acc5; TS5220f739077=0868f8be6fab2800e8ad6ed23ee60ffab011307cc11a386c5dab00720c8cbf9920a352e4f7dc5eeaa25aece3c2b58bd008ea09f86b172000fc71d45a9d572741c3c8117b7376d457e14e4c39308cc475d4bbd34cb5b72b46; TS5220f739029=0868f8be6fab2800374560a75ee7b06d66a0eab16d2e473715760a41e17bd9cfeb73f0c0c08e7b3f64a3dc5beaa4ff9f; TSf1edb2d2027=0868f8be6fab2000dab56672a4f40ca2d336de5e50f2d0807685f854d4bea259ddbe014947c13b4508103d110111300024c77cb089abdd03eaf193b11d33d67a3b30d86d3b71db0a081f69bcf06412dea691dafdf99c84b09ef682e4a0a23fc9',
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

        if response.status_code != 200:
            print(f"❌ Error di page {page}")
            print(f"Status Code: {response.status_code}")
            print(response.text[:1000])
            break

        json_res = response.json()
        data_block = json_res.get("data", {})
        data = data_block.get("content", [])
        is_last = data_block.get("last", True)

        print(f"📄 Page {page} | jumlah data: {len(data)} | last: {is_last}")

        # 🔽 Flatten
        for user in data:
            for region in user.get("regionSummary", []):
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

                all_rows.append(row)

        if is_last:
            print("✅ Sudah sampai halaman terakhir")
            break

        page += 1
        time.sleep(random.uniform(1, 2))  # delay acak 1-3 detik antar request

    if all_rows:
        save_and_merge(all_rows)

    print("🎉 Semua data berhasil disimpan!")


def job():
    print(f"\n[+] Memulai proses scraping pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_data()
    auto_push_github()

if __name__ == "__main__":
    # Menjadwalkan job setiap 1 jam
    schedule.every(3).hours.do(job)

    print("⏱️  Script berjalan otomatis setiap 3 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)