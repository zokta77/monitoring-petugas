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

# ===== PENGATURAN REQUEST SERVER =====
# Ukuran halaman lebih besar mengurangi jumlah request total.
# Jika server menolak ukuran 20, turunkan menjadi 10.
PAGE_SIZE = 5

# Jeda normal antarpages.
PAGE_DELAY_MIN = 5.0
PAGE_DELAY_MAX = 8.0

# Istirahat tambahan secara berkala agar request tidak terus-menerus.
COOLDOWN_EVERY_PAGES = 15
COOLDOWN_MIN_SECONDS = 20
COOLDOWN_MAX_SECONDS = 30

# Penanganan 429. Jika server memberi Retry-After, nilai server diprioritaskan.
MAX_REQUEST_RETRIES = 5
DEFAULT_429_WAIT_SECONDS = 60
MAX_429_WAIT_SECONDS = 15 * 60

# Timeout koneksi dan pembacaan respons.
REQUEST_TIMEOUT = (20, 120)

# ===== KONFIGURASI SELENIUM =====
# Cara cek path: buka chrome://version di profil yang sudah login FASIH
# lihat baris "Profile Path" → folder induknya = CHROME_PROFILE_DIR
CHROME_PROFILE_DIR  = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Profil 1"   # ganti sesuai profil (Default / Profile 1 / dst)
FASIH_HOME_URL      = "https://fasih-sm.bps.go.id/app/"

# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'f5avraaaaaaaaaaaaaaaa_session_': 'JCKBBIICDNNBBEGOOMCBFGPLNMKFCKOONPMKLIALHOLINJLMFGMDJNHICLMDOBNFGIADDCIKEGMAKNINGEHALGLPFNMMEHJHHAEEAOBCDCNIJLHPHLCJBDIHMGHPEKMG',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'be5460ae3b833e19da5f9e4a305d7414',
    'XSRF-TOKEN': 'e34a5763-15d6-4444-8637-c7f251bab96f',
    'JSESSIONID': '8C071BB9536ACB64377BFC2C0D324347',
    'SESSION': 'a033b42a-d6fa-47e9-a627-c3d91785dc48',
    'f5avraaaaaaaaaaaaaaaa_session_': 'DKMLLLOAPLKLOBENGKPFEDDNNLABCGEPJPKHFADHCJMJJBAOCGICNCNIJFBDPBELEFEDNFKPBHEGEBGNJAGAOJLDGMIAONDCOOLHCOGNECBJMIONOGGMNJAFLDPACDOM',
    'XSRF-TOKEN': 'eyJpdiI6InVGejl6L0VEc25xNW1JbC9yOTFWOUE9PSIsInZhbHVlIjoiTU1PTDA2TEhhQVk2S29URTYzRWtqSFpxcytQZ051dVZaZHpCTXNOcHZ4SVE5c2t1UFZkUVEvdG53b28yT2ZzVGZuOU1GcVUzSnk2dkZ3amsySVN4WkZ2c0dDTlJBKzc2aVFlb1g0a1JvTTZmeEhmdjFoc3pCT2Zka3M0T0VidWIiLCJtYWMiOiI5NjE2MGEzZjMxMjM3ZjAwMmQ2MGIzMDc3YmU1ZjlkOTZlNjk0Yjc1ZGJlMTYyMTk2MDRkMTk0N2Y5ZjM3YTM5IiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6IjFIME5mZFRBdzYrK1dVWE9aWFNTVmc9PSIsInZhbHVlIjoiYlRVVGR6RHF1M0JzQk51aTBUdjBVbkVtUGdOWmZxWFN1V3B3Ym9iNjIwa2JwVWdwaWQxRVNRZmQyZUJHNjZSWmd1SnBwQXV3dWtuZmdUVU9rZC9NS1o0Rkk1MDF5ZmtDWmovSFgvY1N1ZUlEampIMFRmMUpmOGFvOE54cFFGZEMiLCJtYWMiOiJhMzJmMzY1ZmQzZjVjZjk5M2E0OWYxMjYxNGEyNjExNThjOWRiZDdmNGQwYWE1MDBjNjk1M2Y1Mjk0YjA2MTVjIiwidGFnIjoiIn0%3D',
    'tZKLRMRUZChQSwuHkOl1pndSfc1H6rzy3VUMXMd0': 'eyJpdiI6Im12clJBUTVzSEorN1BFaXRjaGpkY1E9PSIsInZhbHVlIjoiQzVJRmlHQjJLRE5UeS9ZTzlpcytMTnlWTHI2aXhrYllUTVo2am5PZ05BdHh2U2dQQTUxUElVbFNWNHJlcnhDOU9oZUVtbU5heXE1S1pTK1ZsdUo2QVY3UlVETW0xLzF0a25OeVRZYWVoRzNMYUIrK3piUDl1SXFEcXQyZFR5bEM0L1FTK1o0Zk4vQlkyemUyMXRSVkZTNVMrMjBKdTA1WThNTUgvLy8wRUw4NHp0ZHhLaTg1TFpLRnhmaHZmVU5HVnlsaWRESXdUWngzT1pXVFNYRWlVWGtTN212dnMrQjRKZ2lGMmplNHlwNEVYVTJhZlFpd3VFU1NnNjNxckpnQlZTM0V0S0ZNMnpSRjBXU2dHTkM5OGh0ZHAvSVAxRkc0b3h1N1dwYU8yWVVCQkt2Nzdjd25Gb3licmNFNHZNTnJsV2d1MXJFZGg5dEtvRi9pL1hhclVQb2RhU2FGaGpmWEQ4eTZuMEFGcVgzWHM1Qks3NVdMckxOQXpnekY3Wk9iNDRZd3RHdFd2SnpRWnlUVVhRcHlQZz09IiwibWFjIjoiMThkZTI4MDlhOWNmZDEzM2VjMzQ0MGMyNGI2Zjg0MzJlMzE0YjBjY2I5ODM3OWJjZGYwNDVlNzRiNTc2MGZjZSIsInRhZyI6IiJ9',
    'TS0151fc2b': '0167a1c8611a1417ffafa77e2d3d4e6243227eb93222bd6c29dcf8d9676f918096fb57074516e88ab9a764bcfe9d26afd30a59fcd1',
    'TS00000000076': '0868f8be6fab2800bed1fd81a6e1bc3294f3aa87df881bfbbf118c70495bc7d8084f54341ad96b5c3f9b6361ed049505080c644fb209d00045a4393fe139859abc8e4f851aaef8d7e17076247dc7effd6f05ccfd68ada40a9e0337f0955bca1cd83150cdf36dd32a55824810db50f0ee6122d74d59f72a5e48bcabc6501b01ddc8287c27c5b42d5bcbb3b90690656c6db9cecf1214c3a4472081dd6078efacb4b4694ce8b55bccce8838210ceb7b19a59e933a1ded42272308e42da4584e3ef10d3b474deb9b9c51fbbf35e1c08daa074882476eef571c3ff74d07fe3fcee152aaef77caa3fca41902b772b8757326d7ffa4571e25f58cb1ffc7d6003be645998ff9f58a65eed46f',
    'TSPD_101_DID': '0868f8be6fab2800bed1fd81a6e1bc3294f3aa87df881bfbbf118c70495bc7d8084f54341ad96b5c3f9b6361ed049505080c644fb2063800da0a0f623da94cf5a76136fc157a6229907f88b6219178b895449a623154de0533e1729ea030b5b291eab540bf82ecfc2d0ada1d6b43fa2f',
    'TSPD_101': '0868f8be6fab28003dc5e49f5b8819bff2065650a8324bcaa6700fcafacaab2619f0db78c67ac6008927bdca5784fddf080b18d9050518005c1880d6029fc3fe5ca1732140a3428bba23ce13beb1c95e',
    'TS011f2d1a': '01266d26d073ad15a6f338d67d0aed85cad06d9a8b9cfb79348614f45a1ffe22819f0db4d81e50f055494aec74a41724237a257f02',
    'TS5220f739077': '0868f8be6fab28009059a3be5f17da922ec50001f5a6ddfead0b7f5c65d76d97cb3f6d20e9973f088bf3ffd9011f682e080adbe455172000dc029d4693cb096253478dc77d59deb2e94cea379ef170ae77aa88512e8b0018',
    'TS5220f739029': '0868f8be6fab280011d5dd1e296ee7ef4df02443ab4c664626c8bf22075b02b51aa92f59c52042a9dad75d60fbbd0838',
    'TSf1edb2d2027': '0868f8be6fab2000c5acc6f4d3e0f1665f9fd01848f1752c470048428d54dc45c8bd338a85708b06086ae94426113000895d2546522bf9bf8e6a797f1efac88b71da3648854f4a3be5f5fc3ff241381cbc3f85d1528e08aa6aa8afc88dacbf09',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'referer': 'https://fasih-sm.bps.go.id/app/surveys/a0429e96-51a5-477b-a415-485f9c153004/fd68e454-ba45-4b85-8205-f3bf777ded24',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': 'e34a5763-15d6-4444-8637-c7f251bab96f',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=JCKBBIICDNNBBEGOOMCBFGPLNMKFCKOONPMKLIALHOLINJLMFGMDJNHICLMDOBNFGIADDCIKEGMAKNINGEHALGLPFNMMEHJHHAEEAOBCDCNIJLHPHLCJBDIHMGHPEKMG; db8ca2b43ed851cc93e71fd5fd72bff7=be5460ae3b833e19da5f9e4a305d7414; XSRF-TOKEN=e34a5763-15d6-4444-8637-c7f251bab96f; JSESSIONID=8C071BB9536ACB64377BFC2C0D324347; SESSION=a033b42a-d6fa-47e9-a627-c3d91785dc48; f5avraaaaaaaaaaaaaaaa_session_=DKMLLLOAPLKLOBENGKPFEDDNNLABCGEPJPKHFADHCJMJJBAOCGICNCNIJFBDPBELEFEDNFKPBHEGEBGNJAGAOJLDGMIAONDCOOLHCOGNECBJMIONOGGMNJAFLDPACDOM; XSRF-TOKEN=eyJpdiI6InVGejl6L0VEc25xNW1JbC9yOTFWOUE9PSIsInZhbHVlIjoiTU1PTDA2TEhhQVk2S29URTYzRWtqSFpxcytQZ051dVZaZHpCTXNOcHZ4SVE5c2t1UFZkUVEvdG53b28yT2ZzVGZuOU1GcVUzSnk2dkZ3amsySVN4WkZ2c0dDTlJBKzc2aVFlb1g0a1JvTTZmeEhmdjFoc3pCT2Zka3M0T0VidWIiLCJtYWMiOiI5NjE2MGEzZjMxMjM3ZjAwMmQ2MGIzMDc3YmU1ZjlkOTZlNjk0Yjc1ZGJlMTYyMTk2MDRkMTk0N2Y5ZjM3YTM5IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IjFIME5mZFRBdzYrK1dVWE9aWFNTVmc9PSIsInZhbHVlIjoiYlRVVGR6RHF1M0JzQk51aTBUdjBVbkVtUGdOWmZxWFN1V3B3Ym9iNjIwa2JwVWdwaWQxRVNRZmQyZUJHNjZSWmd1SnBwQXV3dWtuZmdUVU9rZC9NS1o0Rkk1MDF5ZmtDWmovSFgvY1N1ZUlEampIMFRmMUpmOGFvOE54cFFGZEMiLCJtYWMiOiJhMzJmMzY1ZmQzZjVjZjk5M2E0OWYxMjYxNGEyNjExNThjOWRiZDdmNGQwYWE1MDBjNjk1M2Y1Mjk0YjA2MTVjIiwidGFnIjoiIn0%3D; tZKLRMRUZChQSwuHkOl1pndSfc1H6rzy3VUMXMd0=eyJpdiI6Im12clJBUTVzSEorN1BFaXRjaGpkY1E9PSIsInZhbHVlIjoiQzVJRmlHQjJLRE5UeS9ZTzlpcytMTnlWTHI2aXhrYllUTVo2am5PZ05BdHh2U2dQQTUxUElVbFNWNHJlcnhDOU9oZUVtbU5heXE1S1pTK1ZsdUo2QVY3UlVETW0xLzF0a25OeVRZYWVoRzNMYUIrK3piUDl1SXFEcXQyZFR5bEM0L1FTK1o0Zk4vQlkyemUyMXRSVkZTNVMrMjBKdTA1WThNTUgvLy8wRUw4NHp0ZHhLaTg1TFpLRnhmaHZmVU5HVnlsaWRESXdUWngzT1pXVFNYRWlVWGtTN212dnMrQjRKZ2lGMmplNHlwNEVYVTJhZlFpd3VFU1NnNjNxckpnQlZTM0V0S0ZNMnpSRjBXU2dHTkM5OGh0ZHAvSVAxRkc0b3h1N1dwYU8yWVVCQkt2Nzdjd25Gb3licmNFNHZNTnJsV2d1MXJFZGg5dEtvRi9pL1hhclVQb2RhU2FGaGpmWEQ4eTZuMEFGcVgzWHM1Qks3NVdMckxOQXpnekY3Wk9iNDRZd3RHdFd2SnpRWnlUVVhRcHlQZz09IiwibWFjIjoiMThkZTI4MDlhOWNmZDEzM2VjMzQ0MGMyNGI2Zjg0MzJlMzE0YjBjY2I5ODM3OWJjZGYwNDVlNzRiNTc2MGZjZSIsInRhZyI6IiJ9; TS0151fc2b=0167a1c8611a1417ffafa77e2d3d4e6243227eb93222bd6c29dcf8d9676f918096fb57074516e88ab9a764bcfe9d26afd30a59fcd1; TS00000000076=0868f8be6fab2800bed1fd81a6e1bc3294f3aa87df881bfbbf118c70495bc7d8084f54341ad96b5c3f9b6361ed049505080c644fb209d00045a4393fe139859abc8e4f851aaef8d7e17076247dc7effd6f05ccfd68ada40a9e0337f0955bca1cd83150cdf36dd32a55824810db50f0ee6122d74d59f72a5e48bcabc6501b01ddc8287c27c5b42d5bcbb3b90690656c6db9cecf1214c3a4472081dd6078efacb4b4694ce8b55bccce8838210ceb7b19a59e933a1ded42272308e42da4584e3ef10d3b474deb9b9c51fbbf35e1c08daa074882476eef571c3ff74d07fe3fcee152aaef77caa3fca41902b772b8757326d7ffa4571e25f58cb1ffc7d6003be645998ff9f58a65eed46f; TSPD_101_DID=0868f8be6fab2800bed1fd81a6e1bc3294f3aa87df881bfbbf118c70495bc7d8084f54341ad96b5c3f9b6361ed049505080c644fb2063800da0a0f623da94cf5a76136fc157a6229907f88b6219178b895449a623154de0533e1729ea030b5b291eab540bf82ecfc2d0ada1d6b43fa2f; TSPD_101=0868f8be6fab28003dc5e49f5b8819bff2065650a8324bcaa6700fcafacaab2619f0db78c67ac6008927bdca5784fddf080b18d9050518005c1880d6029fc3fe5ca1732140a3428bba23ce13beb1c95e; TS011f2d1a=01266d26d073ad15a6f338d67d0aed85cad06d9a8b9cfb79348614f45a1ffe22819f0db4d81e50f055494aec74a41724237a257f02; TS5220f739077=0868f8be6fab28009059a3be5f17da922ec50001f5a6ddfead0b7f5c65d76d97cb3f6d20e9973f088bf3ffd9011f682e080adbe455172000dc029d4693cb096253478dc77d59deb2e94cea379ef170ae77aa88512e8b0018; TS5220f739029=0868f8be6fab280011d5dd1e296ee7ef4df02443ab4c664626c8bf22075b02b51aa92f59c52042a9dad75d60fbbd0838; TSf1edb2d2027=0868f8be6fab2000c5acc6f4d3e0f1665f9fd01848f1752c470048428d54dc45c8bd338a85708b06086ae94426113000895d2546522bf9bf8e6a797f1efac88b71da3648854f4a3be5f5fc3ff241381cbc3f85d1528e08aa6aa8afc88dacbf09',
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
# ================================================================
if not os.path.exists(base_path):
    os.makedirs(base_path)


def _atomic_write_excel(df, path):
    """Tulis Excel secara atomik agar file tidak terbaca setengah jadi."""
    folder = os.path.dirname(path) or "."
    os.makedirs(folder, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(suffix=".xlsx", dir=folder)
    os.close(fd)
    try:
        df.to_excel(tmp_path, index=False)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def save_and_merge(new_data):
    """
    Simpan satu snapshot yang sudah selesai.

    - Tepat satu baris dipertahankan untuk setiap userId + regionCode.
    - Satu proses scraping sukses menghasilkan satu file history baru.
    - File history tidak di-append dengan snapshot sebelumnya.
    - LATEST selalu ditimpa snapshot sukses terbaru.
    """
    if not new_data:
        return False

    df_new = pd.DataFrame(new_data)

    required_keys = ["userId", "regionCode"]
    missing_keys = [c for c in required_keys if c not in df_new.columns]
    if missing_keys:
        raise ValueError(f"Kolom kunci tidak ditemukan: {missing_keys}")

    before_dedupe = len(df_new)
    df_new["userId"] = df_new["userId"].astype(str).str.strip()
    df_new["regionCode"] = df_new["regionCode"].astype(str).str.strip()

    # Bukan menghapus semua key yang kembar: tetap simpan tepat satu baris,
    # dan pertahankan kemunculan terakhir sebagai nilai terbaru.
    df_new = df_new.drop_duplicates(
        subset=["userId", "regionCode"],
        keep="last",
    ).reset_index(drop=True)

    duplicate_extra = before_dedupe - len(df_new)
    if duplicate_extra:
        print(
            f"🧹 Ditemukan {duplicate_extra:,} kemunculan tambahan untuk "
            "userId + regionCode. Tepat satu baris per key tetap disimpan."
        )

    scraped_at = datetime.now()
    df_new["scraped_at"] = scraped_at.strftime("%Y-%m-%d %H:%M:%S")

    master = pd.read_excel("data/master_data.xlsx")
    master["pencacah"] = master["pencacah"].astype(str).str.strip().str.lower()
    master["regionCode"] = master["regionCode"].astype(str).str.strip()

    # Cegah merge master menggandakan hasil scraping.
    master_before = len(master)
    master = master.drop_duplicates(
        subset=["pencacah", "regionCode"],
        keep="last",
    ).copy()
    master_dup = master_before - len(master)
    if master_dup:
        print(
            f"⚠️  Master data memiliki {master_dup:,} baris key pencacah + "
            "regionCode yang berulang. Hanya satu baris per key dipakai saat merge."
        )

    df_new["email"] = df_new["email"].astype(str).str.strip().str.lower()

    master_cols = [
        "regionCode", "nmkab", "nmkec", "nmdesa", "nmsls", "nmsubsls",
        "pengawas", "pencacah", "nama_pcl", "nama_pml",
        "jumlah_prelist_awal",
    ]
    missing_master = [c for c in master_cols if c not in master.columns]
    if missing_master:
        raise ValueError(f"Kolom master_data.xlsx belum lengkap: {missing_master}")

    rows_before_merge = len(df_new)
    df_new = df_new.merge(
        master[master_cols],
        left_on=["email", "regionCode"],
        right_on=["pencacah", "regionCode"],
        how="left",
        validate="many_to_one",
    )
    if len(df_new) != rows_before_merge:
        raise RuntimeError(
            "Jumlah baris berubah setelah merge master. Snapshot dibatalkan untuk "
            "mencegah data ganda."
        )

    timestamp = scraped_at.strftime("%Y%m%d_%H%M%S")
    backup_file = archive_filename(timestamp)

    _atomic_write_excel(df_new, backup_file)
    _atomic_write_excel(df_new, LATEST_FILE)

    print(f"🗂️  History tersimpan: {backup_file}")
    print(f"💾 Snapshot terbaru tersimpan: {LATEST_FILE}")
    print(f"✅ Jumlah baris unik: {len(df_new):,}")
    return True


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
 
 
def _retry_after_seconds(response, fallback_seconds):
    """Ambil waktu tunggu dari header Retry-After jika tersedia."""
    raw = response.headers.get("Retry-After")
    if raw:
        try:
            return max(float(raw), 1.0)
        except (TypeError, ValueError):
            pass
    return fallback_seconds


def request_with_backoff(
    session,
    method,
    url,
    max_retries=MAX_REQUEST_RETRIES,
    **kwargs,
):

    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    network_delay = 10.0
    response = None

    for attempt in range(1, max_retries + 1):
        try:
            response = session.request(method, url, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Network error (percobaan {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise

            wait_seconds = min(
                network_delay + random.uniform(1, 5),
                MAX_429_WAIT_SECONDS,
            )
            print(f"⏳ Menunggu {wait_seconds:.0f} detik sebelum mencoba lagi...")
            time.sleep(wait_seconds)
            network_delay *= 2
            continue

        if response.status_code == 200:
            return response

        if response.status_code == 429:
            fallback = min(
                DEFAULT_429_WAIT_SECONDS * (2 ** (attempt - 1)),
                MAX_429_WAIT_SECONDS,
            )
            wait_seconds = _retry_after_seconds(response, fallback)
            wait_seconds = min(
                wait_seconds + random.uniform(5, 15),
                MAX_429_WAIT_SECONDS,
            )

            print(
                f"⚠️  Status 429 (percobaan {attempt}/{max_retries}). "
                f"Server meminta request diperlambat; tunggu {wait_seconds:.0f} detik."
            )

            if attempt == max_retries:
                raise RuntimeError(
                    "Rate limit 429 masih aktif setelah seluruh percobaan. "
                    "Snapshot tidak disimpan. Jalankan kembali setelah masa cooldown."
                )

            time.sleep(wait_seconds)
            continue

        # Jangan menghantam ulang 401/403. Serahkan ke fetch_data untuk refresh session.
        if response.status_code in (302, 401, 403):
            return response

        # Gangguan server sementara.
        if 500 <= response.status_code < 600 and attempt < max_retries:
            wait_seconds = min(
                15 * (2 ** (attempt - 1)) + random.uniform(1, 5),
                180,
            )
            print(
                f"⚠️  Status {response.status_code}. "
                f"Menunggu {wait_seconds:.0f} detik sebelum retry..."
            )
            time.sleep(wait_seconds)
            continue

        return response

    return response


def fetch_data():
    # Dictionary memastikan satu userId + regionCode hanya memiliki satu baris.
    rows_by_key = {}
    page = 0
    session = requests.Session()
    max_refresh = 2
    refresh_count = 0
    reached_last_page = False

    while True:
        payload = dict(json_data)
        payload["page"] = page
        payload["size"] = PAGE_SIZE

        try:
            response = request_with_backoff(
                session,
                "POST",
                URL_DATA,
                cookies=cookies,
                headers=headers,
                json=payload,
            )
        except (RuntimeError, requests.exceptions.RequestException) as e:
            print(f"🛑 Berhenti scraping: {e}")
            return False

        session_expired = (
            (response.status_code == 200 and is_session_expired(response))
            or response.status_code in (302, 401, 403)
        )
        if session_expired:
            if refresh_count >= max_refresh:
                print(
                    f"🛑 Session expired lagi setelah {max_refresh}x refresh. "
                    "Kemungkinan profil Chrome perlu login manual ulang."
                )
                return False

            try:
                refresh_cookies()
                refresh_count += 1
                session.close()
                session = requests.Session()
                wait_seconds = random.uniform(10, 20)
                print(
                    f"↩️  Mengulang page {page} dengan cookies baru setelah "
                    f"jeda {wait_seconds:.0f} detik..."
                )
                time.sleep(wait_seconds)
                continue
            except Exception as e:
                print(f"🛑 Gagal refresh cookies: {e}")
                return False

        if response.status_code != 200:
            print(f"❌ Error di page {page} | Status: {response.status_code}")
            print(response.text[:500])
            return False

        try:
            json_res = response.json()
        except Exception:
            print(f"❌ Response bukan JSON di page {page}.")
            return False

        data_block = json_res.get("data", {})
        data = data_block.get("content", [])
        is_last = bool(data_block.get("last", True))

        print(
            f"📄 Page {page} | user: {len(data)} | "
            f"key unik sementara: {len(rows_by_key):,} | last: {is_last}"
        )

        duplicate_on_page = 0
        for user in data:
            user_id = str(user.get("userId") or "").strip()
            for region in user.get("regionSummary", []):
                region_code = str(region.get("regionCode") or "").strip()
                key = (user_id, region_code)

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

                if key in rows_by_key:
                    duplicate_on_page += 1

                # Tetap simpan satu baris; kemunculan terakhir mengganti yang sebelumnya.
                rows_by_key[key] = row

        if duplicate_on_page:
            print(
                f"🧹 Page {page}: {duplicate_on_page:,} kemunculan tambahan "
                "userId + regionCode ditemukan; satu baris per key tetap disimpan."
            )

        if is_last:
            reached_last_page = True
            print("✅ Sudah sampai halaman terakhir.")
            break

        page += 1

        # Jeda normal antarpages.
        delay = random.uniform(PAGE_DELAY_MIN, PAGE_DELAY_MAX)
        print(f"⏳ Jeda {delay:.1f} detik sebelum page {page}...")
        time.sleep(delay)

        # Istirahat berkala untuk menurunkan burst request panjang.
        if page > 0 and page % COOLDOWN_EVERY_PAGES == 0:
            cooldown = random.uniform(
                COOLDOWN_MIN_SECONDS,
                COOLDOWN_MAX_SECONDS,
            )
            print(
                f"🧊 Cooldown setelah {page} page: "
                f"menunggu {cooldown:.0f} detik..."
            )
            time.sleep(cooldown)

    if not reached_last_page:
        print("🛑 Halaman terakhir belum tercapai. Snapshot parsial tidak disimpan.")
        return False

    if not rows_by_key:
        print("⚠️  Tidak ada data yang diperoleh.")
        return False

    try:
        return save_and_merge(list(rows_by_key.values()))
    except Exception as e:
        print(f"🛑 Gagal menyimpan snapshot: {e}")
        return False


def job():
    print(
        f"\n[+] Memulai proses scraping pada "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    success = fetch_data()
    if success:
        print("🎉 Scraping lengkap berhasil disimpan.")
        auto_push_github()
    else:
        print("⏭️ Push GitHub dilewati karena scraping tidak berhasil lengkap.")


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