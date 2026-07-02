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
    'f5avraaaaaaaaaaaaaaaa_session_': 'IMGEHCPIODAJJLLKAIDLANGCFMFIDAPCBOLMHAKEJLDOFJJGMDNKBALELFFCIHFCDPGDJHAKCFODIMNLDALAGJIMDFEJHEMKKBIJGFDDIIDGEGAODPAKLEOBBMEGJHPH',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'fa562932fc28ca0b3fccefa0da837e6b',
    'XSRF-TOKEN': '897c433f-58c1-4253-90b1-7eb38362df83',
    'JSESSIONID': '5DC74262F6F8C9E391AC5A56EFC8BC38',
    'SESSION': '4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b',
    'TS018af012': '0167a1c861d9f977d4ad34e59cc2f2b52eb25fc8d733b35d035cd9387fb248da0d6971119ddb6065e8bcd76d559f196190f1eda48e5e0a4aeb8cf3e131cb6f5f214191995763171114b01df82acaff237db0c5b9a7',
    'TS0151fc2b': '0167a1c8610a0fa7db56cc7c61b2f0563ff035091a191943ae422dee95bcdfdd8f2247135be641a92a5a2cfa49690e7bd9227a45d0',
    'TS00000000076': '0868f8be6fab28005f306d49c9d3c8932a6b568fd4c8ebb3588ac9c64971bdf3aca993269101fa6f7590c562e919f0a508ac95f72c09d000e8d7c51769e548736c4bf5b274d951595e8a4a9f1fa29fb4657670a0f52e1180f09c53775190976a67573d043aabeabd8e1a2f9b466d31c3e32ca5fde92d4f46a9e932252b67000a148c87759337b640a9d7ac281432e548e00946d44b200760d13837354c0950fbd3f09560d60672a9b59f40617c1b68e5bf5f80b3a97ba34a661a8e0bc6571b67d6d6dd5026b43b0f25360275368b8189ae000d06ad5634fffdb4a39fe0b1b6076232ccb24bff7b0925b69fe8f0ebb8db11ccb3152052f373110c04356a5cb318fc50f9ffa1586896',
    'TSPD_101_DID': '0868f8be6fab28005f306d49c9d3c8932a6b568fd4c8ebb3588ac9c64971bdf3aca993269101fa6f7590c562e919f0a508ac95f72c063800fb1516c052a9211066acc64929fe120c6d215cb5d5ec0b50ecf17e8d046a9bf727369acb1eb388ce3a1ad7f763c82e4f1d5bb632c258f8ff',
    'TS011f2d1a': '01266d26d019cd02b482e7b2ed49f153be7fdbad83c755096832ec227adcc47a128fc4f89aad2b2cce9ee77be1a907be5faf5dc747',
    'TSPD_101': '0868f8be6fab2800ba5c3463f8a7f7382279f4e4c388c0c0ff0ed675cc8e1f4dfbb0f3790eafefaf8b9e597cfe0d453e083c9a59cf0518007d5e33088576536c5ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'PJGKHCGGBFCDIOGBPIBLIBCFPEFBBEDBLLBICFNJIEGFFHAKDEKNKJFCHHNIFBGKEKGDNBDBFFLBINMAPIIALCHAEFOOFKPFOLNOKPDMNDGOBCPIOJNKOKHMLPGGNEBL',
    'TS5220f739077': '0868f8be6fab28003dfd89fa5230d86880b65bc4691b094d41ecf4d75db79166e476a91889a5369b49b8ebad15cf3dd008efda4d8017200075493d10644a8f533b11f0ed105e728a49edddfaadb389c3d06fae0ce931a7c8',
    'TS5220f739029': '0868f8be6fab28006816bb8abc460a65e2aaa016b3d08b33d9dcf42e5fb385ba740bbcb6275b646586663249ce0074ad',
    'TSf1edb2d2027': '0868f8be6fab20009b74a238e34cb6f0c2b15b96e9b4f61647cb787df8badf77007d23d251b7cfbd082b87e567113000878d67727dcb23a2665b5682d72fb1ef5b9ad9555a64302e2ef691ff196ad1ceb2a79179dd7293741b23887e9093894a',
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
    # 'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=IMGEHCPIODAJJLLKAIDLANGCFMFIDAPCBOLMHAKEJLDOFJJGMDNKBALELFFCIHFCDPGDJHAKCFODIMNLDALAGJIMDFEJHEMKKBIJGFDDIIDGEGAODPAKLEOBBMEGJHPH; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; db8ca2b43ed851cc93e71fd5fd72bff7=fa562932fc28ca0b3fccefa0da837e6b; XSRF-TOKEN=897c433f-58c1-4253-90b1-7eb38362df83; JSESSIONID=5DC74262F6F8C9E391AC5A56EFC8BC38; SESSION=4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b; TS018af012=0167a1c861d9f977d4ad34e59cc2f2b52eb25fc8d733b35d035cd9387fb248da0d6971119ddb6065e8bcd76d559f196190f1eda48e5e0a4aeb8cf3e131cb6f5f214191995763171114b01df82acaff237db0c5b9a7; TS0151fc2b=0167a1c8610a0fa7db56cc7c61b2f0563ff035091a191943ae422dee95bcdfdd8f2247135be641a92a5a2cfa49690e7bd9227a45d0; TS00000000076=0868f8be6fab28005f306d49c9d3c8932a6b568fd4c8ebb3588ac9c64971bdf3aca993269101fa6f7590c562e919f0a508ac95f72c09d000e8d7c51769e548736c4bf5b274d951595e8a4a9f1fa29fb4657670a0f52e1180f09c53775190976a67573d043aabeabd8e1a2f9b466d31c3e32ca5fde92d4f46a9e932252b67000a148c87759337b640a9d7ac281432e548e00946d44b200760d13837354c0950fbd3f09560d60672a9b59f40617c1b68e5bf5f80b3a97ba34a661a8e0bc6571b67d6d6dd5026b43b0f25360275368b8189ae000d06ad5634fffdb4a39fe0b1b6076232ccb24bff7b0925b69fe8f0ebb8db11ccb3152052f373110c04356a5cb318fc50f9ffa1586896; TSPD_101_DID=0868f8be6fab28005f306d49c9d3c8932a6b568fd4c8ebb3588ac9c64971bdf3aca993269101fa6f7590c562e919f0a508ac95f72c063800fb1516c052a9211066acc64929fe120c6d215cb5d5ec0b50ecf17e8d046a9bf727369acb1eb388ce3a1ad7f763c82e4f1d5bb632c258f8ff; TS011f2d1a=01266d26d019cd02b482e7b2ed49f153be7fdbad83c755096832ec227adcc47a128fc4f89aad2b2cce9ee77be1a907be5faf5dc747; TSPD_101=0868f8be6fab2800ba5c3463f8a7f7382279f4e4c388c0c0ff0ed675cc8e1f4dfbb0f3790eafefaf8b9e597cfe0d453e083c9a59cf0518007d5e33088576536c5ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=PJGKHCGGBFCDIOGBPIBLIBCFPEFBBEDBLLBICFNJIEGFFHAKDEKNKJFCHHNIFBGKEKGDNBDBFFLBINMAPIIALCHAEFOOFKPFOLNOKPDMNDGOBCPIOJNKOKHMLPGGNEBL; TS5220f739077=0868f8be6fab28003dfd89fa5230d86880b65bc4691b094d41ecf4d75db79166e476a91889a5369b49b8ebad15cf3dd008efda4d8017200075493d10644a8f533b11f0ed105e728a49edddfaadb389c3d06fae0ce931a7c8; TS5220f739029=0868f8be6fab28006816bb8abc460a65e2aaa016b3d08b33d9dcf42e5fb385ba740bbcb6275b646586663249ce0074ad; TSf1edb2d2027=0868f8be6fab20009b74a238e34cb6f0c2b15b96e9b4f61647cb787df8badf77007d23d251b7cfbd082b87e567113000878d67727dcb23a2665b5682d72fb1ef5b9ad9555a64302e2ef691ff196ad1ceb2a79179dd7293741b23887e9093894a',
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
    schedule.every(1).hours.do(job)

    print("⏱️  Script berjalan otomatis setiap 3 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)