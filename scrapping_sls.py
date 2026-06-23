import pandas as pd
import requests
import os
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
    'f5avraaaaaaaaaaaaaaaa_session_': 'OBALHINHOCNLFAIFAJCAANFOBLAFNFHMNHOJOCLIFHEJNPPKENPIPNGDGLECAEPIMKMDAOJHOFGLMDOKMGKALAKFPBAKLDDNGKAAHMONCIEAFKECLPIMFCNKCFJECEAO',
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'XSRF-TOKEN': 'ca51d619-add5-4bad-9780-d83e54bc1f0d',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '9659465e252a0faffcb932a11d8b78ba',
    'TS011f2d1a': '01266d26d06e30d7eb37059230d21ac38b841ad654d69a2fbbc8a9d577692f3868b4a4ca51c262c05dd6858d15aa93d402a06abcf0',
    'TSPD_101': '0868f8be6fab280079cab0a834f205db51f1d9226a00c76bc0898f0761820e0dda58944c45aea7e91e9870c11981575108453c006205180000fe55e47944f4205ca1732140a3428bba23ce13beb1c95e',
    'SESSION': '1e351f63-9c9f-427a-86e5-1fa83fffaf0d',
    'f5avraaaaaaaaaaaaaaaa_session_': 'KPKIAHCAFEMMOJAJDENJKHHGJNFDEDAGAAECDACAMMFDDBFGKHLPCGCBKEKBOLGCILODMMFAPFKIMJMDCEBABGMLMBGGJHJOEMMDLKLALMNALLLDPNOKBKFELJJCHDAI',
    'TS5220f739077': '0868f8be6fab28007cc75178f75db9a359b1bd6eae0f01f64a310f1466d721fc83d90d4bbb92af43fc33eec2b898a11d082168b75a172000dd044b14fb438019582ce4df747a8c776deb2a59b691193d2b0b38c458b37587',
    'TS5220f739029': '0868f8be6fab2800950bbce9112d8040e2f7c9b3dc32cf2b1c40a1bbbff1ba3c4d031f7a5f744cf9bb62f95da0929e84',
    'TSf1edb2d2027': '0868f8be6fab2000a0544dab0fbb7d09452fcd9734296f3c1dc6fc148719c46ddb9e6904c0d049ec08dac3cabd113000ab40b24695b56a3d0c354e2aa66c9b0aeba5a7fa6f8962004242d20731f2e8734865b51e1ad1ea7b489b56b3bf67e544',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://fasih-sm.bps.go.id',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
    'X-XSRF-TOKEN': 'ca51d619-add5-4bad-9780-d83e54bc1f0d',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"iOS"',
    'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=OBALHINHOCNLFAIFAJCAANFOBLAFNFHMNHOJOCLIFHEJNPPKENPIPNGDGLECAEPIMKMDAOJHOFGLMDOKMGKALAKFPBAKLDDNGKAAHMONCIEAFKECLPIMFCNKCFJECEAO; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; XSRF-TOKEN=ca51d619-add5-4bad-9780-d83e54bc1f0d; db8ca2b43ed851cc93e71fd5fd72bff7=9659465e252a0faffcb932a11d8b78ba; TS011f2d1a=01266d26d06e30d7eb37059230d21ac38b841ad654d69a2fbbc8a9d577692f3868b4a4ca51c262c05dd6858d15aa93d402a06abcf0; TSPD_101=0868f8be6fab280079cab0a834f205db51f1d9226a00c76bc0898f0761820e0dda58944c45aea7e91e9870c11981575108453c006205180000fe55e47944f4205ca1732140a3428bba23ce13beb1c95e; SESSION=1e351f63-9c9f-427a-86e5-1fa83fffaf0d; f5avraaaaaaaaaaaaaaaa_session_=KPKIAHCAFEMMOJAJDENJKHHGJNFDEDAGAAECDACAMMFDDBFGKHLPCGCBKEKBOLGCILODMMFAPFKIMJMDCEBABGMLMBGGJHJOEMMDLKLALMNALLLDPNOKBKFELJJCHDAI; TS5220f739077=0868f8be6fab28007cc75178f75db9a359b1bd6eae0f01f64a310f1466d721fc83d90d4bbb92af43fc33eec2b898a11d082168b75a172000dd044b14fb438019582ce4df747a8c776deb2a59b691193d2b0b38c458b37587; TS5220f739029=0868f8be6fab2800950bbce9112d8040e2f7c9b3dc32cf2b1c40a1bbbff1ba3c4d031f7a5f744cf9bb62f95da0929e84; TSf1edb2d2027=0868f8be6fab2000a0544dab0fbb7d09452fcd9734296f3c1dc6fc148719c46ddb9e6904c0d049ec08dac3cabd113000ab40b24695b56a3d0c354e2aa66c9b0aeba5a7fa6f8962004242d20731f2e8734865b51e1ad1ea7b489b56b3bf67e544',
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
 
 
def fetch_data():
    all_rows = []
    page = 0
    size = 10

    while True:
        json_data['page'] = page
        json_data['size'] = size

        response = requests.post(
            URL_DATA,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

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