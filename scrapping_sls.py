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
    'f5avraaaaaaaaaaaaaaaa_session_': 'BAHMHCKBIPPKGHAODANAKOCBPBHGMALAENONDENCMFOEHOCLNLAMJHIDANHLAJCIFDIDAOLGFEFNCBPGJLCAPBCLIMJPIONMIKOLBJGCAOEKIMJNNDABBNOKGAGNFGHI',
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '09c6c084112d2ab4096ac8c4f89fb34a',
    'XSRF-TOKEN': '84f2201c-c86c-4843-ab4e-69ef47d6c6ce',
    'SESSION': '8e71590b-dfc2-457e-8b4f-5aaee8e5f7b8',
    'TS0151fc2b': '0167a1c861cbf38629c13582276f21d12b5ab640eb7ba87579cd40e500fdfe1f44b498ec518558420112414768fcaaea0c66fabf16',
    'f5avraaaaaaaaaaaaaaaa_session_': 'DGMOPICCBHPMGEHOPBKCLEMGAGGCMAHMMLDPGCPJMAOIBAPJDEPLPLDMAHKNAIPMKBKDLBPDNEKAFLDGOGFALDFLIMBOMBOHCAMPPLGLPGADBCPBMDHEKJNBBJFGBLMD',
    'TS011f2d1a': '01266d26d03aaa984a01fe4f3a958d11299713dbaa798324a6a264f24c9b5afdd75d94c5dd5561b2bc13929420f97e978a1f0d5ebd',
    'TS00000000076': '0868f8be6fab280052bfbfd2538ec030e2051c91dda218e857cf2c37d2b39103bd69b006ccb2c1283fba1cf69c24d8400831e8457f09d000255880659d9ad72ebaa4f9c9abea5102da4c2abca003054bee44892013cfc866c79d92d419aa4bf52b3ce54db005657a7d4a53eeb2b4c1fef3b1d73d8413a9092286908a798d823fef6cac6e2a5b7030e69f871d4461a9acdd625be529b13f7e388fc8d377a4e54268d19e285a974fb7bdddc523da42ac994ca2cdb40d381521594005693f78451e713ca697dbd7af4ab3e720733bffa77f1a46dfa235793bf8c4d35663d4e17975401cd78d0015152837edc4a6c9fc3fc48878add9c6186df9671b9920947fe6584f8cb3d07b1b7633',
    'TSPD_101_DID': '0868f8be6fab280052bfbfd2538ec030e2051c91dda218e857cf2c37d2b39103bd69b006ccb2c1283fba1cf69c24d8400831e8457f06380099beb783b89d89ae2070a044d50c0416faeaa87d392eff3f89a0b837477b630657f557a31aebcb636c8c3d25acf33c2a4ff49aa2b4620b5e',
    'TSPD_101': '0868f8be6fab2800b3a49e0476c76aba199ca68c68a1912c9e67a82864cf76a5b5ecac644f0b0ea7abd7a53199699f4308de54146d0518004e9e447175adac975ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800aa3bdd3a6470d5676d3bb72980524175472da4de31190a5c3341106ed4f485ecd6b62bef0ac7d48d08635425aa17200034c7a751a63e10f04737e286b09ec317949c46dcb44d59cbd710c623794cc0ff',
    'TS5220f739029': '0868f8be6fab2800be08d8cb0de9af005deeceb5aa277d81d704be38b5d3c014699d2a1d3a39dcb1d900f4a291b92695',
    'TSf1edb2d2027': '0868f8be6fab20004dafb310f1c203b9129224284142d17e76e9567759349d3072aa012ca7ee813508423e4a63113000401fa276341c769f09ba2fbf2a2d1f44695e04b3f9577f3c9ad38fa4b626e5424c196fdbe6738686c6ef5bfb4405c44b',
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
    'x-xsrf-token': '84f2201c-c86c-4843-ab4e-69ef47d6c6ce',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=BAHMHCKBIPPKGHAODANAKOCBPBHGMALAENONDENCMFOEHOCLNLAMJHIDANHLAJCIFDIDAOLGFEFNCBPGJLCAPBCLIMJPIONMIKOLBJGCAOEKIMJNNDABBNOKGAGNFGHI; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=09c6c084112d2ab4096ac8c4f89fb34a; XSRF-TOKEN=84f2201c-c86c-4843-ab4e-69ef47d6c6ce; SESSION=8e71590b-dfc2-457e-8b4f-5aaee8e5f7b8; TS0151fc2b=0167a1c861cbf38629c13582276f21d12b5ab640eb7ba87579cd40e500fdfe1f44b498ec518558420112414768fcaaea0c66fabf16; f5avraaaaaaaaaaaaaaaa_session_=DGMOPICCBHPMGEHOPBKCLEMGAGGCMAHMMLDPGCPJMAOIBAPJDEPLPLDMAHKNAIPMKBKDLBPDNEKAFLDGOGFALDFLIMBOMBOHCAMPPLGLPGADBCPBMDHEKJNBBJFGBLMD; TS011f2d1a=01266d26d03aaa984a01fe4f3a958d11299713dbaa798324a6a264f24c9b5afdd75d94c5dd5561b2bc13929420f97e978a1f0d5ebd; TS00000000076=0868f8be6fab280052bfbfd2538ec030e2051c91dda218e857cf2c37d2b39103bd69b006ccb2c1283fba1cf69c24d8400831e8457f09d000255880659d9ad72ebaa4f9c9abea5102da4c2abca003054bee44892013cfc866c79d92d419aa4bf52b3ce54db005657a7d4a53eeb2b4c1fef3b1d73d8413a9092286908a798d823fef6cac6e2a5b7030e69f871d4461a9acdd625be529b13f7e388fc8d377a4e54268d19e285a974fb7bdddc523da42ac994ca2cdb40d381521594005693f78451e713ca697dbd7af4ab3e720733bffa77f1a46dfa235793bf8c4d35663d4e17975401cd78d0015152837edc4a6c9fc3fc48878add9c6186df9671b9920947fe6584f8cb3d07b1b7633; TSPD_101_DID=0868f8be6fab280052bfbfd2538ec030e2051c91dda218e857cf2c37d2b39103bd69b006ccb2c1283fba1cf69c24d8400831e8457f06380099beb783b89d89ae2070a044d50c0416faeaa87d392eff3f89a0b837477b630657f557a31aebcb636c8c3d25acf33c2a4ff49aa2b4620b5e; TSPD_101=0868f8be6fab2800b3a49e0476c76aba199ca68c68a1912c9e67a82864cf76a5b5ecac644f0b0ea7abd7a53199699f4308de54146d0518004e9e447175adac975ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800aa3bdd3a6470d5676d3bb72980524175472da4de31190a5c3341106ed4f485ecd6b62bef0ac7d48d08635425aa17200034c7a751a63e10f04737e286b09ec317949c46dcb44d59cbd710c623794cc0ff; TS5220f739029=0868f8be6fab2800be08d8cb0de9af005deeceb5aa277d81d704be38b5d3c014699d2a1d3a39dcb1d900f4a291b92695; TSf1edb2d2027=0868f8be6fab20004dafb310f1c203b9129224284142d17e76e9567759349d3072aa012ca7ee813508423e4a63113000401fa276341c769f09ba2fbf2a2d1f44695e04b3f9577f3c9ad38fa4b626e5424c196fdbe6738686c6ef5bfb4405c44b',
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