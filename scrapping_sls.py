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
    'f5avraaaaaaaaaaaaaaaa_session_': 'CEIAONEJDHOOIIIKAMMLLGPPNFDFKFOEILJPFLLFDILFAFNLAMPECICECNMBMBBIFFODEEDJNLKPDDCMKDJAFBBHPBJIFPKNCPHBPEILAIDGKKAEAKHBDAIJDJNLKOGC',
    'TS00000000076': '0868f8be6fab2800d7ed7281147db2ce2f10390f29db28fec082b0ef6294b6c3556bb8bf99a7ede237cbc7306eabfe0f087d4892f909d0003bb94fc262d13460ecc77314f0e2ebf3ddede0e6a985db90ef84efb499da119ffbb14025356179b618e726260cfe3ecaaec0c6da5adc3bcf0104fd05e6b772627b3908ffbe5f368fab4a7382be83790401e58ddbd698d2b5fd11966c9b34d601b1298a498213118ff19a62ded549e6be641180ab220e985b9b6d1b9a2c4ecc0e9d03f42d5f5b336a405181e73d45830a7700818bef71b6f019df737e449139c67990007540808c8045461573f377cb67d8f3571e525b3671c90f6ff4f225eac8cfbeffc274dfd604353bb676710927fd',
    'TSPD_101_DID': '0868f8be6fab2800d7ed7281147db2ce2f10390f29db28fec082b0ef6294b6c3556bb8bf99a7ede237cbc7306eabfe0f087d4892f9063800ec2bf43d7a718ad6fd1fdb348318ba7871f17e08f69ec0573ad1a0482e13beca5138752682d8279a31d3193e82ca6274b1997579098d82c8',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'ce25186e750651d5e1e61a27d48e3469',
    'TS011f2d1a': '01266d26d02ea944c76d99b8038337affb0933050bd8724c4a6bf5cef107b1513cb8f7f160efdb6ca187556613eca2f9556f54a4b0',
    'TSPD_101': '0868f8be6fab28002c7838ae51234909fd914006f6fb308511083873b035c267ab7984974585201b607382f2988923b208442e1edd0518000e5712532a3502255ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': 'eb395f69-5714-48f5-b099-6e59329b735f',
    'SESSION': 'ccdc0ca3-b58f-4acf-8bb7-d8ee0248b41e',
    'TS5220f739077': '0868f8be6fab28008e8aa1a9f5a469349c99f97d538c0ab498c11e8db9a4b5e1fdeaa612a8a885db72c6256ef72972190885998678172000c65464eada6bc10b62d1ca75c8c709500607e83eaf1770ed3e4766495f661ef1',
    'TS5220f739029': '0868f8be6fab28008e47993b9f3f33a4cde5b7d4b6a87989c8d07cf08906148b44ab33e5fab4361863ac12fec277e312',
    'TSf1edb2d2027': '0868f8be6fab20003f34b4639505e48a821ed03fddab2d2d257754a05ba05f1768726d6ece0bf844086fc113421130005a9a82771fae38c9bbebbc47eba6e5e4301a9372d9d966f3ee31fa3e3ae92ed8db43d262fc12f42804acd5ac77d7af4d',
    'TS0151fc2b': '0167a1c861485aae9db69194bee579ee0fb6e2d0eef4aadc618be5d1147752fe510a412a03bbcba2ee4e560da394c6aa6818e28aff',
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
    'x-xsrf-token': 'eb395f69-5714-48f5-b099-6e59329b735f',
    'cookie': '_ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=CEIAONEJDHOOIIIKAMMLLGPPNFDFKFOEILJPFLLFDILFAFNLAMPECICECNMBMBBIFFODEEDJNLKPDDCMKDJAFBBHPBJIFPKNCPHBPEILAIDGKKAEAKHBDAIJDJNLKOGC; TS00000000076=0868f8be6fab2800d7ed7281147db2ce2f10390f29db28fec082b0ef6294b6c3556bb8bf99a7ede237cbc7306eabfe0f087d4892f909d0003bb94fc262d13460ecc77314f0e2ebf3ddede0e6a985db90ef84efb499da119ffbb14025356179b618e726260cfe3ecaaec0c6da5adc3bcf0104fd05e6b772627b3908ffbe5f368fab4a7382be83790401e58ddbd698d2b5fd11966c9b34d601b1298a498213118ff19a62ded549e6be641180ab220e985b9b6d1b9a2c4ecc0e9d03f42d5f5b336a405181e73d45830a7700818bef71b6f019df737e449139c67990007540808c8045461573f377cb67d8f3571e525b3671c90f6ff4f225eac8cfbeffc274dfd604353bb676710927fd; TSPD_101_DID=0868f8be6fab2800d7ed7281147db2ce2f10390f29db28fec082b0ef6294b6c3556bb8bf99a7ede237cbc7306eabfe0f087d4892f9063800ec2bf43d7a718ad6fd1fdb348318ba7871f17e08f69ec0573ad1a0482e13beca5138752682d8279a31d3193e82ca6274b1997579098d82c8; db8ca2b43ed851cc93e71fd5fd72bff7=ce25186e750651d5e1e61a27d48e3469; TS011f2d1a=01266d26d02ea944c76d99b8038337affb0933050bd8724c4a6bf5cef107b1513cb8f7f160efdb6ca187556613eca2f9556f54a4b0; TSPD_101=0868f8be6fab28002c7838ae51234909fd914006f6fb308511083873b035c267ab7984974585201b607382f2988923b208442e1edd0518000e5712532a3502255ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=eb395f69-5714-48f5-b099-6e59329b735f; SESSION=ccdc0ca3-b58f-4acf-8bb7-d8ee0248b41e; TS5220f739077=0868f8be6fab28008e8aa1a9f5a469349c99f97d538c0ab498c11e8db9a4b5e1fdeaa612a8a885db72c6256ef72972190885998678172000c65464eada6bc10b62d1ca75c8c709500607e83eaf1770ed3e4766495f661ef1; TS5220f739029=0868f8be6fab28008e47993b9f3f33a4cde5b7d4b6a87989c8d07cf08906148b44ab33e5fab4361863ac12fec277e312; TSf1edb2d2027=0868f8be6fab20003f34b4639505e48a821ed03fddab2d2d257754a05ba05f1768726d6ece0bf844086fc113421130005a9a82771fae38c9bbebbc47eba6e5e4301a9372d9d966f3ee31fa3e3ae92ed8db43d262fc12f42804acd5ac77d7af4d; TS0151fc2b=0167a1c861485aae9db69194bee579ee0fb6e2d0eef4aadc618be5d1147752fe510a412a03bbcba2ee4e560da394c6aa6818e28aff',
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