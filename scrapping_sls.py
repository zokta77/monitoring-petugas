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
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'f3ce754d78c0a02cad70931f73f5d3da',
    'XSRF-TOKEN': '262a4c25-690f-4c7b-a297-271908c7eaa4',
    'SESSION': '945a23e6-aa1b-44da-bbd7-9c2106ba07ca',
    'TS011f2d1a': '01266d26d044ded7120fa21f8f0b77a084b368df8df338f5a673bd9c0963cc9bb6759119f654dd80857a40e57506fa457808e32692',
    'f5avraaaaaaaaaaaaaaaa_session_': 'PDPNKMPAMCDDGCOBGPLJINIMEMIDCGLBPLICDHNOEOBAFEDOOBIENKMPBLPKIFNKMLEDEECADFIHCHFNPNOAGJALAHNBJNLLMHKAOHODGADLEGHLLBBJLOINKIHCNELB',
    'TS00000000076': '0868f8be6fab2800b38d254720039bec67607f0c4436a651ec14778944e8832308dfde5e6b53b89a1560ac68cfaef6d808c5d6c15b09d0001f1c70dff3253396ea9014fb3d9f184696c7bfed35f45a4f12e11ea9a1074979bc79d528ac44e7e0a0cad98322bcf7106f1c6b4e461581da8959f08d8aa646236fddc3872e6684a7bac83bcf60d819071394d5828eed6022e44e34a5f038e63ba18421ecc5dc65fefb29cdbfb984ce8f019e965719a453a74f7c2a70cbf57b68338f96c456165bda53450ce4d8d6af97458038e83a85e4162dbe1cba428ac3d2876b4c438d6b71a017ddb31273890e8744ca279401a02ad64416d23583febc7ce08198c406b5d882068ecf22d2918ea7',
    'TSPD_101_DID': '0868f8be6fab2800b38d254720039bec67607f0c4436a651ec14778944e8832308dfde5e6b53b89a1560ac68cfaef6d808c5d6c15b063800cae0c43dfe0603a32fdd2b1381135fd7bb6d3fdc3bbd14501737168e594193c397ed93d899d40e602463da1a8da5b31d82428484c4365731',
    'TSPD_101': '0868f8be6fab2800455b01bca0e4f1d2a1f1b5e203fc368d0603a969b55c834bfca5623bd2651bea09f246112530ce9c0859103adb0518002789228f14555a185ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800cdfe3ec6a7ff5ae7671f2e474c7cc00ac7e2698751b18d8c7ddb68865e2b473145fe5d8af91a8e2008ab14e9bd172000b6e10c68c3c49b985bfca5ff8ecde17e66d3d2614b8f4060f27e0d5ce4d1f35d',
    'TS5220f739029': '0868f8be6fab28009a277a0b0b76de4d2a675ab209c56a99353368d18e4a6173f3fb5b305a269179c7813b859143ce22',
    'TSf1edb2d2027': '0868f8be6fab2000f8f2f12a01bee96e5f20d9445e0a41aeab4ab5135484e5b6b258f522722c3a4108339283a31130009a794b79bcb2a33e59be080657c60f5ab95dbc1d1a5646a157f25491bc1e51d17047fa96e4ce6fc3a1ab697fc81a854d',
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
    'x-xsrf-token': '262a4c25-690f-4c7b-a297-271908c7eaa4',
    'cookie': '_ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=f3ce754d78c0a02cad70931f73f5d3da; XSRF-TOKEN=262a4c25-690f-4c7b-a297-271908c7eaa4; SESSION=945a23e6-aa1b-44da-bbd7-9c2106ba07ca; TS011f2d1a=01266d26d044ded7120fa21f8f0b77a084b368df8df338f5a673bd9c0963cc9bb6759119f654dd80857a40e57506fa457808e32692; f5avraaaaaaaaaaaaaaaa_session_=PDPNKMPAMCDDGCOBGPLJINIMEMIDCGLBPLICDHNOEOBAFEDOOBIENKMPBLPKIFNKMLEDEECADFIHCHFNPNOAGJALAHNBJNLLMHKAOHODGADLEGHLLBBJLOINKIHCNELB; TS00000000076=0868f8be6fab2800b38d254720039bec67607f0c4436a651ec14778944e8832308dfde5e6b53b89a1560ac68cfaef6d808c5d6c15b09d0001f1c70dff3253396ea9014fb3d9f184696c7bfed35f45a4f12e11ea9a1074979bc79d528ac44e7e0a0cad98322bcf7106f1c6b4e461581da8959f08d8aa646236fddc3872e6684a7bac83bcf60d819071394d5828eed6022e44e34a5f038e63ba18421ecc5dc65fefb29cdbfb984ce8f019e965719a453a74f7c2a70cbf57b68338f96c456165bda53450ce4d8d6af97458038e83a85e4162dbe1cba428ac3d2876b4c438d6b71a017ddb31273890e8744ca279401a02ad64416d23583febc7ce08198c406b5d882068ecf22d2918ea7; TSPD_101_DID=0868f8be6fab2800b38d254720039bec67607f0c4436a651ec14778944e8832308dfde5e6b53b89a1560ac68cfaef6d808c5d6c15b063800cae0c43dfe0603a32fdd2b1381135fd7bb6d3fdc3bbd14501737168e594193c397ed93d899d40e602463da1a8da5b31d82428484c4365731; TSPD_101=0868f8be6fab2800455b01bca0e4f1d2a1f1b5e203fc368d0603a969b55c834bfca5623bd2651bea09f246112530ce9c0859103adb0518002789228f14555a185ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800cdfe3ec6a7ff5ae7671f2e474c7cc00ac7e2698751b18d8c7ddb68865e2b473145fe5d8af91a8e2008ab14e9bd172000b6e10c68c3c49b985bfca5ff8ecde17e66d3d2614b8f4060f27e0d5ce4d1f35d; TS5220f739029=0868f8be6fab28009a277a0b0b76de4d2a675ab209c56a99353368d18e4a6173f3fb5b305a269179c7813b859143ce22; TSf1edb2d2027=0868f8be6fab2000f8f2f12a01bee96e5f20d9445e0a41aeab4ab5135484e5b6b258f522722c3a4108339283a31130009a794b79bcb2a33e59be080657c60f5ab95dbc1d1a5646a157f25491bc1e51d17047fa96e4ce6fc3a1ab697fc81a854d',
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
        time.sleep(random.uniform(1, 3))  # delay acak 1-3 detik antar request

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