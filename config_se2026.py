"""
Konfigurasi bersama untuk scrapping_sls.py dan dashboard_petugas.py.
Satu sumber kebenaran untuk path file, biar scraper dan dashboard
selalu nunjuk ke file yang sama.
"""
import os

NAMA_KABUPATEN = "AMBON"

BASE_PATH = "data"

LATEST_FILE = os.path.join(
    BASE_PATH,
    f"SCRAPING_REKAP_SE2026_{NAMA_KABUPATEN}_LATEST.xlsx"
)

HISTORY_PATH = os.path.join(BASE_PATH, "history")

os.makedirs(BASE_PATH, exist_ok=True)
os.makedirs(HISTORY_PATH, exist_ok=True)


def archive_filename(timestamp):
    return os.path.join(
        HISTORY_PATH,
        f"SCRAPING_REKAP_SE2026_{NAMA_KABUPATEN}_{timestamp}.xlsx"
    )