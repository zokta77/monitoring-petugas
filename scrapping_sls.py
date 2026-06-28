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
    'XSRF-TOKEN': '8305bb7c-8f1d-47be-8da5-5f07e971d8e2',
    'TS01acc472': '01266d26d0ba9fa87680b32c433fed6b4deff8b497a05d44c5e26eb607dfedabe11613e6499e374f10e072d668fc54e1572b52d261bf019ee4ab9c15dcd4c02c5d000d06b64d0af319fefaa39e733821846d567818ea0956859240abe71b2277e5675894925f44dfeefc0ef12ba7c383dfac3327aefcfa0d9ae2342a7d9035f4f0a68f0b40463d09e7b8295462eccb7fcd365577bf3f92ee20c3c4fc01779c1589c4a5b7fa026b5f72680e0086eaaf37ca7d4bb4ff34e13230c6b4e4fe85f103bc8b96f44271c4d21e83f74d960521922f65e2192b57b14e48a5220d8af774e9c37407bf36',
    'TS0151fc2b': '0167a1c86159c3a64f6d3c0c2688169a3bbe7b53a747e12571245735baa90e9cdb4b2700397dda7ca84c45e6f4cc8d6aafa1e00f1c',
    'f5avraaaaaaaaaaaaaaaa_session_': 'LKCCHEMELCEGOLAMMNPKGLKIHEMPMHCPOOCHBOHKDGLEHNPGIKBBGKJPFPDEHAIKMDODCOEDOEJHEPMKHDNAHDMAJBCKLNGCKAEHKHLHHCOLOHCKGJJPBCKLKNPNAIBB',
    'TS00000000076': '0868f8be6fab28006d6b4004204add0b95df09976268fe6039c9c864a468d940b52a25cae016ed48226f9c4e04d1cfe40827ce699b09d0000e298cfb1662aa1fe2e49c2489ec8c520d9d4d93bdb3ffefdd2355578b38ab7a96c62996d1a68372616c9939196d6333625a0d51706c534fcb351014fd6b0d4be97f3e47b5950e4a2d21c672c4611c578c7f4636435d026f0cc957ed2fa8359b4bb78190850f327ce3e2f2fcfe1d09350e775774a1d893075798f00f3df2153539b829518f8a5a58f943706539a03702a9963de153f12293700e8978ef1196a84716580c52e1e378b9c6e915ca392a6291ea4a796f1b21779c53421984c52c19bbd8543f4c3d17308eaea5e77189d6db',
    'TSPD_101_DID': '0868f8be6fab28006d6b4004204add0b95df09976268fe6039c9c864a468d940b52a25cae016ed48226f9c4e04d1cfe40827ce699b0638001cf8a7816d031242b74c54eed6d1c67da1147d82429d2e99b61e461e93d08004f2d6b1c63464542e965d47913e8e750eb6f553d0a22e4e9b',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'bf162ec33e2b5147861ac75bd6d57da9',
    'TS011f2d1a': '01266d26d03297f09436a3c8b0c99a34887f2f92b918b7e72336ca6f47db8d817e8925bdb1e9020135dd35940e2d5e16f1b89efba0',
    'TSPD_101': '0868f8be6fab28004ca21964fb855d002bfefbbc952e79dbd9f50b479196116694893b176866ab2c976df072a97fd3b90826fd51e0051800cff8e7eadd61435e5ca1732140a3428bba23ce13beb1c95e',
    'SESSION': '36c83977-6d3f-4472-a58d-fa09876280ac',
    'TS5220f739077': '0868f8be6fab280013b7c65e76ff562469ec49669b321420e0ba5252429a3fe593523b69cc0ede5da089d2d564e7b60508e21648c0172000be832f8b5bdc2e34374ce98fa9b7b64509450d6ef0291104969db12bc790ba0e',
    'TS5220f739029': '0868f8be6fab2800dfcf765b3d36f56e7dc8bd22e97e3e52b22b53cbdda4a2859404b68876a4472208f47c2fcb7bd733',
    'TSf1edb2d2027': '0868f8be6fab20003dddc17d24b1f3f3b55ce196c45380a7506a4c81eff3f8d93fd1dfa426cd51f0080deb0d23113000d2e33e8cd4af2c2a47b3441d97e388a9a6bc78abe2f6f809172ccbbb782a1932b1a2126479a5742ad4c0f3dcb4d77c75',
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
    'x-xsrf-token': '8305bb7c-8f1d-47be-8da5-5f07e971d8e2',
    'cookie': '_ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; XSRF-TOKEN=8305bb7c-8f1d-47be-8da5-5f07e971d8e2; TS01acc472=01266d26d0ba9fa87680b32c433fed6b4deff8b497a05d44c5e26eb607dfedabe11613e6499e374f10e072d668fc54e1572b52d261bf019ee4ab9c15dcd4c02c5d000d06b64d0af319fefaa39e733821846d567818ea0956859240abe71b2277e5675894925f44dfeefc0ef12ba7c383dfac3327aefcfa0d9ae2342a7d9035f4f0a68f0b40463d09e7b8295462eccb7fcd365577bf3f92ee20c3c4fc01779c1589c4a5b7fa026b5f72680e0086eaaf37ca7d4bb4ff34e13230c6b4e4fe85f103bc8b96f44271c4d21e83f74d960521922f65e2192b57b14e48a5220d8af774e9c37407bf36; TS0151fc2b=0167a1c86159c3a64f6d3c0c2688169a3bbe7b53a747e12571245735baa90e9cdb4b2700397dda7ca84c45e6f4cc8d6aafa1e00f1c; f5avraaaaaaaaaaaaaaaa_session_=LKCCHEMELCEGOLAMMNPKGLKIHEMPMHCPOOCHBOHKDGLEHNPGIKBBGKJPFPDEHAIKMDODCOEDOEJHEPMKHDNAHDMAJBCKLNGCKAEHKHLHHCOLOHCKGJJPBCKLKNPNAIBB; TS00000000076=0868f8be6fab28006d6b4004204add0b95df09976268fe6039c9c864a468d940b52a25cae016ed48226f9c4e04d1cfe40827ce699b09d0000e298cfb1662aa1fe2e49c2489ec8c520d9d4d93bdb3ffefdd2355578b38ab7a96c62996d1a68372616c9939196d6333625a0d51706c534fcb351014fd6b0d4be97f3e47b5950e4a2d21c672c4611c578c7f4636435d026f0cc957ed2fa8359b4bb78190850f327ce3e2f2fcfe1d09350e775774a1d893075798f00f3df2153539b829518f8a5a58f943706539a03702a9963de153f12293700e8978ef1196a84716580c52e1e378b9c6e915ca392a6291ea4a796f1b21779c53421984c52c19bbd8543f4c3d17308eaea5e77189d6db; TSPD_101_DID=0868f8be6fab28006d6b4004204add0b95df09976268fe6039c9c864a468d940b52a25cae016ed48226f9c4e04d1cfe40827ce699b0638001cf8a7816d031242b74c54eed6d1c67da1147d82429d2e99b61e461e93d08004f2d6b1c63464542e965d47913e8e750eb6f553d0a22e4e9b; db8ca2b43ed851cc93e71fd5fd72bff7=bf162ec33e2b5147861ac75bd6d57da9; TS011f2d1a=01266d26d03297f09436a3c8b0c99a34887f2f92b918b7e72336ca6f47db8d817e8925bdb1e9020135dd35940e2d5e16f1b89efba0; TSPD_101=0868f8be6fab28004ca21964fb855d002bfefbbc952e79dbd9f50b479196116694893b176866ab2c976df072a97fd3b90826fd51e0051800cff8e7eadd61435e5ca1732140a3428bba23ce13beb1c95e; SESSION=36c83977-6d3f-4472-a58d-fa09876280ac; TS5220f739077=0868f8be6fab280013b7c65e76ff562469ec49669b321420e0ba5252429a3fe593523b69cc0ede5da089d2d564e7b60508e21648c0172000be832f8b5bdc2e34374ce98fa9b7b64509450d6ef0291104969db12bc790ba0e; TS5220f739029=0868f8be6fab2800dfcf765b3d36f56e7dc8bd22e97e3e52b22b53cbdda4a2859404b68876a4472208f47c2fcb7bd733; TSf1edb2d2027=0868f8be6fab20003dddc17d24b1f3f3b55ce196c45380a7506a4c81eff3f8d93fd1dfa426cd51f0080deb0d23113000d2e33e8cd4af2c2a47b3441d97e388a9a6bc78abe2f6f809172ccbbb782a1932b1a2126479a5742ad4c0f3dcb4d77c75',
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
    size = 10
    session = requests.Session()

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
        time.sleep(random.uniform(1, 2))  # delay acak 1-3 detik antar request

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