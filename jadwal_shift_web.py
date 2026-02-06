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
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* ===== SEMUA TEXT PUTIH ===== */
    p, span, div, label, .stMarkdown, .stAlert, .stWarning, .stSuccess, .stInfo, .stError {
        color: #FFFFFF !important;
    }
    
    /* ===== HEADER PUTIH ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* ===== INPUT FIELD ===== */
    /* Text Input */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* Selectbox (Grup Shift & Jabatan) */
    .stSelectbox>div>div>div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Selectbox dropdown options */
    .stSelectbox>div>div>div[role="listbox"]>div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Selectbox text yang terpilih */
    .stSelectbox>div>div>div[data-baseweb="select"]>div {
        color: #000000 !important;
    }
    
    /* ===== BUTTON SUBMIT ===== */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        font-weight: bold !important;
    }
    
    /* Button hover effect */
    .stButton>button:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background-color: #222222 !important;
        color: #FFFFFF !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border-color: #FFFFFF !important;
    }
    
    /* ===== CUSTOM BOXES ===== */
    .info-box {
        border: 2px solid #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #111111;
    }
    
    .warning-box {
        border: 2px solid #FF4444;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #111111;
    }
    
    /* ===== FIX UNTUK DROPDOWN OPTIONS ===== */
    /* Background dropdown saat dibuka */
    div[data-baseweb="select"] div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
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
    
    /* ===== LABEL PUTIH ===== */
    label {
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* ===== STREAMLIT COMPONENTS ===== */
    /* Radio button */
    .stRadio > div {
        color: #FFFFFF !important;
    }
    
    /* Checkbox */
    .stCheckbox > label {
        color: #FFFFFF !important;
    }
    
    /* Code block */
    code {
        background-color: #222222 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
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
