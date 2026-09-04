import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Visualisasi Jadwal",
    page_icon="📊",
    layout="wide"
)

# ===========================
# Helper
# ===========================

urutan_hari = {
    "Senin": 1,
    "Selasa": 2,
    "Rabu": 3,
    "Kamis": 4,
    "Jumat": 5
}

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
# Sidebar
# ===========================

st.sidebar.title("Filter Condition")

all_hari = sorted(
    df['Hari'].unique()
)

hari = st.sidebar.multiselect(
    "Program Studi",
    all_hari,
    default=[
        "Senin",
        "Selasa",
        "Rabu",
        "Kamis",
        "Jumat"
    ],
)

all_ruang = sorted(
    df["Ruang"].unique()
)

selected_ruang = st.sidebar.multiselect(
    "Ruangan",
    all_ruang,
    default=all_ruang
)

# ===========================
# Filter
# ===========================

filtered = df.copy()

filtered = filtered[
    filtered["Hari"].isin(
        hari
    )
]

filtered = filtered[
    filtered["Ruang"].isin(
        selected_ruang
    )
]

filtered = filtered.sort_values(
    "jam_mulai_dt"
)

filtered["urutan_hari"] = filtered["Hari"].map(urutan_hari)

# ===========================
# Header
# ===========================

st.title("📊 Daftar Ruang Kelas Semester Gasal 2026-2027 ")

st.caption(
    "Daftar lengkap penggunaan ruang kelas."
)

# ===========================
# Jadwal Lengkap
# ===========================

jadwal_lengkap = filtered.sort_values(by="No", ascending=True)

st.header("📄 Jadwal Lengkap")

st.dataframe(
    jadwal_lengkap,
    column_order=[
       "No",
        "Ruang",
        "Kapasitas",
        "Peserta",
        "Kode MK",
        "Kurikulum",
        "Nama MK",
        "Nama Kelas",
        "Dosen",
        "Waktu",
        "Hari",
        "Jam",
        "Jam Masuk",
        "Jam Keluar",
        "Program Studi"

    ],
    use_container_width=True,
    hide_index=True
)

# ===========================
# Daftar Ruang
# ===========================

st.header("📄 Daftar Ruang Kelas")

grouped_ruang = filtered.groupby("Ruang")

for ruang, group in grouped_ruang:

    st.subheader(f"🏫 Ruang {ruang}")

    group = group.sort_values(["urutan_hari", "jam_mulai_dt"])

    st.dataframe(
        group[
            [
                "Hari",
                "Jam",
                "Kode MK",
                "Nama MK",
                "Nama Kelas",
                "Dosen",
                "Program Studi"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()