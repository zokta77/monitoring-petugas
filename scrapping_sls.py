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
    'db8ca2b43ed851cc93e71fd5fd72bff7': '526925235607b7fcccd9bb48a0f522c7',
    'XSRF-TOKEN': '8305bb7c-8f1d-47be-8da5-5f07e971d8e2',
    'SESSION': 'caf95f0e-a2fa-478d-9531-2bda0498a40f',
    'XSRF-TOKEN': 'eyJpdiI6IkdnOTZtRTV3MGtkN1k5YkQ0R0hJR0E9PSIsInZhbHVlIjoiSDNlRzdUaFY1T2VhQTNQMWg1Nk53WmJEVUQySkcvMWdyUmk4WHA3djFabmllOXo2allLbnNIeFpyVm5NYmh3SU5DNVgrd2w3L1JEQW9wTXdTYzdpK0RjZ1FwdVdaME5rQ3pUOTdvNlFtMjJQdXhRemFHQ29leDk5dFpyWFhiTkYiLCJtYWMiOiJiM2ViNWUwYjhmMjljMmNiZDUxZGE4ODIwMjE4MTgwM2NiOWY0NWQ2ZDU2NmRiYTQ0MzlkYzkxMGMxMmViNTc5IiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6IkdKMmpaZWlVZWRmN1E5eG5TbDRDS0E9PSIsInZhbHVlIjoiN0JXYTVKZzVPQ1A3YmIvU3p2UGJzbnUyaVErSFZWQi9yeEgyczd3QlpTMXdiMG1wdlptZDlwK0J3ek9FVG5teDVnc3Q2ZEZ4NXlITVVrcGoxOWhFRlpnNVFlZDlBZ1VqNjRjVGlEZ1gzc2QrNUozTFBDc3pLZngvUnQ1R0JTbzUiLCJtYWMiOiI2NzExZjNlNDAwMTRkMTA3YjkxNWUzYmZmZWMzMDJkNDBjODg2ZjZiZGYyZTZmZDVlY2QzMDE2ZDgwNDQxMjBiIiwidGFnIjoiIn0%3D',
    'nYjYyhkBkIl589MpRGQojdOOOmw5Alj7qZ8G7RyL': 'eyJpdiI6IlRrWDE4L1JrTUNQcDcyMVZXS3dKSWc9PSIsInZhbHVlIjoiRmdPdFo4RWRueVRWYWY2YmIyaWVvbXE3aG9PWEY0VmRPNTkrVkdNQmsrcVJZelFDU1N3YVYwSW44Z2JzdkI1YkVORHZLbW0xRWlUenhEU0dLWEN4Rklma3RSaURBc3JvUzNKR2xyR3ozOFBzWmw0TjB1YTdMVTk2b0xLUUNwLy9CVEFRclVmL05pNzZNM25xck5UMjNXOUhTQUdsSlBxY0t3QjAvYVI3U1ZhMDZvejJYdkhvdGYxN08wOHhHQldrc0c2YTRZZHFFcjVCRTY5TVF4eXMwUGc4V0VjS3JPTWNWeWdEUkowcFpjVHNkQlBBMThTNTg5VnQvZDU0RG1JOEVVVWJDYTBicC9WZ2FUV2NDcFNMYWN2bHFidDFyZ1h6aVdlNEF1Wmh2NzFuYVRlWk84QkN4OWZyM0dtcFZodmVtaG1pN0ZlZlNWekNlL2UwOGJTZnZnMnZRNHppelJmVis5UGM0cDFYeWRJajZMcExqSllSeHN4NTFUVzFSTW03TVNIRDM2Vkg3MEFkOUErTzdxeTJNUT09IiwibWFjIjoiMWI5NGJkYzJkNDFhMjYzMjMxOGQ1MDBhNDdkMzRiYTdjMjAzZTc0N2FlMGQ2NzViZmZhMjg5MWQ5YmJhODQzZSIsInRhZyI6IiJ9',
    'f5avraaaaaaaaaaaaaaaa_session_': 'KGKODNCDDHCEFEEEBABPFEAPFNDHKFACHHMPEOJJFJPHIODDIDNAFKBIIAEONPBGFLADMCBAKCEFADEDGNHABMNIGLPLLNDIDOGMBLDEFGIAFBLAPNGKFGHKCMGMFPKG',
    'TS01acc472': '01266d26d07f2608d348add31e13ed88750fd58649d83e8fa89fe8ea785cd146a0e2855d3845e648ffb682e481d86e607e8fedca100e7e9fe5319009b51b652fec7f08544e55c20fe706cd86b42628464f220e59ca1503d9dc314a1b0e0e69419fd40526a4ae9570367509ae6a9b48449a4c9e22d118ebb5ff5c6c08c030d194a47be2e46446436b0e00d9a594835cacb369f367eee9a1803299931564ba229765fb1305bf96f60180a3a8a82aabc630ad83d752a546fb92376089aed5631c9a6cb191dd4899950255a3e89eb47c5a956288cacc4d59194d6b430f71bf40a364f8812e4b70',
    'TS0151fc2b': '0167a1c8616477d76a15f9722060f91cc6bf4e2b0d5b070475f6b86721cdf90654c8201ac7c32c6eeaace0ff59c1c236c4369b9e04',
    'TS00000000076': '0868f8be6fab280074863d58525d3573d909e19ef0d045671c2c72f8becea549f354f006db88788985e05eabc6d99d780868d329a909d000d1d882ffb53ea636b86461e05178e2b2ace512df216e663a025e341dc7d0df13815c2cab4c5141d746666210f04f9b0333721ca3fff09481c85cb1af96e3cb3cb1f6fdaa571e6ab34e124239d86f67927a04c22c6a960e94ac6e9b072c45141e6074e7300152a9bd9b005d18e52a3b71b434181b562c311cd975906762664f3e19e64616cc8aa45560aba032b6a70b87089b5a94d06d0c8df7942360c41c729fb45a93b046c64691dd59bdb304cf1fe7951ff3ced386f8802fd7aaf4aa9814b759eea196ed2a936c1735697cbb40d829',
    'TSPD_101_DID': '0868f8be6fab280074863d58525d3573d909e19ef0d045671c2c72f8becea549f354f006db88788985e05eabc6d99d780868d329a9063800fed403c521109558aa9ddfb04497218a54374b6911caebc0797aaea69571cd4386280416e452eaa2535d583656de59530c2714aed6e2a40f',
    'TS011f2d1a': '01266d26d08cb0fdfc9cf972ab2c0a3cbd62104be57679c479b11c9f904152fa062d1b103d987bc9589dcfa876bf279fa53c4e669e',
    'TSPD_101': '0868f8be6fab28004e570f341a0a3e226560d1c941bbc0beaf3e76424fb61bb42ed2f70aab88fc06f59156e35ea08d6a085021859c0518003e6cdf40669bb76d5ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800fbc5ce33a2179dcbb9d2f5768f77dcbd194e6f4681cc508af5db77d04d01e634cdf4d28c85d80de60827af27c61720000d1ceece50cbfe838bc3535ec1428bca2a7b3c16f60f442744322f75ad6af374',
    'TS5220f739029': '0868f8be6fab28006da8c3e1b30bf4b7869abc1c68483294389b9a62cb8069168295bf36ba00a4a2502254aa76a49180',
    'TSf1edb2d2027': '0868f8be6fab200006240aba4dfce91347ada483681bb863a9e243610dd3b6e68b7b468e77bed0c8088b862027113000d5c63bb4669229d3f07f1e1d9c9647576b38b45ceb20c9193b6b334604b3e3dfe33ed34e8c056c21b6db0b0c25ff2271',
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
    'cookie': '_ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=526925235607b7fcccd9bb48a0f522c7; XSRF-TOKEN=8305bb7c-8f1d-47be-8da5-5f07e971d8e2; SESSION=caf95f0e-a2fa-478d-9531-2bda0498a40f; XSRF-TOKEN=eyJpdiI6IkdnOTZtRTV3MGtkN1k5YkQ0R0hJR0E9PSIsInZhbHVlIjoiSDNlRzdUaFY1T2VhQTNQMWg1Nk53WmJEVUQySkcvMWdyUmk4WHA3djFabmllOXo2allLbnNIeFpyVm5NYmh3SU5DNVgrd2w3L1JEQW9wTXdTYzdpK0RjZ1FwdVdaME5rQ3pUOTdvNlFtMjJQdXhRemFHQ29leDk5dFpyWFhiTkYiLCJtYWMiOiJiM2ViNWUwYjhmMjljMmNiZDUxZGE4ODIwMjE4MTgwM2NiOWY0NWQ2ZDU2NmRiYTQ0MzlkYzkxMGMxMmViNTc5IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IkdKMmpaZWlVZWRmN1E5eG5TbDRDS0E9PSIsInZhbHVlIjoiN0JXYTVKZzVPQ1A3YmIvU3p2UGJzbnUyaVErSFZWQi9yeEgyczd3QlpTMXdiMG1wdlptZDlwK0J3ek9FVG5teDVnc3Q2ZEZ4NXlITVVrcGoxOWhFRlpnNVFlZDlBZ1VqNjRjVGlEZ1gzc2QrNUozTFBDc3pLZngvUnQ1R0JTbzUiLCJtYWMiOiI2NzExZjNlNDAwMTRkMTA3YjkxNWUzYmZmZWMzMDJkNDBjODg2ZjZiZGYyZTZmZDVlY2QzMDE2ZDgwNDQxMjBiIiwidGFnIjoiIn0%3D; nYjYyhkBkIl589MpRGQojdOOOmw5Alj7qZ8G7RyL=eyJpdiI6IlRrWDE4L1JrTUNQcDcyMVZXS3dKSWc9PSIsInZhbHVlIjoiRmdPdFo4RWRueVRWYWY2YmIyaWVvbXE3aG9PWEY0VmRPNTkrVkdNQmsrcVJZelFDU1N3YVYwSW44Z2JzdkI1YkVORHZLbW0xRWlUenhEU0dLWEN4Rklma3RSaURBc3JvUzNKR2xyR3ozOFBzWmw0TjB1YTdMVTk2b0xLUUNwLy9CVEFRclVmL05pNzZNM25xck5UMjNXOUhTQUdsSlBxY0t3QjAvYVI3U1ZhMDZvejJYdkhvdGYxN08wOHhHQldrc0c2YTRZZHFFcjVCRTY5TVF4eXMwUGc4V0VjS3JPTWNWeWdEUkowcFpjVHNkQlBBMThTNTg5VnQvZDU0RG1JOEVVVWJDYTBicC9WZ2FUV2NDcFNMYWN2bHFidDFyZ1h6aVdlNEF1Wmh2NzFuYVRlWk84QkN4OWZyM0dtcFZodmVtaG1pN0ZlZlNWekNlL2UwOGJTZnZnMnZRNHppelJmVis5UGM0cDFYeWRJajZMcExqSllSeHN4NTFUVzFSTW03TVNIRDM2Vkg3MEFkOUErTzdxeTJNUT09IiwibWFjIjoiMWI5NGJkYzJkNDFhMjYzMjMxOGQ1MDBhNDdkMzRiYTdjMjAzZTc0N2FlMGQ2NzViZmZhMjg5MWQ5YmJhODQzZSIsInRhZyI6IiJ9; f5avraaaaaaaaaaaaaaaa_session_=KGKODNCDDHCEFEEEBABPFEAPFNDHKFACHHMPEOJJFJPHIODDIDNAFKBIIAEONPBGFLADMCBAKCEFADEDGNHABMNIGLPLLNDIDOGMBLDEFGIAFBLAPNGKFGHKCMGMFPKG; TS01acc472=01266d26d07f2608d348add31e13ed88750fd58649d83e8fa89fe8ea785cd146a0e2855d3845e648ffb682e481d86e607e8fedca100e7e9fe5319009b51b652fec7f08544e55c20fe706cd86b42628464f220e59ca1503d9dc314a1b0e0e69419fd40526a4ae9570367509ae6a9b48449a4c9e22d118ebb5ff5c6c08c030d194a47be2e46446436b0e00d9a594835cacb369f367eee9a1803299931564ba229765fb1305bf96f60180a3a8a82aabc630ad83d752a546fb92376089aed5631c9a6cb191dd4899950255a3e89eb47c5a956288cacc4d59194d6b430f71bf40a364f8812e4b70; TS0151fc2b=0167a1c8616477d76a15f9722060f91cc6bf4e2b0d5b070475f6b86721cdf90654c8201ac7c32c6eeaace0ff59c1c236c4369b9e04; TS00000000076=0868f8be6fab280074863d58525d3573d909e19ef0d045671c2c72f8becea549f354f006db88788985e05eabc6d99d780868d329a909d000d1d882ffb53ea636b86461e05178e2b2ace512df216e663a025e341dc7d0df13815c2cab4c5141d746666210f04f9b0333721ca3fff09481c85cb1af96e3cb3cb1f6fdaa571e6ab34e124239d86f67927a04c22c6a960e94ac6e9b072c45141e6074e7300152a9bd9b005d18e52a3b71b434181b562c311cd975906762664f3e19e64616cc8aa45560aba032b6a70b87089b5a94d06d0c8df7942360c41c729fb45a93b046c64691dd59bdb304cf1fe7951ff3ced386f8802fd7aaf4aa9814b759eea196ed2a936c1735697cbb40d829; TSPD_101_DID=0868f8be6fab280074863d58525d3573d909e19ef0d045671c2c72f8becea549f354f006db88788985e05eabc6d99d780868d329a9063800fed403c521109558aa9ddfb04497218a54374b6911caebc0797aaea69571cd4386280416e452eaa2535d583656de59530c2714aed6e2a40f; TS011f2d1a=01266d26d08cb0fdfc9cf972ab2c0a3cbd62104be57679c479b11c9f904152fa062d1b103d987bc9589dcfa876bf279fa53c4e669e; TSPD_101=0868f8be6fab28004e570f341a0a3e226560d1c941bbc0beaf3e76424fb61bb42ed2f70aab88fc06f59156e35ea08d6a085021859c0518003e6cdf40669bb76d5ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800fbc5ce33a2179dcbb9d2f5768f77dcbd194e6f4681cc508af5db77d04d01e634cdf4d28c85d80de60827af27c61720000d1ceece50cbfe838bc3535ec1428bca2a7b3c16f60f442744322f75ad6af374; TS5220f739029=0868f8be6fab28006da8c3e1b30bf4b7869abc1c68483294389b9a62cb8069168295bf36ba00a4a2502254aa76a49180; TSf1edb2d2027=0868f8be6fab200006240aba4dfce91347ada483681bb863a9e243610dd3b6e68b7b468e77bed0c8088b862027113000d5c63bb4669229d3f07f1e1d9c9647576b38b45ceb20c9193b6b334604b3e3dfe33ed34e8c056c21b6db0b0c25ff2271',
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