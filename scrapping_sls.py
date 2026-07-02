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
    'f5avraaaaaaaaaaaaaaaa_session_': 'JHLBHNADKMKNDLBNDBECKLGECNIOJHLJEMGBKFELCLBCOPFOHOHNJDPPHODEHACJKCODLKFKGOEEDHHOGGCACKHEADBPELKFMKDPLILJKIOCPNMEFEAGFDFDCCFCOCLD',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'fa562932fc28ca0b3fccefa0da837e6b',
    'XSRF-TOKEN': '897c433f-58c1-4253-90b1-7eb38362df83',
    'JSESSIONID': '5DC74262F6F8C9E391AC5A56EFC8BC38',
    'SESSION': '4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b',
    'TS018af012': '0167a1c861d9f977d4ad34e59cc2f2b52eb25fc8d733b35d035cd9387fb248da0d6971119ddb6065e8bcd76d559f196190f1eda48e5e0a4aeb8cf3e131cb6f5f214191995763171114b01df82acaff237db0c5b9a7',
    'TS0151fc2b': '0167a1c86121c44c673adb4fab3dd03836950011df0e4b0c0410161d0846d2a2a0f5063fa1a1ed426009296a634a202b5f3f6d948e',
    'TS00000000076': '0868f8be6fab2800500df36bf43b1fac683d464a8c1bd9cd801320b658a16655d1ae2953b47cf52da42d2f48cadd564808677ecaf009d0009139d44f9edd821c1eb9dddbbe008f5e1e1411e2a771cb28f66f73c34627119d5b201c911840ae84bab41ba03b723a7bbd14f0907829e613cdf11edbe622a121bc5b610641597a0deaee7cbdf2efbdac84f71a99b3ba1f2ebaab5766d1648793a0a5a9e3fb09bcd2865cf94fe108faa0904c19f92cc3d05dc4021e9a96d9abc93b53ca3877d9d16e99edcb92c684fcea4d4488eeaff68e6f01b451debb97ba41b24135318fc55c867174261930a94f9cef0374e640b5030eb985ead382ff9d52208b16e921771758fea0e6ab905683da',
    'TSPD_101_DID': '0868f8be6fab2800500df36bf43b1fac683d464a8c1bd9cd801320b658a16655d1ae2953b47cf52da42d2f48cadd564808677ecaf0063800743553cf2873349a1087cdee420cbfe6448d4c4c2ebf9f250ae1cec4f67ebc318e6b18d8712c690db07c6b3bb85e021bb4477382f931726a',
    'TS011f2d1a': '01266d26d059c39024c51759e3177464d039640d1349d7a72eb961fe133613acf8ccf5e5a7264da670c83d7a1b520071a6d5bc6405',
    'TSPD_101': '0868f8be6fab280091944099aa704fdf995bd77e80a38bea1eb72cff6ac4dd37f98e0361df2ab3a4a019b72093b39fcf087bb836e205180002b906e0c7930b605ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'DGKPMENIMNBJDODKLDGNMEHLOALGHJIFENIAFNFNDAJCEJNEPENBAKPGJKDKNJIKHJCDIOFNONABKHHJKCHAHJLKPDGJICMCMLCADEFKIPAFLGILKAOGBEBAHMACFIDD',
    'TS5220f739077': '0868f8be6fab280009ee9994a290a045453b57954213c3232cf990cb6ac4323bce212412f3ba9902c578c1f928998b72081c0ecfce17200088d7e95f1e88dc68b00b9259152397a94e4e62331773700bdf68088c0061b34f',
    'TS5220f739029': '0868f8be6fab2800f147b82b59ac12e32fb53b707a6e7383baa29840a1f0552ca34e30bedb3db0abde9eadbb43c4dfba',
    'TSf1edb2d2027': '0868f8be6fab2000b31e42ecf365588707510c15bcf970eaf4a6be295aa0af55c84099bced4ff2ab08b16d60091130007bcb17298af2a28e53a551143ffda5dcc24d6431aa0d97292f624ec579d173ed737666f6c74d734991ec77e9c9af4092',
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
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=JHLBHNADKMKNDLBNDBECKLGECNIOJHLJEMGBKFELCLBCOPFOHOHNJDPPHODEHACJKCODLKFKGOEEDHHOGGCACKHEADBPELKFMKDPLILJKIOCPNMEFEAGFDFDCCFCOCLD; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; db8ca2b43ed851cc93e71fd5fd72bff7=fa562932fc28ca0b3fccefa0da837e6b; XSRF-TOKEN=897c433f-58c1-4253-90b1-7eb38362df83; JSESSIONID=5DC74262F6F8C9E391AC5A56EFC8BC38; SESSION=4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b; TS018af012=0167a1c861d9f977d4ad34e59cc2f2b52eb25fc8d733b35d035cd9387fb248da0d6971119ddb6065e8bcd76d559f196190f1eda48e5e0a4aeb8cf3e131cb6f5f214191995763171114b01df82acaff237db0c5b9a7; TS0151fc2b=0167a1c86121c44c673adb4fab3dd03836950011df0e4b0c0410161d0846d2a2a0f5063fa1a1ed426009296a634a202b5f3f6d948e; TS00000000076=0868f8be6fab2800500df36bf43b1fac683d464a8c1bd9cd801320b658a16655d1ae2953b47cf52da42d2f48cadd564808677ecaf009d0009139d44f9edd821c1eb9dddbbe008f5e1e1411e2a771cb28f66f73c34627119d5b201c911840ae84bab41ba03b723a7bbd14f0907829e613cdf11edbe622a121bc5b610641597a0deaee7cbdf2efbdac84f71a99b3ba1f2ebaab5766d1648793a0a5a9e3fb09bcd2865cf94fe108faa0904c19f92cc3d05dc4021e9a96d9abc93b53ca3877d9d16e99edcb92c684fcea4d4488eeaff68e6f01b451debb97ba41b24135318fc55c867174261930a94f9cef0374e640b5030eb985ead382ff9d52208b16e921771758fea0e6ab905683da; TSPD_101_DID=0868f8be6fab2800500df36bf43b1fac683d464a8c1bd9cd801320b658a16655d1ae2953b47cf52da42d2f48cadd564808677ecaf0063800743553cf2873349a1087cdee420cbfe6448d4c4c2ebf9f250ae1cec4f67ebc318e6b18d8712c690db07c6b3bb85e021bb4477382f931726a; TS011f2d1a=01266d26d059c39024c51759e3177464d039640d1349d7a72eb961fe133613acf8ccf5e5a7264da670c83d7a1b520071a6d5bc6405; TSPD_101=0868f8be6fab280091944099aa704fdf995bd77e80a38bea1eb72cff6ac4dd37f98e0361df2ab3a4a019b72093b39fcf087bb836e205180002b906e0c7930b605ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=DGKPMENIMNBJDODKLDGNMEHLOALGHJIFENIAFNFNDAJCEJNEPENBAKPGJKDKNJIKHJCDIOFNONABKHHJKCHAHJLKPDGJICMCMLCADEFKIPAFLGILKAOGBEBAHMACFIDD; TS5220f739077=0868f8be6fab280009ee9994a290a045453b57954213c3232cf990cb6ac4323bce212412f3ba9902c578c1f928998b72081c0ecfce17200088d7e95f1e88dc68b00b9259152397a94e4e62331773700bdf68088c0061b34f; TS5220f739029=0868f8be6fab2800f147b82b59ac12e32fb53b707a6e7383baa29840a1f0552ca34e30bedb3db0abde9eadbb43c4dfba; TSf1edb2d2027=0868f8be6fab2000b31e42ecf365588707510c15bcf970eaf4a6be295aa0af55c84099bced4ff2ab08b16d60091130007bcb17298af2a28e53a551143ffda5dcc24d6431aa0d97292f624ec579d173ed737666f6c74d734991ec77e9c9af4092',
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