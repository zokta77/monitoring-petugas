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
    'f5avraaaaaaaaaaaaaaaa_session_': 'KODGALDIKOMAINBBKNADMLLKGMIKGOPDFAPCHOMJMLCBHBBIOBDHLMHPMJDBBOODKIGDGEHHCLGNPDDLDHAALDJMENDLFDFLHNDGBIEMJHFMIDNCHBDAKFBONGJGOJJP',
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'XSRF-TOKEN': 'a0133170-2394-4410-a45f-7fdcfa536a98',
    'TS01acc472': '01266d26d0c8fa101b76957a535af6abce5288e28796075317c8c9dfb17807c2af6ad91b19e6d051fb8a0870acfaf009a9cff3cc35cadfb9bfa2c681971af2051f829e8e761d8b9a276a92d9d46f8491174618a3169b167b8dbc226c9ad2a57a93b46f5cf83fa05525a764d9a38973d8a81aca6400571dc9cf7b0295441f27b445a8de24d5',
    'TS0151fc2b': '0167a1c8614f1f392238e30e1052d0859ce87658222bfdd28fcfabd2fb05ca9e97d8eabb0f123a21a26bf06a9e863420eaeec81e73',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '17a35dd725f4402b9f56894dd2b0d876',
    'SESSION': 'a9d6bfa3-0a58-469d-869c-6aa320994eda',
    'f5avraaaaaaaaaaaaaaaa_session_': 'HFNMLAMHBNANAOFOIOHBLFFCLFDJMODDPGMHGKDPDDGCHDMPLNAKNFLPJOEJGJLPIDIDCGIDAKIILJEKFFOAIHNGMNILMHLNMOPPOJEFOIDHAPLJFIMJGNGGPKPGOJAJ',
    'TS00000000076': '0868f8be6fab2800afc5c104f789ef7db177a8942fc7d3cbcfcb3641a2dc3d664f3675e6090cc7641e439425b90d2480080fd3be9909d000a95eceb1761efa8da7cf86e2c653029d07a9bc1ea08e601348f7aaf0ccbd58299be408ecb73d6bc36f7e37230303b28edb2067f6657e77dd289b0a4b3744e178e70fa7321d3b525222a0b4faea92fb1e09cafa2eb1ac628ef8661b0a88471dc626ef6a57c63c1e7646ed5f75e6ed90a67cb0af4d3408bc644d8cf148a01ae5158d3dc6969031741414078c8585c6ccc8332c485399351e607fd5120d0123eb4330daebb3e874308c85c3366718ac362baf65293749253896b34a1ca2b8496317f63ca2d713404502cbedaa490d15e4b8',
    'TSPD_101_DID': '0868f8be6fab2800afc5c104f789ef7db177a8942fc7d3cbcfcb3641a2dc3d664f3675e6090cc7641e439425b90d2480080fd3be9906380031ea0e8b8553916fed48a9e13bd6cb6dbca220d02b0f47b02859a3b37c6d22011e43f7f13219ba24ab52d5a8386780f39c39dc1edf7c7170',
    'TS011f2d1a': '01266d26d0676cc14efac1abb51e673f73d5dc5901619923ce569449c6f60f13a53be2702c2a39275bac7820a93620945022f07345',
    'TSPD_101': '0868f8be6fab2800508e5b06eb722a2cf6b9df50ec66f022a1d89ffba3e466a1f0a41127c2f04dfe0a757e92c143d037089d0a618c051800c642638227c739285ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab280029cf704f2c846fad96b6b980b8342a94abd9918e190185e79feee176408fabeb55f87219b6c36f970853951e92172000a4ec565dd048593b750a39f8997484afd12cb5bee2024db6fbb03f676a270540',
    'TS5220f739029': '0868f8be6fab2800678ab31a973fdeb56bf1a11c4f922eb3ceeade9557c4a6b8a6536b915a207eb6a5c83eda410e3805',
    'TSf1edb2d2027': '0868f8be6fab20009797cf17d219b8025171af6034ec0bdc77c07c51e6859ae91b6fa31c2304f4dc085767b37c1130006489aac2e4fe10770361d7a9d5d9e1d95d612eabf2c6961d73b472458a48641c8df993d7592c6a7214a5a0ff88e614c4',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
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
    'x-xsrf-token': 'a0133170-2394-4410-a45f-7fdcfa536a98',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=KODGALDIKOMAINBBKNADMLLKGMIKGOPDFAPCHOMJMLCBHBBIOBDHLMHPMJDBBOODKIGDGEHHCLGNPDDLDHAALDJMENDLFDFLHNDGBIEMJHFMIDNCHBDAKFBONGJGOJJP; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; XSRF-TOKEN=a0133170-2394-4410-a45f-7fdcfa536a98; TS01acc472=01266d26d0c8fa101b76957a535af6abce5288e28796075317c8c9dfb17807c2af6ad91b19e6d051fb8a0870acfaf009a9cff3cc35cadfb9bfa2c681971af2051f829e8e761d8b9a276a92d9d46f8491174618a3169b167b8dbc226c9ad2a57a93b46f5cf83fa05525a764d9a38973d8a81aca6400571dc9cf7b0295441f27b445a8de24d5; TS0151fc2b=0167a1c8614f1f392238e30e1052d0859ce87658222bfdd28fcfabd2fb05ca9e97d8eabb0f123a21a26bf06a9e863420eaeec81e73; db8ca2b43ed851cc93e71fd5fd72bff7=17a35dd725f4402b9f56894dd2b0d876; SESSION=a9d6bfa3-0a58-469d-869c-6aa320994eda; f5avraaaaaaaaaaaaaaaa_session_=HFNMLAMHBNANAOFOIOHBLFFCLFDJMODDPGMHGKDPDDGCHDMPLNAKNFLPJOEJGJLPIDIDCGIDAKIILJEKFFOAIHNGMNILMHLNMOPPOJEFOIDHAPLJFIMJGNGGPKPGOJAJ; TS00000000076=0868f8be6fab2800afc5c104f789ef7db177a8942fc7d3cbcfcb3641a2dc3d664f3675e6090cc7641e439425b90d2480080fd3be9909d000a95eceb1761efa8da7cf86e2c653029d07a9bc1ea08e601348f7aaf0ccbd58299be408ecb73d6bc36f7e37230303b28edb2067f6657e77dd289b0a4b3744e178e70fa7321d3b525222a0b4faea92fb1e09cafa2eb1ac628ef8661b0a88471dc626ef6a57c63c1e7646ed5f75e6ed90a67cb0af4d3408bc644d8cf148a01ae5158d3dc6969031741414078c8585c6ccc8332c485399351e607fd5120d0123eb4330daebb3e874308c85c3366718ac362baf65293749253896b34a1ca2b8496317f63ca2d713404502cbedaa490d15e4b8; TSPD_101_DID=0868f8be6fab2800afc5c104f789ef7db177a8942fc7d3cbcfcb3641a2dc3d664f3675e6090cc7641e439425b90d2480080fd3be9906380031ea0e8b8553916fed48a9e13bd6cb6dbca220d02b0f47b02859a3b37c6d22011e43f7f13219ba24ab52d5a8386780f39c39dc1edf7c7170; TS011f2d1a=01266d26d0676cc14efac1abb51e673f73d5dc5901619923ce569449c6f60f13a53be2702c2a39275bac7820a93620945022f07345; TSPD_101=0868f8be6fab2800508e5b06eb722a2cf6b9df50ec66f022a1d89ffba3e466a1f0a41127c2f04dfe0a757e92c143d037089d0a618c051800c642638227c739285ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab280029cf704f2c846fad96b6b980b8342a94abd9918e190185e79feee176408fabeb55f87219b6c36f970853951e92172000a4ec565dd048593b750a39f8997484afd12cb5bee2024db6fbb03f676a270540; TS5220f739029=0868f8be6fab2800678ab31a973fdeb56bf1a11c4f922eb3ceeade9557c4a6b8a6536b915a207eb6a5c83eda410e3805; TSf1edb2d2027=0868f8be6fab20009797cf17d219b8025171af6034ec0bdc77c07c51e6859ae91b6fa31c2304f4dc085767b37c1130006489aac2e4fe10770361d7a9d5d9e1d95d612eabf2c6961d73b472458a48641c8df993d7592c6a7214a5a0ff88e614c4',
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