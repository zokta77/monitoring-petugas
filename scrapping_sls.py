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
    'f5avraaaaaaaaaaaaaaaa_session_': 'GCGGLGEPFMGLMOHLEDJLILCEHFBJENBFPHGIAPOMPPEALJGCOGLGINDDGFOBLPGLINMDCGJOJFNKFICCKMOAIFIGCBAEFIGNKNLIABCKJKLDLMMPJKKPFEGIBLIJIGBK',
    '_ga_G604FXJW6E': 'GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0',
    '_ga_WQKDWE3S3T': 'GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0',
    'cf_clearance': 'KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw',
    '_ga_T7YPSCVK8R': 'GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0',
    '_ga': 'GA1.3.1484741960.1780902145',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '9167d391c996d1ee03a563e7bdb935d3',
    'XSRF-TOKEN': '9c143a0d-ebdb-4da0-98a4-882ec57371ab',
    'SESSION': '60449344-edba-4098-986d-02963afe4636',
    'TS018af012': '0167a1c8617a3473845fc43d03dd672c117c557f4dc2db4c1f52e0f84430e3fbc477bab1efea108e089938f6e00069faf58869fec8605432a45edae5bc586e1cb92901f7a000e28b10f4336202c4cf5a14af650e82',
    'TS01acc472': '01266d26d0342f5c80dbfcf6a60dcc15d17fa58b7b645cdfa75072c68c6c84ad60792434a5d78733ca9e9477526f0ac3d1475e00346b03931000bd41b0872e700db19504a4e7c9f7bf10cc47e9c95f4c6cd655ab9728f26687488e06bc81dc694d07e85da98a4044d93bbded3b000264d09fe6688d584f6f994cbb30562e9ec9b31004b0d6',
    'TS00000000076': '0868f8be6fab2800517aaf366e1ffb513012c3e55031f611bab7c4287a003d743fdf803f0f6f2da1ffa208b6c6aafcca086bff587909d000978abc29a64f1be5443819aa7fec905b3ed4cef80b78bdafa7b7748838ad087d63e1a05485e6954e39565d100629052611ac75bf158fa58c4f89c3926c599eaeea03e3c107f594042c4f9c03c0af4d86abe023112ec5a432b52c56fb97dead0dea58acac771e995cf0c8d58d1f2a72b61e1480fe9aa086bf2f9e20dd4ba5547d41a9771dd77c09ca015bf48c6b5bcd4bc0b9692223c590120741356266e7f9f36c2e176845b96d37d030f448846b1c66c33b481097600dc8efb48767e1acd91ab66a7fd5e03037fb24b21de9ce749b0a',
    'TSPD_101_DID': '0868f8be6fab2800517aaf366e1ffb513012c3e55031f611bab7c4287a003d743fdf803f0f6f2da1ffa208b6c6aafcca086bff58790638008fffdba509a4fd68950e8d0da4bec76e3bd69852a473e99090ff4d246e825dcce64c232df623d2ab8c057e02ddb45bd799328bfad5595a11',
    'TS011f2d1a': '01266d26d043d77d74eb34b7711d585c33b5cb07997ac752e0f9485c6496e82817623281343f00055d10ca3e9a7ecfe2b96d066952',
    'TSPD_101': '0868f8be6fab280044a65c7f990b0bb73a32d6e37f35f64e3d395990e6a9675d43611b6f5a09aafb497e2dcc55771cd7085a8dab38051800204939decef4c7ba5ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'ENJDCOCIFBNEBGLPLLLNNEDGLKLOOPHMNOPGEGLHNHGKMCNCGNIDDBELKBICDHMMDLGDGLANIFDOELLGGPIAMFILBBMBNKKFEBLPAIABBPMOOJPKIJBFDGADECNIAFNL',
    'TS5220f739077': '0868f8be6fab2800203191adfc1631c6f6fbdde3744676b075ad4a5a6269f40336bd277109db6cba7345dcf742a3e7e5085e6ac9e41720000482732ed949c9947fa4f6a277e1e46b4823e2fd8985171d38fcaa5be24cd59a',
    'TS5220f739029': '0868f8be6fab28009f874a6c29452050a19a1aff4723df7a9ca6bbf41efba085eff9a5ebc4f204a288d672110bc88ac9',
    'TSf1edb2d2027': '0868f8be6fab2000ab0e15cc2e0354d0478fd69a7aa4e6071f2f3dbcd3554e5a4a787354b080c9a4082d36825a113000b7ee229fabb7dfab66c0ec6436d8d5da57fdac82dda83fd3b1d3106b3ec0252c42ce0607e2011281886d4064cd0b615d',
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
    'x-xsrf-token': '9c143a0d-ebdb-4da0-98a4-882ec57371ab',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=GCGGLGEPFMGLMOHLEDJLILCEHFBJENBFPHGIAPOMPPEALJGCOGLGINDDGFOBLPGLINMDCGJOJFNKFICCKMOAIFIGCBAEFIGNKNLIABCKJKLDLMMPJKKPFEGIBLIJIGBK; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=9167d391c996d1ee03a563e7bdb935d3; XSRF-TOKEN=9c143a0d-ebdb-4da0-98a4-882ec57371ab; SESSION=60449344-edba-4098-986d-02963afe4636; TS018af012=0167a1c8617a3473845fc43d03dd672c117c557f4dc2db4c1f52e0f84430e3fbc477bab1efea108e089938f6e00069faf58869fec8605432a45edae5bc586e1cb92901f7a000e28b10f4336202c4cf5a14af650e82; TS01acc472=01266d26d0342f5c80dbfcf6a60dcc15d17fa58b7b645cdfa75072c68c6c84ad60792434a5d78733ca9e9477526f0ac3d1475e00346b03931000bd41b0872e700db19504a4e7c9f7bf10cc47e9c95f4c6cd655ab9728f26687488e06bc81dc694d07e85da98a4044d93bbded3b000264d09fe6688d584f6f994cbb30562e9ec9b31004b0d6; TS00000000076=0868f8be6fab2800517aaf366e1ffb513012c3e55031f611bab7c4287a003d743fdf803f0f6f2da1ffa208b6c6aafcca086bff587909d000978abc29a64f1be5443819aa7fec905b3ed4cef80b78bdafa7b7748838ad087d63e1a05485e6954e39565d100629052611ac75bf158fa58c4f89c3926c599eaeea03e3c107f594042c4f9c03c0af4d86abe023112ec5a432b52c56fb97dead0dea58acac771e995cf0c8d58d1f2a72b61e1480fe9aa086bf2f9e20dd4ba5547d41a9771dd77c09ca015bf48c6b5bcd4bc0b9692223c590120741356266e7f9f36c2e176845b96d37d030f448846b1c66c33b481097600dc8efb48767e1acd91ab66a7fd5e03037fb24b21de9ce749b0a; TSPD_101_DID=0868f8be6fab2800517aaf366e1ffb513012c3e55031f611bab7c4287a003d743fdf803f0f6f2da1ffa208b6c6aafcca086bff58790638008fffdba509a4fd68950e8d0da4bec76e3bd69852a473e99090ff4d246e825dcce64c232df623d2ab8c057e02ddb45bd799328bfad5595a11; TS011f2d1a=01266d26d043d77d74eb34b7711d585c33b5cb07997ac752e0f9485c6496e82817623281343f00055d10ca3e9a7ecfe2b96d066952; TSPD_101=0868f8be6fab280044a65c7f990b0bb73a32d6e37f35f64e3d395990e6a9675d43611b6f5a09aafb497e2dcc55771cd7085a8dab38051800204939decef4c7ba5ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=ENJDCOCIFBNEBGLPLLLNNEDGLKLOOPHMNOPGEGLHNHGKMCNCGNIDDBELKBICDHMMDLGDGLANIFDOELLGGPIAMFILBBMBNKKFEBLPAIABBPMOOJPKIJBFDGADECNIAFNL; TS5220f739077=0868f8be6fab2800203191adfc1631c6f6fbdde3744676b075ad4a5a6269f40336bd277109db6cba7345dcf742a3e7e5085e6ac9e41720000482732ed949c9947fa4f6a277e1e46b4823e2fd8985171d38fcaa5be24cd59a; TS5220f739029=0868f8be6fab28009f874a6c29452050a19a1aff4723df7a9ca6bbf41efba085eff9a5ebc4f204a288d672110bc88ac9; TSf1edb2d2027=0868f8be6fab2000ab0e15cc2e0354d0478fd69a7aa4e6071f2f3dbcd3554e5a4a787354b080c9a4082d36825a113000b7ee229fabb7dfab66c0ec6436d8d5da57fdac82dda83fd3b1d3106b3ec0252c42ce0607e2011281886d4064cd0b615d',
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