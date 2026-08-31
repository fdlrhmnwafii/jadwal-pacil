import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


st.set_page_config(
    page_title="Visualisasi Jadwal",
    page_icon="📊",
    layout="wide"
)

# ===========================
# Helper
# ===========================

hari_map = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu",
}

today = hari_map[
    datetime.today().strftime("%A")
]

# ===========================
# Load CSV
# ===========================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data-bersih.csv",
        sep=";"
    )

    df["Jam Masuk"] = (
        df["Jam"]
        .str.split(" - ")
        .str[0]
        .str.replace(
            ".",
            ":",
            regex=False
        )
    )

    df["Jam Keluar"] = (
        df["Jam"]
        .str.split(" - ")
        .str[1]
        .str.replace(
            ".",
            ":",
            regex=False
        )
    )

    df["jam_mulai_dt"] = pd.to_datetime(
        df["Jam Masuk"],
        format="%H:%M"
    )

    df["jam_selesai_dt"] = pd.to_datetime(
        df["Jam Keluar"],
        format="%H:%M"
    )

    return df


df = load_data()

# ===========================
# Header
# ===========================

st.title("📊 Visualisasi Jadwal")

st.caption(
    "Visualisasi interaktif penggunaan ruang kelas."
)

# ===========================
# Filter Hari
# ===========================

hari_list = sorted(
    df["Hari"].unique()
)

hari = st.selectbox(
    "Pilih Hari",
    hari_list,
    index=hari_list.index(today)
)

# ===========================
# Filter Data
# ===========================

filtered = df[
    df["Hari"] == hari
].copy()

filtered = filtered.sort_values(
    [
        "Ruang",
        "jam_mulai_dt"
    ]
)

# ===========================
# Metrics
# ===========================

c1, c2 = st.columns(2)

c1.metric(
    "Ruangan Digunakan",
    filtered["Ruang"].nunique()
)

c2.metric(
    "Jumlah Jadwal",
    len(filtered)
)

st.divider()

# ===========================
# Gantt Chart
# ===========================

st.header(
    "🕒 Timeline Penggunaan Ruangan"
)

if filtered.empty:

    st.info(
        "Tidak terdapat jadwal pada hari yang dipilih."
    )

else:

    filtered["Label"] = (
        filtered["Kode MK"]
        + " - "
        + filtered["Nama MK"]
    )

    fig = px.timeline(
        filtered,

        x_start="jam_mulai_dt",

        x_end="jam_selesai_dt",

        y="Ruang",

        color="Kode MK",

        text="Kode MK",

        hover_data=[
            "Nama MK",
            "Nama Kelas",
            "Dosen",
            "Program Studi",
            "Jam Masuk",
            "Jam Keluar",
            "Kapasitas",
            "Peserta"
        ]
    )

    # Room paling atas
    fig.update_yaxes(
        autorange="reversed",
        title="Ruangan"
    )

    # Timeline
    fig.update_xaxes(
        title="Waktu",
        tickformat="%H:%M",
        dtick=60 * 60 * 1000,
        showgrid=True
    )

    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle"
    )

    fig.update_layout(
        height=max(
            500,
            filtered["Ruang"].nunique() * 55
        ),

        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),

        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,

        config={
            "displayModeBar": True,
            "scrollZoom": True
        }
    )