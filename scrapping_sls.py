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
    'f5avraaaaaaaaaaaaaaaa_session_': 'MLAAENJNCOMBDDAFHBPJPIILLBJKGJKLAFBENHKMHJCFAEKAPCHJLADIICODAGJPFCMDOFIHJEBKFPDFINFADBNPGPOOCHFEEBOANGKMIIKMFNCIAIPIFNCLGOBHAJGK',
    'cf_clearance': 'eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg',
    '_ga': 'GA1.3.967752592.1784785844',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0',
    'XSRF-TOKEN': '8a78cc84-f362-4d31-8e0f-bf746c0c91ff',
    'JSESSIONID': '8EB4DA5B9229BBD6D51F746F4FED08E9',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '4f2806231eb66c8992f000f38d707caa',
    'SESSION': '232c5e61-5626-4fe2-bed9-265afd5ea42b',
    'f5avraaaaaaaaaaaaaaaa_session_': 'IBBNEHBKNANCDDHPOFHBHNNKLMENKPMKEBIIBEHBOOKBKBDBFMDJLOHHCKCONIGCLNODBDGFNCIFOEANOODAMFKFDPHPIPIPEDIHOCMHLDCOAGKGHCPDIJNLAKNHOHHB',
    'TS00000000076': '0868f8be6fab2800e87fd475e2800ffd4244ef2f11db617447d4ceb5b8cd6aeff0b47ec0adce2c3d2fa0dcbf4902fbad0853b9c19509d00092c6522ef13da3820478ac87f52a0fe22f368c1eef7bee9d62bb7a113466be7a24ba41f042eb9b0805395de4d93e2c865fd178d582e6c376beb38bc73734b4d6549b2003c1308d7ec012a6e4e7a872c44dba74c778af14f23d2bbff2afae187692820b7f5412d218d16ae65865a7df1c82c3e83525f3737603a89526f8dfddc322c85cd9c5589bb81c1d9eafcd9314b0eb022713fbe13c33ab40c9083886dbb0740f158667ea5c35ee423e01c501cce5345e87b92eb23ee14e91c933f44ae5cf35ff7ad53d79335b4423277252db49bd',
    'TSPD_101_DID': '0868f8be6fab2800e87fd475e2800ffd4244ef2f11db617447d4ceb5b8cd6aeff0b47ec0adce2c3d2fa0dcbf4902fbad0853b9c1950638007923376d27dbb1fe1a4f7c33150ce0f555650886b07c103abf941d34633e353a8bac0adfd552d6a02f638294fd7e2c5634d3f30c9ed89103',
    'TS011f2d1a': '01266d26d073c642cbf2723858e08a8725200b10bf2268b45fa0bd03aa2689b7506b53faf7b83d696ac38d49bd07208439a998178f',
    'TSPD_101': '0868f8be6fab2800b7a47bfc99174c00ba95447b1978b2158a40591e6df99f9259fe0bc0575fde9f6407e8e1ff0780fe08b7cfb354051800857f014ec659a8e35ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800abf9edd55328d92486d0f274077a8d66c54b1e7d82f1b3777a41ecd4e73a2eaf6e714097bc80696e08e1c9b6de1720005fda72b46922cd4a707213e7d34bb50101af17688ab080ef5a8066601361aae2',
    'TS5220f739029': '0868f8be6fab28007ec1fb8df0a30ae298bd889accda53a95b698477d523307da0a4a0f36abc2bb2511b7052d0ad2c80',
    'TSf1edb2d2027': '0868f8be6fab2000a61278ada9f0777f37a3b9649d1b5955e17bb0d30e2ab84d7ee348b9032eb7db08c8a1b57a11300017fa7b08a4f4f3effdaf4d70011a83039bb218763b914fc3732f86adddc174246908a41c8c5c67ef5385e3465f0b9d41',
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
    'x-xsrf-token': '8a78cc84-f362-4d31-8e0f-bf746c0c91ff',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=MLAAENJNCOMBDDAFHBPJPIILLBJKGJKLAFBENHKMHJCFAEKAPCHJLADIICODAGJPFCMDOFIHJEBKFPDFINFADBNPGPOOCHFEEBOANGKMIIKMFNCIAIPIFNCLGOBHAJGK; cf_clearance=eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg; _ga=GA1.3.967752592.1784785844; _ga_XXTTVXWHDB=GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0; XSRF-TOKEN=8a78cc84-f362-4d31-8e0f-bf746c0c91ff; JSESSIONID=8EB4DA5B9229BBD6D51F746F4FED08E9; db8ca2b43ed851cc93e71fd5fd72bff7=4f2806231eb66c8992f000f38d707caa; SESSION=232c5e61-5626-4fe2-bed9-265afd5ea42b; f5avraaaaaaaaaaaaaaaa_session_=IBBNEHBKNANCDDHPOFHBHNNKLMENKPMKEBIIBEHBOOKBKBDBFMDJLOHHCKCONIGCLNODBDGFNCIFOEANOODAMFKFDPHPIPIPEDIHOCMHLDCOAGKGHCPDIJNLAKNHOHHB; TS00000000076=0868f8be6fab2800e87fd475e2800ffd4244ef2f11db617447d4ceb5b8cd6aeff0b47ec0adce2c3d2fa0dcbf4902fbad0853b9c19509d00092c6522ef13da3820478ac87f52a0fe22f368c1eef7bee9d62bb7a113466be7a24ba41f042eb9b0805395de4d93e2c865fd178d582e6c376beb38bc73734b4d6549b2003c1308d7ec012a6e4e7a872c44dba74c778af14f23d2bbff2afae187692820b7f5412d218d16ae65865a7df1c82c3e83525f3737603a89526f8dfddc322c85cd9c5589bb81c1d9eafcd9314b0eb022713fbe13c33ab40c9083886dbb0740f158667ea5c35ee423e01c501cce5345e87b92eb23ee14e91c933f44ae5cf35ff7ad53d79335b4423277252db49bd; TSPD_101_DID=0868f8be6fab2800e87fd475e2800ffd4244ef2f11db617447d4ceb5b8cd6aeff0b47ec0adce2c3d2fa0dcbf4902fbad0853b9c1950638007923376d27dbb1fe1a4f7c33150ce0f555650886b07c103abf941d34633e353a8bac0adfd552d6a02f638294fd7e2c5634d3f30c9ed89103; TS011f2d1a=01266d26d073c642cbf2723858e08a8725200b10bf2268b45fa0bd03aa2689b7506b53faf7b83d696ac38d49bd07208439a998178f; TSPD_101=0868f8be6fab2800b7a47bfc99174c00ba95447b1978b2158a40591e6df99f9259fe0bc0575fde9f6407e8e1ff0780fe08b7cfb354051800857f014ec659a8e35ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800abf9edd55328d92486d0f274077a8d66c54b1e7d82f1b3777a41ecd4e73a2eaf6e714097bc80696e08e1c9b6de1720005fda72b46922cd4a707213e7d34bb50101af17688ab080ef5a8066601361aae2; TS5220f739029=0868f8be6fab28007ec1fb8df0a30ae298bd889accda53a95b698477d523307da0a4a0f36abc2bb2511b7052d0ad2c80; TSf1edb2d2027=0868f8be6fab2000a61278ada9f0777f37a3b9649d1b5955e17bb0d30e2ab84d7ee348b9032eb7db08c8a1b57a11300017fa7b08a4f4f3effdaf4d70011a83039bb218763b914fc3732f86adddc174246908a41c8c5c67ef5385e3465f0b9d41',
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


def _normalize_text(series: pd.Series) -> pd.Series:
    """Normalisasi teks untuk key merge/deduplikasi tanpa mengubah nilai kosong menjadi 'nan'."""
    return series.fillna("").astype(str).str.strip().str.lower()


def _deduplicate_api_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pastikan satu snapshot hanya memiliki satu baris untuk setiap petugas-wilayah.

    Key utama menggunakan userId + regionCode. Jika userId tidak tersedia,
    fallback menggunakan email + regionCode.
    """
    if df.empty:
        return df

    if {"userId", "regionCode"}.issubset(df.columns):
        key_cols = ["userId", "regionCode"]
    elif {"email", "regionCode"}.issubset(df.columns):
        key_cols = ["email", "regionCode"]
    else:
        raise ValueError(
            "Tidak dapat melakukan deduplikasi karena kolom key "
            "`userId/regionCode` atau `email/regionCode` tidak lengkap."
        )

    before = len(df)
    duplicate_mask = df.duplicated(subset=key_cols, keep=False)

    if duplicate_mask.any():
        duplicate_count = int(duplicate_mask.sum())
        print(
            f"⚠️  Ditemukan {duplicate_count:,} baris yang memiliki key duplikat "
            f"{key_cols}. Hanya data terakhir untuk setiap key yang dipakai."
        )

    df = df.drop_duplicates(subset=key_cols, keep="last").reset_index(drop=True)
    removed = before - len(df)

    if removed:
        print(f"🧹 {removed:,} baris duplikat API dihapus sebelum penyimpanan.")

    return df


def save_snapshot(new_data):
    """
    Simpan satu hasil scraping lengkap sebagai satu snapshot.

    Aturan anti-duplikat:
    1. Data API dideduplikasi berdasarkan userId + regionCode.
    2. Master dideduplikasi berdasarkan pencacah + regionCode sebelum merge.
    3. File history selalu berisi satu snapshot saja, tidak pernah append.
    4. LATEST selalu ditimpa secara atomik oleh snapshot lengkap terbaru.
    """
    if not new_data:
        raise ValueError("Data scraping kosong; snapshot tidak disimpan.")

    run_at = datetime.now()
    scraped_at = run_at.strftime("%Y-%m-%d %H:%M:%S")
    backup_file = archive_filename(run_at.strftime("%Y%m%d_%H%M%S"))

    df_new = pd.DataFrame(new_data)

    # Normalisasi key terlebih dahulu, lalu buang hasil API yang terulang.
    if "email" in df_new.columns:
        df_new["email"] = _normalize_text(df_new["email"])
    if "regionCode" in df_new.columns:
        df_new["regionCode"] = df_new["regionCode"].fillna("").astype(str).str.strip()

    df_new = _deduplicate_api_rows(df_new)
    api_row_count = len(df_new)

    master = pd.read_excel("data/master_data.xlsx")
    required_master_cols = [
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
        "jumlah_prelist_awal",
    ]

    missing_master_cols = [c for c in required_master_cols if c not in master.columns]
    if missing_master_cols:
        raise ValueError(
            "Kolom master_data.xlsx tidak lengkap: "
            + ", ".join(missing_master_cols)
        )

    master = master[required_master_cols].copy()
    master["pencacah"] = _normalize_text(master["pencacah"])
    master["regionCode"] = master["regionCode"].fillna("").astype(str).str.strip()

    master_key = ["pencacah", "regionCode"]
    master_dup_mask = master.duplicated(subset=master_key, keep=False)

    if master_dup_mask.any():
        duplicate_rows = int(master_dup_mask.sum())
        print(
            f"⚠️  master_data.xlsx memiliki {duplicate_rows:,} baris dengan key "
            f"{master_key} yang berulang. Hanya baris terakhir untuk setiap key yang dipakai."
        )
        master = (
            master.drop_duplicates(subset=master_key, keep="last")
            .reset_index(drop=True)
        )

    # many_to_one memastikan satu baris API tidak berkembang menjadi beberapa baris
    # akibat key master yang berulang.
    df_new = df_new.merge(
        master,
        left_on=["email", "regionCode"],
        right_on=["pencacah", "regionCode"],
        how="left",
        validate="many_to_one",
    )

    # Merge tidak boleh menambah jumlah baris snapshot.
    if len(df_new) != api_row_count:
        raise RuntimeError(
            "Jumlah baris berubah setelah merge master "
            f"({api_row_count:,} menjadi {len(df_new):,}). "
            "Snapshot dibatalkan untuk mencegah duplikasi."
        )

    # Pemeriksaan terakhir setelah merge.
    final_key = ["userId", "regionCode"] if "userId" in df_new.columns else ["email", "regionCode"]
    if df_new.duplicated(subset=final_key).any():
        raise RuntimeError(
            f"Masih ditemukan key duplikat setelah merge: {final_key}. "
            "Snapshot dibatalkan."
        )

    df_new["scraped_at"] = scraped_at

    # History adalah satu file per scraping berhasil. Jangan pernah concat/append
    # dengan isi history lama.
    _atomic_write_excel(df_new, backup_file)
    _atomic_write_excel(df_new, LATEST_FILE)

    print(f"🗂️  History tersimpan: {backup_file}")
    print(f"💾 Snapshot terbaru tersimpan: {LATEST_FILE}")
    print(f"✅ Jumlah baris unik yang disimpan: {len(df_new):,}")

    return backup_file


def _atomic_write_excel(df, path):
    """Tulis Excel dengan aman: tulis ke file sementara dulu, baru rename.
    Mencegah dashboard membaca file yang setengah jadi/korup saat scraping sedang menulis."""
    folder = os.path.dirname(path) or "."
    os.makedirs(folder, exist_ok=True)
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
        # Hindari header Cookie lama menimpa cookies baru yang dikirim requests.
        headers["cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
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

        # 401/403 dikembalikan ke fetch_data agar session dapat di-refresh,
        # bukan diulang terus memakai cookies lama.
        if response.status_code in (401, 403):
            return response

        if response.status_code == 429:
            print(
                f"⚠️  Status 429 (percobaan {attempt}/{max_retries}) - "
                "request dibatasi sementara."
            )
            if attempt == max_retries:
                raise RuntimeError(
                    f"Berhenti: status 429 berulang {max_retries}x. "
                    "Tunggu sebelum mencoba lagi atau koordinasi ke admin FASIH."
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


def _user_identity(user):
    """Identitas stabil untuk satu item `content` dari API."""
    user_id = user.get("userId")
    if user_id not in (None, ""):
        return ("userId", str(user_id).strip())

    email = user.get("email")
    if email not in (None, ""):
        return ("email", str(email).strip().lower())

    username = user.get("username")
    if username not in (None, ""):
        return ("username", str(username).strip().lower())

    return None


def _fetch_data_once(run_number=1, page_size=10):
    """
    Lakukan satu putaran scraping penuh.

    Overlap antarpages tidak langsung dianggap fatal karena API memakai offset
    pagination atas data yang terus berubah. Data yang berulang disimpan satu kali,
    lalu kelengkapan diperiksa dari jumlah item `content` unik terhadap
    `totalElements`.

    Return:
        (True, "ok")                    -> snapshot berhasil disimpan
        (False, "pagination_unstable") -> ada item terulang dan ada item lain hilang
        (False, "fatal")               -> error request/struktur/session
    """
    page = 0
    session = requests.Session()
    max_refresh = 2
    refresh_count = 0

    completed = False
    expected_total_elements = None
    raw_content_count = 0

    # Simpan content unik dan baris region unik. Kemunculan terakhir dipakai karena
    # nilainya merupakan posisi API yang paling baru selama proses scraping.
    seen_user_keys = set()
    rows_by_region_key = {}

    repeated_user_count = 0
    repeated_region_count = 0
    seen_page_fingerprints = set()

    while True:
        json_data["page"] = page
        json_data["size"] = page_size

        try:
            response = request_with_backoff(
                session,
                "POST",
                URL_DATA,
                cookies=cookies,
                headers=headers,
                json=json_data,
            )
        except (RuntimeError, requests.exceptions.RequestException) as e:
            print(f"🛑 Scraping gagal di page {page}: {e}")
            return False, "fatal"

        session_expired = (
            (response.status_code == 200 and is_session_expired(response))
            or response.status_code in (302, 401, 403)
        )

        if session_expired:
            if refresh_count >= max_refresh:
                print(
                    f"🛑 Session tetap expired setelah {max_refresh}x refresh. "
                    "Tidak ada data yang disimpan."
                )
                return False, "fatal"

            try:
                refresh_cookies()
                refresh_count += 1
                session = requests.Session()
                print(f"↩️  Mengulang page {page} dengan cookies baru...")
                time.sleep(2)
                continue
            except Exception as e:
                print(f"🛑 Gagal refresh cookies: {e}")
                return False, "fatal"

        if response.status_code != 200:
            print(f"❌ Error di page {page} | Status: {response.status_code}")
            print(response.text[:500])
            print("🛑 Snapshot dibatalkan; history dan LATEST tidak diubah.")
            return False, "fatal"

        try:
            json_res = response.json()
        except Exception:
            print(f"❌ Response bukan JSON di page {page}.")
            print("🛑 Snapshot dibatalkan; history dan LATEST tidak diubah.")
            return False, "fatal"

        data_block = json_res.get("data")
        if not isinstance(data_block, dict):
            print(f"❌ Struktur `data` tidak valid di page {page}.")
            return False, "fatal"

        data = data_block.get("content", [])
        if not isinstance(data, list):
            print(f"❌ Struktur `content` tidak valid di page {page}.")
            return False, "fatal"

        is_last = bool(data_block.get("last", False))

        total_elements = data_block.get("totalElements")
        if total_elements is not None:
            try:
                total_elements = int(total_elements)
                if expected_total_elements is None:
                    expected_total_elements = total_elements
                elif expected_total_elements != total_elements:
                    print(
                        "❌ Nilai totalElements berubah selama scraping "
                        f"({expected_total_elements:,} menjadi {total_elements:,})."
                    )
                    return False, "pagination_unstable"
            except (TypeError, ValueError):
                pass

        print(
            f"📄 Run {run_number} | Page {page} | data: {len(data)} | "
            f"last: {is_last} | raw terkumpul: {raw_content_count + len(data):,}"
        )

        if not data and not is_last:
            print(
                f"❌ Page {page} kosong tetapi belum menjadi halaman terakhir. "
                "Snapshot dibatalkan."
            )
            return False, "fatal"

        page_user_keys = []

        for user in data:
            user_key = _user_identity(user)
            if user_key is None:
                print(
                    f"❌ Item content pada page {page} tidak memiliki userId, email, "
                    "maupun username. Snapshot dibatalkan."
                )
                return False, "fatal"

            page_user_keys.append(user_key)

            if user_key in seen_user_keys:
                repeated_user_count += 1
            seen_user_keys.add(user_key)

            user_id = user.get("userId")
            email = user.get("email")
            region_summary = user.get("regionSummary", []) or []

            if not isinstance(region_summary, list):
                print(f"❌ regionSummary tidak valid pada page {page}.")
                return False, "fatal"

            for region in region_summary:
                region_code = region.get("regionCode")
                region_key = (user_key, str(region_code).strip())

                row = {
                    "userId": user_id,
                    "username": user.get("username"),
                    "email": email,
                    "role": user.get("roleName"),
                    "regionCode": region_code,
                    "total_data": region.get("total"),
                }

                for status in region.get("statusBreakdown", []) or []:
                    status_name = status.get("status")
                    if status_name:
                        row[status_name] = status.get("count")

                if region_key in rows_by_region_key:
                    repeated_region_count += 1

                # Kemunculan terakhir dipakai. Ini mencegah duplikat fisik tanpa
                # menyembunyikan data hilang karena validasi jumlah user unik ada di akhir.
                rows_by_region_key[region_key] = row

        # Jika server terus mengembalikan keseluruhan page yang sama, hentikan agar
        # tidak terjadi loop panjang. Overlap sebagian masih diperbolehkan.
        fingerprint = tuple(sorted(page_user_keys))
        if fingerprint and fingerprint in seen_page_fingerprints:
            print(
                f"❌ Seluruh isi page {page} identik dengan page sebelumnya. "
                "Pagination API kemungkinan tidak bergerak."
            )
            return False, "pagination_unstable"
        if fingerprint:
            seen_page_fingerprints.add(fingerprint)

        raw_content_count += len(data)

        if is_last:
            completed = True
            print("✅ Sudah sampai halaman terakhir.")
            break

        page += 1
        time.sleep(random.uniform(1, 2))

    if not completed:
        print("🛑 Scraping belum lengkap. Tidak ada file yang disimpan.")
        return False, "fatal"

    unique_user_count = len(seen_user_keys)

    if repeated_user_count:
        print(
            f"ℹ️  Ditemukan {repeated_user_count:,} kemunculan user berulang "
            "antarpages. Data tidak langsung dibatalkan; kelengkapan diperiksa "
            "menggunakan jumlah user unik."
        )

    if repeated_region_count:
        print(
            f"🧹 Ditemukan {repeated_region_count:,} kemunculan petugas-wilayah "
            "berulang. Hanya kemunculan terakhir yang dipakai."
        )

    # Validasi utama. Jika satu user bergeser dan muncul dua kali, biasanya ada user
    # lain yang tidak ikut terambil. Dalam kondisi itu unique_user_count akan kurang
    # dari totalElements, sehingga seluruh run harus diulang dari page 0.
    if (
        expected_total_elements is not None
        and unique_user_count != expected_total_elements
    ):
        print(
            "❌ Pagination tidak stabil: jumlah user unik yang diterima "
            f"{unique_user_count:,}, sedangkan totalElements "
            f"{expected_total_elements:,}. Raw content: {raw_content_count:,}."
        )
        print(
            "🔁 Snapshot tidak disimpan karena kemungkinan ada user yang terlewat."
        )
        return False, "pagination_unstable"

    if (
        expected_total_elements is not None
        and raw_content_count != expected_total_elements
    ):
        print(
            "⚠️  Jumlah raw content berbeda dari totalElements, tetapi seluruh user "
            f"unik tetap lengkap ({unique_user_count:,}). Proses dapat dilanjutkan."
        )

    all_rows = list(rows_by_region_key.values())
    if not all_rows:
        print("⚠️ Tidak ada baris regionSummary yang diterima. Snapshot tidak disimpan.")
        return False, "fatal"

    try:
        save_snapshot(all_rows)
    except Exception as e:
        print(f"🛑 Gagal menyimpan snapshot anti-duplikat: {e}")
        return False, "fatal"

    print("🎉 Semua data berhasil diambil dan disimpan tanpa duplikasi.")
    return True, "ok"


def fetch_data(max_full_retries=3, page_size=10):
    """
    Jalankan scraping penuh. Jika pagination bergeser karena data FASIH berubah
    saat proses berlangsung, ulangi seluruh scraping dari page 0.
    """
    for run_number in range(1, max_full_retries + 1):
        if run_number > 1:
            wait_seconds = 5 * (run_number - 1)
            print(
                f"\n🔄 Mengulang seluruh scraping dari page 0 dalam "
                f"{wait_seconds} detik (percobaan {run_number}/{max_full_retries})..."
            )
            time.sleep(wait_seconds)

        success, reason = _fetch_data_once(
            run_number=run_number,
            page_size=page_size,
        )

        if success:
            return True

        if reason != "pagination_unstable":
            return False

    print(
        f"🛑 Pagination masih tidak stabil setelah {max_full_retries} percobaan penuh. "
        "History dan LATEST tidak diubah. Coba lagi saat aktivitas FASIH lebih rendah."
    )
    return False

def job():
    print(
        f"\n[+] Memulai proses scraping pada "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    success = fetch_data()

    if success:
        auto_push_github()
    else:
        print("⏭️ Push GitHub dilewati karena scraping tidak berhasil lengkap.")


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