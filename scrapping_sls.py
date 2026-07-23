import pandas as pd
import requests
import os
import random
import tempfile
from datetime import datetime
import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config_se2026 import NAMA_KABUPATEN, BASE_PATH, LATEST_FILE, archive_filename

# ================= SETTINGS =================
URL_DATA = 'https://fasih-sm.bps.go.id/app/api/analytic/api/v2/assignment/report-progress-by-responsibility'
base_path = BASE_PATH

# ===== KONFIGURASI SELENIUM =====
# Cara cek path: buka chrome://version di profil yang sudah login FASIH
# lihat baris "Profile Path" → folder induknya = CHROME_PROFILE_DIR
CHROME_PROFILE_DIR  = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Profil 1"   # ganti sesuai profil (Default / Profile 1 / dst)
FASIH_HOME_URL      = "https://fasih-sm.bps.go.id/app/"
# ==========================================================

# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'f5avraaaaaaaaaaaaaaaa_session_': 'MCLNNFHDBAGDHFMDJKMMNBPFPKCLMJKMJOGENDIECLMKGPCANOLLFICCLKFAKLCDDFCDMIKGBCPPEENMDFKAKLKJFLDFIPMJAAPLPJPBBCDMIBGNMPPJPHJKAIKBHEGC',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'a73c35acd30a5f2c2e12d3bd0105e248',
    'XSRF-TOKEN': 'a81866e0-7776-4b29-88a3-42f18b70bd8a',
    'XSRF-TOKEN': 'eyJpdiI6IjJ4NVRlSCtKbk1HUjNBNkNkcXZGZmc9PSIsInZhbHVlIjoiZ2x2REswV3FrUGFrSEYvVHl4S2RQQ1hPbkdEeWR4VGxMZXl1TTRUK3BWYVp6Um1sbzZUZE5VcCt5Zml3eVR3clhGaFVZV2tSekVDUnUxbTl6QnYxODF5cUdyU2RlWFltU0ErOG0yWDl4Um1tWHhkN2xsamJHMGN1OC9wRXZ1dnEiLCJtYWMiOiI0Nzc5OGJkZWJiMTFmZmFiODI0ODJlMzdiOTAxNzVkNzZlYjc4MmNkOTE3MjRjMjk5NDdlYTBiN2NhNTFiNzk4IiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6InJBQUphaXdFRVk0NnYyVVVWNzFobXc9PSIsInZhbHVlIjoiMGpmeXNMWDd1VVdqUWFiaitNODlQczcyczBzSXU1cFZhNUlybDBNL3pkQ3ZNbzA0SG83WmZzUEovY1ZlakJVYTNyV3cydVNrRjVvaGl6elM4bHRhRi95bTY4U0h6aFJxQ1NIMDQ3eFdGYmszR29vdnYxK3lYNVc0Q1kzd2xXcksiLCJtYWMiOiIyYzk5Yjk5ZTA2MGJmOTZjMzNiMzYxZWY3MGE2YTUyZWUxZDg5YjdkYWQyMzNiMDFjNzUzMTFlNzE4NDcyODAwIiwidGFnIjoiIn0%3D',
    'zyRlBw9w49NYzV06GfuVY1Tav5uaKXQ5f2P26BLh': 'eyJpdiI6Ijh4QnhBOTVPY2NHSzRPckxOajBXdmc9PSIsInZhbHVlIjoieElWZ01Qc3AvL1JOVTdEOVBqQ1dKbCtKWk9ZM2E4ZmcyUHU2UmJoWHo1aHhpWkdQSkcwV3lhRkZlUitHY1JZeWhyMmVITm1TSHFueEtZM0VldkdGQkorQkRFWUlrVGtMbUxPWTdIRmM4bW9sK2FTRHR2Y3MzQk9pV0pCOS9LNXg0K1NXakJCeU9Xc0tvaUFuWDhRbHNNKzR5VEU2aElkcGJYWVBKc2Q0VklGVFRzbnpIMXY1WEtIbG8ydUJibGhlcEh6ais3SndnTUtSTHFIb1VFN0pkWHZ3RytpS1g5UUpROUVsQ2VkaTQ4VkY3Nm9OU3NDZVNCc0NtNEYwWnJja3hWM2JsdDJzRktwUFBJTTU5NmQ3d2ZJZ2F2Q2dXS1BwNGN4ekhiMThUZTFNZDE0ejN0eDYvQWRKZzlZaHI3aXl2dmcvOHVJRXZBckhwQjIyM1FQOHhhV1JQWCs3Zm9sOWZ6U0FrRlJJQVJOeVZ0WldyL3lGeDBDazlETFRsZHZGc1VTMkdzMFNYeEZwQkdSUkR4eUdKQT09IiwibWFjIjoiYmNhOGJjYWY4YTk4ZjFiY2M3OTVkYmE2NDI1Y2RmYmJhYTlkYjMzYjVlN2ZjYzY1NjFmZjgwNGUxMzg5YjY0YSIsInRhZyI6IiJ9',
    'cf_clearance': 'eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg',
    '_ga': 'GA1.3.967752592.1784785844',
    'TS0151fc2b': '0167a1c8617f1dd83c4fec87640fc304c8301970e692579419787a1e7c357d61fa5c3569965f8256b7584dab0c57046c4fd86be90c',
    '__cf_bm': 'Q4IrwOAlOSq99LzdG7bPXkGXd1ikgwFfnDewKN3VNGc-1784785953.7767494-1.0.1.1-m0hBnMouJ83ejroycnsLbMSduOHT1WNto3.wNwe5e0O3shKnA399NXaqFV1jR6a8AKUmRzcXn5fOc1y1iM84WEHBXnSQz69pLEJXuLMVEPD1RmCkA2cWN._1YfvEd64R',
    'JSESSIONID': '97161D2634782176B17F2EB15B4B933D',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0',
    'SESSION': '5e901c33-c2eb-4f29-9bb9-999306f77ccd',
    'f5avraaaaaaaaaaaaaaaa_session_': 'FNGKGJPILFFGADBDEFCBFLAHCOCMKFLOJAIPMHLPNENNCDDBKDLMPHFDDOBOBPEOJHKDOJGNBOIJGKIHHPCABEFECKNMJINHEOKIDAHGDFJKHEPEIMONPELLMCCLFLDH',
    'f5avr1980069168aaaaaaaaaaaaaaaa_cspm_': 'NLEOOBCODNHNBFDMIJKJJPFBIGBAKDEOLLCCMEABBLJEBLALHCMNCDLHAJACJFOBCEICNKDAICNEBIBGAIGAHPPDACDNADMHHDAFGLFGOBCPMCDJDHPBKAAIJMMCBKHL',
    'TS00000000076': '0868f8be6fab2800f6fde2df9f3b3cf0be369ae8bd49f1f6745b8923cb9f73b42014232030590a9aec80fd7720ce321c086474d17b09d00005bbe8b00ed5090ede5a049f18c1568bb7746eb8ba87caccd3cbe8d16fdee6f70a98446ec35b12b954fc63f39cb0bf7b3b3fa7bf74cc1bf9933a4ec5438e47d4961b4b1c8312559496583034f07aaedc08081df8670de56b789eac0b4c0e47084e227e737bd50cee83bc54bed98700d23cb2c76e96b5d16567b32bc4bdb3ed9428889cb7e474626b53b49779453948493c0ec000c217fc63f9617fd8adac428ab83a841b2bd20f4fc8487a7abf126bacc60f31d048838f75fb30797e295b0c6ab476680e0b252474c7c90bf1068fa829',
    'TSPD_101_DID': '0868f8be6fab2800f6fde2df9f3b3cf0be369ae8bd49f1f6745b8923cb9f73b42014232030590a9aec80fd7720ce321c086474d17b0638002324328a0c04e0f57224b48c546db14a222b3febb68cd66f5e2aab255efa1ec4f00171ad6707aa22af5a3952754a2fb9daf1610075525dc6',
    'TS011f2d1a': '01266d26d0004094e4726d4a29937f2805922063631c062671186d2a967e00f9472398fd818b15536ae2e413f3e4263a4cd5b4e5d3',
    'TSPD_101': '0868f8be6fab28004c0438844cbc744b025c56482d91a04d2b7440994d279d4f932e75c6128afa2d786f83371ed385a708668fd38705180007b2eea447db9ed95ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab28008db8baf791435c1a7e53bf2b39fadd06618f148a1e0de8c3a1d66e5be89cf2ea89bb884ab80da50408dbecbc0c1720008a7b3c3a7911e85de0ef121f7de8ded8335b1d070c09060ca9eb152d8e645d66',
    'TS5220f739029': '0868f8be6fab2800f553e628a6280bd1568dbe875a3a92b4432e376a7b73fc9dd97584ed4de0e4251916765d43b9d513',
    'TSf1edb2d2027': '0868f8be6fab2000b3dbef95cd9c505eb98307288060d916c295c6354a4a180c35f70cc69bed82440846f07a72113000124f4ee29c043e8f88dfefd906a1fb1b6517bbd616794312d00c19af34b8cf3dc72138dd2b25cf3195c9572104a752a3',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'referer': 'https://fasih-sm.bps.go.id/app/surveys/a0429e96-51a5-477b-a415-485f9c153004/fd68e454-ba45-4b85-8205-f3bf777ded24',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': 'a81866e0-7776-4b29-88a3-42f18b70bd8a',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=MCLNNFHDBAGDHFMDJKMMNBPFPKCLMJKMJOGENDIECLMKGPCANOLLFICCLKFAKLCDDFCDMIKGBCPPEENMDFKAKLKJFLDFIPMJAAPLPJPBBCDMIBGNMPPJPHJKAIKBHEGC; db8ca2b43ed851cc93e71fd5fd72bff7=a73c35acd30a5f2c2e12d3bd0105e248; XSRF-TOKEN=a81866e0-7776-4b29-88a3-42f18b70bd8a; XSRF-TOKEN=eyJpdiI6IjJ4NVRlSCtKbk1HUjNBNkNkcXZGZmc9PSIsInZhbHVlIjoiZ2x2REswV3FrUGFrSEYvVHl4S2RQQ1hPbkdEeWR4VGxMZXl1TTRUK3BWYVp6Um1sbzZUZE5VcCt5Zml3eVR3clhGaFVZV2tSekVDUnUxbTl6QnYxODF5cUdyU2RlWFltU0ErOG0yWDl4Um1tWHhkN2xsamJHMGN1OC9wRXZ1dnEiLCJtYWMiOiI0Nzc5OGJkZWJiMTFmZmFiODI0ODJlMzdiOTAxNzVkNzZlYjc4MmNkOTE3MjRjMjk5NDdlYTBiN2NhNTFiNzk4IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6InJBQUphaXdFRVk0NnYyVVVWNzFobXc9PSIsInZhbHVlIjoiMGpmeXNMWDd1VVdqUWFiaitNODlQczcyczBzSXU1cFZhNUlybDBNL3pkQ3ZNbzA0SG83WmZzUEovY1ZlakJVYTNyV3cydVNrRjVvaGl6elM4bHRhRi95bTY4U0h6aFJxQ1NIMDQ3eFdGYmszR29vdnYxK3lYNVc0Q1kzd2xXcksiLCJtYWMiOiIyYzk5Yjk5ZTA2MGJmOTZjMzNiMzYxZWY3MGE2YTUyZWUxZDg5YjdkYWQyMzNiMDFjNzUzMTFlNzE4NDcyODAwIiwidGFnIjoiIn0%3D; zyRlBw9w49NYzV06GfuVY1Tav5uaKXQ5f2P26BLh=eyJpdiI6Ijh4QnhBOTVPY2NHSzRPckxOajBXdmc9PSIsInZhbHVlIjoieElWZ01Qc3AvL1JOVTdEOVBqQ1dKbCtKWk9ZM2E4ZmcyUHU2UmJoWHo1aHhpWkdQSkcwV3lhRkZlUitHY1JZeWhyMmVITm1TSHFueEtZM0VldkdGQkorQkRFWUlrVGtMbUxPWTdIRmM4bW9sK2FTRHR2Y3MzQk9pV0pCOS9LNXg0K1NXakJCeU9Xc0tvaUFuWDhRbHNNKzR5VEU2aElkcGJYWVBKc2Q0VklGVFRzbnpIMXY1WEtIbG8ydUJibGhlcEh6ais3SndnTUtSTHFIb1VFN0pkWHZ3RytpS1g5UUpROUVsQ2VkaTQ4VkY3Nm9OU3NDZVNCc0NtNEYwWnJja3hWM2JsdDJzRktwUFBJTTU5NmQ3d2ZJZ2F2Q2dXS1BwNGN4ekhiMThUZTFNZDE0ejN0eDYvQWRKZzlZaHI3aXl2dmcvOHVJRXZBckhwQjIyM1FQOHhhV1JQWCs3Zm9sOWZ6U0FrRlJJQVJOeVZ0WldyL3lGeDBDazlETFRsZHZGc1VTMkdzMFNYeEZwQkdSUkR4eUdKQT09IiwibWFjIjoiYmNhOGJjYWY4YTk4ZjFiY2M3OTVkYmE2NDI1Y2RmYmJhYTlkYjMzYjVlN2ZjYzY1NjFmZjgwNGUxMzg5YjY0YSIsInRhZyI6IiJ9; cf_clearance=eb1_j1xLGml_ZqiSx9iKgQ3Uizq2h9ZFygtS4xoqvE4-1784785841-1.2.1.1-nbr7VgdGPJowYAIq.vvVHZ61je0OxJGwfE5TraTCWTs8wlH0fWSKMzHd5040SsCYqIH53XfED3vS8S603T4rogP7zG7Xn1_JlYHoAYTNQZ8mFC2e_Ah2gOtgSt6RginShnWtSwN9AksEIV32HMAmTmOhJSSFR5IlFOmRA8UqopLHI7_QPhNleBydbh9RImuiE3vrvWlzChxim7zScvGPBxKhDX6dImOCmh8cfpCEi6GOftwAeeWTH0lrM0a0D72cfZ389WGRvaqpmDcmXM4tQU85AVzCF6OLRKBSfBQoAvsbw_f1qZQWS6qVKaSHWW60gFFGRh__TSWipPiWMauI7fEYTnayjirMHVpJ7FDBwdg; _ga=GA1.3.967752592.1784785844; TS0151fc2b=0167a1c8617f1dd83c4fec87640fc304c8301970e692579419787a1e7c357d61fa5c3569965f8256b7584dab0c57046c4fd86be90c; __cf_bm=Q4IrwOAlOSq99LzdG7bPXkGXd1ikgwFfnDewKN3VNGc-1784785953.7767494-1.0.1.1-m0hBnMouJ83ejroycnsLbMSduOHT1WNto3.wNwe5e0O3shKnA399NXaqFV1jR6a8AKUmRzcXn5fOc1y1iM84WEHBXnSQz69pLEJXuLMVEPD1RmCkA2cWN._1YfvEd64R; JSESSIONID=97161D2634782176B17F2EB15B4B933D; _ga_XXTTVXWHDB=GS2.3.s1784785844$o1$g1$t1784786486$j60$l0$h0; SESSION=5e901c33-c2eb-4f29-9bb9-999306f77ccd; f5avraaaaaaaaaaaaaaaa_session_=FNGKGJPILFFGADBDEFCBFLAHCOCMKFLOJAIPMHLPNENNCDDBKDLMPHFDDOBOBPEOJHKDOJGNBOIJGKIHHPCABEFECKNMJINHEOKIDAHGDFJKHEPEIMONPELLMCCLFLDH; f5avr1980069168aaaaaaaaaaaaaaaa_cspm_=NLEOOBCODNHNBFDMIJKJJPFBIGBAKDEOLLCCMEABBLJEBLALHCMNCDLHAJACJFOBCEICNKDAICNEBIBGAIGAHPPDACDNADMHHDAFGLFGOBCPMCDJDHPBKAAIJMMCBKHL; TS00000000076=0868f8be6fab2800f6fde2df9f3b3cf0be369ae8bd49f1f6745b8923cb9f73b42014232030590a9aec80fd7720ce321c086474d17b09d00005bbe8b00ed5090ede5a049f18c1568bb7746eb8ba87caccd3cbe8d16fdee6f70a98446ec35b12b954fc63f39cb0bf7b3b3fa7bf74cc1bf9933a4ec5438e47d4961b4b1c8312559496583034f07aaedc08081df8670de56b789eac0b4c0e47084e227e737bd50cee83bc54bed98700d23cb2c76e96b5d16567b32bc4bdb3ed9428889cb7e474626b53b49779453948493c0ec000c217fc63f9617fd8adac428ab83a841b2bd20f4fc8487a7abf126bacc60f31d048838f75fb30797e295b0c6ab476680e0b252474c7c90bf1068fa829; TSPD_101_DID=0868f8be6fab2800f6fde2df9f3b3cf0be369ae8bd49f1f6745b8923cb9f73b42014232030590a9aec80fd7720ce321c086474d17b0638002324328a0c04e0f57224b48c546db14a222b3febb68cd66f5e2aab255efa1ec4f00171ad6707aa22af5a3952754a2fb9daf1610075525dc6; TS011f2d1a=01266d26d0004094e4726d4a29937f2805922063631c062671186d2a967e00f9472398fd818b15536ae2e413f3e4263a4cd5b4e5d3; TSPD_101=0868f8be6fab28004c0438844cbc744b025c56482d91a04d2b7440994d279d4f932e75c6128afa2d786f83371ed385a708668fd38705180007b2eea447db9ed95ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab28008db8baf791435c1a7e53bf2b39fadd06618f148a1e0de8c3a1d66e5be89cf2ea89bb884ab80da50408dbecbc0c1720008a7b3c3a7911e85de0ef121f7de8ded8335b1d070c09060ca9eb152d8e645d66; TS5220f739029=0868f8be6fab2800f553e628a6280bd1568dbe875a3a92b4432e376a7b73fc9dd97584ed4de0e4251916765d43b9d513; TSf1edb2d2027=0868f8be6fab2000b3dbef95cd9c505eb98307288060d916c295c6354a4a180c35f70cc69bed82440846f07a72113000124f4ee29c043e8f88dfefd906a1fb1b6517bbd616794312d00c19af34b8cf3dc72138dd2b25cf3195c9572104a752a3',
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
                "nama_pml",
                "jumlah_prelist_awal"
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
 
 
def refresh_cookies():
    """
    Buka Chrome pakai profil yang sudah login SSO BPS, ambil cookies segar,
    lalu update variabel global cookies & headers secara otomatis.
    Dipanggil otomatis ketika session terdeteksi expired.
 
    Syarat:
    - VPN BPS sudah konek
    - Profil Chrome di CHROME_PROFILE_DIR/CHROME_PROFILE_NAME sudah pernah
      login manual ke FASIH minimal sekali
    - Tidak ada window Chrome lain yang sedang memakai profil yang sama
    """
    global cookies
 
    print("🔄 Session expired — membuka browser untuk ambil cookies segar...")
    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    options.add_argument(f"--profile-directory={CHROME_PROFILE_NAME}")
    # Aktifkan baris di bawah setelah yakin jalan (browser gak muncul di layar):
    # options.add_argument("--headless=new")
 
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(FASIH_HOME_URL)
        time.sleep(6)   # tunggu redirect SSO + halaman selesai load
 
        fresh = {c["name"]: c["value"] for c in driver.get_cookies()}
 
        if not fresh.get("SESSION") and not fresh.get("XSRF-TOKEN"):
            raise RuntimeError(
                "Cookies SESSION/XSRF-TOKEN tidak ditemukan. "
                "Buka Chrome dengan profil ini dan login manual ke FASIH dulu."
            )
 
        cookies.update(fresh)
        headers["x-xsrf-token"] = fresh.get("XSRF-TOKEN", headers["x-xsrf-token"])
        print(f"✅ Cookies segar berhasil diambil ({len(fresh)} cookie). Lanjut scraping...")
    finally:
        driver.quit()
 
 
def is_session_expired(response):
    """
    Deteksi apakah session sudah expired berdasarkan respons API.
    FASIH/Keycloak biasanya redirect ke halaman login (HTML) saat session habis —
    sehingga Content-Type bukan JSON, atau JSON-nya tidak punya field 'data'.
    """
    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type:
        return True
 
    try:
        body = response.json()
        # Kalau response JSON tapi field 'data' hilang dan ada pesan error auth
        if body.get("status") in (401, 403):
            return True
        if "login" in str(body).lower() or "unauthorized" in str(body).lower():
            return True
        return False
    except Exception:
        # Kalau response sama sekali gak bisa di-parse sebagai JSON → HTML login page
        return True
 
 
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
    max_refresh = 2          # maksimal berapa kali boleh refresh cookies dalam 1 run
    refresh_count = 0

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

        # ── Deteksi session expired → auto-refresh cookies lalu ulangi page ini ──
        if response.status_code in (200,) and is_session_expired(response) or \
           response.status_code in (302, 401):
            if refresh_count >= max_refresh:
                print(f"🛑 Session expired lagi setelah {max_refresh}x refresh. "
                      "Kemungkinan profil Chrome perlu login manual ulang.")
                break
            try:
                refresh_cookies()
                refresh_count += 1
                # Reset session agar cookies baru ikut terpakai
                session = requests.Session()
                print(f"↩️  Mengulang page {page} dengan cookies baru...")
                time.sleep(2)
                continue   # ulangi iterasi loop dengan page yang sama
            except Exception as e:
                print(f"🛑 Gagal refresh cookies: {e}")
                break

        if response.status_code != 200:
            print(f"❌ Error di page {page} | Status: {response.status_code}")
            print(response.text[:500])
            break

        try:
            json_res    = response.json()
        except Exception:
            print(f"❌ Response bukan JSON di page {page}. Kemungkinan session expired.")
            break

        data_block  = json_res.get("data", {})
        data        = data_block.get("content", [])
        is_last     = data_block.get("last", True)

        print(f"📄 Page {page} | data: {len(data)} | last: {is_last}")

        for user in data:
            for region in user.get("regionSummary", []):
                row = {
                    "userId":     user.get("userId"),
                    "username":   user.get("username"),
                    "email":      user.get("email"),
                    "role":       user.get("roleName"),
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
        time.sleep(random.uniform(1, 2))

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