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
    'f5avraaaaaaaaaaaaaaaa_session_': 'MIFOJODPNKMPHBIJOOICDAJMDNGNBJMFGDBEGDPJBEJGCOKEPAPJOAEJCCCMHIINLCIDBAGKCJHJMCFBBNNAMDINAEMFHPENACIFMNILNPPMCAHHJLACHIGJNNNHCHDH',
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
    'SESSION': '1e351f63-9c9f-427a-86e5-1fa83fffaf0d',
    'TS018af012': '0167a1c861db323178387e88013b857522d2cf8eed656446bd793cdc0e28271514d7214de48fea6cb6157dc9aab98d952fd61e1a94bf603d89f33653aa8ed3fffd8e2ed924',
    'XSRF-TOKEN': 'eyJpdiI6ImJqZjFIU0ZGRTRhVnhwRlN4SWlXQVE9PSIsInZhbHVlIjoiQ0dCa2JOdkJuWHZxc3VQek4rTUI0ckhtbUdhRVpTczJrYjBqcE14WStSYTBVejlRd1NqUGVRR0JXOUdJSWxUS1o5c2xTUjcvSmdMNkhtYVh5M3MxODlKbitKb2F5RkNORkFnRVNPbktiTnJJQXkwbTBWRXFvY25JK3lNU2hoYzEiLCJtYWMiOiI5YmNjNDNlZmI3YTE0ZGMwMjMyMzQ4MzQ3YTkwNDFhMjk0YWE1MmE2NGQwYjQwN2I5M2U2N2Y1OTBkMTY1MzMxIiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6IlJTU3hZc2M4eEE2bktvbjdha1ArMWc9PSIsInZhbHVlIjoiM3RQNDM5ODBHVjM4ekhqSGkzVTJjYmVOSUVna1FjMDV2VmRWak5KdFdkMTdBSDFybW0xczJqdUN3MWJQVmtVcmV3SVFselhMMWxGTVozUHYzZHpjVG5Da0krQUQyckh1M0tyREdPYzhHMWxwZytVVHRZenZkZHdnaGMyOGk3VEQiLCJtYWMiOiIwNjRiMmI2NTMwNDJkNTgwNTg3ZGM3MWJjZGRiZTU3ODQ3ZWI2NDE5NjEzNzViZTAzMjRkNjQ4MTZmY2M4OGY3IiwidGFnIjoiIn0%3D',
    'gxQIGTeR0m7gwj57TQtPQkmlJJ7Sygzii3FT1Bfk': 'eyJpdiI6Ik9vMXBNSCtpajBDQWluUWRXRVZ2bVE9PSIsInZhbHVlIjoiUWlPSDBRV1d0RkpHckQ4c0xoMlVqeTJCRW9IU2xDSUpVYit0YTM4c21nN3F3SjF4NVhKdU91ZG9jVnN5MllIY2hzNkdQSlQ4dlVjODRqcTRPZFdDL1MwRzBaSjE5R0VibzVPOWZiU3hEaFc5d3U0S01QWDR4c05kaXAvb2k3eGJmMTF5TThGQ0IyTWdtU1UzTDMySllra2x3YTFld0E1UVRzWnY3dTZCZkFFMk9xS28rY1lPakZTL2pMOW56VXFlK0Y3dCswUVRKRGFoUmlVTXV5MURvY2xwS1FhaGh3RkNNZVdoM2JEVTNHdS9lLytBNUw5SGIvZFlMTjVKLzNJcVJqdDRFNE5sOGVFa2tLVitZcjVqbGZtSjZoNDA4MzN4NDIrdUNmWFdGZzMzN3dkUUxITnQ3L0g1WXZucTAydmdBN0MreFpJTlhTdjZPdTlLVzYzUEZDYm1DeDRGSDVVVFVKZXY5dllrRUo2ODB2NFF3TUhydTBKMHdqdjRZc0tKQmVGNDY5NVVXendOb2pUSURoNHRsQT09IiwibWFjIjoiNmY5YjhlM2ZhN2M5ODVhMzViNDA0NzIyN2ZiODRhYzAzZGRmMWFjMmIxMThmOWRlZWI5ZDE4YWI5YWUxMzRjZSIsInRhZyI6IiJ9',
    'TS01acc472': '01266d26d019e714f066dc02f882925183a9195939722853db593c2caf05183582e5196e5a9f7e6079bf028ec2a8a8c3cad4b7c15a79be960219d3d00a6fa17e19505c6f7b25d10b9ab99ad32754dd06a20ba301eae3296352de62ca57f40071e1ac5ce5d372a4796020622dfd31594bc3ee3a197258d40a5dbb26aa6e54c0e5554bf98200cfaf48b343a6f9b62c06b7f0ce1d583ad99bfba1a24969a01b295ca6167f0d233fc16c5129390b34123b4c4714f225e5daaa9dd49a278ad75e407b4beb7da680f50d2aea3b0e21b4f3d9d326f05d941f',
    'TS00000000076': '0868f8be6fab2800198a35061a440b5f99097161fb9a87312673aa42ce03a12f3ce8910b5af9ea504652bb2874536f810861de978e09d000f2c6cafa864f042844e386a8341920e6d640fc12988783632799f7014e9553b08c6947646993829c1b84ff70c643ab53cfd0be93a16cbed62dd773213968cbbb40b5a5b740cf112e34be69ec4c3a05d8e44f5dddea76ff82e60bcb46ab3805bf9d46d14a82277913235fea18683c4e2f62a3bc4722be0ee40afcea9fe3224bd6ebb8a4c0d61373ab5457bd4da7305e369d65e39787a12c2f156d4be77176093da57b930bd8510c20f0f41e554d0f56ad72a620c255eb4537da7ddc08f966a4cfe82791826e0e5f50a0051dec65b5fd81',
    'TSPD_101_DID': '0868f8be6fab2800198a35061a440b5f99097161fb9a87312673aa42ce03a12f3ce8910b5af9ea504652bb2874536f810861de978e06380020bb6854c1347b5be0a79b93d8716b63b295c159e664bd39d4de8034a6d1f495b84c0683b3c8f451db45eb028ea4b034011a94b4f6d99999',
    'TS011f2d1a': '01266d26d0a72553465bbe92b0ea79f63fae2728f0b690e18dc954685b46c0273102fdf3b9f32b33545d45e07a033dd056f16f810e',
    'TSPD_101': '0868f8be6fab2800ad02b94c47e36c9b9cc1351fc5cf663988d455cfe2e33ff211aacb713a6bfb7893f773dbf03b43f008ff2e6f5405180017b91d0137ff6ccd5ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'LMGLOAAFCEKFFBLHPIAHLLCJEGJCLDODFPEJENOFOFJDHNLCOOIIBCAANJNIDJKCKCEDLIDOMJELJPJFHFIAALPKBEEMFHJDAGJPHGLIKHKKJNAOJCCELEGOFODGBAGM',
    'TS5220f739077': '0868f8be6fab28003438db0363c51275afd58dec0d718d54efaf5ac31db1f0184e09cd034aafe2571b96d502840159e208e7067758172000d212861708dd586a9e0e6a21e6042c51c9665129b41b4c2b2e67203e94b5456b',
    'TS5220f739029': '0868f8be6fab2800f83d4408985eccc07f61a97e47b477447b10c224ef554d8d5f72ddd917112f284b92d31c8f6fd739',
    'TSf1edb2d2027': '0868f8be6fab2000462b626549f02985980b3459e6fdc73abb2abd8514ae07d8dd435b629a88c57a08c2a03767113000710d58e6d92fd0be2735c5fef3a791a253779252f572cde02fd8df5e568e842f16b5277b5a4003c28cd94a34c8eed679',
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
    'x-xsrf-token': 'ca51d619-add5-4bad-9780-d83e54bc1f0d',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=MIFOJODPNKMPHBIJOOICDAJMDNGNBJMFGDBEGDPJBEJGCOKEPAPJOAEJCCCMHIINLCIDBAGKCJHJMCFBBNNAMDINAEMFHPENACIFMNILNPPMCAHHJLACHIGJNNNHCHDH; _ga_G604FXJW6E=GS2.1.s1780902144$o1$g0$t1780902163$j41$l0$h0; _ga_K98R6MSKRH=GS2.1.s1780922743$o1$g1$t1780922897$j47$l0$h0; _ga_WQKDWE3S3T=GS2.1.s1780971857$o1$g0$t1780971857$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1781251554$o2$g0$t1781252726$j60$l0$h0; cf_clearance=KttlSqHtGfsM7lh5MeJqKHklKtsF467nca20raHcd0U-1781401979-1.2.1.1-vmXRVLPxjwzTVN1gbBiDgF9GprAD3Yo0lMKa6D7Kzbiqfvu5adUtCMtOOjqcQ9qVJhuoYoJ1L3Z6Kih46GdyKgIcKtQthQydkV.l8XEvdMfhcAXci7tQGKIlR5hJATeWOndNHgYi3k4kWHjVwnkLAigodZGn8_itOe4uZgjuXPCn6sqKut3DOIHkg4TIXeqoCQ0TocBDeyA6S5.CPkNOoxiZzuheDUT_EsytNLfQ3AzqmwHhl5Hyck6zd8s0Q1tmn5GicaFwCHt10r.u0U8bP4dbpdI5wU3AYY2rPOPEvrjgVZVcPh4oyr_VrqQyl0hs4_e_pcDHJcgrD6N_RhrbVw; _ga_T7YPSCVK8R=GS2.1.s1782095603$o1$g0$t1782095607$j56$l0$h0; _ga=GA1.3.1484741960.1780902145; _ga_XXTTVXWHDB=GS2.3.s1782095624$o9$g1$t1782095696$j50$l0$h0; XSRF-TOKEN=ca51d619-add5-4bad-9780-d83e54bc1f0d; db8ca2b43ed851cc93e71fd5fd72bff7=9659465e252a0faffcb932a11d8b78ba; SESSION=1e351f63-9c9f-427a-86e5-1fa83fffaf0d; TS018af012=0167a1c861db323178387e88013b857522d2cf8eed656446bd793cdc0e28271514d7214de48fea6cb6157dc9aab98d952fd61e1a94bf603d89f33653aa8ed3fffd8e2ed924; XSRF-TOKEN=eyJpdiI6ImJqZjFIU0ZGRTRhVnhwRlN4SWlXQVE9PSIsInZhbHVlIjoiQ0dCa2JOdkJuWHZxc3VQek4rTUI0ckhtbUdhRVpTczJrYjBqcE14WStSYTBVejlRd1NqUGVRR0JXOUdJSWxUS1o5c2xTUjcvSmdMNkhtYVh5M3MxODlKbitKb2F5RkNORkFnRVNPbktiTnJJQXkwbTBWRXFvY25JK3lNU2hoYzEiLCJtYWMiOiI5YmNjNDNlZmI3YTE0ZGMwMjMyMzQ4MzQ3YTkwNDFhMjk0YWE1MmE2NGQwYjQwN2I5M2U2N2Y1OTBkMTY1MzMxIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IlJTU3hZc2M4eEE2bktvbjdha1ArMWc9PSIsInZhbHVlIjoiM3RQNDM5ODBHVjM4ekhqSGkzVTJjYmVOSUVna1FjMDV2VmRWak5KdFdkMTdBSDFybW0xczJqdUN3MWJQVmtVcmV3SVFselhMMWxGTVozUHYzZHpjVG5Da0krQUQyckh1M0tyREdPYzhHMWxwZytVVHRZenZkZHdnaGMyOGk3VEQiLCJtYWMiOiIwNjRiMmI2NTMwNDJkNTgwNTg3ZGM3MWJjZGRiZTU3ODQ3ZWI2NDE5NjEzNzViZTAzMjRkNjQ4MTZmY2M4OGY3IiwidGFnIjoiIn0%3D; gxQIGTeR0m7gwj57TQtPQkmlJJ7Sygzii3FT1Bfk=eyJpdiI6Ik9vMXBNSCtpajBDQWluUWRXRVZ2bVE9PSIsInZhbHVlIjoiUWlPSDBRV1d0RkpHckQ4c0xoMlVqeTJCRW9IU2xDSUpVYit0YTM4c21nN3F3SjF4NVhKdU91ZG9jVnN5MllIY2hzNkdQSlQ4dlVjODRqcTRPZFdDL1MwRzBaSjE5R0VibzVPOWZiU3hEaFc5d3U0S01QWDR4c05kaXAvb2k3eGJmMTF5TThGQ0IyTWdtU1UzTDMySllra2x3YTFld0E1UVRzWnY3dTZCZkFFMk9xS28rY1lPakZTL2pMOW56VXFlK0Y3dCswUVRKRGFoUmlVTXV5MURvY2xwS1FhaGh3RkNNZVdoM2JEVTNHdS9lLytBNUw5SGIvZFlMTjVKLzNJcVJqdDRFNE5sOGVFa2tLVitZcjVqbGZtSjZoNDA4MzN4NDIrdUNmWFdGZzMzN3dkUUxITnQ3L0g1WXZucTAydmdBN0MreFpJTlhTdjZPdTlLVzYzUEZDYm1DeDRGSDVVVFVKZXY5dllrRUo2ODB2NFF3TUhydTBKMHdqdjRZc0tKQmVGNDY5NVVXendOb2pUSURoNHRsQT09IiwibWFjIjoiNmY5YjhlM2ZhN2M5ODVhMzViNDA0NzIyN2ZiODRhYzAzZGRmMWFjMmIxMThmOWRlZWI5ZDE4YWI5YWUxMzRjZSIsInRhZyI6IiJ9; TS01acc472=01266d26d019e714f066dc02f882925183a9195939722853db593c2caf05183582e5196e5a9f7e6079bf028ec2a8a8c3cad4b7c15a79be960219d3d00a6fa17e19505c6f7b25d10b9ab99ad32754dd06a20ba301eae3296352de62ca57f40071e1ac5ce5d372a4796020622dfd31594bc3ee3a197258d40a5dbb26aa6e54c0e5554bf98200cfaf48b343a6f9b62c06b7f0ce1d583ad99bfba1a24969a01b295ca6167f0d233fc16c5129390b34123b4c4714f225e5daaa9dd49a278ad75e407b4beb7da680f50d2aea3b0e21b4f3d9d326f05d941f; TS00000000076=0868f8be6fab2800198a35061a440b5f99097161fb9a87312673aa42ce03a12f3ce8910b5af9ea504652bb2874536f810861de978e09d000f2c6cafa864f042844e386a8341920e6d640fc12988783632799f7014e9553b08c6947646993829c1b84ff70c643ab53cfd0be93a16cbed62dd773213968cbbb40b5a5b740cf112e34be69ec4c3a05d8e44f5dddea76ff82e60bcb46ab3805bf9d46d14a82277913235fea18683c4e2f62a3bc4722be0ee40afcea9fe3224bd6ebb8a4c0d61373ab5457bd4da7305e369d65e39787a12c2f156d4be77176093da57b930bd8510c20f0f41e554d0f56ad72a620c255eb4537da7ddc08f966a4cfe82791826e0e5f50a0051dec65b5fd81; TSPD_101_DID=0868f8be6fab2800198a35061a440b5f99097161fb9a87312673aa42ce03a12f3ce8910b5af9ea504652bb2874536f810861de978e06380020bb6854c1347b5be0a79b93d8716b63b295c159e664bd39d4de8034a6d1f495b84c0683b3c8f451db45eb028ea4b034011a94b4f6d99999; TS011f2d1a=01266d26d0a72553465bbe92b0ea79f63fae2728f0b690e18dc954685b46c0273102fdf3b9f32b33545d45e07a033dd056f16f810e; TSPD_101=0868f8be6fab2800ad02b94c47e36c9b9cc1351fc5cf663988d455cfe2e33ff211aacb713a6bfb7893f773dbf03b43f008ff2e6f5405180017b91d0137ff6ccd5ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=LMGLOAAFCEKFFBLHPIAHLLCJEGJCLDODFPEJENOFOFJDHNLCOOIIBCAANJNIDJKCKCEDLIDOMJELJPJFHFIAALPKBEEMFHJDAGJPHGLIKHKKJNAOJCCELEGOFODGBAGM; TS5220f739077=0868f8be6fab28003438db0363c51275afd58dec0d718d54efaf5ac31db1f0184e09cd034aafe2571b96d502840159e208e7067758172000d212861708dd586a9e0e6a21e6042c51c9665129b41b4c2b2e67203e94b5456b; TS5220f739029=0868f8be6fab2800f83d4408985eccc07f61a97e47b477447b10c224ef554d8d5f72ddd917112f284b92d31c8f6fd739; TSf1edb2d2027=0868f8be6fab2000462b626549f02985980b3459e6fdc73abb2abd8514ae07d8dd435b629a88c57a08c2a03767113000710d58e6d92fd0be2735c5fef3a791a253779252f572cde02fd8df5e568e842f16b5277b5a4003c28cd94a34c8eed679',
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