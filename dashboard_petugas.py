import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from config_se2026 import LATEST_FILE

# ─────────────────────────────────────────────────────────────────────────────
# Konfigurasi halaman — sidebar disembunyikan sepenuhnya
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

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sembunyikan sidebar toggle & sidebar sepenuhnya */
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Main area full-width */
.main .block-container {
    background: #0f172a;
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

/* ── KPI Cards ── */
div[data-testid="stMetric"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    position: relative;
    overflow: hidden;
}
div[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #14b8a6, #0ea5e9);
    border-radius: 12px 0 0 12px;
}
div[data-testid="stMetric"] label {
    color: #94a3b8 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #6ee7b7 !important;
    font-size: 0.8rem !important;
}

/* ── Section headers ── */
h2, h3 {
    color: #e2e8f0 !important;
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
    color: #64748b !important;
    border-bottom: 2px solid transparent !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #14b8a6 !important;
    border-bottom-color: #14b8a6 !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border: 1px solid #1e293b;
    border-radius: 12px;
    overflow: hidden;
}
iframe { border-radius: 12px !important; }

/* ── Divider ── */
hr {
    border-color: #1e293b !important;
    margin: 1.5rem 0 !important;
}

/* ── Expander ── */
details {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
}
details summary { color: #94a3b8 !important; font-size: 0.85rem !important; }

/* ── Caption ── */
small, .stCaption { color: #64748b !important; font-size: 0.78rem !important; }

/* ── Alert ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 4px !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] button {
    background: #14b8a6 !important;
    color: #0f172a !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.45rem 1rem !important;
    font-size: 0.82rem !important;
}
div[data-testid="stDownloadButton"] button:hover { background: #0d9488 !important; }

/* ── Plotly chart container ── */
.stPlotlyChart {
    border: 1px solid #1e293b;
    border-radius: 12px;
    overflow: hidden;
    background: #1e293b;
}

/* ── Filter bar ── */
.filter-bar {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 0.75rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

/* ── Badge update ── */
.badge-update {
    background: #0d3d2e;
    border: 1px solid #10b981;
    border-radius: 20px;
    padding: 3px 12px;
    color: #6ee7b7;
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Auto-refresh (tanpa sidebar warning)
# ─────────────────────────────────────────────────────────────────────────────
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60 * 1000, key="auto_refresh_dashboard")
except ImportError:
    pass  # Nonaktif diam-diam, tidak perlu pesan sidebar

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

DONE_KEYWORDS     = ["APPROVED", "SUBMITTED"]
NOT_DONE_KEYWORDS = ["OPEN", "DRAFT"]

PLOT_TEMPLATE = "plotly_dark"
PLOT_BG       = "rgba(30,41,59,1)"
PAPER_BG      = "rgba(30,41,59,1)"
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

# ─────────────────────────────────────────────────────────────────────────────
# Load data otomatis dari LATEST_FILE
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
# Header — termasuk badge waktu update
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; align-items:center; justify-content:space-between;
            flex-wrap:wrap; gap:10px; margin-bottom:0.8rem;">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="background:linear-gradient(135deg,#14b8a6,#0ea5e9);
                    width:44px;height:44px;border-radius:12px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.4rem;flex-shrink:0;">📊</div>
        <div>
            <h1 style="margin:0;color:#f1f5f9;font-size:1.55rem;font-weight:700;
                       letter-spacing:-0.02em;line-height:1.2;">
                SE2026 — Monitoring Status Pencacahan
            </h1>
            <p style="margin:0;color:#64748b;font-size:0.8rem;">
                Progress per PCL / Desa · Data otomatis dari scraping FASIH
            </p>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:8px;">
        <span class="badge-update">🟢 Diperbarui: {last_updated}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Deteksi kolom
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
# Filter bar — inline di halaman utama (bukan sidebar)
# ─────────────────────────────────────────────────────────────────────────────
with st.container():
    f1, f2, f3 = st.columns([2, 3, 1])

    with f1:
        if "nmkec" in df_raw.columns:
            all_kec = sorted(df_raw["nmkec"].dropna().unique().tolist())
            sel_kec = st.multiselect(
                "🏙️ Filter Kecamatan", all_kec,
                default=[], placeholder="Semua kecamatan", label_visibility="collapsed"
            )
        else:
            sel_kec = []
            st.caption("(kolom kecamatan tidak tersedia)")

    with f2:
        if "nama_pcl" in df_raw.columns:
            all_pcl = sorted(df_raw["nama_pcl"].dropna().unique().tolist())
            sel_pcl = st.multiselect(
                "👤 Filter PCL", all_pcl,
                default=[], placeholder="👤 Cari nama PCL...", label_visibility="collapsed"
            )
        else:
            sel_pcl = []
            st.caption("(kolom nama_pcl tidak tersedia)")

    with f3:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Unduh CSV",
            df_raw.to_csv(index=False).encode("utf-8"),
            file_name="se2026_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

# Terapkan filter
df = df_raw.copy()
if sel_kec and "nmkec" in df.columns:
    df = df[df["nmkec"].isin(sel_kec)]
if sel_pcl and "nama_pcl" in df.columns:
    df = df[df["nama_pcl"].isin(sel_pcl)]

if len(df) < len(df_raw):
    st.caption(f"Filter aktif · Menampilkan **{len(df):,}** dari **{len(df_raw):,}** baris")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Hitung KPI
# ─────────────────────────────────────────────────────────────────────────────
n_pcl    = df["nama_pcl"].nunique() if "nama_pcl" in df.columns else 0
n_pml    = df["nama_pml"].nunique() if "nama_pml" in df.columns else 0
n_desa   = df["nmdesa"].nunique()   if "nmdesa"   in df.columns else 0
total_data = int(df["total_data"].sum()) if "total_data" in df.columns else int(df[status_cols].sum().sum())

done_cols     = [c for c in status_cols if any(k in c.upper() for k in DONE_KEYWORDS)]
not_done_cols = [c for c in status_cols if any(k in c.upper() for k in NOT_DONE_KEYWORDS)]
rejected_cols = [c for c in status_cols if "REJECTED" in c.upper()]

total_done     = int(df[done_cols].sum().sum())      if done_cols     else 0
total_open     = int(df[not_done_cols].sum().sum())  if not_done_cols else 0
total_rejected = int(df[rejected_cols].sum().sum())  if rejected_cols else 0
pct_done       = total_done / total_data * 100        if total_data    else 0

# ─────────────────────────────────────────────────────────────────────────────
# KPI Cards
# ─────────────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total PCL",      f"{n_pcl:,}")
k2.metric("Total PML",      f"{n_pml:,}")
k3.metric("Total Desa",     f"{n_desa:,}")
k4.metric("Total Muatan",   f"{total_data:,}")
k5.metric("Selesai (Done)", f"{total_done:,}", f"{pct_done:.1f}%")
k6.metric("Ditolak",        f"{total_rejected:,}",
          f"{total_rejected/total_data*100:.1f}%" if total_data else "0%")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TABS UTAMA
# ─────────────────────────────────────────────────────────────────────────────
tab_overview, tab_pcl, tab_desa, tab_raw = st.tabs([
    "📈 Distribusi Status",
    "👤 Per PCL (Pencacah)",
    "🏘️ Per Desa",
    "🗃️ Data Mentah",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Distribusi Status Keseluruhan
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
            text=[f"{v:,}" for v in status_totals.values],
            color=status_totals.index,
            color_discrete_sequence=TEAL_PALETTE,
            template=PLOT_TEMPLATE,
        )
        fig_bar.update_traces(textposition="outside", textfont_size=11)
        fig_bar.update_layout(
            **styled_chart_layout(showlegend=False, height=360),
            xaxis=dict(showgrid=True, gridcolor="#1e293b"),
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
        fig_pie.update_layout(**styled_chart_layout(height=360, showlegend=True,
                              legend=dict(orientation="v", x=1.05)))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct_done,
            number={"suffix": "%", "font": {"size": 36, "color": "#14b8a6",
                                            "family": "JetBrains Mono"}},
            title={"text": "Overall Progress", "font": {"color": "#94a3b8", "size": 13}},
            gauge={
                "axis":      {"range": [0, 100], "tickcolor": "#475569",
                              "tickfont": {"color": "#64748b", "size": 10}},
                "bar":       {"color": "#14b8a6", "thickness": 0.25},
                "bgcolor":   "#0f172a",
                "bordercolor": "#334155",
                "steps": [
                    {"range": [0,  50], "color": "#1e293b"},
                    {"range": [50, 80], "color": "#172554"},
                    {"range": [80, 100],"color": "#0d3d2e"},
                ],
                "threshold": {"line": {"color": "#0ea5e9", "width": 3},
                              "thickness": 0.8, "value": pct_done},
            },
        ))
        fig_gauge.update_layout(**styled_chart_layout(height=360))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # ── Tren harian (jika ada scraped_at) ────────────────────────────────────
    if "scraped_at" in df.columns:
        st.markdown("---")
        st.subheader("Ringkasan Snapshot")
        try:
            df["_date"] = pd.to_datetime(df["scraped_at"]).dt.date
            trend = df.groupby("_date")[status_cols].sum().reset_index()
            trend = trend.rename(columns={"_date": "Tanggal"})
            if done_cols:
                fig_trend = px.area(
                    trend, x="Tanggal", y=done_cols,
                    color_discrete_sequence=TEAL_PALETTE,
                    template=PLOT_TEMPLATE,
                    labels={"value": "Jumlah", "variable": "Status"},
                )
                fig_trend.update_layout(**styled_chart_layout(height=260))
                st.plotly_chart(fig_trend, use_container_width=True)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Per PCL (Pencacah)
# ══════════════════════════════════════════════════════════════════════════════
with tab_pcl:
    st.subheader("Monitoring Per PCL / Pencacah")

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

        # ── Stacked bar per PCL ──────────────────────────────────────────────
        max_show  = 30
        chart_pcl = agg_pcl.head(max_show)
        if len(agg_pcl) > max_show:
            st.caption(
                f"Grafik menampilkan {max_show} PCL teratas dari {len(agg_pcl)} total. "
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
            xaxis=dict(tickangle=-40, showgrid=False, tickfont_size=10),
            yaxis=dict(showgrid=True, gridcolor="#1e293b", title="Jumlah Usaha"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1, font_size=11),
        )
        st.plotly_chart(fig_pcl, use_container_width=True)

        # ── Ranking Progress PCL ─────────────────────────────────────────────
        if "Progress (%)" in agg_pcl.columns:
            st.markdown("#### Ranking Progress PCL")
            top_n  = st.slider("Tampilkan top-N PCL", 5, min(50, len(agg_pcl)),
                               min(20, len(agg_pcl)), key="pcl_topn")
            rank_df = agg_pcl.nlargest(top_n, "Progress (%)")[
                ["nama_pcl", "total_data", "Progress (%)"] + done_cols
            ].reset_index(drop=True)

            fig_rank = px.bar(
                rank_df.sort_values("Progress (%)"),
                x="Progress (%)", y="nama_pcl",
                orientation="h",
                text="Progress (%)",
                color="Progress (%)",
                color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
                range_color=[0, 100],
                template=PLOT_TEMPLATE,
                labels={"nama_pcl": ""},
            )
            fig_rank.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                textfont_size=10,
            )
            fig_rank.update_layout(
                **styled_chart_layout(height=max(300, top_n * 22),
                                      coloraxis_showscale=False),
                xaxis=dict(range=[0, 115], showgrid=False),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_rank, use_container_width=True)

        # ── Tabel Detail per PCL ─────────────────────────────────────────────
        st.markdown("#### Tabel Detail per PCL")

        if "total_data" in agg_pcl.columns:
            agg_pcl["_sum"]   = agg_pcl[status_cols].sum(axis=1)
            agg_pcl["Selisih"] = agg_pcl["total_data"] - agg_pcl["_sum"]
            agg_pcl = agg_pcl.drop(columns=["_sum"])

        col_cfg_pcl = {}
        if "Progress (%)" in agg_pcl.columns:
            col_cfg_pcl["Progress (%)"] = st.column_config.ProgressColumn(
                "Progress (%)", min_value=0, max_value=100, format="%.1f%%"
            )

        # Sisipkan kolom PML jika ada
        if "nama_pml" in df.columns:
            pml_map = df.groupby("nama_pcl")["nama_pml"].first().reset_index()
            agg_pcl = agg_pcl.merge(pml_map, on="nama_pcl", how="left")
            col_order = ["nama_pcl", "nama_pml"] + [
                c for c in agg_pcl.columns if c not in ["nama_pcl", "nama_pml"]
            ]
            agg_pcl = agg_pcl[col_order]

        st.dataframe(agg_pcl, use_container_width=True,
                     column_config=col_cfg_pcl, hide_index=True)

        if "Selisih" in agg_pcl.columns:
            bad = agg_pcl[agg_pcl["Selisih"] != 0]
            if not bad.empty:
                with st.expander(f"⚠️ {len(bad)} PCL punya selisih total_data vs jumlah status"):
                    st.dataframe(bad, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Unduh Rekap Per PCL (CSV)",
            agg_pcl.to_csv(index=False).encode("utf-8"),
            file_name="se2026_rekap_pcl.csv",
            mime="text/csv",
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

        # Jumlah PCL per desa
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
                hover_data={
                    "total_data": True,
                    **({ "Jumlah PCL": True } if "Jumlah PCL" in hm_df.columns else {}),
                },
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

        # ── Proporsi Done vs Belum per Kecamatan ────────────────────────────
        if len(agg_desa) <= 80 and "nmkec" in agg_desa.columns and done_cols:
            st.markdown("#### Proporsi Penyelesaian per Kecamatan")
            kec_agg = df.groupby("nmkec")[agg_cols_d].sum().reset_index()
            if "total_data" in kec_agg.columns:
                kec_agg["Done"]  = kec_agg[done_cols].sum(axis=1)
                kec_agg["Belum"] = kec_agg["total_data"] - kec_agg["Done"]
                kec_melt = kec_agg.melt(
                    id_vars="nmkec", value_vars=["Done", "Belum"],
                    var_name="Status", value_name="Jumlah"
                )
                fig_kec = px.bar(
                    kec_melt, x="nmkec", y="Jumlah", color="Status",
                    color_discrete_map={"Done": "#14b8a6", "Belum": "#334155"},
                    barmode="stack",
                    template=PLOT_TEMPLATE,
                    labels={"nmkec": "Kecamatan"},
                )
                fig_kec.update_layout(
                    **styled_chart_layout(height=340),
                    xaxis=dict(tickangle=-30, showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#1e293b"),
                    legend=dict(orientation="h", y=1.05),
                )
                st.plotly_chart(fig_kec, use_container_width=True)

        # ── Tabel Desa ────────────────────────────────────────────────────────
        st.markdown("#### Tabel Detail per Desa")

        col_cfg_desa = {}
        if "Progress (%)" in agg_desa.columns:
            col_cfg_desa["Progress (%)"] = st.column_config.ProgressColumn(
                "Progress (%)", min_value=0, max_value=100, format="%.1f%%"
            )

        disp_desa = agg_desa.drop(columns=["_label"], errors="ignore")
        st.dataframe(disp_desa, use_container_width=True,
                     column_config=col_cfg_desa, hide_index=True)

        st.download_button(
            "⬇️ Unduh Rekap Per Desa (CSV)",
            disp_desa.to_csv(index=False).encode("utf-8"),
            file_name="se2026_rekap_desa.csv",
            mime="text/csv",
        )


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
    view_df = df[show_cols] if show_cols else df
    st.dataframe(view_df, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Unduh Data Terfilter (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        file_name="se2026_filtered.csv",
        mime="text/csv",
    )