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

# ===== CSS AGGRESIF UNTUK HITAM-PUTIH =====
st.markdown("""
<style>
    /* RESET SEMUA */
    * {
        --primary-color: #000000 !important;
        --background-color: #000000 !important;
        --text-color: #FFFFFF !important;
    }
    
    /* BACKGROUND UTAMA - HITAM */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* DEFAULT TEXT - PUTIH */
    body, p, h1, h2, h3, h4, h5, h6, label, div, span {
        color: #FFFFFF !important;
    }
    
    /* ===== INPUT FIELD ===== */
    /* Text Input */
    input[type="text"], input[type="password"], input[type="email"], input[type="number"] {
        background-color: #FFFFFF !important;
        color: #000000 !important !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* ===== SELECTBOX (GRUP & JABATAN) ===== */
    /* SEMUA ELEMEN DALAM SELECTBOX HITAM DI ATAS PUTIH */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
    }
    
    div[data-baseweb="select"] * {
        color: #000000 !important !important;
    }
    
    div[data-baseweb="select"] div {
        background-color: #FFFFFF !important;
        color: #000000 !important !important;
    }
    
    /* Dropdown menu */
    div[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    
    /* Options */
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #000000 !important !important;
    }
    
    /* Selected option text */
    div[data-baseweb="select"] > div:first-child {
        color: #000000 !important !important;
    }
    
    /* ===== BUTTON SUBMIT ===== */
    /* Tombol dengan background hitam dan text putih */
    button {
        background-color: #000000 !important;
        color: #FFFFFF !important !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* Primary button (tombol submit) */
    button[data-testid="baseButton-primary"],
    button[kind="primary"] {
        background-color: #000000 !important;
        color: #FFFFFF !important !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important !important;
    }
    
    /* ===== LABEL ===== */
    /* Label harus putih */
    label[for] {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    
    /* ===== OVERRIDE STREAMLIT THEME ===== */
    /* Force black text in all inputs */
    .st-bd, .st-bc, .st-bb, .st-be {
        color: #000000 !important !important;
    }
    
    /* Selectbox value */
    .stSelectbox [data-baseweb="select"] [aria-activedescendant] {
        color: #000000 !important !important;
    }
    
    /* ===== IMPORTANT: INJECT STYLE TO SHADOW DOM ===== */
    /* Style untuk dropdown options yang ada di shadow DOM */
    style#streamlit-selectbox-styles {
        display: none;
    }
    
    /* ===== LAST RESORT: JAVASCRIPT INJECTION READY ===== */
    /* Siapkan untuk injection JavaScript jika CSS tidak cukup */
</style>

<script>
// JavaScript untuk memastikan warna benar (jika CSS tidak cukup)
document.addEventListener('DOMContentLoaded', function() {
    // Fungsi untuk mengubah warna selectbox
    function fixSelectboxColors() {
        // Cari semua selectbox
        const selectboxes = document.querySelectorAll('[data-baseweb="select"]');
        
        selectboxes.forEach(selectbox => {
            // Set background putih dan text hitam
            selectbox.style.backgroundColor = 'white';
            selectbox.style.color = 'black';
            
            // Set semua child elements
            const children = selectbox.querySelectorAll('*');
            children.forEach(child => {
                child.style.color = 'black';
                child.style.backgroundColor = 'white';
            });
            
            // Set value yang ditampilkan
            const displayValue = selectbox.querySelector('[aria-activedescendant]');
            if (displayValue) {
                displayValue.style.color = 'black';
            }
        });
    }
    
    // Jalankan segera dan setiap 500ms untuk menangkap perubahan
    fixSelectboxColors();
    setInterval(fixSelectboxColors, 500);
    
    // Fix button colors
    function fixButtonColors() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            if (button.textContent.includes('TAMPILKAN JADWAL') || 
                button.textContent.includes('Submit') ||
                button.getAttribute('kind') === 'primary') {
                button.style.backgroundColor = 'black';
                button.style.color = 'white';
                button.style.border = '2px solid white';
                button.style.fontWeight = 'bold';
            }
        });
    }
    
    fixButtonColors();
    setInterval(fixButtonColors, 500);
});
</script>
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
