"""
Konfigurasi bersama untuk scrapping_sls.py dan dashboard_petugas.py.
Satu sumber kebenaran untuk path file, biar scraper dan dashboard
selalu nunjuk ke file yang sama.
"""
import os
 
NAMA_KABUPATEN = "AMBON"  # NAMA KABUPATEN
BASE_PATH = "C:/ZULFAA/BPS/Scrapping/"  # FOLDER UNTUK MENYIMPAN DATA HASIL SCRAPPING
 
# File ini SELALU berisi snapshot TERBARU (di-overwrite tiap kali scraping selesai).
# Inilah yang dibaca otomatis oleh dashboard.
LATEST_FILE = os.path.join(BASE_PATH, f"SCRAPING_REKAP_SE2026_{NAMA_KABUPATEN}_LATEST.xlsx")
 
 
def archive_filename(timestamp: str) -> str:
    """Nama file arsip/histori (tidak ditimpa, satu file per waktu scraping)."""
    return os.path.join(BASE_PATH, f"SCRAPING_REKAP_SE2026_{NAMA_KABUPATEN}_{timestamp}.xlsx")
 