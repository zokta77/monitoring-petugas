import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import glob
from datetime import datetime, date
from zoneinfo import ZoneInfo
from io import BytesIO
import folium
from streamlit_folium import st_folium
import json

from config_se2026 import LATEST_FILE, BASE_PATH, NAMA_KABUPATEN, HISTORY_PATH

# ─────────────────────────────────────────────────────────────────────────────
# Konfigurasi halaman
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SE2026 — Monitoring Pencacahan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset font global untuk SEMUA mode (terang & gelap) ── */
html, body,
[class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
p, div, label, td, th, li, a, button {
    font-family: 'Inter', sans-serif !important;
}

/* Sembunyikan sidebar & toggle */
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] {
    display: none !important;
}

/* ── Warna teks utama mengikuti tema ── */
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}
.main .block-container {
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

/* ───────────────── KPI Cards ───────────────── */

div[data-testid="stMetric"] {
    border-radius: 14px;
    padding: 1.1rem 1.2rem 1rem 1.4rem;
    position: relative;
    overflow: hidden;

    background: var(--secondary-background-color);
    border: 1px solid rgba(100,116,139,0.15);

    box-shadow:
        0 1px 2px rgba(15,23,42,0.04),
        0 4px 12px rgba(15,23,42,0.06);
}

div[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(
        180deg,
        #14b8a6,
        #0ea5e9
    );
}
            

/* Label KPI */

div[data-testid="stMetric"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;

    color: var(--text-color) !important;
    opacity: .7;
}

/* Nilai KPI */

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;

    color: var(--text-color) !important;
}

/* Delta KPI */

div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    color: #10b981 !important;
}

/* Tooltip Help (?) */

div[data-testid="stMetric"] button {
    color: var(--text-color) !important;
    opacity: .6;
}

div[data-testid="stMetric"] button:hover {
    color: #14b8a6 !important;
    opacity: 1;
}

/* ── Section headers ── */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}
h2::after {
    content: "";
    display: block;
    width: 40px;
    height: 3px;
    background: linear-gradient(90deg, #14b8a6, #0ea5e9);
    border-radius: 2px;
    margin-top: 6px;
}

/* ── Tab styling ── */
button[data-baseweb="tab"] {
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1rem !important;
    color: #64748b !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #14b8a6 !important;
    border-bottom-color: #14b8a6 !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(100,116,139,0.25);
    border-radius: 12px;
    overflow: hidden;
}
iframe { border-radius: 12px !important; }

/* ── Divider ── */
hr {
    border-color: rgba(100,116,139,0.2) !important;
    margin: 1.25rem 0 !important;
}

/* ── Expander ── */
details {
    border-radius: 10px !important;
    padding: 0.5rem !important;
    border: 1px solid rgba(100,116,139,0.25) !important;
}
details summary {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ── Caption / small text ── */
small, .stCaption, [data-testid="stCaptionContainer"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important;
    color: #64748b !important;
}

/* ── Alert ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 4px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Multiselect & selectbox ── */
div[data-baseweb="select"] span,
div[data-baseweb="tag"] span {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ── Plotly chart container ── */
.stPlotlyChart {
    border: 1px solid rgba(100,116,139,0.2);
    border-radius: 12px;
    overflow: hidden;
}

/* ── Badge update ── */
.badge-update {
    background: rgba(16,185,129,0.15);
    border: 1px solid #10b981;
    border-radius: 20px;
    padding: 4px 14px;
    color: #10b981;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.76rem;
    font-weight: 600;
    white-space: nowrap;
}
    /* Warna ikon help metric */
[data-testid="stMetric"] button {
    color: #0f172a !important;
}

/* Hover */
[data-testid="stMetric"] button:hover {
    color: #14b8a6 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Auto-refresh
# ─────────────────────────────────────────────────────────────────────────────
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60 * 1000, key="auto_refresh_dashboard")
except ImportError:
    pass

# ─────────────────────────────────────────────────────────────────────────────
# Konstanta
# ─────────────────────────────────────────────────────────────────────────────
IDENTITY_COLS = [
    "userId", "username", "email", "role", "regionCode",
    "total_data", "scraped_at",
    "nmkab", "nmkec", "nmdesa", "nmsls", "nmsubsls",
    "pengawas", "pencacah",
    "nama_pcl", "nama_pml",
]

# Pemetaan nama kolom teknis → nama tampilan
COL_LABELS = {
    "nama_pcl":  "Nama Pencacah",
    "nama_pml":  "Nama Pengawas",
    "nmkec":     "Kecamatan",
    "nmdesa":    "Desa",
    "nmkab":     "Kabupaten",
    "nmsls":     "SLS",
    "nmsubsls":  "Sub-SLS",
    "total_data":"Total Muatan",
    "regionCode":"Kode Wilayah",
    "Progress (%)": "Progress (%)",
    "Jumlah PCL": "Jumlah Pencacah",
    "Selisih":   "Selisih",
}

def nice_col(c: str) -> str:
    return COL_LABELS.get(c, c)


DONE_KEYWORDS     = ["APPROVED", "SUBMITTED"]
NOT_DONE_KEYWORDS = ["OPEN", "DRAFT"]

PLOT_TEMPLATE = "plotly_dark"
PLOT_BG       = "rgba(30,41,59,0)"
PAPER_BG      = "rgba(30,41,59,0)"
TEAL_PALETTE  = [
    "#14b8a6", "#0ea5e9", "#6366f1", "#f59e0b",
    "#ef4444", "#84cc16", "#ec4899", "#f97316",
]

def styled_chart_layout(**kwargs):
    return dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color="#94a3b8", family="Inter, sans-serif", size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        **kwargs,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(path_or_file, cache_key=None) -> pd.DataFrame:
    name = getattr(path_or_file, "name", str(path_or_file))
    if str(name).lower().endswith(".csv"):
        df = pd.read_csv(path_or_file)
    else:
        df = pd.read_excel(path_or_file)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def detect_status_cols(df: pd.DataFrame) -> list:
    return [c for c in df.columns if c not in IDENTITY_COLS]

def to_numeric_safe(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df

def rename_display(df: pd.DataFrame) -> pd.DataFrame:
    """Rename kolom teknis ke nama tampilan untuk ditampilkan ke user."""
    return df.rename(columns=nice_col)
from io import BytesIO

from io import BytesIO

def to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Rekap Pencacah")

    return output.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# Histori multi-hari (untuk rekap progress harian per pencacah)
# ─────────────────────────────────────────────────────────────────────────────
def _history_files():
    pattern = os.path.join(HISTORY_PATH, f"SCRAPING_REKAP_SE2026_{NAMA_KABUPATEN}_*.xlsx")
    return [f for f in glob.glob(pattern) if not f.endswith("_LATEST.xlsx")]


def _history_cache_key():
    files = _history_files()
    if not files:
        return "empty"
    return (len(files), round(max(os.path.getmtime(f) for f in files), 0))


@st.cache_data(show_spinner=False)
def load_history(cache_key=None) -> pd.DataFrame:
    """Baca SEMUA file arsip hasil scraping (bukan cuma snapshot terbaru),
    dipakai untuk membangun rekap progress harian per pencacah."""
    files = _history_files()
    if not files:
        return pd.DataFrame()

    frames = []
    for f in files:
        try:
            frames.append(pd.read_excel(f))
        except Exception:
            continue
    if not frames:
        return pd.DataFrame()

    hist = pd.concat(frames, ignore_index=True)
    hist.columns = [str(c).strip() for c in hist.columns]

    if "scraped_at" not in hist.columns:
        return pd.DataFrame()

    hist["scraped_at"] = pd.to_datetime(hist["scraped_at"], errors="coerce")
    hist = hist.dropna(subset=["scraped_at"])
    hist["tanggal"] = hist["scraped_at"].dt.date

    hist_status_cols = [c for c in detect_status_cols(hist) if c != "tanggal"]
    numeric_cols_h = hist_status_cols + (["total_data"] if "total_data" in hist.columns else [])
    hist = to_numeric_safe(hist, numeric_cols_h)

    return hist


def build_daily_recap(pcl_name: str):
    """
    Bangun rekap progress harian untuk 1 pencacah dari data arsip histori.

    - Kalau 1 hari discraping beberapa kali → diambil snapshot TERAKHIR hari itu
      (karena angka status bersifat KUMULATIF, bukan dijumlah mentah — menjumlah
      mentah snapshot yang sama akan melipatgandakan angka secara keliru).
    - "Selisih" / delta harian = snapshot hari ini dikurangi snapshot hari
      sebelumnya → ini yang merepresentasikan "berapa yang baru submit/draft/
      approve HARI ITU".

    Return: (daily, delta, diag) — diag berisi info diagnostik untuk membantu
    menemukan penyebab spesifik kalau data kosong (bukan cuma pesan generik).
    """
    files = _history_files()
    diag = {
        "history_path": HISTORY_PATH,
        "pattern": os.path.join(HISTORY_PATH, f"SCRAPING_REKAP_SE2026_{NAMA_KABUPATEN}_*.xlsx"),
        "n_files": len(files),
        "files": files,
        "n_rows_total": 0,
        "has_nama_pcl_col": False,
        "n_rows_for_pcl": 0,
        "n_unique_dates": 0,
        "sample_names": [],
    }

    hist = load_history(cache_key=_history_cache_key())
    if hist.empty:
        return None, None, diag

    diag["n_rows_total"] = len(hist)
    diag["has_nama_pcl_col"] = "nama_pcl" in hist.columns

    if not diag["has_nama_pcl_col"]:
        return None, None, diag

    diag["sample_names"] = sorted(hist["nama_pcl"].dropna().unique().tolist())[:10]

    sub = hist[hist["nama_pcl"] == pcl_name].copy()
    diag["n_rows_for_pcl"] = len(sub)
    if sub.empty:
        return None, None, diag

    hist_status_cols = [c for c in detect_status_cols(hist) if c != "tanggal"]
    agg_dict = {c: "last" for c in hist_status_cols}
    if "total_data" in sub.columns:
        agg_dict["total_data"] = "last"

    daily = (
        sub.sort_values("scraped_at")
           .groupby("tanggal", as_index=False)
           .agg(agg_dict)
           .sort_values("tanggal")
           .reset_index(drop=True)
    )
    diag["n_unique_dates"] = len(daily)

    # ── Delta harian: hari pertama dipakai sebagai baseline (delta = nilai itu sendiri) ──
    delta = daily.copy()
    cols_to_diff = hist_status_cols + (["total_data"] if "total_data" in daily.columns else [])
    for c in cols_to_diff:
        delta[c] = daily[c].diff().fillna(daily[c]).clip(lower=0)

    return daily, delta, diag


def render_pencacah_daily_panel(pcl_name: str):
    """Tampilkan tabel + line chart rekap progress harian untuk 1 pencacah yang diklik."""
    daily, delta, diag = build_daily_recap(pcl_name)

    st.markdown(f"##### 📅 Rekap Progress Harian — {pcl_name}")

    if daily is None:
        # ── Bedakan penyebabnya, jangan cuma pesan generik ──────────────────
        if diag["n_files"] == 0:
            st.warning(
                f"Tidak ditemukan file arsip sama sekali di folder:\n\n`{diag['history_path']}`\n\n"
                f"Pola nama file yang dicari: `{os.path.basename(diag['pattern'])}`\n\n"
                "Kemungkinan: `scrapping_sls.py` belum pernah dijalankan di PC ini, atau "
                "`BASE_PATH`/`NAMA_KABUPATEN` di `config_se2026.py` berbeda dari yang dipakai scraper."
            )
        elif diag["n_rows_total"] == 0:
            st.warning(
                f"Ditemukan {diag['n_files']} file arsip, tapi semuanya kosong/gagal dibaca "
                "(kemungkinan formatnya rusak atau kolom `scraped_at` tidak ada)."
            )
        elif not diag["has_nama_pcl_col"]:
            st.warning(
                f"Ditemukan {diag['n_files']} file arsip ({diag['n_rows_total']:,} baris), tapi "
                "kolom `nama_pcl` tidak ada di dalamnya. Ini berarti file arsip itu dibuat "
                "SEBELUM fitur merge ke `master_data.xlsx` ditambahkan — data lama ini tidak "
                "akan pernah punya nama_pcl. Rekap harian akan mulai muncul dari scraping "
                "berikutnya yang sudah ter-merge."
            )
        elif diag["n_rows_for_pcl"] == 0:
            sample = ", ".join(diag["sample_names"][:5]) or "(tidak ada nama terbaca)"
            st.warning(
                f"Ditemukan {diag['n_files']} file arsip ({diag['n_rows_total']:,} baris), tapi "
                f"tidak ada baris dengan nama pencacah **persis** `{pcl_name}`. "
                f"Contoh nama yang ADA di histori: {sample}...\n\n"
                "Kemungkinan penyebab: ejaan/spasi nama_pcl di master_data.xlsx berubah, atau "
                "pencacah ini baru ditambahkan setelah file-file arsip lama dibuat."
            )
        else:
            st.info(
                "Belum ada data histori multi-hari untuk pencacah ini. Fitur ini butuh "
                "setidaknya beberapa hari scraping berjalan."
            )

        with st.expander("🔍 Info diagnostik teknis"):
            st.json({k: v for k, v in diag.items() if k != "files"})
            if diag["files"]:
                st.caption("File arsip yang terbaca:")
                st.code("\n".join(os.path.basename(f) for f in diag["files"]))
        return

    if len(daily) < 2:
        st.info(
            f"Baru ada **1 hari** data ({daily['tanggal'].iloc[0]}) untuk pencacah ini. "
            "Line chart & tren delta akan muncul setelah ada data di hari berikutnya."
        )

    st.caption(
        "📌 Kalau 1 hari discraping berkali-kali, yang dipakai adalah snapshot "
        "**terakhir** hari itu (angka status bersifat kumulatif, bukan dijumlah mentah). "
        "Kolom di bawah menunjukkan **selisih (baru bertambah) dibanding hari sebelumnya**."
    )

    # 1. Tambahkan deteksi kolom untuk REJECT
    submit_cols  = [c for c in delta.columns if "SUBMIT"  in c.upper()]
    draft_cols   = [c for c in delta.columns if "DRAFT"   in c.upper()]
    approve_cols = [c for c in delta.columns if "APPROV"  in c.upper()]
    reject_cols  = [c for c in delta.columns if "REJECT"  in c.upper()]

    tampil = pd.DataFrame({"Tanggal": daily["tanggal"]})
    # if "total_data" in daily.columns:
    #     tampil["Total Muatan"] = daily["total_data"]
    
    # 2. Masukkan data ke DataFrame berdasarkan urutan alur data yang diinginkan
    if draft_cols:
        tampil["Draft (Baru)"] = delta[draft_cols].sum(axis=1).astype(int)
    if submit_cols:
        tampil["Submit (Baru)"] = delta[submit_cols].sum(axis=1).astype(int)
    if approve_cols:
        tampil["Approve (Baru)"] = delta[approve_cols].sum(axis=1).astype(int)
    if reject_cols:
        tampil["Reject (Baru)"] = delta[reject_cols].sum(axis=1).astype(int)

    st.dataframe(tampil, use_container_width=True, hide_index=True)

    # 3. Update daftar kolom yang akan diplot beserta warna spesifiknya
    line_cols = [c for c in ["Draft (Baru)", "Submit (Baru)", "Approve (Baru)", "Reject (Baru)"] if c in tampil.columns]
    
    if line_cols:
        line_colors = {
            "Draft (Baru)": "#f59e0b",    # Amber
            "Submit (Baru)": "#0ea5e9",   # Biru
            "Approve (Baru)": "#14b8a6",  # Teal/Hijau
            "Reject (Baru)": "#ef4444",   # Merah
        }
        fig_line = go.Figure()
        for c in line_cols:
            fig_line.add_trace(go.Scatter(
                x=tampil["Tanggal"], y=tampil[c],
                mode="lines+markers", name=c,
                line=dict(width=2.5, color=line_colors.get(c)),
                marker=dict(size=7),
            ))
        fig_line.update_layout(
            **styled_chart_layout(height=340),
            xaxis=dict(title="Tanggal", showgrid=False, type="date"),
            yaxis=dict(title="Jumlah Baru per Hari", showgrid=True,
                       gridcolor="rgba(100,116,139,0.15)"),
            legend=dict(orientation="h", y=1.15),
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Kolom status Draft/Submit/Approve/Reject tidak terdeteksi untuk membuat line chart.")
def build_overall_daily_recap():
    """Bangun rekap progress harian kumulatif untuk KESELURUHAN pencacah."""
    hist = load_history(cache_key=_history_cache_key())
    if hist.empty or "nama_pcl" not in hist.columns:
        return None, None

    hist_status_cols = [c for c in detect_status_cols(hist) if c != "tanggal"]
    
    # 1. Ambil snapshot TERAKHIR per pencacah untuk tiap harinya
    agg_dict_pcl = {c: "last" for c in hist_status_cols}
    if "total_data" in hist.columns:
        agg_dict_pcl["total_data"] = "last"
        
    snapshot_per_pcl = (
        hist.sort_values("scraped_at")
            .groupby(["tanggal", "nama_pcl"], as_index=False)
            .agg(agg_dict_pcl)
    )
    
    # 2. Jumlahkan semua pencacah untuk mendapatkan total harian se-Kabupaten/Kota
    agg_dict_total = {c: "sum" for c in hist_status_cols}
    if "total_data" in snapshot_per_pcl.columns:
        agg_dict_total["total_data"] = "sum"
        
    daily = (
        snapshot_per_pcl.groupby("tanggal", as_index=False)
            .agg(agg_dict_total)
            .sort_values("tanggal")
            .reset_index(drop=True)
    )
    
    # 3. Hitung delta (selisih) dari hari ke hari
    delta = daily.copy()
    cols_to_diff = hist_status_cols + (["total_data"] if "total_data" in daily.columns else [])
    for c in cols_to_diff:
        delta[c] = daily[c].diff().fillna(daily[c]).clip(lower=0)
        
    return daily, delta

def render_overall_daily_panel():
    """Tampilkan grafik tren harian untuk keseluruhan wilayah."""
    daily, delta = build_overall_daily_recap()
    
    if daily is None or len(daily) < 2:
        st.info("Belum ada data histori multi-hari yang cukup untuk menampilkan tren keseluruhan wilayah.")
        return

    st.markdown("#### 📈 Tren Progress Harian Keseluruhan")
    st.caption("Grafik di bawah menunjukkan total penambahan data (Baru) setiap hari untuk **seluruh pencacah**.")

    submit_cols  = [c for c in delta.columns if "SUBMIT"  in c.upper()]
    draft_cols   = [c for c in delta.columns if "DRAFT"   in c.upper()]
    approve_cols = [c for c in delta.columns if "APPROV"  in c.upper()]
    reject_cols  = [c for c in delta.columns if "REJECT"  in c.upper()]
    done_cols_daily = [c for c in daily.columns if any(k in c.upper() for k in DONE_KEYWORDS)]

    tampil = pd.DataFrame({"Tanggal": daily["tanggal"]})
    if "total_data" in daily.columns:
        tampil["Total Muatan"] = daily["total_data"]
        
    # Hitung Persentase
    if done_cols_daily and "total_data" in daily.columns:
        daily_done = daily[done_cols_daily].sum(axis=1)
        tampil["Progress Keseluruhan (%)"] = (daily_done / daily["total_data"].replace(0, pd.NA) * 100).round(2).fillna(0)
        
    if draft_cols: tampil["Draft (Baru)"] = delta[draft_cols].sum(axis=1).astype(int)
    if submit_cols: tampil["Submit (Baru)"] = delta[submit_cols].sum(axis=1).astype(int)
    if approve_cols: tampil["Approve (Baru)"] = delta[approve_cols].sum(axis=1).astype(int)
    if reject_cols: tampil["Reject (Baru)"] = delta[reject_cols].sum(axis=1).astype(int)

    line_cols = [c for c in ["Draft (Baru)", "Submit (Baru)", "Approve (Baru)", "Reject (Baru)"] if c in tampil.columns]
    
    if line_cols or "Progress Keseluruhan (%)" in tampil.columns:
        fig_line = go.Figure()
        line_colors = {
            "Draft (Baru)": "#f59e0b",
            "Submit (Baru)": "#0ea5e9",
            "Approve (Baru)": "#14b8a6",
            "Reject (Baru)": "#ef4444",
        }

        for c in line_cols:
            fig_line.add_trace(go.Scatter(
                x=tampil["Tanggal"], y=tampil[c],
                mode="lines+markers", name=c,
                line=dict(width=2.5, color=line_colors.get(c)),
                marker=dict(size=7),
                yaxis="y1"
            ))
            
        if "Progress Keseluruhan (%)" in tampil.columns:
            fig_line.add_trace(go.Scatter(
                x=tampil["Tanggal"], y=tampil["Progress Keseluruhan (%)"],
                mode="lines+markers", name="Progress (%)",
                line=dict(width=3.5, color="#8b5cf6", dash="dot"),
                marker=dict(size=9, symbol="diamond"),
                yaxis="y2"
            ))
        fig_line.update_layout(
            # Masukkan margin ke dalam styled_chart_layout agar menimpa default-nya
            **styled_chart_layout(height=380, margin=dict(l=10, r=10, t=20, b=10)),
            xaxis=dict(title="Tanggal", showgrid=False, type="date"),
            yaxis=dict(title="Jumlah Status (Baru)", showgrid=True, gridcolor="rgba(100,116,139,0.15)", side="left"),
            yaxis2=dict(title="Progress Keseluruhan (%)", overlaying="y", side="right", range=[0, 105], showgrid=False),
            legend=dict(orientation="h", y=1.15)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        with st.expander("Tampilkan Data Tabel Keseluruhan"):
            st.dataframe(tampil, use_container_width=True, hide_index=True)
# ─────────────────────────────────────────────────────────────────────────────
# Load data otomatis
# ─────────────────────────────────────────────────────────────────────────────
if not os.path.exists(LATEST_FILE):
    st.error(
        f"Belum ada hasil scraping di `{LATEST_FILE}`. "
        "Jalankan `scrapping_sls.py` terlebih dahulu."
    )
    st.stop()

file_mtime   = os.path.getmtime(LATEST_FILE)
df_raw       = load_data(LATEST_FILE, cache_key=file_mtime)
last_updated = datetime.fromtimestamp(
    file_mtime, tz=ZoneInfo("Asia/Jayapura")
).strftime("%d %b %Y · %H:%M WIT")

# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            flex-wrap:wrap;gap:10px;margin-bottom:1rem;">
    <div style="display:flex;align-items:center;gap:12px;">
        <div style="background:linear-gradient(135deg,#14b8a6,#0ea5e9);
                    width:44px;height:44px;border-radius:12px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.4rem;flex-shrink:0;">📊</div>
        <div>
            <h1 style="margin:0;font-size:1.55rem;font-weight:700;
                       letter-spacing:-0.02em;line-height:1.2;
                       font-family:'Inter',sans-serif;">
                SE2026 — Monitoring Status Pencacahan KOTA AMBON 
            </h1>
            <p style="margin:0;color:#64748b;font-size:0.8rem;
                      font-family:'Inter',sans-serif;">
                Progress per Pencacah / Desa · Data update dari FASIH-SM 
            </p>
        </div>
    </div>
    <span class="badge-update">🟢 Diperbarui: {last_updated}</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Deteksi kolom status
# ─────────────────────────────────────────────────────────────────────────────
status_cols  = detect_status_cols(df_raw)
numeric_cols = status_cols + (["total_data"] if "total_data" in df_raw.columns else [])
df_raw       = to_numeric_safe(df_raw, numeric_cols)

if not status_cols:
    st.error(
        "Tidak ada kolom status terdeteksi. Pastikan file punya kolom "
        "selain: " + ", ".join(IDENTITY_COLS)
    )
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# Filter bar — inline
# ─────────────────────────────────────────────────────────────────────────────
f1, f2 = st.columns([2, 3])

with f1:
    if "nmkec" in df_raw.columns:
        all_kec = sorted(df_raw["nmkec"].dropna().unique().tolist())
        sel_kec = st.multiselect(
            "Kecamatan", all_kec,
            default=[], placeholder="🏙️ Semua kecamatan",
        )
    else:
        sel_kec = []

with f2:
    if "nama_pcl" in df_raw.columns:
        all_pcl = sorted(df_raw["nama_pcl"].dropna().unique().tolist())
        sel_pcl = st.multiselect(
            "Pencacah", all_pcl,
            default=[], placeholder="👤 Cari nama pencacah...",
        )
    else:
        sel_pcl = []

df = df_raw.copy()
if sel_kec and "nmkec" in df.columns:
    df = df[df["nmkec"].isin(sel_kec)]
if sel_pcl and "nama_pcl" in df.columns:
    df = df[df["nama_pcl"].isin(sel_pcl)]

if len(df) < len(df_raw):
    st.caption(f"Filter aktif · Menampilkan **{len(df):,}** dari **{len(df_raw):,}** baris")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# KPI
# ─────────────────────────────────────────────────────────────────────────────
n_pcl    = df["nama_pcl"].nunique() if "nama_pcl" in df.columns else 0
n_pml    = df["nama_pml"].nunique() if "nama_pml" in df.columns else 0
n_desa   = df["nmdesa"].nunique()   if "nmdesa"   in df.columns else 0
total_data = int(df["total_data"].sum()) if "total_data" in df.columns else int(df[status_cols].sum().sum())

done_cols     = [c for c in status_cols if any(k in c.upper() for k in DONE_KEYWORDS)]
not_done_cols = [c for c in status_cols if any(k in c.upper() for k in NOT_DONE_KEYWORDS)]
rejected_cols = [c for c in status_cols if "REJECTED" in c.upper()]

total_done     = int(df[done_cols].sum().sum())     if done_cols     else 0
total_rejected = int(df[rejected_cols].sum().sum()) if rejected_cols else 0
pct_done       = ((total_done+total_rejected) / total_data * 100)      if total_data    else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Pencacah",  f"{n_pcl:,}")
k2.metric("Total Pengawas",  f"{n_pml:,}")
k3.metric("Total Desa",      f"{n_desa:,}")
k4.metric("Total Muatan",    f"{total_data:,}")
k5.metric(
    "Selesai (Done)",
    f"{total_done:,}",
    help="Approved by Pengawas + Submitted by Pencacah"
)

k6.metric(
    "Ditolak",
    f"{total_rejected:,}",
    help="Rejected by Pengawas"
)
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_overview, tab_pcl, tab_target, tab_desa, tab_raw = st.tabs([
    "📈 Distribusi Status",
    "👤 Per Pencacah",
    "🎯 Target Harian",
    "🏘️ Per Desa",
    "🗃️ Data Mentah",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Distribusi Status
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.subheader("Distribusi Status Keseluruhan")

    status_totals = df[status_cols].sum().sort_values(ascending=False)
    status_totals = status_totals[status_totals > 0]

    c_bar, c_pie, c_gauge = st.columns([3, 2, 2])

    with c_bar:
        fig_bar = px.bar(
            x=status_totals.values,
            y=status_totals.index,
            orientation="h",
            labels={"x": "Jumlah", "y": ""},
             text=[f"{int(v):,}" for v in status_totals.values],
            color=status_totals.index,
            color_discrete_sequence=TEAL_PALETTE,
            template=PLOT_TEMPLATE,
        )
        fig_bar.update_traces(textposition="outside", textfont_size=11)
        fig_bar.update_layout(
            **styled_chart_layout(showlegend=False, height=360),
            xaxis=dict(showgrid=True, gridcolor="rgba(100,116,139,0.15)"),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_pie:
        fig_pie = px.pie(
            values=status_totals.values,
            names=status_totals.index,
            hole=0.55,
            color_discrete_sequence=TEAL_PALETTE,
            template=PLOT_TEMPLATE,
        )
        fig_pie.update_traces(
            textinfo="percent",
            textfont_size=11,
            hovertemplate="<b>%{label}</b><br>%{value:,} usaha<br>%{percent}<extra></extra>",
        )
        fig_pie.update_layout(**styled_chart_layout(
            height=360, showlegend=True,
            legend=dict(orientation="v", x=1.05),
        ))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct_done,
            number={"suffix": "%", "valueformat": ".2f","font": {"size": 36, "color": "#14b8a6",
                                            "family": "JetBrains Mono"}},
            title={"text": "Overall Progress",
                   "font": {"color": "#94a3b8", "size": 13, "family": "Inter"}},
            gauge={
                "axis":      {"range": [0, 100], "tickcolor": "#475569",
                              "tickfont": {"color": "#64748b", "size": 10}},
                "bar":       {"color": "#14b8a6", "thickness": 0.25},
                "bgcolor":   "rgba(0,0,0,0)",
                "bordercolor": "rgba(100,116,139,0.3)",
                "steps": [
                    {"range": [0,  50], "color": "rgba(30,41,59,0.6)"},
                    {"range": [50, 80], "color": "rgba(23,37,84,0.6)"},
                    {"range": [80,100], "color": "rgba(13,61,46,0.6)"},
                ],
                "threshold": {"line": {"color": "#0ea5e9", "width": 3},
                              "thickness": 0.8, "value": pct_done},
            },
        ))
        fig_gauge.update_layout(**styled_chart_layout(height=360))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.divider()
    st.subheader("🗺️ Peta Progress Wilayah")

    # Menggunakan try-except agar dashboard tidak error jika file geojson belum ada
    try:
        with open('kecamatan.geojson', 'r') as f:
            geo_kec = json.load(f)
        with open('desa.geojson', 'r') as f:
            geo_desa = json.load(f)

        # 1. State Management untuk Peta
        if 'selected_kecamatan' not in st.session_state:
            st.session_state.selected_kecamatan = None

        # 2. Persiapan Data (Menghitung Progress per Kecamatan & Desa)
        # Aggregasi Kecamatan
        agg_kec_map = df.groupby("nmkec")[status_cols + ["total_data"]].sum().reset_index()
        if done_cols and "total_data" in agg_kec_map.columns:
            agg_kec_map["Progress"] = (agg_kec_map[done_cols].sum(axis=1) / agg_kec_map["total_data"].replace(0, pd.NA) * 100).fillna(0)
        else:
            agg_kec_map["Progress"] = 0

        # Aggregasi Desa
        agg_desa_map = df.groupby(["nmkec", "nmdesa"])[status_cols + ["total_data"]].sum().reset_index()
        if done_cols and "total_data" in agg_desa_map.columns:
            agg_desa_map["Progress"] = (agg_desa_map[done_cols].sum(axis=1) / agg_desa_map["total_data"].replace(0, pd.NA) * 100).fillna(0)
        else:
            agg_desa_map["Progress"] = 0

       # 3. Logika Render Peta
        if st.session_state.selected_kecamatan is None:
            st.markdown("**Level: Kecamatan** (Klik area kecamatan pada peta untuk melihat detail level desa)")

            m_kec = folium.Map(location=[-3.69, 128.18], zoom_start=11)

            # --- Layer Choropleth (Hanya untuk Warna Dasar) ---
            folium.Choropleth(
                geo_data=geo_kec,
                data=agg_kec_map,
                columns=['nmkec', 'Progress'],
                key_on='feature.properties.nmkec', 
                fill_color='YlGnBu',
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name='Progress Pencacahan (%)',
                name='Progress Kecamatan'
            ).add_to(m_kec)

            # --- TAMBAHAN: Layer Transparan untuk Tooltip Hover Kecamatan ---
            # 1. Konversi DataFrame ke Dictionary agar mudah dicari
            kec_dict = agg_kec_map.set_index('nmkec').to_dict(orient='index')

            # 2. Suntikkan data dari Pandas ke dalam Properties GeoJSON
            for feature in geo_kec['features']:
                k_name = feature['properties'].get('nmkec')
                if k_name in kec_dict:
                    feature['properties']['Progress Hover'] = f"{kec_dict[k_name]['Progress']:.2f}%"
                    for col in status_cols:
                        feature['properties'][col] = int(kec_dict[k_name].get(col, 0))
                else:
                    feature['properties']['Progress Hover'] = "0.0%"
                    for col in status_cols:
                        feature['properties'][col] = 0

            # 3. Setup kolom apa saja yang mau ditampilkan di tooltip
            tooltip_fields_kec = ['nmkec', 'Progress Hover'] + status_cols
            tooltip_aliases_kec = ['Kecamatan', 'Progress (%)'] + status_cols

            # 4. Tumpuk layer GeoJSON transparan
            folium.GeoJson(
                geo_kec,
                style_function=lambda x: {'fillOpacity': 0.0001, 'weight': 0}, # Dibuat nyaris tembus pandang
                tooltip=folium.GeoJsonTooltip(
                    fields=tooltip_fields_kec,
                    aliases=tooltip_aliases_kec,
                    style="background-color: white; color: #333; font-family: 'Inter', sans-serif; font-size: 13px; padding: 10px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
                )
            ).add_to(m_kec)
            # ----------------------------------------------------------------

            # Render di Streamlit
            map_data = st_folium(m_kec, width=None, height=600, key="map_kec", returned_objects=["last_active_drawing"])

            if map_data and map_data.get('last_active_drawing'):
                clicked_kec = map_data['last_active_drawing']['properties']['nmkec'] 
                st.session_state.selected_kecamatan = clicked_kec
                st.rerun()

        else:
            kec_aktif = st.session_state.selected_kecamatan
            
            col_title, col_btn = st.columns([3, 1])
            with col_title:
                st.markdown(f"**Level: Desa (Kecamatan {kec_aktif})**")
            with col_btn:
                if st.button("⬅ Kembali ke Peta Kecamatan", use_container_width=True):
                    st.session_state.selected_kecamatan = None
                    st.rerun()

            df_desa_filtered = agg_desa_map[agg_desa_map['nmkec'] == kec_aktif]
            
            geo_desa_filtered = {
                "type": "FeatureCollection",
                "features": [f for f in geo_desa['features'] if f['properties'].get('nmkec') == kec_aktif] 
            }
            geo_desa_rendered = geo_desa_filtered if geo_desa_filtered['features'] else geo_desa

            m_desa = folium.Map(location=[-3.69, 128.18], zoom_start=12)

            # --- Layer Choropleth (Warna Dasar Desa) ---
            folium.Choropleth(
                geo_data=geo_desa_rendered,
                data=df_desa_filtered,
                columns=['nmdesa', 'Progress'],
                key_on='feature.properties.nmdesa', 
                fill_color='YlGnBu',
                fill_opacity=0.8,
                line_opacity=0.5,
                legend_name=f'Progress Kelurahan/Desa (%)'
            ).add_to(m_desa)

            # --- TAMBAHAN: Layer Transparan untuk Tooltip Hover Desa ---
            desa_dict = df_desa_filtered.set_index('nmdesa').to_dict(orient='index')

            for feature in geo_desa_rendered['features']:
                d_name = feature['properties'].get('nmdesa')
                if d_name in desa_dict:
                    feature['properties']['Progress Hover'] = f"{desa_dict[d_name]['Progress']:.2f}%"
                    for col in status_cols:
                        feature['properties'][col] = int(desa_dict[d_name].get(col, 0))
                else:
                    feature['properties']['Progress Hover'] = "0.0%"
                    for col in status_cols:
                        feature['properties'][col] = 0

            tooltip_fields_desa = ['nmdesa', 'Progress Hover'] + status_cols
            tooltip_aliases_desa = ['Desa/Kelurahan', 'Progress (%)'] + status_cols

            folium.GeoJson(
                geo_desa_rendered,
                style_function=lambda x: {'fillOpacity': 0.0001, 'weight': 0},
                tooltip=folium.GeoJsonTooltip(
                    fields=tooltip_fields_desa,
                    aliases=tooltip_aliases_desa,
                    style="background-color: white; color: #333; font-family: 'Inter', sans-serif; font-size: 13px; padding: 10px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
                )
            ).add_to(m_desa)
            # -----------------------------------------------------------

            st_folium(m_desa, width=None, height=600, key="map_desa")
    except FileNotFoundError:
        st.info("💡 **Tips:** Letakkan file `kecamatan.geojson` dan `desa.geojson` di dalam folder yang sama dengan script ini untuk mengaktifkan fitur peta.")
    except Exception as e:
        st.error(f"Gagal memuat peta: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Per Pencacah (PCL)
# ══════════════════════════════════════════════════════════════════════════════
with tab_pcl:
    st.subheader("Monitoring Per Pencacah")
    # ---> TAMBAHKAN PEMANGGILAN FUNGSI DI SINI <---
    render_overall_daily_panel()
    st.divider()
    # ----------------------------------------------
    if "nama_pcl" not in df.columns:
        st.warning("Kolom `nama_pcl` tidak ditemukan dalam data.")
    else:
        agg_cols = status_cols + (["total_data"] if "total_data" in df.columns else [])
        agg_pcl  = df.groupby("nama_pcl")[agg_cols].sum().reset_index()

        if "total_data" in agg_pcl.columns and done_cols:
            agg_pcl["Progress (%)"] = (
                agg_pcl[done_cols].sum(axis=1)
                / agg_pcl["total_data"].replace(0, pd.NA) * 100
            ).round(1).fillna(0)
        if "total_data" in agg_pcl.columns:
            agg_pcl = agg_pcl.sort_values("total_data", ascending=False)

        # ── Stacked bar ──────────────────────────────────────────────────────
        max_show  = 30
        chart_pcl = agg_pcl.head(max_show)
        if len(agg_pcl) > max_show:
            st.caption(
                f"Grafik menampilkan {max_show} pencacah teratas dari {len(agg_pcl)} total. "
                "Lihat tabel di bawah untuk data lengkap."
            )

        fig_pcl = go.Figure()
        for i, c in enumerate(status_cols):
            if c in chart_pcl.columns:
                fig_pcl.add_trace(go.Bar(
                    name=c,
                    x=chart_pcl["nama_pcl"],
                    y=chart_pcl[c],
                    marker_color=TEAL_PALETTE[i % len(TEAL_PALETTE)],
                    hovertemplate="<b>%{x}</b><br>" + c + ": %{y:,}<extra></extra>",
                ))
        fig_pcl.update_layout(
            barmode="stack",
            **styled_chart_layout(height=420),
            xaxis=dict(tickangle=-40, showgrid=False, tickfont_size=10,
                       title="Nama Pencacah"),
            yaxis=dict(showgrid=True, gridcolor="rgba(100,116,139,0.15)",
                       title="Jumlah Muatan"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1, font_size=11),
        )
        st.plotly_chart(fig_pcl, use_container_width=True)

        # ── Tabel Detail ─────────────────────────────────────────────────────
        st.markdown("#### Tabel Detail per Pencacah")

        if "total_data" in agg_pcl.columns:
            agg_pcl["_sum"]    = agg_pcl[status_cols].sum(axis=1)
            agg_pcl["Selisih"] = agg_pcl["total_data"] - agg_pcl["_sum"]
            agg_pcl = agg_pcl.drop(columns=["_sum"])

        # Sisipkan kolom Pengawas jika ada
        if "nama_pml" in df.columns:
            pml_map = df.groupby("nama_pcl")["nama_pml"].first().reset_index()
            agg_pcl = agg_pcl.merge(pml_map, on="nama_pcl", how="left")
            col_order = ["nama_pcl", "nama_pml"] + [
                c for c in agg_pcl.columns if c not in ["nama_pcl", "nama_pml"]
            ]
            agg_pcl = agg_pcl[col_order]
            # Urutkan tabel detail berdasarkan nama Pengawas, lalu nama Pencacah
            agg_pcl = agg_pcl.sort_values(["nama_pml", "nama_pcl"], na_position="last").reset_index(drop=True)

        # Rename kolom untuk tampilan
        disp_pcl = rename_display(agg_pcl)
        if "Selisih" in agg_pcl.columns:
                    bad = disp_pcl[disp_pcl.get("Selisih", 0) != 0] if "Selisih" in disp_pcl.columns else pd.DataFrame()
                    if not bad.empty:
                        with st.expander(f"⚠️ {len(bad)} pencacah punya selisih total_data vs jumlah status"):
                            st.dataframe(bad, use_container_width=True, hide_index=True)
        col_cfg_pcl = {}

        if "Progress (%)" in disp_pcl.columns:
            col_cfg_pcl["Progress (%)"] = st.column_config.ProgressColumn(
                "Progress (%)",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            )

        st.caption("💡 Klik salah satu baris di tabel untuk melihat rekap progress harian pencacah tersebut.")

        try:
            pcl_table_event = st.dataframe(
                disp_pcl,
                use_container_width=True,
                column_config=col_cfg_pcl,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="pcl_detail_table",
            )
            selected_rows = (
                list(pcl_table_event.selection.rows)
                if pcl_table_event and pcl_table_event.selection else []
            )
        except TypeError:
            st.dataframe(
                disp_pcl,
                use_container_width=True,
                column_config=col_cfg_pcl,
                hide_index=True,
            )
            selected_rows = []
            st.warning(
                "⚠️ Fitur klik-baris butuh Streamlit versi lebih baru. "
                "Jalankan `pip install -U streamlit` lalu restart dashboard untuk mengaktifkannya."
            )

        if selected_rows and "Nama Pencacah" in disp_pcl.columns:
            clicked_name = disp_pcl.iloc[selected_rows[0]]["Nama Pencacah"]
            st.divider()
            render_pencacah_daily_panel(clicked_name)

        # =========================
        # Download Rekap Pencacah
        # =========================
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
            label="📊 Download Rekap Pencacah (XLSX)",
            data=to_excel(disp_pcl),
            file_name=f"rekap_pencacah_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_pcl"
        )
       



# ══════════════════════════════════════════════════════════════════════════════
# TAB — Target Harian & Forecasting
# ══════════════════════════════════════════════════════════════════════════════
with tab_target:
    st.subheader("Target Harian & Proyeksi Penyelesaian")

    if "nama_pcl" not in df.columns or "total_data" not in df.columns:
        st.warning("Kolom `nama_pcl` atau `total_data` tidak ditemukan dalam data.")
    else:
        today_wit = datetime.now(ZoneInfo("Asia/Jayapura")).date()

        # ── Jadwal milestone (bisa diubah langsung di tabel ini) ────────────
        st.markdown("#### 🗓️ Jadwal Milestone SE2026")
        st.caption("Sesuaikan tanggal/persentase di sini kalau ada perubahan jadwal resmi.")

        if "milestone_editor_data" not in st.session_state:
            st.session_state["milestone_editor_data"] = pd.DataFrame([
                {"Tanggal": date(2026, 6, 30), "Target (%)": 25},
                {"Tanggal": date(2026, 7, 14), "Target (%)": 40},
                {"Tanggal": date(2026, 7, 31), "Target (%)": 75},
                {"Tanggal": date(2026, 8, 31), "Target (%)": 100},
            ])

        milestone_df = st.data_editor(
            st.session_state["milestone_editor_data"],
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="milestone_editor",
            column_config={
                "Tanggal": st.column_config.DateColumn("Tanggal", format="DD MMM YYYY"),
                "Target (%)": st.column_config.NumberColumn("Target (%)", min_value=0, max_value=100, step=1),
            },
        )
        milestone_df = milestone_df.dropna().copy()
        milestone_df["Tanggal"] = pd.to_datetime(milestone_df["Tanggal"]).dt.date
        milestone_df = milestone_df.sort_values("Tanggal").reset_index(drop=True)

        if milestone_df.empty:
            st.warning("Belum ada milestone yang diatur.")
        else:
            # ── Progress keseluruhan saat ini ───────────────────────────────
            total_data_all = float(df["total_data"].sum())
            total_done_all = float(df[done_cols].sum().sum()) if done_cols else 0.0
            pct_now = (total_done_all / total_data_all * 100) if total_data_all else 0.0

            # ── Klasifikasi tiap milestone: tercapai / belum / akan datang ──
            status_rows = []
            next_milestone = None
            for _, m in milestone_df.iterrows():
                m_date, m_pct = m["Tanggal"], m["Target (%)"]
                if m_date < today_wit:
                    status = "✅ Tercapai" if pct_now >= m_pct else "⚠️ Belum tercapai (lewat tanggal)"
                elif m_date == today_wit:
                    status = "✅ Tercapai" if pct_now >= m_pct else "🔴 Target hari ini"
                else:
                    status = "⏳ Akan datang"
                    if next_milestone is None and pct_now < m_pct:
                        next_milestone = (m_date, m_pct)
                status_rows.append({
                    "Tanggal": m_date,
                    "Target (%)": m_pct,
                    "Target Muatan": int(total_data_all * m_pct / 100),
                    "Status": status,
                })
            milestone_status_df = pd.DataFrame(status_rows)

            st.dataframe(milestone_status_df, use_container_width=True, hide_index=True)

            # ── Kurva rencana vs posisi sekarang ─────────────────────────────
            fig_curve = go.Figure()
            fig_curve.add_trace(go.Scatter(
                x=pd.to_datetime(milestone_status_df["Tanggal"]),
                y=milestone_status_df["Target (%)"],
                mode="lines+markers+text",
                name="Target Rencana",
                text=[f"{p}%" for p in milestone_status_df["Target (%)"]],
                textposition="top center",
                line=dict(color="#0ea5e9", width=3, dash="dot"),
                marker=dict(size=9, color="#0ea5e9"),
            ))
            fig_curve.add_trace(go.Scatter(
                x=[pd.to_datetime(today_wit)],
                y=[pct_now],
                mode="markers+text",
                name="Posisi Sekarang",
                text=[f"{pct_now:.1f}%"],
                textposition="bottom center",
                marker=dict(size=15, color="#14b8a6", symbol="diamond"),
            ))
            fig_curve.update_layout(
                **styled_chart_layout(height=340),
                xaxis=dict(title="Tanggal", showgrid=False),
                yaxis=dict(title="Progress (%)", range=[0, 108], showgrid=True,
                           gridcolor="rgba(100,116,139,0.15)"),
                legend=dict(orientation="h", y=1.15),
            )
            st.plotly_chart(fig_curve, use_container_width=True)

            st.divider()

            # ── Target harian menuju milestone aktif (terdekat & belum tercapai) ──
            if next_milestone is None:
                st.success("🎉 Progress saat ini sudah memenuhi seluruh milestone yang terjadwal!")
            else:
                target_date, target_pct = next_milestone
                days_left = max((target_date - today_wit).days, 1)

                st.info(
                    f"🎯 Milestone aktif: **{target_pct}%** pada **{target_date:%d %b %Y}** "
                    f"({days_left} hari lagi)"
                )

                target_value_team = total_data_all * target_pct / 100
                sisa_team = max(target_value_team - total_done_all, 0)
                target_harian_team = int(np.ceil(sisa_team / days_left))

                tk1, tk2, tk3, tk4 = st.columns(4)
                tk1.metric("Progress Saat Ini", f"{pct_now:.1f}%")
                tk2.metric("Target Milestone", f"{target_pct:.0f}%")
                tk3.metric("Hari Tersisa", f"{days_left} hari")
                tk4.metric("Target Harian", f"{target_harian_team:,}/hari")

                st.divider()

                # ── Per pencacah, menuju milestone aktif yang sama ──────────
                agg_t = df.groupby("nama_pcl")[status_cols + ["total_data"]].sum().reset_index()
                agg_t["Selesai"] = agg_t[done_cols].sum(axis=1) if done_cols else 0
                agg_t["Progress (%)"] = (
                    agg_t["Selesai"] / agg_t["total_data"].replace(0, pd.NA) * 100
                ).round(1).fillna(0)
                agg_t["Target Muatan (Milestone)"] = (
                    agg_t["total_data"] * target_pct / 100
                ).round().astype(int)
                agg_t["Sisa ke Milestone"] = (
                    agg_t["Target Muatan (Milestone)"] - agg_t["Selesai"]
                ).clip(lower=0)
                agg_t["Target Harian"] = np.ceil(agg_t["Sisa ke Milestone"] / days_left).astype(int)
                agg_t = agg_t.sort_values("Target Harian", ascending=False)

                # ── Bar chart target harian per pencacah ────────────────────
                top_n_target = 30
                chart_t = agg_t[agg_t["Sisa ke Milestone"] > 0].head(top_n_target)

                if chart_t.empty:
                    st.success("🎉 Semua pencacah sudah mencapai target milestone aktif ini.")
                else:
                    fig_target = px.bar(
                        chart_t.sort_values("Target Harian"),
                        x="Target Harian", y="nama_pcl",
                        orientation="h",
                        text="Target Harian",
                        color="Target Harian",
                        color_continuous_scale=["#14b8a6", "#f59e0b", "#ef4444"],
                        template=PLOT_TEMPLATE,
                        labels={"nama_pcl": ""},
                    )
                    fig_target.update_traces(textposition="outside", textfont_size=10)
                    fig_target.update_layout(
                        **styled_chart_layout(
                            height=max(400, len(chart_t) * 22),
                            coloraxis_showscale=False,
                        ),
                        xaxis=dict(showgrid=True, gridcolor="rgba(100,116,139,0.15)",
                                   title="Target (per hari)"),
                        yaxis=dict(showgrid=False),
                    )
                    st.plotly_chart(fig_target, use_container_width=True)
                    if (agg_t["Sisa ke Milestone"] > 0).sum() > top_n_target:
                        st.caption(
                            f"Menampilkan {top_n_target} pencacah dengan target harian tertinggi "
                            f"dari {(agg_t['Sisa ke Milestone'] > 0).sum()} pencacah yang masih punya sisa."
                        )

                st.divider()

                # ── Tabel detail ─────────────────────────────────────────────
                st.markdown("#### Tabel Target Harian per Pencacah")

                cols_show = ["nama_pcl", "total_data", "Selesai", "Progress (%)",
                             "Target Muatan (Milestone)", "Sisa ke Milestone", "Target Harian"]
                if "nama_pml" in df.columns:
                    pml_map = df.groupby("nama_pcl")["nama_pml"].first().reset_index()
                    agg_t = agg_t.merge(pml_map, on="nama_pcl", how="left")
                    cols_show.insert(1, "nama_pml")

                disp_t = rename_display(agg_t[cols_show])

                st.dataframe(
                    disp_t,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Progress (%)": st.column_config.ProgressColumn(
                            "Progress (%)", min_value=0, max_value=100, format="%.1f%%"
                        ),
                        "Target Harian": st.column_config.NumberColumn(
                            "Target Harian (per hari)",
                            help=f"Jumlah muatan yang harus diselesaikan per hari agar mencapai "
                                 f"{target_pct:.0f}% pada {target_date:%d %b %Y}",
                        ),
                    },
                )

                st.download_button(
                    "📥 Download Target Harian (XLSX)",
                    data=to_excel(disp_t),
                    file_name=f"target_harian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_target",
                )

                st.caption(
                    f"💡 **Target Harian** = ({target_pct:.0f}% × Total Muatan − Selesai) ÷ Hari Tersisa "
                    f"ke milestone aktif, dibulatkan ke atas. Milestone yang sudah terlewati tanggalnya "
                    f"otomatis dilewati kalau progress sudah memenuhi targetnya."
                )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Per Desa
# ══════════════════════════════════════════════════════════════════════════════
with tab_desa:
    st.subheader("Rekap Per Desa / Kelurahan")

    if "nmdesa" not in df.columns:
        st.warning("Kolom `nmdesa` tidak ditemukan dalam data.")
    else:
        grp_keys   = [c for c in ["nmkec", "nmdesa"] if c in df.columns]
        agg_cols_d = status_cols + (["total_data"] if "total_data" in df.columns else [])
        agg_desa   = df.groupby(grp_keys)[agg_cols_d].sum().reset_index()

        if "total_data" in agg_desa.columns and done_cols:
            agg_desa["Progress (%)"] = (
                agg_desa[done_cols].sum(axis=1)
                / agg_desa["total_data"].replace(0, pd.NA) * 100
            ).round(1).fillna(0)
            agg_desa = agg_desa.sort_values("Progress (%)", ascending=False)

        if "nama_pcl" in df.columns:
            pcl_per_desa = df.groupby(grp_keys)["nama_pcl"].nunique().reset_index(
                name="Jumlah PCL")
            agg_desa = agg_desa.merge(pcl_per_desa, on=grp_keys, how="left")

        # ── Bar progress per desa ────────────────────────────────────────────
        if "Progress (%)" in agg_desa.columns:
            top_desa = 40
            hm_df    = agg_desa.head(top_desa).copy()

            label_col = "nmdesa"
            if "nmkec" in hm_df.columns:
                hm_df["_label"] = hm_df["nmkec"] + " · " + hm_df["nmdesa"]
                label_col = "_label"

            hover_extra = {}
            if "total_data" in hm_df.columns:
                hover_extra["total_data"] = True
            if "Jumlah PCL" in hm_df.columns:
                hover_extra["Jumlah PCL"] = True

            fig_desa_bar = px.bar(
                hm_df.sort_values("Progress (%)"),
                x="Progress (%)", y=label_col,
                orientation="h",
                text="Progress (%)",
                color="Progress (%)",
                color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
                range_color=[0, 100],
                template=PLOT_TEMPLATE,
                labels={label_col: ""},
                hover_data=hover_extra if hover_extra else None,
            )
            fig_desa_bar.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                textfont_size=10,
            )
            fig_desa_bar.update_layout(
                **styled_chart_layout(
                    height=max(400, len(hm_df) * 22),
                    coloraxis_showscale=False,
                ),
                xaxis=dict(range=[0, 115], showgrid=False),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_desa_bar, use_container_width=True)

        # ── Proporsi per Kecamatan ───────────────────────────────────────────
        if len(agg_desa) <= 80 and "nmkec" in agg_desa.columns and done_cols:
            st.markdown("#### Proporsi Penyelesaian per Kecamatan")
            kec_agg = df.groupby("nmkec")[agg_cols_d].sum().reset_index()
            if "total_data" in kec_agg.columns:
                kec_agg["Selesai"] = kec_agg[done_cols].sum(axis=1)
                kec_agg["Belum"]   = kec_agg["total_data"] - kec_agg["Selesai"]
                kec_melt = kec_agg.melt(
                    id_vars="nmkec", value_vars=["Selesai", "Belum"],
                    var_name="Status", value_name="Jumlah"
                )
                fig_kec = px.bar(
                    kec_melt, x="nmkec", y="Jumlah", color="Status",
                    color_discrete_map={"Selesai": "#14b8a6",
                                        "Belum": "rgba(51,65,85,0.8)"},
                    barmode="stack",
                    template=PLOT_TEMPLATE,
                    labels={"nmkec": "Kecamatan"},
                )
                fig_kec.update_layout(
                    **styled_chart_layout(height=340),
                    xaxis=dict(tickangle=-30, showgrid=False),
                    yaxis=dict(showgrid=True,
                               gridcolor="rgba(100,116,139,0.15)"),
                    legend=dict(orientation="h", y=1.05),
                )
                st.plotly_chart(fig_kec, use_container_width=True)

        # ── Tabel Desa ────────────────────────────────────────────────────────
        st.markdown("#### Tabel Detail per Desa")

        disp_desa = agg_desa.drop(columns=["_label"], errors="ignore")
        disp_desa = rename_display(disp_desa)

        col_cfg_desa = {}
        if "Progress (%)" in disp_desa.columns:
            col_cfg_desa["Progress (%)"] = st.column_config.ProgressColumn(
                "Progress (%)", min_value=0, max_value=100, format="%.1f%%"
            )

        st.dataframe(disp_desa, use_container_width=True,
                     column_config=col_cfg_desa, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Data Mentah
# ══════════════════════════════════════════════════════════════════════════════
with tab_raw:
    st.subheader("Data Mentah")

    all_cols  = df.columns.tolist()
    show_cols = st.multiselect(
        "Tampilkan kolom", all_cols,
        default=all_cols[:min(15, len(all_cols))],
        key="raw_cols",
    )

    view_df = rename_display(df[show_cols] if show_cols else df)

    st.dataframe(view_df, use_container_width=True, hide_index=True)

# ============================
# Footer (muncul di semua halaman)
# ============================
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 8px;
    font-size: 13px;
    color: gray;
    background-color: white;
    border-top: 1px solid #ddd;
    z-index: 999;
}
</style>

<div class="footer">
    © 2026 Zulfaa Dwi Oktavian (BPS Kota Ambon)
</div>
""", unsafe_allow_html=True)