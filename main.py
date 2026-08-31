import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Jadwal Kelas 2026 - 2027 Gasal",
    page_icon="📅",
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

today = hari_map[datetime.today().strftime("%A")]

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
        .str.replace(".", ":", regex=False)
    )

    df["Jam Keluar"] = (
        df["Jam"]
        .str.split(" - ")
        .str[1]
        .str.replace(".", ":", regex=False)
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

st.sidebar.title("⚙ Filter")

hari = st.sidebar.selectbox(
    "Hari",
    sorted(df["Hari"].unique()),
    index=list(
        sorted(df["Hari"].unique())
    ).index(today)
)

all_prodi = sorted(
    df["Program Studi"].unique()
)

selected_prodi = st.sidebar.multiselect(
    "Program Studi",
    all_prodi,
    default=[
        "S1 - Ilmu Komputer",
        "S1 - Sistem Informasi",
        "S1 - Kecerdasan Artifisial",
        "S1 Kls Internasional - Ilmu Komputer",
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

search = st.sidebar.text_input(
    "Cari Mata Kuliah"
)

# ===========================
# Filter
# ===========================

filtered = df.copy()

filtered = filtered[
    filtered["Hari"] == hari
]

filtered = filtered[
    filtered["Program Studi"].isin(
        selected_prodi
    )
]

filtered = filtered[
    filtered["Ruang"].isin(
        selected_ruang
    )
]

if search:

    filtered = filtered[
        filtered["Nama MK"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

filtered = filtered.sort_values(
    "jam_mulai_dt"
)

# ===========================
# Header
# ===========================

st.title("📅 Dashboard Jadwal Kelas")

st.caption(
    f"Jadwal Hari **{hari}**"
)

# ===========================
# Metrics
# ===========================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Jumlah Kelas",
    len(filtered)
)

c2.metric(
    "Ruangan Aktif",
    filtered["Ruang"].nunique()
)

c3.metric(
    "Jumlah Mata Kuliah",
    filtered["Nama MK"].nunique()
)

c4.metric(
    "Program Studi",
    filtered["Program Studi"].nunique()
)

# ===========================
# Jadwal Per Jam
# ===========================

st.header("🕒 Jadwal Per Jam")

grouped = filtered.groupby(
    "Jam Masuk"
)

for jam, group in grouped:

    group = group.sort_values(
        "Ruang"
    )

    with st.expander(f"{jam}"):

        st.dataframe(
            group[
                [
                    "Ruang",
                    "Nama MK",
                    "Dosen",
                    "Program Studi",
                    "Jam Masuk",
                    "Jam Keluar",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

st.divider()

# ===========================
# Jadwal Lengkap
# ===========================

st.header("📄 Jadwal Lengkap")

st.dataframe(
    filtered,
    column_order=[
        "No.",
        "Ruang",
        "Kap.",
        "Pst.",
        "Kode MK",
        "Nama MK",
        "Dosen",
        "Hari",
        "Jam",
        "Program Studi"
    ],
    use_container_width=True,
    hide_index=True
)