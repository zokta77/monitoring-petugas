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
    'f5avraaaaaaaaaaaaaaaa_session_': 'KFDOMAEADHHKGECFHMNPMGEPLPAANEJEHILBFFNIAEAHKGOGIOGGGFGDFPIHLDDAAKGDOLOCIPBNHJNDAPHACOLAENHELJNPHGINFNOEGBBFFFBGDEJKIHOEHHCHECFC',
    'f5avraaaaaaaaaaaaaaaa_session_': 'COANKBDBPEEFLEOEBEGFBKMBGPBJOCMEBAHFOJDODOJKIGELEPEEEFHMFHIPFJGCCJODNHLDLOAIEJBGKDMAFDJJPNACBCCNCAKHPGCKJKBJGJENBMIBKCANEEEGNKKO',
    'f5_cspm': '1234',
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '15faddc55339961e726413df06a9e1dc',
    'XSRF-TOKEN': '97678423-de9c-4142-8b9a-a341e4715bfc',
    'SESSION': '30246b37-a24f-4b27-b730-628b4059479c',
    'TS011f2d1a': '01266d26d00b8104f1a2b4caa3b04155e1e2d3bedeee004f297cb545047e1ca0c3f1c9e795edf6e754e130235b3c6c8f22add88a9f',
    'TSPD_101': '0868f8be6fab2800d0ac4f1780646957c7745d95db7a45ab74e10611798f1e650930cfef484657a4cc1bae6c82a646a508997edf880518001e19d3bfb37dfb405ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'MPOACJEGMGAHIMJBOGNPHBGIHCMFFBBCDKKMJCGAGLCBHOLKCKAEGNNGJFPOGNINODMDDBLCFPFJOFPNGJGAJDEDDNKIDBKKELLJLCOCBLOGPGDGBDJDOJPFLDMFNNPL',
    'TS0151fc2b': '0167a1c8619dc1908b76efbeb3d5d2a46e78ac2558ba5d5f186b3b750d5506d9308608de354b443e3d8f0bcb835a2e0426dc403e3b',
    'TS5220f739077': '0868f8be6fab2800ef405108b0c6b51746e6c979f4824fda034d9e6494f9864f47994625f73276ed0e6147f94d18e998082a5aa1831720004e68605e409e85fa209222ca350e084fed80a973c2e252f56238db80f676bfa0',
    'TS5220f739029': '0868f8be6fab2800be6fe0e53ab78da1e5da5178f23fa2333a00046cf47ea9787e8ae93e1c497d1275910703df9e137d',
    'TSf1edb2d2027': '0868f8be6fab20005e23d5cd14421b104a6d48cfd52b47a2b1fa051fac249a089ae078effbb54f0008f22387a61130008f036592770b55c9d4c1d0ee6e87ca5b0cbd1570b66608d6d4ca04f5acfc66ee1faa918f3cb6a99e832c397530bca47c',
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
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
    'X-XSRF-TOKEN': '97678423-de9c-4142-8b9a-a341e4715bfc',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=KFDOMAEADHHKGECFHMNPMGEPLPAANEJEHILBFFNIAEAHKGOGIOGGGFGDFPIHLDDAAKGDOLOCIPBNHJNDAPHACOLAENHELJNPHGINFNOEGBBFFFBGDEJKIHOEHHCHECFC; f5avraaaaaaaaaaaaaaaa_session_=COANKBDBPEEFLEOEBEGFBKMBGPBJOCMEBAHFOJDODOJKIGELEPEEEFHMFHIPFJGCCJODNHLDLOAIEJBGKDMAFDJJPNACBCCNCAKHPGCKJKBJGJENBMIBKCANEEEGNKKO; f5_cspm=1234; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=15faddc55339961e726413df06a9e1dc; XSRF-TOKEN=97678423-de9c-4142-8b9a-a341e4715bfc; SESSION=30246b37-a24f-4b27-b730-628b4059479c; TS011f2d1a=01266d26d00b8104f1a2b4caa3b04155e1e2d3bedeee004f297cb545047e1ca0c3f1c9e795edf6e754e130235b3c6c8f22add88a9f; TSPD_101=0868f8be6fab2800d0ac4f1780646957c7745d95db7a45ab74e10611798f1e650930cfef484657a4cc1bae6c82a646a508997edf880518001e19d3bfb37dfb405ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=MPOACJEGMGAHIMJBOGNPHBGIHCMFFBBCDKKMJCGAGLCBHOLKCKAEGNNGJFPOGNINODMDDBLCFPFJOFPNGJGAJDEDDNKIDBKKELLJLCOCBLOGPGDGBDJDOJPFLDMFNNPL; TS0151fc2b=0167a1c8619dc1908b76efbeb3d5d2a46e78ac2558ba5d5f186b3b750d5506d9308608de354b443e3d8f0bcb835a2e0426dc403e3b; TS5220f739077=0868f8be6fab2800ef405108b0c6b51746e6c979f4824fda034d9e6494f9864f47994625f73276ed0e6147f94d18e998082a5aa1831720004e68605e409e85fa209222ca350e084fed80a973c2e252f56238db80f676bfa0; TS5220f739029=0868f8be6fab2800be6fe0e53ab78da1e5da5178f23fa2333a00046cf47ea9787e8ae93e1c497d1275910703df9e137d; TSf1edb2d2027=0868f8be6fab20005e23d5cd14421b104a6d48cfd52b47a2b1fa051fac249a089ae078effbb54f0008f22387a61130008f036592770b55c9d4c1d0ee6e87ca5b0cbd1570b66608d6d4ca04f5acfc66ee1faa918f3cb6a99e832c397530bca47c',
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
        on="regionCode",
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