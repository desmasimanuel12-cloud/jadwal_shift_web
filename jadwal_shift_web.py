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

# ===== CSS UNTUK MENGATASI DARK/LIGHT MODE HP =====
st.markdown("""
<style>
    /* ===== OVERRIDE SYSTEM DARK/LIGHT MODE ===== */
    /* Paksa warna tanpa menghiraukan tema sistem */
    :root {
        color-scheme: light dark;
    }
    
    @media (prefers-color-scheme: dark) {
        /* Saat dark mode aktif di HP */
        :root {
            --select-bg: #FFFFFF !important;
            --select-text: #000000 !important;
            --button-bg: #000000 !important;
            --button-text: #FFFFFF !important;
        }
    }
    
    @media (prefers-color-scheme: light) {
        /* Saat light mode aktif di HP */
        :root {
            --select-bg: #FFFFFF !important;
            --select-text: #000000 !important;
            --button-bg: #000000 !important;
            --button-text: #FFFFFF !important;
        }
    }
    
    /* ===== BACKGROUND UTAMA ===== */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* ===== TEXT PUTIH UNTUK SEMUA KONTEN ===== */
    h1, h2, h3, h4, h5, h6, p, label, div, span {
        color: #FFFFFF !important;
    }
    
    /* ===== FIX UNTUK SELECTBOX (Grup & Jabatan) ===== */
    /* Paksa warna untuk semua state selectbox */
    div[data-baseweb="select"] {
        background-color: var(--select-bg, #FFFFFF) !important;
    }
    
    /* Text dalam selectbox */
    div[data-baseweb="select"] > div:first-child {
        background-color: var(--select-bg, #FFFFFF) !important;
        color: var(--select-text, #000000) !important;
    }
    
    /* Dropdown menu */
    div[role="listbox"] {
        background-color: var(--select-bg, #FFFFFF) !important;
    }
    
    /* Options dalam dropdown */
    div[role="option"] {
        background-color: var(--select-bg, #FFFFFF) !important;
        color: var(--select-text, #000000) !important;
    }
    
    /* Text dalam options */
    div[role="option"] span,
    div[role="option"] div {
        color: var(--select-text, #000000) !important;
    }
    
    /* Placeholder text */
    div[data-baseweb="select"] > div:first-child > div:last-child {
        color: #666666 !important;
    }
    
    /* ===== BUTTON SUBMIT ===== */
    .stButton > button,
    button[kind="primary"] {
        background-color: var(--button-bg, #000000) !important;
        color: var(--button-text, #FFFFFF) !important;
        border: 2px solid #FFFFFF !important;
        font-weight: bold !important;
    }
    
    /* ===== INPUT TEXT (Nama) ===== */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* ===== FIX COLOR PICKER ===== */
    /* Paksa semua text dalam dropdown hitam */
    [data-baseweb="select"] * {
        color: #000000 !important;
    }
    
    /* ===== FORCE LIGHT SCHEME FOR INPUTS ===== */
    /* Buat elemen input tidak terpengaruh tema sistem */
    input, select, textarea, [contenteditable] {
        color-scheme: light !important;
    }
    
    /* ===== MEDIA QUERY UNTUK MOBILE ===== */
    @media (max-width: 768px) {
        /* Tambahan styling untuk mobile */
        .stSelectbox, .stTextInput, .stButton {
            font-size: 16px !important; /* Mencegah zoom di iOS */
        }
        
        /* Pastikan selectbox terlihat baik di mobile */
        div[data-baseweb="select"] {
            min-height: 44px !important; /* Minimum touch target untuk iOS */
        }
    }
</style>

<script>
// JavaScript untuk memaksa warna hitam pada dropdown di semua kondisi
document.addEventListener('DOMContentLoaded', function() {
    function forceBlackTextInDropdowns() {
        // Target semua elemen dalam dropdown
        const dropdowns = document.querySelectorAll('[data-baseweb="select"]');
        
        dropdowns.forEach(dropdown => {
            // Set background putih dan text hitam
            dropdown.style.backgroundColor = 'white';
            
            // Set semua child elements
            const children = dropdown.querySelectorAll('*');
            children.forEach(child => {
                child.style.color = 'black';
                child.style.backgroundColor = 'white';
            });
            
            // Khusus untuk text yang ditampilkan
            const displayValue = dropdown.querySelector('div[aria-activedescendant]');
            if (displayValue) {
                displayValue.style.color = 'black';
            }
            
            // Khusus untuk dropdown options
            const options = document.querySelectorAll('[role="option"]');
            options.forEach(option => {
                option.style.color = 'black';
                option.style.backgroundColor = 'white';
            });
        });
        
        // Juga fix untuk tombol
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            if (button.textContent.includes('TAMPILKAN') || 
                button.textContent.includes('JADWAL') ||
                button.getAttribute('kind') === 'primary') {
                button.style.backgroundColor = 'black';
                button.style.color = 'white';
                button.style.border = '2px solid white';
            }
        });
    }
    
    // Jalankan segera
    forceBlackTextInDropdowns();
    
    // Jalankan setiap kali ada perubahan (dropdown dibuka/ditutup)
    const observer = new MutationObserver(forceBlackTextInDropdowns);
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Juga jalankan secara periodic untuk memastikan
    setInterval(forceBlackTextInDropdowns, 1000);
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
