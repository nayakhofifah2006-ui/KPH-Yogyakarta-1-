import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Dashboard Valuasi Ekonomi KPH Yogyakarta",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

col1, col2 = st.columns([1,4])

with col1:
    st.image("logo_unisba.png", width=130)

with col2:
    st.title("Dashboard Valuasi Ekonomi KPH Yogyakarta")

    st.write("### Dosen Pengampu")
    st.write("Yuhka Sundaya")

    st.write("### Kelompok 10")
    st.write("""
    - Naya Khofifah Aulia (10090224012)

    - Yulia Yuthika (10090224013)

    - Melvina Putri Aprilianti (10090224029)
    """)

st.divider()

# ==========================================
# SIDEBAR
# ==========================================

menu = st.sidebar.radio(
    "Menu Dashboard",
    [
        "Dashboard Utama",
        "Profil KPH",
        "Tegakan",
        "Nilai Ekonomi",
        "Trade Off",
        "PES",
        "HHBK"
    ]
)

# ==========================================
# DASHBOARD UTAMA
# ==========================================

if menu == "Dashboard Utama":

    st.header("Dashboard Utama")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Luas KPH", "16.358 Ha")
    col2.metric("Jenis Tegakan", "8")
    col3.metric("Komoditas HHBK", "4")
    col4.metric("TEV", "Rp120 Miliar")

    st.divider()

    st.subheader("Pendahuluan")

    st.write("""
    Kesatuan Pengelolaan Hutan (KPH) Yogyakarta merupakan unit pengelolaan hutan
    di Daerah Istimewa Yogyakarta yang tersebar di Kabupaten Gunungkidul,
    Bantul, dan Kulon Progo.

    KPH Yogyakarta memiliki fungsi produksi, perlindungan, konservasi,
    jasa lingkungan, serta pemberdayaan masyarakat.

    Selain menghasilkan kayu, kawasan hutan juga memberikan manfaat berupa
    jasa air, cadangan karbon, wisata alam, hasil hutan bukan kayu,
    dan perlindungan biodiversitas.

    Dalam ekonomi sumber daya hutan, seluruh manfaat tersebut dianalisis
    menggunakan pendekatan Total Economic Value (TEV).
    """)

    st.subheader("Indikator Pengelolaan Hutan")

    st.write("Keberlanjutan")
    st.progress(85)

    st.write("Jasa Lingkungan")
    st.progress(80)

    st.write("Kontribusi Ekonomi")
    st.progress(75)

    indikator = pd.DataFrame({
        "Komponen": [
            "Kayu",
            "HHBK",
            "Wisata",
            "Karbon",
            "Jasa Air"
        ],
        "Kontribusi": [
            40,
            20,
            15,
            15,
            10
        ]
    })

    fig = px.line(
        indikator,
        x="Komponen",
        y="Kontribusi",
        markers=True,
        title="Kontribusi Ekonomi Hutan"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PROFIL KPH
# ==========================================

elif menu == "Profil KPH":

    kawasan = pd.read_csv("kawasan_hutan.csv")
    fungsi = pd.read_csv("fungsi_hutan.csv")

    st.header("Profil KPH")

    col1, col2, col3 = st.columns(3)

    col1.metric("Luas KPH", "16.358 Ha")
    col2.metric("Hutan Produksi", "13.411 Ha")
    col3.metric("Hutan Lindung", "2.312 Ha")

    fig1 = px.bar(
        kawasan,
        x="Kabupaten",
        y="Luas_Ha",
        title="Sebaran Kawasan Hutan"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.write("""
    Gunungkidul merupakan wilayah dengan kawasan hutan terbesar sehingga
    memiliki potensi ekonomi dan jasa lingkungan yang tinggi.
    """)

    fig2 = px.pie(
        fungsi,
        names="Fungsi_Hutan",
        values="Luas_Ha",
        title="Fungsi Kawasan Hutan"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# TEGAKAN
# ==========================================

elif menu == "Tegakan":

    tegakan = pd.read_csv("jenis_tegakan.csv")

    st.header("Analisis Tegakan")

    # ==========================
    # KPI
    # ==========================

    total_tegakan = tegakan["Luas_Ha"].sum()

    jenis_pohon = len(tegakan)

    dominan = tegakan.loc[
        tegakan["Luas_Ha"].idxmax(),
        "Jenis_Tegakan"
    ]

    hhbk = tegakan["HHBK"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Tegakan",
        f"{total_tegakan:,.0f} Ha"
    )

    col2.metric(
        "Jenis Pohon",
        jenis_pohon
    )

    col3.metric(
        "Tegakan Dominan",
        dominan
    )

    col4.metric(
        "Potensi HHBK",
        hhbk
    )

    st.divider()

    pohon = st.selectbox(
        "Pilih Jenis Pohon",
        tegakan["Jenis_Tegakan"]
    )

    data = tegakan[
        tegakan["Jenis_Tegakan"] == pohon
    ]

    luas = float(data["Luas_Ha"].iloc[0])
    harga = int(data["Harga_m3"].iloc[0])
    umur = int(data["Umur_Tebang"].iloc[0])
    produksi = int(data["Produksi"].iloc[0])
    potensi = data["HHBK"].iloc[0]

    st.subheader(f"Informasi Tegakan {pohon}")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Luas", f"{luas:.1f} Ha")
    c2.metric("Umur Tebang", f"{umur} Tahun")
    c3.metric("Produksi", f"{produksi} m³")
    c4.metric("Potensi HHBK", potensi)

    st.divider()

    fig = px.bar(
        tegakan,
        x="Jenis_Tegakan",
        y="Luas_Ha",
        color="Jenis_Tegakan",
        title="Sebaran Luas Tegakan"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Simulasi Pemanenan")

    panen = st.slider(
        "Persentase Pemanenan (%)",
        0,
        100,
        20
    )

    produksi_panen = produksi * panen / 100

    pendapatan = produksi_panen * harga

    col1, col2 = st.columns(2)

    col1.metric(
        "Produksi Panen",
        f"{produksi_panen:.0f} m³"
    )

    col2.metric(
        "Pendapatan",
        f"Rp {pendapatan:,.0f}"
    )

    simulasi = pd.DataFrame({
        "Komponen": [
            "Produksi",
            "Pendapatan"
        ],
        "Nilai": [
            produksi_panen,
            pendapatan/1000000
        ]
    })

    fig2 = px.bar(
        simulasi,
        x="Komponen",
        y="Nilai",
        color="Komponen",
        title="Simulasi Ekonomi Tegakan"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.write(f"""
    Tegakan **{pohon}** memiliki luas sekitar **{luas:.1f} hektar**
    dengan umur tebang sekitar **{umur} tahun**.

    Potensi hasil hutan bukan kayu dari tegakan ini berupa
    **{potensi}**.

    Dengan tingkat pemanenan sebesar **{panen}%**, estimasi
    pendapatan yang dihasilkan mencapai sekitar
    **Rp {pendapatan:,.0f}**.
    """)

# ==========================================
# NILAI EKONOMI
# ==========================================

    # ==========================================
# NILAI EKONOMI
# ==========================================

elif menu == "Nilai Ekonomi":

    st.header("Total Economic Value (TEV)")

    st.write("""
    Total Economic Value merupakan pendekatan yang digunakan
    untuk menghitung seluruh manfaat ekonomi yang diperoleh
    dari kawasan hutan, baik manfaat langsung maupun tidak langsung.
    """)

    tev = pd.DataFrame({
        "Komponen": [
            "Kayu",
            "HHBK",
            "Wisata Alam",
            "Jasa Air",
            "Karbon",
            "Biodiversitas"
        ],
        "Nilai": [
            45,
            15,
            10,
            12,
            10,
            8
        ]
    })

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "TEV Total",
        "Rp120 Miliar"
    )

    col2.metric(
        "Nilai Kayu",
        "Rp54 M"
    )

    col3.metric(
        "Jasa Lingkungan",
        "Rp36 M"
    )

    col4.metric(
        "Nilai Non-Kayu",
        "Rp30 M"
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "Diagram",
        "Tabel",
        "Analisis"
    ])

    # ====================
    # TAB DIAGRAM
    # ====================

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            fig1 = px.pie(
                tev,
                names="Komponen",
                values="Nilai",
                title="Komposisi TEV"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        with col2:

            fig2 = px.bar(
                tev,
                x="Komponen",
                y="Nilai",
                color="Komponen",
                title="Nilai Ekonomi"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    # ====================
    # TAB TABEL
    # ====================

    with tab2:

        tev["Nilai (Miliar Rp)"] = tev["Nilai"]

        st.dataframe(
            tev,
            use_container_width=True
        )

    # ====================
    # TAB ANALISIS
    # ====================

    with tab3:

        st.write("""
        Kayu masih menjadi komponen ekonomi terbesar
        dalam KPH Yogyakarta.

        Namun demikian, jasa lingkungan seperti karbon,
        air, wisata, dan biodiversitas memberikan kontribusi
        yang cukup besar terhadap nilai ekonomi total.

        Hal ini menunjukkan bahwa pengelolaan hutan tidak
        hanya berorientasi pada produksi kayu tetapi juga
        pada keberlanjutan ekosistem.
        """)

    st.divider()

    st.subheader("Kontribusi Manfaat Hutan")

    st.progress(90)
    st.write("Manfaat Langsung")

    st.progress(75)
    st.write("Jasa Lingkungan")

    st.progress(80)
    st.write("Keberlanjutan")

    st.divider()

    st.subheader("Simulasi Perubahan TEV")

    persentase = st.slider(
        "Kerusakan Hutan (Luas/Ha)",
        0,
        50,
        10,
        format="%d%%"
    )

    tev_baru = 120 * (1 - persentase / 100)

    col1, col2 = st.columns(2)

    col1.metric(
        "Kerusakan",
        f"{persentase}%"
    )

    col2.metric(
        "TEV Baru",
        f"Rp {tev_baru:.1f} Miliar"
    )

    st.metric(
        "TEV Setelah Degradasi",
        f"Rp {tev_baru:.1f} Miliar",
        f"-{persentase}%"
    )

    if persentase <= 10:

        st.success(
            "Kondisi hutan masih relatif baik."
        )

    elif persentase <= 30:

        st.warning(
            "Nilai ekonomi mulai menurun."
        )

    else:

        st.error(
            "Degradasi tinggi menyebabkan kehilangan manfaat ekonomi."
        )

    st.divider()

    st.subheader("Nilai per Hektar")

    luas_kph = 16358

    nilai_per_ha = 120000000000 / luas_kph

    st.metric(
        "Nilai Ekonomi per Hektar",
        f"Rp {nilai_per_ha:,.0f}"
    )

    st.info("""
    Nilai ekonomi per hektar menunjukkan besarnya manfaat
    ekonomi yang dihasilkan setiap hektar kawasan hutan.
    """)

# ==========================================
# TRADE OFF
# ==========================================

elif menu == "Trade Off":

    st.header("Analisis Trade Off Penggunaan Lahan")

    konversi = st.slider(
        "Luas Hutan yang Dikonversi (Ha)",
        0,
        500,
        100,
        25
    )

    nilai_kayu = max(45 - (konversi * 0.05), 0)
    nilai_karbon = max(20 - (konversi * 0.03), 0)
    nilai_air = max(15 - (konversi * 0.02), 0)
    nilai_wisata = max(10 - (konversi * 0.015), 0)

    pendapatan_sawit = konversi * 0.10

    tradeoff = pd.DataFrame({
        "Komponen": [
            "Kayu",
            "Karbon",
            "Air",
            "Wisata",
            "Sawit"
        ],
        "Nilai": [
            nilai_kayu,
            nilai_karbon,
            nilai_air,
            nilai_wisata,
            pendapatan_sawit
        ]
    })

    fig = px.bar(
        tradeoff,
        x="Komponen",
        y="Nilai",
        color="Komponen",
        title="Trade Off Konversi Hutan Menjadi Sawit"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        "Pendapatan Sawit",
        f"Rp {pendapatan_sawit:.2f} Miliar"
    )

    if konversi <= 100:

        st.success(
            "Konversi lahan masih relatif rendah."
        )

    elif konversi <= 300:

        st.warning(
            "Terjadi trade off antara pendapatan sawit dan jasa lingkungan."
        )

    else:

        st.error(
            "Konversi tinggi menyebabkan kehilangan jasa lingkungan yang signifikan."
        )

elif menu == "PES":

    st.header("Payment for Ecosystem Services (PES)")

    st.write("""
    Payment for Ecosystem Services (PES) merupakan mekanisme
    pembayaran kepada pihak yang menjaga hutan agar jasa
    ekosistem tetap tersedia. Simulasi ini menunjukkan potensi
    insentif yang diterima berdasarkan luas kawasan yang dilindungi.
    """)

    # =====================
    # KPI
    # =====================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Jenis Jasa",
        "4"
    )

    col2.metric(
        "Luas Maksimum",
        "5.000 Ha"
    )

    col3.metric(
        "Tarif Tertinggi",
        "Rp1.000.000"
    )

    col4.metric(
        "Skema PES",
        "Aktif"
    )

    st.divider()

    # =====================
    # PILIH JASA
    # =====================

    jasa = st.selectbox(
        "Pilih Jenis Jasa Ekosistem",
        [
            "Penyimpanan Karbon",
            "Penyedia Air",
            "Ekowisata",
            "Keanekaragaman Hayati"
        ]
    )

    luas = st.slider(
        "Luas Hutan yang Dilindungi (Ha)",
        50,
        5000,
        500,
        50
    )

    tarif = st.selectbox(
        "Tarif Insentif (Rp/Ha/Tahun)",
        [
            500000,
            750000,
            1000000
        ]
    )

    # =====================
    # PERHITUNGAN
    # =====================

    total_pes = luas * tarif

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Luas Hutan",
        f"{luas:,} Ha"
    )

    col2.metric(
        "Tarif",
        f"Rp {tarif:,.0f}"
    )

    col3.metric(
        "Nilai PES",
        f"Rp {total_pes:,.0f}"
    )

    st.divider()

    # =====================
    # GRAFIK
    # =====================

    simulasi = pd.DataFrame({
        "Komponen": [
            "Luas (Ha)",
            "Tarif (ribu Rp)",
            "PES (juta Rp)"
        ],
        "Nilai": [
            luas,
            tarif/1000,
            total_pes/1000000
        ]
    })

    fig = px.bar(
        simulasi,
        x="Komponen",
        y="Nilai",
        color="Komponen",
        title="Simulasi Payment for Ecosystem Services"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================
    # INDEKS PES
    # =====================

    st.subheader("Indeks Keberlanjutan PES")

    indeks = min(int((luas / 5000) * 100), 100)

    st.progress(indeks)

    st.write(
        f"Indeks perlindungan kawasan: {indeks}%"
    )

    # =====================
    # ANALISIS
    # =====================

    st.subheader("Interpretasi Ekonomi")

    st.info(f"""
    Jika kawasan hutan yang dilindungi mencapai **{luas:,} hektar**
    dengan tarif insentif sebesar **Rp {tarif:,.0f}/ha/tahun**,
    maka potensi nilai Payment for Ecosystem Services mencapai
    **Rp {total_pes:,.0f} per tahun**.
    """)

    if jasa == "Penyimpanan Karbon":

        st.success("""
        Perlindungan karbon berkontribusi terhadap mitigasi
        perubahan iklim dan perdagangan karbon.
        """)

    elif jasa == "Penyedia Air":

        st.success("""
        Perlindungan daerah tangkapan air menjaga ketersediaan
        air bagi masyarakat dan sektor pertanian.
        """)

    elif jasa == "Ekowisata":

        st.success("""
        Jasa wisata memberikan manfaat ekonomi melalui kunjungan
        wisata dan kegiatan rekreasi alam.
        """)

    else:

        st.success("""
        Perlindungan keanekaragaman hayati mendukung konservasi
        flora dan fauna serta menjaga stabilitas ekosistem.
        """)

        st.divider()

    st.subheader("Perbandingan Potensi Jasa Ekosistem")

    if jasa == "Penyimpanan Karbon":

        dasar = {
            "Karbon":95,
            "Air":75,
            "Ekowisata":60,
            "Biodiversitas":90
        }

    elif jasa == "Penyedia Air":

        dasar = {
            "Karbon":70,
            "Air":98,
            "Ekowisata":65,
            "Biodiversitas":80
        }

    elif jasa == "Ekowisata":

        dasar = {
            "Karbon":65,
            "Air":75,
            "Ekowisata":98,
            "Biodiversitas":82
        }

    else:

        dasar = {
            "Karbon":85,
            "Air":80,
            "Ekowisata":72,
            "Biodiversitas":98
        }

    skala = luas / 5000

    karbon = round(dasar["Karbon"] * skala,1)
    air = round(dasar["Air"] * skala,1)
    wisata = round(dasar["Ekowisata"] * skala,1)
    biodiversitas = round(dasar["Biodiversitas"] * skala,1)

    fig2 = go.Figure()

    # Radar Potensi Maksimum
    fig2.add_trace(
        go.Scatterpolar(
            r=[100, 100, 100, 100],
            theta=[
                "Karbon",
                "Air",
                "Ekowisata",
                "Biodiversitas"
            ],
            fill=None,
            name="Potensi Maksimum"
        )
    )

    # Radar Hasil Simulasi
    fig2.add_trace(
        go.Scatterpolar(
            r=[
                karbon,
                air,
                wisata,
                biodiversitas
            ],
            theta=[
                "Karbon",
                "Air",
                "Ekowisata",
                "Biodiversitas"
            ],
            fill="toself",
            name="Hasil Simulasi"
        )
    )

    fig2.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Perbandingan Potensi Jasa Ekosistem"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # KPI

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Karbon",
        f"{karbon}"
    )

    col2.metric(
        "Air",
        f"{air}"
    )

    col3.metric(
        "Ekowisata",
        f"{wisata}"
    )

    col4.metric(
        "Biodiversitas",
        f"{biodiversitas}"
    )

    # Indeks

    indeks = (karbon + air + wisata + biodiversitas) / 4

    fig3 = go.Figure(go.Indicator(

        mode="gauge+number",

        value=indeks,

        title={"text":"Indeks Potensi PES"},

        gauge={

            "axis":{"range":[0,100]},

            "bar":{"color":"green"},

            "steps":[

                {"range":[0,40],"color":"#f4cccc"},

                {"range":[40,70],"color":"#ffe599"},

                {"range":[70,100],"color":"#b6d7a8"}

            ]

        }

    ))

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    if indeks >= 85:

        st.success("Potensi jasa ekosistem sangat tinggi.")

    elif indeks >= 70:

        st.info("Potensi jasa ekosistem tinggi.")

    elif indeks >= 50:

        st.warning("Potensi jasa ekosistem sedang.")

    else:

        st.error("Potensi jasa ekosistem rendah.")

# ==========================================
# HHBK
# ==========================================

elif menu == "HHBK":

    st.header("Hasil Hutan Bukan Kayu (HHBK)")

    st.write("""
    Hasil Hutan Bukan Kayu (HHBK) merupakan hasil hutan selain kayu
    yang dapat dimanfaatkan secara berkelanjutan tanpa menebang pohon.
    Dashboard ini menyajikan simulasi potensi ekonomi beberapa
    komoditas HHBK di KPH Yogyakarta.
    """)

    # ======================
    # KPI
    # ======================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Komoditas", "4")
    col2.metric("Nilai HHBK", "Rp15 Miliar")
    col3.metric("Kontribusi TEV", "12,5%")
    col4.metric("Status", "Berkelanjutan")

    st.divider()

    # ======================
    # PILIH KOMODITAS
    # ======================

    komoditas = st.selectbox(
        "Pilih Komoditas HHBK",
        [
            "Madu Hutan",
            "Getah Akasia",
            "Minyak Kayu Putih",
            "Bambu"
        ]
    )

   if komoditas == "Madu Hutan":

    produksi_ha = 20
    harga = 120000
    satuan = "kg"

    radar = [98, 75, 92, 65]

   elif komoditas == "Getah Akasia":

    produksi_ha = 450
    harga = 9000
    satuan = "kg"

    radar = [60, 95, 80, 72]

   elif komoditas == "Minyak Kayu Putih":

    produksi_ha = 18
    harga = 250000
    satuan = "Liter"

    radar = [82, 70, 65, 98]

   else:

    produksi_ha = 200
    harga = 15000
    satuan = "Batang"

    radar = [72, 98, 88, 60]

    luas = st.slider(
        "Luas Pemanfaatan (Ha)",
        10,
        500,
        100
    )

    produksi = produksi_ha * luas

    pendapatan = produksi * harga

    # ======================
    # KPI HASIL
    # ======================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Produksi",
        f"{produksi:,.0f} {satuan}"
    )

    col2.metric(
        "Harga",
        f"Rp {harga:,.0f}/{satuan}"
    )

    col3.metric(
        "Pendapatan",
        f"Rp {pendapatan:,.0f}"
    )

    st.divider()

    # ======================
    # GRAFIK
    # ======================

    simulasi = pd.DataFrame({

        "Komponen":[
            "Produksi",
            "Harga (Ribu)",
            "Pendapatan (Juta)"
        ],

        "Nilai":[
            produksi,
            harga/1000,
            pendapatan/1000000
        ]

    })

    fig = px.bar(
        simulasi,
        x="Komponen",
        y="Nilai",
        color="Komponen",
        title=f"Simulasi Ekonomi {komoditas}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ======================
    # RADAR
    # ======================

    fig2 = go.Figure()

fig2.add_trace(
    go.Scatterpolar(
        r=[100,100,100,100,100],
        theta=[
            "Nilai Ekonomi",
            "Keberlanjutan",
            "Produksi",
            "Permintaan",
            "Nilai Ekonomi"
        ],
        line=dict(color="lightgray", dash="dot"),
        name="Maksimum"
    )
)

fig2.add_trace(
    go.Scatterpolar(
        r=radar + [radar[0]],
        theta=[
            "Nilai Ekonomi",
            "Keberlanjutan",
            "Produksi",
            "Permintaan",
            "Nilai Ekonomi"
        ],
        fill="toself",
        name=komoditas
    )
)

fig2.update_layout(

    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0,100]
        )
    ),

    showlegend=True,

    title=f"Potensi {komoditas}"

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

    # ======================
    # GAUGE
    # ======================

    indeks = sum(radar)/4

    fig3 = go.Figure(
        go.Indicator(

            mode="gauge+number",

            value=indeks,

            title={"text":"Indeks Potensi HHBK"},

            gauge={

                "axis":{"range":[0,100]},

                "steps":[

                    {"range":[0,40],"color":"#f4cccc"},

                    {"range":[40,70],"color":"#ffe599"},

                    {"range":[70,100],"color":"#b6d7a8"}

                ]

            }

        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ======================
    # INTERPRETASI
    # ======================

    st.subheader("Interpretasi Ekonomi")

    st.info(f"""
    Dengan luas pemanfaatan **{luas} hektar**, komoditas
    **{komoditas}** menghasilkan sekitar
    **{produksi:,.0f} {satuan}**.

    Dengan harga rata-rata
    **Rp {harga:,.0f}/{satuan}**, maka nilai ekonomi
    yang dihasilkan mencapai
    **Rp {pendapatan:,.0f}**.

    Pemanfaatan HHBK memberikan manfaat ekonomi bagi
    masyarakat tanpa mengurangi tutupan hutan sehingga
    mendukung pengelolaan hutan secara berkelanjutan.
    """)
