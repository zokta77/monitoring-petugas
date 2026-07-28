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
    'f5avraaaaaaaaaaaaaaaa_session_': 'BBGNOEIOIMJACEEIAIHNNHKHCDJGPICOBLONJHOHOBFICPDBACJKLBFEHGIPKKOCIOODCECIEHHNOMOGCCDANFEBBANIFMDNPAHOCLJCIJKKLBFBMEGCDGMIEHAFNBNA',
    'cf_clearance': 'eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg',
    '_ga': 'GA1.3.967752592.1784785844',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0',
    'XSRF-TOKEN': '8a78cc84-f362-4d31-8e0f-bf746c0c91ff',
    'JSESSIONID': '8EB4DA5B9229BBD6D51F746F4FED08E9',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '4f2806231eb66c8992f000f38d707caa',
    'SESSION': '232c5e61-5626-4fe2-bed9-265afd5ea42b',
    'f5avraaaaaaaaaaaaaaaa_session_': 'NPCGNNCPFJFOJEBJFEMOKBANHNFJFKFMKBKMIPJMOJFONFJMHAIBJJLIFIJCDJHHAMEDABKDBBFDILHHCMDAKJFPNAABMBNIKCIGFDBMFKJICLBKILFCHEIEJINNNPGB',
    'XSRF-TOKEN': 'eyJpdiI6IlVpZk5YZEFLR0xRb21KaEZJS0RKeXc9PSIsInZhbHVlIjoiMnZkVU9hNDZ3NWZYYjU3NmxKQzgzT09IVXpZMlRsNGdoemdNZ3JvQ0lZdkRVWHJlTGZ1ZFlEQmJXZllKL0ZVT2V0ZWdPK3VVc3dJa1pjNVpwYkVndTlMTVVkYU5HUzBMY0M2N2NlOXlvM2hZbm9TWU9OK1BRMU8zakJVWDRDVDMiLCJtYWMiOiJlOTg3NTlmNzM0NDhmNDNhYzc4YmIwNjM1MWQ4MzY0ZDliODNmMjQzMzIyNDA1NzIyNGQ2YzhiNzM1ZTUyZWRlIiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6ImMycEEwWmFvaWh2TzNUbTJGV210U0E9PSIsInZhbHVlIjoiN3lEWlU5UWIxeGhYR3ZZVlhUcTNNUmFoQW5VeDEvd1QzU1d5d0dGQUxFTWk3Ti9XcjZRZXlzMktFVW94NXdkNGllcFZhVmdDdEwxSHRFTHFUOGZHOW5FYS9ZdHZHd2V3MnFBRFhZN09hcU5GT1VjMERhUVpTL0FwcDhOTi9WSFMiLCJtYWMiOiJlZGE0Y2JmYjQxNGZiZTgwYzFlMTAwMzcxMzc3ZDUwMWYxOTU0ZjQzZWIxOWQ1YTk3NmEzMmE3ZWU4ZmFkMGRiIiwidGFnIjoiIn0%3D',
    'VReg30sVRccCX6m3aSzIOFcxli9ezYAI79yZpBGe': 'eyJpdiI6IjBiSlo2RmMxVG0zMXRHd3drNzlyd0E9PSIsInZhbHVlIjoiVDNhVUxjQ0ZuOW1NdFlKUUlDYnhyckpOMjBMMjhXSG1iZFhST3lxM2Z0bXBlK3RaT0dSZVdvNUJEd2xOUnRtSWQ4V3Z3TzAzQmFHcE5tZzFlU2pVUXdMS29Jb0d5NnVVSDhyR1d6Q3ZCVDNSQmNSWEFVQ2VRa1YyOHRVZFE5TEpnSmVzOTk3NnFQVFFUYU92aGpVRTc5QzVnNkpWTXFUNGJUV3lMU1BSZ3NEQTc4ZUxVdyt3eWFlSWJ3NFUrS3FrREdTejBRZHNLNktOSmdUb1EwOCtUSElXYWFha0lUelNZWjdGRWttTG0xOVh4Snk2WlhLa3h6TGFFczM4b3JtOGJCeUptTE5peExoVldGUW84dXJTZThEVW1NYm5Oa09kVUZnZ3FXNnpZV1djTmVrNWFtaFhlSGIybXk0cHJZdE9jd2dOTkRaVGdiejhMNlBHb1ZHYXFrRys5a0xBZ1JESmwxdlZGZVpMeUh1cUlSRDdZQldUMDdwNmJ6SHRWWTlTVmU3bTAwVnd1S01WVUVpdjdYdTR3UT09IiwibWFjIjoiYWYzMzY4M2M2YTNhMmI4MzNkMzE2MGMxZGE3YjEzZTJkY2MyZjkwZGFkYWE1YTcyN2JjMjE3NDliOTg1NGJjNiIsInRhZyI6IiJ9',
    'TS00000000076': '0868f8be6fab2800b1edfb27bfc28e83d88dc70a87e9f92349de9dfacb226485f0002a6ebbfb009aa64224612031c5920889ee682f09d0006f1b0d308ae67e5c7651c232e54a1cf1326ed14c2905a2940dc2f41f9a93f7bcb0b5ee283c860b343d4ac49f2832366dd3cb39ef9e2700ba4804b6f463ab96561f53b952bee323383b7f5b2d155e224287c2e9f50b44f21013deae82b7ece23ff41592d4af9400d7ac98a6d462a1ce90865b8becd9b226638c7222bd6df620e6aa57f6d31840c00732b59ea273294d7bb2ce5a633e85b1f16d14f25317989cd509c1ebde6299d4b9a7a8f23ecbe24384fada62277a8e1f158252c29b8fafcbf06e17bd04eb50912f91b9f2e0799beedf',
    'TSPD_101_DID': '0868f8be6fab2800b1edfb27bfc28e83d88dc70a87e9f92349de9dfacb226485f0002a6ebbfb009aa64224612031c5920889ee682f06380086a63b931c68791fa218f5fc9ffb3b30c67115c2514455c5d7b88bc26fe827fd25c7b63f595e2c5dafbf3052289e5764f1f4af1ab86d3860',
    'TS011f2d1a': '01266d26d08110df4b88acb90dd34949d6349abc0ee816d8643cf025761fecf6eee11148361255abc54fa1723e1530a9ab75949fa7',
    'TSPD_101': '0868f8be6fab28001e543973f4028a53dc7aece4d10c5fe2759c88ff16805a481876a81480c6387e4d502bf6ecb0f55e08a2d57fdb0518005e27d2beb0e8c9d25ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800ce60889b4a6e11c95c8533f7911804265fbd8bf4e3dd232391f79778249cbe61b0be18129f7ceb5f083638484017200097efea4b90a7ce49197885cd82a2fcf02e039775f401eb552d09651bbf951106',
    'TS5220f739029': '0868f8be6fab2800036b993310a5df4743e2669136f030557b5aa0ec90992fbdd66c20141ce5f85ecc38773ba37cbd49',
    'TSf1edb2d2027': '0868f8be6fab2000d27e7faaf37eb2de69dce0dfc01d6410e0305539e5d5ae7c9eff0cf4ea63567f0815872d74113000df62b47aa95d76e1553800365cdc68a9bb40b05233f7299ae88fa413f2b92bcdaffb392c5a576032f3785880223a1d0d',
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
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=BBGNOEIOIMJACEEIAIHNNHKHCDJGPICOBLONJHOHOBFICPDBACJKLBFEHGIPKKOCIOODCECIEHHNOMOGCCDANFEBBANIFMDNPAHOCLJCIJKKLBFBMEGCDGMIEHAFNBNA; cf_clearance=eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg; _ga=GA1.3.967752592.1784785844; _ga_XXTTVXWHDB=GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0; XSRF-TOKEN=8a78cc84-f362-4d31-8e0f-bf746c0c91ff; JSESSIONID=8EB4DA5B9229BBD6D51F746F4FED08E9; db8ca2b43ed851cc93e71fd5fd72bff7=4f2806231eb66c8992f000f38d707caa; SESSION=232c5e61-5626-4fe2-bed9-265afd5ea42b; f5avraaaaaaaaaaaaaaaa_session_=NPCGNNCPFJFOJEBJFEMOKBANHNFJFKFMKBKMIPJMOJFONFJMHAIBJJLIFIJCDJHHAMEDABKDBBFDILHHCMDAKJFPNAABMBNIKCIGFDBMFKJICLBKILFCHEIEJINNNPGB; XSRF-TOKEN=eyJpdiI6IlVpZk5YZEFLR0xRb21KaEZJS0RKeXc9PSIsInZhbHVlIjoiMnZkVU9hNDZ3NWZYYjU3NmxKQzgzT09IVXpZMlRsNGdoemdNZ3JvQ0lZdkRVWHJlTGZ1ZFlEQmJXZllKL0ZVT2V0ZWdPK3VVc3dJa1pjNVpwYkVndTlMTVVkYU5HUzBMY0M2N2NlOXlvM2hZbm9TWU9OK1BRMU8zakJVWDRDVDMiLCJtYWMiOiJlOTg3NTlmNzM0NDhmNDNhYzc4YmIwNjM1MWQ4MzY0ZDliODNmMjQzMzIyNDA1NzIyNGQ2YzhiNzM1ZTUyZWRlIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6ImMycEEwWmFvaWh2TzNUbTJGV210U0E9PSIsInZhbHVlIjoiN3lEWlU5UWIxeGhYR3ZZVlhUcTNNUmFoQW5VeDEvd1QzU1d5d0dGQUxFTWk3Ti9XcjZRZXlzMktFVW94NXdkNGllcFZhVmdDdEwxSHRFTHFUOGZHOW5FYS9ZdHZHd2V3MnFBRFhZN09hcU5GT1VjMERhUVpTL0FwcDhOTi9WSFMiLCJtYWMiOiJlZGE0Y2JmYjQxNGZiZTgwYzFlMTAwMzcxMzc3ZDUwMWYxOTU0ZjQzZWIxOWQ1YTk3NmEzMmE3ZWU4ZmFkMGRiIiwidGFnIjoiIn0%3D; VReg30sVRccCX6m3aSzIOFcxli9ezYAI79yZpBGe=eyJpdiI6IjBiSlo2RmMxVG0zMXRHd3drNzlyd0E9PSIsInZhbHVlIjoiVDNhVUxjQ0ZuOW1NdFlKUUlDYnhyckpOMjBMMjhXSG1iZFhST3lxM2Z0bXBlK3RaT0dSZVdvNUJEd2xOUnRtSWQ4V3Z3TzAzQmFHcE5tZzFlU2pVUXdMS29Jb0d5NnVVSDhyR1d6Q3ZCVDNSQmNSWEFVQ2VRa1YyOHRVZFE5TEpnSmVzOTk3NnFQVFFUYU92aGpVRTc5QzVnNkpWTXFUNGJUV3lMU1BSZ3NEQTc4ZUxVdyt3eWFlSWJ3NFUrS3FrREdTejBRZHNLNktOSmdUb1EwOCtUSElXYWFha0lUelNZWjdGRWttTG0xOVh4Snk2WlhLa3h6TGFFczM4b3JtOGJCeUptTE5peExoVldGUW84dXJTZThEVW1NYm5Oa09kVUZnZ3FXNnpZV1djTmVrNWFtaFhlSGIybXk0cHJZdE9jd2dOTkRaVGdiejhMNlBHb1ZHYXFrRys5a0xBZ1JESmwxdlZGZVpMeUh1cUlSRDdZQldUMDdwNmJ6SHRWWTlTVmU3bTAwVnd1S01WVUVpdjdYdTR3UT09IiwibWFjIjoiYWYzMzY4M2M2YTNhMmI4MzNkMzE2MGMxZGE3YjEzZTJkY2MyZjkwZGFkYWE1YTcyN2JjMjE3NDliOTg1NGJjNiIsInRhZyI6IiJ9; TS00000000076=0868f8be6fab2800b1edfb27bfc28e83d88dc70a87e9f92349de9dfacb226485f0002a6ebbfb009aa64224612031c5920889ee682f09d0006f1b0d308ae67e5c7651c232e54a1cf1326ed14c2905a2940dc2f41f9a93f7bcb0b5ee283c860b343d4ac49f2832366dd3cb39ef9e2700ba4804b6f463ab96561f53b952bee323383b7f5b2d155e224287c2e9f50b44f21013deae82b7ece23ff41592d4af9400d7ac98a6d462a1ce90865b8becd9b226638c7222bd6df620e6aa57f6d31840c00732b59ea273294d7bb2ce5a633e85b1f16d14f25317989cd509c1ebde6299d4b9a7a8f23ecbe24384fada62277a8e1f158252c29b8fafcbf06e17bd04eb50912f91b9f2e0799beedf; TSPD_101_DID=0868f8be6fab2800b1edfb27bfc28e83d88dc70a87e9f92349de9dfacb226485f0002a6ebbfb009aa64224612031c5920889ee682f06380086a63b931c68791fa218f5fc9ffb3b30c67115c2514455c5d7b88bc26fe827fd25c7b63f595e2c5dafbf3052289e5764f1f4af1ab86d3860; TS011f2d1a=01266d26d08110df4b88acb90dd34949d6349abc0ee816d8643cf025761fecf6eee11148361255abc54fa1723e1530a9ab75949fa7; TSPD_101=0868f8be6fab28001e543973f4028a53dc7aece4d10c5fe2759c88ff16805a481876a81480c6387e4d502bf6ecb0f55e08a2d57fdb0518005e27d2beb0e8c9d25ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800ce60889b4a6e11c95c8533f7911804265fbd8bf4e3dd232391f79778249cbe61b0be18129f7ceb5f083638484017200097efea4b90a7ce49197885cd82a2fcf02e039775f401eb552d09651bbf951106; TS5220f739029=0868f8be6fab2800036b993310a5df4743e2669136f030557b5aa0ec90992fbdd66c20141ce5f85ecc38773ba37cbd49; TSf1edb2d2027=0868f8be6fab2000d27e7faaf37eb2de69dce0dfc01d6410e0305539e5d5ae7c9eff0cf4ea63567f0815872d74113000df62b47aa95d76e1553800365cdc68a9bb40b05233f7299ae88fa413f2b92bcdaffb392c5a576032f3785880223a1d0d',
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
    size = 5
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