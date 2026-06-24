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
    '_ga_FMZTHHQN2K': 'GS2.1.s1778035370$o1$g1$t1778035723$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1778035727$o1$g1$t1778035852$j60$l0$h0',
    '_ga_K98R6MSKRH': 'GS2.1.s1778314369$o1$g1$t1778314389$j40$l0$h0',
    '_ga_9E7L2XJ89Y': 'GS2.1.s1778465304$o1$g0$t1778465307$j57$l0$h0',
    'cf_clearance': 'CwLXIaLV3mmGpRwuhuAC30Uco3Pjb_tz_1ZEbXnsvlo-1780364611-1.2.1.1-JeJaibKrj6XS4kPV4Ip25uQkYHC0SxIs56rfZupCrrK8yP_H6zi1dSFcMZnahwgzur4pRIS8XT8t.FS4e5IZD.l09FvOnFaWnw1eLG9FQpfiCb6rGNDUqraHwu0yGtfqjoATjtiW8VgnuTu7I13XGK8qcdi5YicZDzmWAEfbg0GfAms1zt6a3TtivoUKuPHm91832sMMPQ4eCQ77uVHVtMj8thYLEZbhWlQGGd8TE3ZqmJ1dIjlbGtBIMzKCS9YrdI3BX4QMqGMRNKdCVHFpJhQyO3yvQt5ZK3mFh83hjYJJSLZJnszvXzwkM5Q._LIPvYpMzOE_zhyRpUg2Nrd2rA',
    '_ga': 'GA1.3.337823039.1778035336',
    '_ga_XXTTVXWHDB': 'GS2.3.s1780364612$o4$g1$t1780364813$j60$l0$h0',
    'f5avraaaaaaaaaaaaaaaa_session_': 'BMNNBEEOEMIHPFNPGLEKMKCNGPJNBJAOOBMBCBDJGNEHJPGIPNGDPNPCCCNDJAEKIKKDGEPBIKLPOPCMNKOAHHACAFKKMGLMHPLFDCMGICBOLEJFDKNMGPCLAFECMJLH',
    'TS00000000076': '0868f8be6fab28005f0e4997f5efe6af55eb896c4e70a0f28f2571425cdf3a82d2ff30b52d098121c43983b4f2aff9ef084d51969c09d0007946dbf900ab12446650ec365ac445759c547051dd9ac49645b8e0d5382f9c2eadcc9d1d1963d4f80d5d861b1ff3cfcc8bd2b56aa673dd8eacab6f23ab98599276255cab2d8391d4fd6365c4a8d91c74de9878866e458897620ab58890ee66d0e52cf9e26c6393fded745d4afdc9421b71e7211583662d97db02a92d43cd6e32f0bdd533be18498dbef75a2a83e675ceb284a454185025f30e977060ceb416c288b0efb59f0abdf5e5d853704f1b661e2bedebc714bd0df8909be30e04d46e26433c9d1cd4d3e846d5e9816cda8d2b8e',
    'TSPD_101_DID': '0868f8be6fab28005f0e4997f5efe6af55eb896c4e70a0f28f2571425cdf3a82d2ff30b52d098121c43983b4f2aff9ef084d51969c063800e4e34d607835aedea29e02f84129420c256c12b94a46af0192470803158bc26cea09d5d9ff4d714bc9d78d66fd296697276c6ca468b06b9c',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '9659465e252a0faffcb932a11d8b78ba',
    'TSPD_101': '0868f8be6fab28002472fcfababaf368840528fcdecae196619fce6358d579d252be9132b1cd71e1d10cbf23d2fac8ae083ebbb5b4051800abbc17771219b5145ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': '64e27983-6f22-4330-90d0-c074febbe3dd',
    'SESSION': 'cdc1861b-263e-4eb5-ab84-075cefeefd14',
    'TS5220f739077': '0868f8be6fab280084fb612b0b4bf513c0c7d981aa36de5364cfd91f65f45940c799d2f8bc375c8414d926118f464e0f089a3c7d40172000b6df36ee708b7c04da6eb3f6b4008fd17c6e44347286da1c90bd29a2a15a3569',
    'TS011f2d1a': '01266d26d067b18bffe565da8990159b99a0bc37a1226a0157d21bfc80cf034357cdd6524e8e0c033814cafb898c3cb29537e1b66a',
    'TS5220f739029': '0868f8be6fab28000189878941da10fd564592e068a702880b881d533c19e964aecd8da5445fd39d188044f02d516352',
    'TSf1edb2d2027': '0868f8be6fab2000b27e48c1731ab1e93ce84fb0db225a431015355149f2a4e7ff79d8982944e5050863a70f81113000c875e96e2a59de711db621f5a9dcb13e2a4fba9622976dbee1e271d01910497ed6d4525d483da5c8a881c716283659c0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8,sv;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Microsoft Edge";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': '64e27983-6f22-4330-90d0-c074febbe3dd',
    'cookie': '_ga_FMZTHHQN2K=GS2.1.s1778035370$o1$g1$t1778035723$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1778035727$o1$g1$t1778035852$j60$l0$h0; _ga_K98R6MSKRH=GS2.1.s1778314369$o1$g1$t1778314389$j40$l0$h0; _ga_9E7L2XJ89Y=GS2.1.s1778465304$o1$g0$t1778465307$j57$l0$h0; cf_clearance=CwLXIaLV3mmGpRwuhuAC30Uco3Pjb_tz_1ZEbXnsvlo-1780364611-1.2.1.1-JeJaibKrj6XS4kPV4Ip25uQkYHC0SxIs56rfZupCrrK8yP_H6zi1dSFcMZnahwgzur4pRIS8XT8t.FS4e5IZD.l09FvOnFaWnw1eLG9FQpfiCb6rGNDUqraHwu0yGtfqjoATjtiW8VgnuTu7I13XGK8qcdi5YicZDzmWAEfbg0GfAms1zt6a3TtivoUKuPHm91832sMMPQ4eCQ77uVHVtMj8thYLEZbhWlQGGd8TE3ZqmJ1dIjlbGtBIMzKCS9YrdI3BX4QMqGMRNKdCVHFpJhQyO3yvQt5ZK3mFh83hjYJJSLZJnszvXzwkM5Q._LIPvYpMzOE_zhyRpUg2Nrd2rA; _ga=GA1.3.337823039.1778035336; _ga_XXTTVXWHDB=GS2.3.s1780364612$o4$g1$t1780364813$j60$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=BMNNBEEOEMIHPFNPGLEKMKCNGPJNBJAOOBMBCBDJGNEHJPGIPNGDPNPCCCNDJAEKIKKDGEPBIKLPOPCMNKOAHHACAFKKMGLMHPLFDCMGICBOLEJFDKNMGPCLAFECMJLH; TS00000000076=0868f8be6fab28005f0e4997f5efe6af55eb896c4e70a0f28f2571425cdf3a82d2ff30b52d098121c43983b4f2aff9ef084d51969c09d0007946dbf900ab12446650ec365ac445759c547051dd9ac49645b8e0d5382f9c2eadcc9d1d1963d4f80d5d861b1ff3cfcc8bd2b56aa673dd8eacab6f23ab98599276255cab2d8391d4fd6365c4a8d91c74de9878866e458897620ab58890ee66d0e52cf9e26c6393fded745d4afdc9421b71e7211583662d97db02a92d43cd6e32f0bdd533be18498dbef75a2a83e675ceb284a454185025f30e977060ceb416c288b0efb59f0abdf5e5d853704f1b661e2bedebc714bd0df8909be30e04d46e26433c9d1cd4d3e846d5e9816cda8d2b8e; TSPD_101_DID=0868f8be6fab28005f0e4997f5efe6af55eb896c4e70a0f28f2571425cdf3a82d2ff30b52d098121c43983b4f2aff9ef084d51969c063800e4e34d607835aedea29e02f84129420c256c12b94a46af0192470803158bc26cea09d5d9ff4d714bc9d78d66fd296697276c6ca468b06b9c; db8ca2b43ed851cc93e71fd5fd72bff7=9659465e252a0faffcb932a11d8b78ba; TSPD_101=0868f8be6fab28002472fcfababaf368840528fcdecae196619fce6358d579d252be9132b1cd71e1d10cbf23d2fac8ae083ebbb5b4051800abbc17771219b5145ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=64e27983-6f22-4330-90d0-c074febbe3dd; SESSION=cdc1861b-263e-4eb5-ab84-075cefeefd14; TS5220f739077=0868f8be6fab280084fb612b0b4bf513c0c7d981aa36de5364cfd91f65f45940c799d2f8bc375c8414d926118f464e0f089a3c7d40172000b6df36ee708b7c04da6eb3f6b4008fd17c6e44347286da1c90bd29a2a15a3569; TS011f2d1a=01266d26d067b18bffe565da8990159b99a0bc37a1226a0157d21bfc80cf034357cdd6524e8e0c033814cafb898c3cb29537e1b66a; TS5220f739029=0868f8be6fab28000189878941da10fd564592e068a702880b881d533c19e964aecd8da5445fd39d188044f02d516352; TSf1edb2d2027=0868f8be6fab2000b27e48c1731ab1e93ce84fb0db225a431015355149f2a4e7ff79d8982944e5050863a70f81113000c875e96e2a59de711db621f5a9dcb13e2a4fba9622976dbee1e271d01910497ed6d4525d483da5c8a881c716283659c0',
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