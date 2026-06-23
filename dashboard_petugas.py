import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from config_se2026 import LATEST_FILE

# -----------------------------------------------------------------------------
# Konfigurasi halaman
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SE2026 - Monitoring Status Pencacahan",
    page_icon="📊",
    layout="wide",
)

# Auto-refresh halaman tiap 60 detik supaya data terbaru dari scraping
# otomatis muncul tanpa perlu reload manual.
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60 * 1000, key="auto_refresh_dashboard")
except ImportError:
    st.sidebar.warning(
        "Auto-refresh nonaktif. Install dengan: `pip install streamlit-autorefresh`"
    )

IDENTITY_COLS = ["userId", "username", "email", "role", "regionCode", "total_data", "scraped_at"]

# Kata kunci untuk klasifikasi status "sudah diproses" vs "belum/ditolak"
# dipakai untuk hitung Progress (%) - silakan sesuaikan kalau ada status baru
DONE_KEYWORDS = ["APPROVED", "SUBMITTED"]
NOT_DONE_KEYWORDS = ["OPEN", "DRAFT"]


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.title("📊 Dashboard Monitoring Status Pencacahan — SE2026")
st.caption(
    "Monitoring progress pencatatan usaha per PPL/Pencacah berdasarkan status "
    "OPEN, DRAFT, SUBMITTED BY PENCACAH, APPROVED BY PENGAWAS, REJECTED, dll."
)

# -----------------------------------------------------------------------------
# Sumber data: otomatis dari hasil scraping terbaru, atau upload manual
# -----------------------------------------------------------------------------
use_manual_upload = st.sidebar.toggle(
    "Upload file manual (override)", value=False,
    help="Aktifkan kalau mau pakai file lain selain hasil scraping otomatis",
)

if use_manual_upload:
    uploaded = st.file_uploader(
        "Upload file data (hasil scraping FASIH) — Excel (.xlsx/.xls) atau CSV",
        type=["xlsx", "xls", "csv"],
    )
    if uploaded is None:
        st.info("⬆️ Silakan upload file data progress pencacahan untuk mulai.")
        st.stop()
    df_raw = load_data(uploaded)
    last_updated = "(file upload manual)"
else:
    if not os.path.exists(LATEST_FILE):
        st.warning(
            f"Belum ada hasil scraping di `{LATEST_FILE}`. "
            "Jalankan `scrapping_sls.py` dulu, atau aktifkan upload manual di sidebar."
        )
        st.stop()
    file_mtime = os.path.getmtime(LATEST_FILE)
    df_raw = load_data(LATEST_FILE, cache_key=file_mtime)
    last_updated = datetime.fromtimestamp(
    file_mtime,
    tz=ZoneInfo("Asia/Jayapura")
).strftime("%Y-%m-%d %H:%M:%S WIT")

st.sidebar.success(f"🟢 Data terakhir diperbarui:\n{last_updated}")

status_cols = detect_status_cols(df_raw)
numeric_cols = status_cols + (["total_data"] if "total_data" in df_raw.columns else [])
df_raw = to_numeric_safe(df_raw, numeric_cols)

if not status_cols:
    st.error(
        "Tidak ada kolom status yang terdeteksi. Pastikan file punya kolom "
        "selain: " + ", ".join(IDENTITY_COLS)
    )
    st.stop()

df = df_raw.copy()

# -----------------------------------------------------------------------------
# KPI Cards
# -----------------------------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

n_ppl = df["username"].nunique() if "username" in df.columns else len(df)
total_data = int(df["total_data"].sum()) if "total_data" in df.columns else int(df[status_cols].sum().sum())

col1.metric("Total PPL", f"{n_ppl:,}")
col2.metric("Total Muatan", f"{total_data:,}")

for col, keyword, label in [(col3, "OPEN", "OPEN"), (col4, "APPROVED", "APPROVED"), (col5, "REJECTED", "REJECTED")]:
    matching = [c for c in status_cols if keyword in c.upper()]
    val = int(df[matching].sum().sum()) if matching else 0
    pct = f"{val / total_data * 100:.1f}%" if total_data > 0 else "0%"
    col.metric(label, f"{val:,}", pct)

st.divider()

# -----------------------------------------------------------------------------
# Distribusi status keseluruhan
# -----------------------------------------------------------------------------
st.subheader("Distribusi Status Keseluruhan")

status_totals = df[status_cols].sum().sort_values(ascending=False)
status_totals = status_totals[status_totals > 0]

c1, c2 = st.columns([2, 1])
with c1:
    fig_bar = px.bar(
        x=status_totals.values,
        y=status_totals.index,
        orientation="h",
        labels={"x": "Jumlah Usaha", "y": ""},
        text=status_totals.values,
        color=status_totals.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(showlegend=False, height=420, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    fig_pie = px.pie(
        values=status_totals.values,
        names=status_totals.index,
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_pie.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# Progress per PPL (stacked bar)
# -----------------------------------------------------------------------------
st.subheader("Progress per PPL/Pencacah")

group_col = "nama_pcl" if "nama_pcl" in df.columns else df.columns[0]
agg_cols = status_cols + (["total_data"] if "total_data" in df.columns else [])
agg = df.groupby(group_col)[agg_cols].sum().reset_index()
agg = agg.sort_values("total_data", ascending=False) if "total_data" in agg.columns else agg

max_ppl_chart = 30
chart_df = agg.head(max_ppl_chart)
if len(agg) > max_ppl_chart:
    st.caption(f"Menampilkan {max_ppl_chart} PPL dengan data terbanyak (dari total {len(agg)} PPL). Lihat tabel di bawah untuk data lengkap.")

fig_stack = go.Figure()
for c in status_cols:
    fig_stack.add_trace(go.Bar(name=c, x=chart_df[group_col], y=chart_df[c]))
fig_stack.update_layout(
    barmode="stack",
    height=460,
    xaxis_tickangle=-45,
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_stack, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# Tabel detail per PPL + progress %
# -----------------------------------------------------------------------------
st.subheader("Tabel Detail per PPL")

display_df = agg.copy()
done_cols = [c for c in status_cols if any(k in c.upper() for k in DONE_KEYWORDS)]

if "total_data" in display_df.columns and done_cols:
    display_df["Progress (%)"] = (
        display_df[done_cols].sum(axis=1) / display_df["total_data"].replace(0, pd.NA) * 100
    ).round(1).fillna(0)

# Cek konsistensi data: total_data vs jumlah seluruh status
if "total_data" in display_df.columns:
    display_df["_sum_status"] = display_df[status_cols].sum(axis=1)
    display_df["Selisih"] = display_df["total_data"] - display_df["_sum_status"]
    display_df = display_df.drop(columns=["_sum_status"])

column_config = {}
if "Progress (%)" in display_df.columns:
    column_config["Progress (%)"] = st.column_config.ProgressColumn(
        "Progress (%)", min_value=0, max_value=100, format="%.1f%%"
    )

st.dataframe(display_df, use_container_width=True, column_config=column_config, hide_index=True)

inconsistent = display_df[display_df.get("Selisih", 0) != 0] if "Selisih" in display_df.columns else pd.DataFrame()
if not inconsistent.empty:
    with st.expander(f"⚠️ {len(inconsistent)} PPL dengan selisih total_data vs jumlah status (cek data)"):
        st.dataframe(inconsistent, use_container_width=True, hide_index=True)

st.divider()

# -----------------------------------------------------------------------------
# Rekap per Region Code
# -----------------------------------------------------------------------------
if "regionCode" in df.columns:
    st.subheader("Rekap per Region Code")
    region_agg = df.groupby("regionCode")[agg_cols].sum().reset_index()
    region_agg["Jumlah PPL"] = df.groupby("regionCode")[group_col].nunique().values
    st.dataframe(region_agg, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# Data mentah + download
# -----------------------------------------------------------------------------
with st.expander("Lihat Data Mentah (sesuai filter)"):
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download data terfilter (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        file_name="se2026_filtered.csv",
        mime="text/csv",
    )