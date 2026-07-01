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
    'f5avraaaaaaaaaaaaaaaa_session_': 'GBAIMPFMBDKDIBFGNGBDPGBNIGGBPNIMKIOALEJEPEFILJFOJCLGIGOLILNMBJBNAOEDPMBMEBAIJKPAAFBAGIGBJKJFGCNGNAIIGLNBCAHGGCDODDDGOIIBCPHIOLPM',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'fa562932fc28ca0b3fccefa0da837e6b',
    'XSRF-TOKEN': '897c433f-58c1-4253-90b1-7eb38362df83',
    'SESSION': '4cfb8850-d36e-4acd-a4f1-08070b777dcf',
    'TS0151fc2b': '0167a1c861288f80d3d03a5e3ca14697c52497ea975730c88fb89608749b8707af5cc945ff5582d242a8f3a5695dc2f0ea735260a1',
    'TS011f2d1a': '01266d26d001358faf86dd1d3e560c98e0c1c10456ef66e59539fbd9e7e3a42ba161e6c8601fc5c0282933346733b6acdaf7f9d244',
    'TSPD_101': '0868f8be6fab28009f225068e8465a76f89dd69ba71c3745336619aadb1fc168e06d2642d5819f1b3f4f02c55875b18a08c56a25b00518001ba7009bd52757495ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'GONPPJLGOCIFKKPMOBBMFJBIKFMFCOHFMDDNHIBCACLANDICEAPCAFADJDJHIMNPBKCDHHLGOBIIPCNJJHNAJLGOJKODFIHLMDNFKJLFCHBCKFCIKCLJBGDLKBFMBNNK',
    'TS00000000076': '0868f8be6fab28003aee5a91d56fbfe78afd15e9901a3c032a2c2e0bda5e48f6677c9e45ad474d9eddc995a19362aa6308aadeb4b809d000b6f95a29b2e34cab83fe6d2931cc9de79373ad979579786dd49d5f9286200681004af7529d0e11d3cf62a55d7c5eaa858c1c7c1d4d8dcd8b7be09dd8c43f0c91025ab5979172b3c2886b84ed4100e4900ca0d4602a2996805b3f47cb5ee12688711b85d60121c5f2b7573739e16b471bf270edadf9607ffdf127a768ffbb97b7da09196eb200cc1384491ac6d6bd051548f804790828ca1e8558b0b3c7a4471ce0446ba98c83098432f76e51b578099a47b0c151359d24abc0e819977075e39de1b887a3e3a75828136c6f0d3e109065',
    'TSPD_101_DID': '0868f8be6fab28003aee5a91d56fbfe78afd15e9901a3c032a2c2e0bda5e48f6677c9e45ad474d9eddc995a19362aa6308aadeb4b8063800d856cb599c7fd8c1c471a7c8b34a5775bf4f9cf09e7d6cb218ad9921e4343cbb4c949266811830d15d8701c67554ada2857feab5cbc52f1e',
    'TS5220f739077': '0868f8be6fab2800cf166cd442540aefd6b178cc60ff35e6210f75439b9eb73b1c5677e6e81c7badd6567c29766173a9085d32c4fe17200069b012663cb372b7af820fafbe5a00678b701e1d850639d732f0069754d3b079',
    'TS5220f739029': '0868f8be6fab2800af3ae48497f9eae082e725007555e7bee375fc0a32f49a80a1de905804099e68cb432ceaa94101db',
    'TSf1edb2d2027': '0868f8be6fab200036cc2ec6faa62c0ba9a15debb92444745ac988e9d0a08441fb75bfde7835c4670894f88350113000fa967467531b584f3a9c58ce3b3f39a4001f7a03f9866dbef8d5e1d34369ce0ddc949b3794c3e25f4c719a42f29d0a96',
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
    'x-xsrf-token': '897c433f-58c1-4253-90b1-7eb38362df83',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=GBAIMPFMBDKDIBFGNGBDPGBNIGGBPNIMKIOALEJEPEFILJFOJCLGIGOLILNMBJBNAOEDPMBMEBAIJKPAAFBAGIGBJKJFGCNGNAIIGLNBCAHGGCDODDDGOIIBCPHIOLPM; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; db8ca2b43ed851cc93e71fd5fd72bff7=fa562932fc28ca0b3fccefa0da837e6b; XSRF-TOKEN=897c433f-58c1-4253-90b1-7eb38362df83; SESSION=4cfb8850-d36e-4acd-a4f1-08070b777dcf; TS0151fc2b=0167a1c861288f80d3d03a5e3ca14697c52497ea975730c88fb89608749b8707af5cc945ff5582d242a8f3a5695dc2f0ea735260a1; TS011f2d1a=01266d26d001358faf86dd1d3e560c98e0c1c10456ef66e59539fbd9e7e3a42ba161e6c8601fc5c0282933346733b6acdaf7f9d244; TSPD_101=0868f8be6fab28009f225068e8465a76f89dd69ba71c3745336619aadb1fc168e06d2642d5819f1b3f4f02c55875b18a08c56a25b00518001ba7009bd52757495ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=GONPPJLGOCIFKKPMOBBMFJBIKFMFCOHFMDDNHIBCACLANDICEAPCAFADJDJHIMNPBKCDHHLGOBIIPCNJJHNAJLGOJKODFIHLMDNFKJLFCHBCKFCIKCLJBGDLKBFMBNNK; TS00000000076=0868f8be6fab28003aee5a91d56fbfe78afd15e9901a3c032a2c2e0bda5e48f6677c9e45ad474d9eddc995a19362aa6308aadeb4b809d000b6f95a29b2e34cab83fe6d2931cc9de79373ad979579786dd49d5f9286200681004af7529d0e11d3cf62a55d7c5eaa858c1c7c1d4d8dcd8b7be09dd8c43f0c91025ab5979172b3c2886b84ed4100e4900ca0d4602a2996805b3f47cb5ee12688711b85d60121c5f2b7573739e16b471bf270edadf9607ffdf127a768ffbb97b7da09196eb200cc1384491ac6d6bd051548f804790828ca1e8558b0b3c7a4471ce0446ba98c83098432f76e51b578099a47b0c151359d24abc0e819977075e39de1b887a3e3a75828136c6f0d3e109065; TSPD_101_DID=0868f8be6fab28003aee5a91d56fbfe78afd15e9901a3c032a2c2e0bda5e48f6677c9e45ad474d9eddc995a19362aa6308aadeb4b8063800d856cb599c7fd8c1c471a7c8b34a5775bf4f9cf09e7d6cb218ad9921e4343cbb4c949266811830d15d8701c67554ada2857feab5cbc52f1e; TS5220f739077=0868f8be6fab2800cf166cd442540aefd6b178cc60ff35e6210f75439b9eb73b1c5677e6e81c7badd6567c29766173a9085d32c4fe17200069b012663cb372b7af820fafbe5a00678b701e1d850639d732f0069754d3b079; TS5220f739029=0868f8be6fab2800af3ae48497f9eae082e725007555e7bee375fc0a32f49a80a1de905804099e68cb432ceaa94101db; TSf1edb2d2027=0868f8be6fab200036cc2ec6faa62c0ba9a15debb92444745ac988e9d0a08441fb75bfde7835c4670894f88350113000fa967467531b584f3a9c58ce3b3f39a4001f7a03f9866dbef8d5e1d34369ce0ddc949b3794c3e25f4c719a42f29d0a96',
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