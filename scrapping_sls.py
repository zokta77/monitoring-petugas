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
    'f5avraaaaaaaaaaaaaaaa_session_': 'PGGDNCKKJFJIMIODLDJMNCAGAPDKHJIPNMHJOFBOEPKIPGIKLONMLKLPHGBKOKMPAEODHFOPBOPFKDFJPDGAKMOIAAHPBCHJLODPAFPPPKBHBCEMIEIPNKENEPKKPFPI',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'fa562932fc28ca0b3fccefa0da837e6b',
    'XSRF-TOKEN': '897c433f-58c1-4253-90b1-7eb38362df83',
    'TS018af012': '0167a1c8614c8bf24ee2ab30c1e0f259b1ce18f2cf12da13a72d159674a5afa0fd35e41447b1c65c2668dddef87063b60572ff7fb77b4fec3e7fa51cd77084c5fb7503eef5',
    'JSESSIONID': '5DC74262F6F8C9E391AC5A56EFC8BC38',
    'SESSION': '4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b',
    'TS0151fc2b': '0167a1c8614fe243a3618f70c83bda7bec064e00534ed663f9862905976d3880d69166eb33e474b71b48441308a7de880bba30af24',
    'TS00000000076': '0868f8be6fab2800021c1288c942e279c7c46da0e63756d77049c08eb3ef5514eccb77582a4690384cd5099ab9bb2a6408c516955409d000aac8a2ecea716fc450a1e8601a6b034dfb70edf1b91e54e52980159ad8349add3398e9e3e451c16c28b4c001a7d13dba54afa941eafcd337198bd96db7d19bc4308f824299b513e059ee87acf49cecaf4cc9d95fbe291c109e4d2b179fc129a8872365fb0d51e8a1e045637160e6c7e622f6aa9c86ec67e010a24b51c10d18754fa0ba0b5bc0d4a3c30655293e8d2b5911e49327e778cc8312bafc08237a212a3f181559ec04e196fd0fec76748555709ddf0ef1694ce440a4f6dd442a3c1fcbc7f2329495d0069ab70909cebad07045',
    'TSPD_101_DID': '0868f8be6fab2800021c1288c942e279c7c46da0e63756d77049c08eb3ef5514eccb77582a4690384cd5099ab9bb2a6408c516955406380080cc487bfc07a3ec329e54a6917a8f1c95237851ba60709a992bb8b87960997ea8f6afa999b55056e8467b5d0bb54dcd4db1ce0c2d2612d2',
    'TS011f2d1a': '01266d26d0be6fc893cad12c53aff2872ca47e94496e6d87d439dd5c0e0299f40a805676aa66268182fd4de4fbbf31f7f06d321b5d',
    'TSPD_101': '0868f8be6fab2800967807cf065ff4421d957c66ce50a4fae21d96b1322d3beb94252568a79a9b9be10f04a6b412f268082289c0ca051800a29bf9e6b5b47d385ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'BDADPLLHCBLMJDDIKGABLKCMJOPMBNEDJKPKCHOAEHHLJCMHKPLPDACKAFEPLNMJHGCDOOMNGPLNMBLLMAIAKOBAMAOLKLNDDBKFPIKLKCIJCHLMKMGKCPICLMFFDBJL',
    'TS5220f739077': '0868f8be6fab2800c5af184ff439067741c972aa85a5f0ffb014974e135b728e17513c64f701f1a1f477736dae4285c808f83749351720003e5553599671787e6412e8cf1dbf93e061e691b171af336bd5a7dff3b3a498b4',
    'TS5220f739029': '0868f8be6fab28003f3c4262d1e3c9fcd142ec5d144b6d7cdf2284d2196e8b1cb504aae5fa95324b0e7b628a7da8725c',
    'TSf1edb2d2027': '0868f8be6fab2000465a7afa98cf162abf629bf40a145719b5eaf6251b7cbd2fff9f572ae4096a67089db3213b1130007d7a072a502dc5c191abe118ba549713533fa26f81a5e057ea1c503fd9fe9871203e8dde5d2491d8c73ff6760de9c486',
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
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=PGGDNCKKJFJIMIODLDJMNCAGAPDKHJIPNMHJOFBOEPKIPGIKLONMLKLPHGBKOKMPAEODHFOPBOPFKDFJPDGAKMOIAAHPBCHJLODPAFPPPKBHBCEMIEIPNKENEPKKPFPI; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; db8ca2b43ed851cc93e71fd5fd72bff7=fa562932fc28ca0b3fccefa0da837e6b; XSRF-TOKEN=897c433f-58c1-4253-90b1-7eb38362df83; TS018af012=0167a1c8614c8bf24ee2ab30c1e0f259b1ce18f2cf12da13a72d159674a5afa0fd35e41447b1c65c2668dddef87063b60572ff7fb77b4fec3e7fa51cd77084c5fb7503eef5; JSESSIONID=5DC74262F6F8C9E391AC5A56EFC8BC38; SESSION=4e9e8d5c-96ec-4b65-99e2-d68f52ef0a0b; TS0151fc2b=0167a1c8614fe243a3618f70c83bda7bec064e00534ed663f9862905976d3880d69166eb33e474b71b48441308a7de880bba30af24; TS00000000076=0868f8be6fab2800021c1288c942e279c7c46da0e63756d77049c08eb3ef5514eccb77582a4690384cd5099ab9bb2a6408c516955409d000aac8a2ecea716fc450a1e8601a6b034dfb70edf1b91e54e52980159ad8349add3398e9e3e451c16c28b4c001a7d13dba54afa941eafcd337198bd96db7d19bc4308f824299b513e059ee87acf49cecaf4cc9d95fbe291c109e4d2b179fc129a8872365fb0d51e8a1e045637160e6c7e622f6aa9c86ec67e010a24b51c10d18754fa0ba0b5bc0d4a3c30655293e8d2b5911e49327e778cc8312bafc08237a212a3f181559ec04e196fd0fec76748555709ddf0ef1694ce440a4f6dd442a3c1fcbc7f2329495d0069ab70909cebad07045; TSPD_101_DID=0868f8be6fab2800021c1288c942e279c7c46da0e63756d77049c08eb3ef5514eccb77582a4690384cd5099ab9bb2a6408c516955406380080cc487bfc07a3ec329e54a6917a8f1c95237851ba60709a992bb8b87960997ea8f6afa999b55056e8467b5d0bb54dcd4db1ce0c2d2612d2; TS011f2d1a=01266d26d0be6fc893cad12c53aff2872ca47e94496e6d87d439dd5c0e0299f40a805676aa66268182fd4de4fbbf31f7f06d321b5d; TSPD_101=0868f8be6fab2800967807cf065ff4421d957c66ce50a4fae21d96b1322d3beb94252568a79a9b9be10f04a6b412f268082289c0ca051800a29bf9e6b5b47d385ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=BDADPLLHCBLMJDDIKGABLKCMJOPMBNEDJKPKCHOAEHHLJCMHKPLPDACKAFEPLNMJHGCDOOMNGPLNMBLLMAIAKOBAMAOLKLNDDBKFPIKLKCIJCHLMKMGKCPICLMFFDBJL; TS5220f739077=0868f8be6fab2800c5af184ff439067741c972aa85a5f0ffb014974e135b728e17513c64f701f1a1f477736dae4285c808f83749351720003e5553599671787e6412e8cf1dbf93e061e691b171af336bd5a7dff3b3a498b4; TS5220f739029=0868f8be6fab28003f3c4262d1e3c9fcd142ec5d144b6d7cdf2284d2196e8b1cb504aae5fa95324b0e7b628a7da8725c; TSf1edb2d2027=0868f8be6fab2000465a7afa98cf162abf629bf40a145719b5eaf6251b7cbd2fff9f572ae4096a67089db3213b1130007d7a072a502dc5c191abe118ba549713533fa26f81a5e057ea1c503fd9fe9871203e8dde5d2491d8c73ff6760de9c486',
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