import streamlit as st
import os
from PIL import Image
import sys

# ===== KONFIGURASI HALAMAN =====
st.set_page_config(
    page_title="Jadwal Shift 4G Mainline - PMI",
    page_icon="📅",
    layout="wide"
)

# ===== CSS HITAM-PUTIH LENGKAP =====
st.markdown("""
<style>
    /* ===== BACKGROUND UTAMA ===== */
    .stApp, .main, .block-container {
        background-color: #000000 !important;
    }
    
    /* ===== SEMUA TEXT PUTIH (default) ===== */
    p, span, div, label, .stMarkdown, .stAlert, .stWarning, .stSuccess, .stInfo, .stError {
        color: #FFFFFF !important;
    }
    
    /* ===== HEADER PUTIH ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* ===== TEXT INPUT (Nama) - Putih Background, Hitam Text ===== */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* ===== SELECTBOX (Grup Shift & Jabatan) ===== */
    /* Container utama selectbox */
    .stSelectbox > div {
        background-color: #000000 !important;
    }
    
    /* Area pilihan yang ditampilkan */
    div[data-baseweb="select"] > div:first-child {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Text dalam selectbox yang ditampilkan */
    div[data-baseweb="select"] > div:first-child > div {
        color: #000000 !important;
    }
    
    /* Dropdown menu saat dibuka */
    div[role="listbox"] {
        background-color: #000000 !important;
    }
    
    /* Option dalam dropdown */
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Text dalam option */
    div[role="option"] span {
        color: #000000 !important;
    }
    
    /* Placeholder text */
    div[data-baseweb="select"] > div:first-child > div:last-child {
        color: #666666 !important; /* Abu-abu untuk placeholder */
    }
    
    /* Icon dropdown */
    div[data-baseweb="select"] svg {
        fill: #000000 !important;
    }
    
    /* ===== BUTTON SUBMIT ===== */
    /* Tombol utama */
    .stButton > button {
        background-color: #000000 !important;  /* Background hitam */
        color: #FFFFFF !important;             /* Tulisan putih */
        border: 2px solid #FFFFFF !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    /* Button hover effect */
    .stButton > button:hover {
        background-color: #FFFFFF !important;  /* Background putih saat hover */
        color: #000000 !important;             /* Tulisan hitam saat hover */
        border: 2px solid #FFFFFF !important;
    }
    
    /* ===== LABEL PUTIH ===== */
    /* Label untuk semua input */
    label, .stTextInput label, .stSelectbox label {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* ===== CUSTOM BOXES ===== */
    .info-box {
        border: 2px solid #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #111111;
    }
    
    .info-box h3 {
        color: #FFFFFF !important;
    }
    
    .warning-box {
        border: 2px solid #FF4444;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #111111;
    }
    
    /* ===== ALERT/MESSAGE ===== */
    .stAlert, .stError, .stWarning, .stSuccess, .stInfo {
        color: #FFFFFF !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border-color: #FFFFFF !important;
    }
    
    /* ===== FIX UNTUK SEMUA ELEMEN DROPDOWN ===== */
    /* Target semua elemen dalam dropdown */
    [data-baseweb="select"] [role="listbox"] [role="option"] {
        background-color: white !important;
        color: black !important;
    }
    
    [data-baseweb="select"] [role="listbox"] [role="option"]:hover {
        background-color: #f0f0f0 !important;
        color: black !important;
    }
    
    /* Text yang dipilih di dropdown */
    [data-baseweb="select"] [aria-activedescendant] {
        color: black !important;
    }
    
    /* ===== OVERRIDE COLOR PICKER ===== */
    /* Memastikan semua text dalam selectbox hitam */
    .stSelectbox div[data-baseweb="select"] {
        color: #000000 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div {
        color: #000000 !important;
    }
    
    /* ===== FORCE BLACK TEXT IN SELECTED OPTIONS ===== */
    div[data-baseweb="select"] > div > div {
        color: #000000 !important;
    }
    
    /* ===== FORCE BUTTON STYLING ===== */
    button[data-testid="baseButton-primary"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
    }
    
    button[data-testid="baseButton-primary"]:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

class ShiftSchedulerWeb:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.script_dir = os.path.dirname(sys.executable)
        else:
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        os.chdir(self.script_dir)
        
        self.ls_data = {"LL": "Rendy", "PL": "Zainul", "ML": "Luqman"}
        self.lc_data = {
            "A": "Luqman kecil",
            "B": "Akmad Nurhadi", 
            "C": "Super Priyanto",
            "D": "Rahmad"
        }
        self.positions = ["Protech", "Mekanik", "Managerial"]
        self.groups = ["A", "B", "C", "D"]
    
    def get_image_files(self):
        files = []
        for target in ["SS januari.png", "SS mei.png", "SS september.png", "SS libur.png"]:
            if os.path.exists(target):
                files.append(target)
        return files
    
    def run(self):
        # SIDEBAR
        with st.sidebar:
            st.markdown("## 🔧 INFORMASI")
            st.write(f"**Folder:** {self.script_dir}")
            images = self.get_image_files()
            st.markdown(f"**File:** {len(images)} ditemukan")
            for img in images:
                st.write(f"• {img}")
        
        # HEADER
        st.markdown("<h1 style='text-align: center;'>📅 JADWAL SHIFT 4G MAINLINE</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>PHILIP MORRIS INTERNATIONAL</h3>", unsafe_allow_html=True)
        
        # FORM INPUT - GUNAKAN SELECTBOX BIASA DENGAN CSS YANG SUDAH DIPERBAIKI
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown("### 📝 INPUT DATA")
        
        col1, col2, col3 = st.columns(3)
        with col1: 
            name = st.text_input("NAMA LENGKAP")
        
        with col2: 
            # Menggunakan selectbox biasa dengan CSS fix
            group = st.selectbox("GRUP SHIFT", ["PILIH"] + self.groups)
        
        with col3: 
            position = st.selectbox("JABATAN", ["PILIH"] + self.positions)
        
        # Alternatif: Jika masih bermasalah, ganti dengan radio button
        # Uncomment kode di bawah jika selectbox masih bermasalah di mobile
        # st.markdown("**GRUP SHIFT**")
        # group = st.radio("Pilih Grup:", self.groups, horizontal=True, key="group")
        # st.markdown("**JABATAN**")
        # position = st.radio("Pilih Jabatan:", ["Protech", "Mekanik", "Managerial"], key="position")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2: 
            submit = st.button("🚀 TAMPILKAN JADWAL", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submit:
            if not name or group == "PILIH" or position == "PILIH":
                st.error("❌ HARAP LENGKAPI SEMUA FIELD!")
                return
            
            if position == "Managerial":
                st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
                st.markdown("## ⚠️ AKSES DITOLAK")
                st.markdown("### Jabatan anda terlalu tinggi untuk program sederhana ini")
                st.markdown("</div>", unsafe_allow_html=True)
                return
            
            if position in ["Protech", "Mekanik"]:
                self.show_schedule(name, group, position)
    
    def show_schedule(self, name, group, position):
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown(f"### 👤 {name} | 🏷️ Grup {group} | 💼 {position}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        lc_name = self.lc_data.get(group, "Tidak Diketahui")
        st.markdown(f"### 🎯 LINE COORDINATOR (LC) GRUP {group}:")
        st.markdown(f"# {lc_name}")
        
        st.markdown("### 👥 LEADERSHIP TEAM")
        cols = st.columns(3)
        for idx, (role, ls_name) in enumerate(self.ls_data.items()):
            with cols[idx]:
                st.markdown(f"""
                <div style='border: 2px solid white; padding: 15px; border-radius: 10px;'>
                    <h4 style='text-align: center;'>{role}</h4>
                    <h3 style='text-align: center;'>{ls_name}</h3>
                </div>
                """, unsafe_allow_html=True)
        
        # GAMBAR
        st.markdown("### 📋 JADWAL SHIFT 2026")
        image_files = self.get_image_files()
        for img_file in image_files:
            try:
                img = Image.open(img_file)
                st.markdown(f"#### {img_file}")
                st.image(img)
                st.markdown("---")
            except:
                st.error(f"Gagal memuat {img_file}")

if __name__ == "__main__":
    app = ShiftSchedulerWeb()
    app.run()
