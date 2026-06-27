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
    'f5avraaaaaaaaaaaaaaaa_session_': 'JLICHBKPGDCGPEOLIKHDEFGEAODPJENBHFEEDINCCFEGPDOBDCKJAKENNHFLFCJNBFCDJMNPHNKEKLFBENJANGDNMNOIIGDIJOPMHMOJBCPAFOCMNKHNFMKCEANKCHLH',
    'TS00000000076': '0868f8be6fab2800c2b3ec4c4edbdcbf644508a5da3e03a23119eb5622c85c2c9046d7f04d96d9c57d5ee3abbd8787d208feaddcc909d000059da88b2bd5a11651a3346913822c51461747d9696ff0d4f24c4a1f78aafe47ff1ad4c1b988a47ecdc316342489219b31f25f92f037f80e7affd5b24bdd061530bea6e52d49b570a762f7e494ce1ab25ffa66fbe13b475b02aa6678712291a54f7c9d65838a977f024db55cbaaf19c151351545dba501ca22fa1a29a2574aa8af3938ba830ef04581ec02961ad60099241ee22a2d0a716bda2e19f207d7fa91d2c30656d2dd6b3b13ebd8638c4ef286f338c646942c2af801f55c2a80ed8f3ecf9307b155a1cf750663465255aff6d8',
    'TSPD_101_DID': '0868f8be6fab2800c2b3ec4c4edbdcbf644508a5da3e03a23119eb5622c85c2c9046d7f04d96d9c57d5ee3abbd8787d208feaddcc9063800cd704e10117a55e66035853900755e715e2baf96a5a6efff18666b71aacd716f0cbbd798176140f68cd6a6e49a1c36157cbc58e744afc73c',
    'TS011f2d1a': '01266d26d0063e273bc11618d386e9f29a94faedfc5fb00cccacfb54e471ee335ab90a79a464170bf1d532e04b7c1169076a173369',
    'TSPD_101': '0868f8be6fab28000cad452e10b91ceeecc2822e2bac17577628be74678bd0499ebe1a46dc19d6446514d3f525c5634f08edb544b0051800811bc8965452a8a45ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': 'cb7567eb-145a-4e0b-8730-3ea495de0998',
    'SESSION': 'bf4aac87-f256-4a7c-9fd3-f1cc0d35fe3b',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '9659465e252a0faffcb932a11d8b78ba',
    'TS5220f739077': '0868f8be6fab2800f5bf99528013cf5aa2daa200ad8ae20e31906d6c81148ade35dec08a1e5b35771b34e9fa543ba9ff0819785401172000b72477ed81876b6e91611c7090382364733f43653baa10abf4685f3b65099e38',
    'TS5220f739029': '0868f8be6fab2800990dbcd880e6f385a18c5d39cc2c1982eedc6d3099b147219b26dfa8a2a3cbcc696fc6840c59baa9',
    'TSf1edb2d2027': '0868f8be6fab2000b8344fc5da5461f23d37ba4914730487e66faec3f41de95b17db520c382af2d0088102addc113000c7323651af3c1161d4f5c98687cd44fe67df9eea3b70731e4f0c1f2d8ea0fc61a91e791c5c5a0bafb50cef9674c46f1c',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"iOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
    'x-xsrf-token': 'cb7567eb-145a-4e0b-8730-3ea495de0998',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=JLICHBKPGDCGPEOLIKHDEFGEAODPJENBHFEEDINCCFEGPDOBDCKJAKENNHFLFCJNBFCDJMNPHNKEKLFBENJANGDNMNOIIGDIJOPMHMOJBCPAFOCMNKHNFMKCEANKCHLH; TS00000000076=0868f8be6fab2800c2b3ec4c4edbdcbf644508a5da3e03a23119eb5622c85c2c9046d7f04d96d9c57d5ee3abbd8787d208feaddcc909d000059da88b2bd5a11651a3346913822c51461747d9696ff0d4f24c4a1f78aafe47ff1ad4c1b988a47ecdc316342489219b31f25f92f037f80e7affd5b24bdd061530bea6e52d49b570a762f7e494ce1ab25ffa66fbe13b475b02aa6678712291a54f7c9d65838a977f024db55cbaaf19c151351545dba501ca22fa1a29a2574aa8af3938ba830ef04581ec02961ad60099241ee22a2d0a716bda2e19f207d7fa91d2c30656d2dd6b3b13ebd8638c4ef286f338c646942c2af801f55c2a80ed8f3ecf9307b155a1cf750663465255aff6d8; TSPD_101_DID=0868f8be6fab2800c2b3ec4c4edbdcbf644508a5da3e03a23119eb5622c85c2c9046d7f04d96d9c57d5ee3abbd8787d208feaddcc9063800cd704e10117a55e66035853900755e715e2baf96a5a6efff18666b71aacd716f0cbbd798176140f68cd6a6e49a1c36157cbc58e744afc73c; TS011f2d1a=01266d26d0063e273bc11618d386e9f29a94faedfc5fb00cccacfb54e471ee335ab90a79a464170bf1d532e04b7c1169076a173369; TSPD_101=0868f8be6fab28000cad452e10b91ceeecc2822e2bac17577628be74678bd0499ebe1a46dc19d6446514d3f525c5634f08edb544b0051800811bc8965452a8a45ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=cb7567eb-145a-4e0b-8730-3ea495de0998; SESSION=bf4aac87-f256-4a7c-9fd3-f1cc0d35fe3b; db8ca2b43ed851cc93e71fd5fd72bff7=9659465e252a0faffcb932a11d8b78ba; TS5220f739077=0868f8be6fab2800f5bf99528013cf5aa2daa200ad8ae20e31906d6c81148ade35dec08a1e5b35771b34e9fa543ba9ff0819785401172000b72477ed81876b6e91611c7090382364733f43653baa10abf4685f3b65099e38; TS5220f739029=0868f8be6fab2800990dbcd880e6f385a18c5d39cc2c1982eedc6d3099b147219b26dfa8a2a3cbcc696fc6840c59baa9; TSf1edb2d2027=0868f8be6fab2000b8344fc5da5461f23d37ba4914730487e66faec3f41de95b17db520c382af2d0088102addc113000c7323651af3c1161d4f5c98687cd44fe67df9eea3b70731e4f0c1f2d8ea0fc61a91e791c5c5a0bafb50cef9674c46f1c',
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