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
    'f5avraaaaaaaaaaaaaaaa_session_': 'IMAPMOCKEPDNFOKHFFDNMPEDJGLEGOBNLKIFKPOKCODJDMLPOIEFKMONINACBPOAJDCDPDFDJDMCHODJJKEAEILODGADOCBCEHIOGGIJELCHINLDNHJHEIFMGFPHFNGE',
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'XSRF-TOKEN': 'e4fd2cac-4c84-46a3-ad35-0642e8c8be23',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '9167d391c996d1ee03a563e7bdb935d3',
    'JSESSIONID': 'E64F9E8024307DF79D5F2AD8C74F57B1',
    'SESSION': '2b7b563f-7cb0-46b1-901d-3ca68d3e66de',
    'TS01876da2': '01266d26d07110c0f5a9d967c9c08d43cc2c2ca1209d4fdcdd1d2746a67b0fe1856a42b70c89b8c304286c60271d720c40435bf4bd4efb8a2f7e55b64cfbbda45c470cc97e93fec69f8e946c626207c4f3eb5675410d6a660189ede28386e17372314e9fbb58b3e8ae423977775f631552decccaf8',
    'TS00000000076': '0868f8be6fab2800b2b9fce2a41e968fdacd9bbe6f138035abb326619ae53ae07e6aa14124483f0a1e106a30dcd78fc1089261362609d000f859a3d0522b325d74f4f01a49f4bc97e91714845c382c433f29e442da1113b1cad083fb243bca10cf3199c3cd7f17650db71dc835c607445679dbb90323ec58ae75fdfcab27a002e773606ffd5a2f383c9d1356b925fcaeb7b3a768bd63daecf589ea1c2a40a59576a6c98ed148b60a71bbf2bdf9e7e7402856bc7fdb01e338f603d0f99ea295f63b3d12c57ed756cbdcc730e208d8e3b4e0290b6f3cbe8841eb27b808033ab4300f48e839343fc43ae85e98d9c86ad6fa14aa5e3c2d1c7b3777948a99b967b38b66c8585789026a36',
    'TSPD_101_DID': '0868f8be6fab2800b2b9fce2a41e968fdacd9bbe6f138035abb326619ae53ae07e6aa14124483f0a1e106a30dcd78fc10892613626063800db255d5a2f0ec78fd6ce7f89989d1eaaed2569c6cd922f8c232ad0efaed334d50f2beba7fae0e4cd19031b48168ffcffcf9271a59819b43a',
    'TS011f2d1a': '01266d26d040a480503a27a429d7c40a709940d718f8c4e9a679edeef64e9473fee82a06cea2bfd0f8db8b4f75713cb7b1fbc91e50',
    'TSPD_101': '0868f8be6fab2800ca9a55a82ff565b08c0e3ab1d0766623bea37c57afc2888252ee7e457e14849f5eb49e6a8e60e3940881c9c131051800f9bff09e967022585ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'GKHAMOCKEPDNFOKHICLNMPEDJGLEGOBNLKIFKPOKCODJDMLPOIEFKMONINACBPOAJDCDPDFDFDMCLODJJKEAEILOIGADKCBCEHIOGGIJELCHINDDNHJHEIFMGFPHFNBK',
    'TS5220f739077': '0868f8be6fab280008062832e382e46f4e7e9eeef050fc72eeea73e335450352d935dba26cec79078f5e20cddcc248fa089194cd5e1720008cd8d6d9f23aea8142b429100b018cda45312857a3de5b4a3b0ef7437d407cb2',
    'TS5220f739029': '0868f8be6fab28009e8b5ce85b0a47b4a65dc6e454067004962e41c7abf47d0a60f228052d3a114418b49ebfc0426272',
    'TSf1edb2d2027': '0868f8be6fab200033a3ccc4e832f80530984cf33ca6c267b8d8a3de09cff9a4347167f720b91d88084db837ac113000826b26a07c4df092af3e70565cc0d2fc5a9bfe0d6f8cb64b6edd923d712d115ed71b0ca8fd3eb8c95c1e3ac6298f53c0',
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
    'x-xsrf-token': 'e4fd2cac-4c84-46a3-ad35-0642e8c8be23',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=IMAPMOCKEPDNFOKHFFDNMPEDJGLEGOBNLKIFKPOKCODJDMLPOIEFKMONINACBPOAJDCDPDFDJDMCHODJJKEAEILODGADOCBCEHIOGGIJELCHINLDNHJHEIFMGFPHFNGE; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; XSRF-TOKEN=e4fd2cac-4c84-46a3-ad35-0642e8c8be23; db8ca2b43ed851cc93e71fd5fd72bff7=9167d391c996d1ee03a563e7bdb935d3; JSESSIONID=E64F9E8024307DF79D5F2AD8C74F57B1; SESSION=2b7b563f-7cb0-46b1-901d-3ca68d3e66de; TS01876da2=01266d26d07110c0f5a9d967c9c08d43cc2c2ca1209d4fdcdd1d2746a67b0fe1856a42b70c89b8c304286c60271d720c40435bf4bd4efb8a2f7e55b64cfbbda45c470cc97e93fec69f8e946c626207c4f3eb5675410d6a660189ede28386e17372314e9fbb58b3e8ae423977775f631552decccaf8; TS00000000076=0868f8be6fab2800b2b9fce2a41e968fdacd9bbe6f138035abb326619ae53ae07e6aa14124483f0a1e106a30dcd78fc1089261362609d000f859a3d0522b325d74f4f01a49f4bc97e91714845c382c433f29e442da1113b1cad083fb243bca10cf3199c3cd7f17650db71dc835c607445679dbb90323ec58ae75fdfcab27a002e773606ffd5a2f383c9d1356b925fcaeb7b3a768bd63daecf589ea1c2a40a59576a6c98ed148b60a71bbf2bdf9e7e7402856bc7fdb01e338f603d0f99ea295f63b3d12c57ed756cbdcc730e208d8e3b4e0290b6f3cbe8841eb27b808033ab4300f48e839343fc43ae85e98d9c86ad6fa14aa5e3c2d1c7b3777948a99b967b38b66c8585789026a36; TSPD_101_DID=0868f8be6fab2800b2b9fce2a41e968fdacd9bbe6f138035abb326619ae53ae07e6aa14124483f0a1e106a30dcd78fc10892613626063800db255d5a2f0ec78fd6ce7f89989d1eaaed2569c6cd922f8c232ad0efaed334d50f2beba7fae0e4cd19031b48168ffcffcf9271a59819b43a; TS011f2d1a=01266d26d040a480503a27a429d7c40a709940d718f8c4e9a679edeef64e9473fee82a06cea2bfd0f8db8b4f75713cb7b1fbc91e50; TSPD_101=0868f8be6fab2800ca9a55a82ff565b08c0e3ab1d0766623bea37c57afc2888252ee7e457e14849f5eb49e6a8e60e3940881c9c131051800f9bff09e967022585ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=GKHAMOCKEPDNFOKHICLNMPEDJGLEGOBNLKIFKPOKCODJDMLPOIEFKMONINACBPOAJDCDPDFDFDMCLODJJKEAEILOIGADKCBCEHIOGGIJELCHINDDNHJHEIFMGFPHFNBK; TS5220f739077=0868f8be6fab280008062832e382e46f4e7e9eeef050fc72eeea73e335450352d935dba26cec79078f5e20cddcc248fa089194cd5e1720008cd8d6d9f23aea8142b429100b018cda45312857a3de5b4a3b0ef7437d407cb2; TS5220f739029=0868f8be6fab28009e8b5ce85b0a47b4a65dc6e454067004962e41c7abf47d0a60f228052d3a114418b49ebfc0426272; TSf1edb2d2027=0868f8be6fab200033a3ccc4e832f80530984cf33ca6c267b8d8a3de09cff9a4347167f720b91d88084db837ac113000826b26a07c4df092af3e70565cc0d2fc5a9bfe0d6f8cb64b6edd923d712d115ed71b0ca8fd3eb8c95c1e3ac6298f53c0',
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
    schedule.every(3).hours.do(job)

    print("⏱️  Script berjalan otomatis setiap 3 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)