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

# ===== CSS HITAM-PUTIH =====
st.markdown("""
<style>
    /* Background hitam untuk seluruh halaman */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Header putih di atas hitam */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Text putih */
    p, div, span {
        color: #FFFFFF !important;
    }
    
    /* Input field: putih dengan tulisan hitam */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Button: putih dengan tulisan hitam */
    .stButton>button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        font-weight: bold !important;
    }
    
    /* Sidebar hitam */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #222222 !important;
        color: #FFFFFF !important;
    }
    
    /* Divider putih */
    hr {
        border-color: #FFFFFF !important;
    }
    
    /* Box info dengan border putih */
    .info-box {
        border: 2px solid #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #111111;
    }
    
    /* Box warning dengan border merah */
    .warning-box {
        border: 2px solid #FF4444;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #111111;
    }
</style>
""", unsafe_allow_html=True)

class ShiftSchedulerWeb:
    def __init__(self):
        # Auto-detect folder
        if getattr(sys, 'frozen', False):
            self.script_dir = os.path.dirname(sys.executable)
        else:
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        os.chdir(self.script_dir)
        
        # Data
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
        targets = ["SS januari.png", "SS mei.png", "SS september.png", "SS libur.png"]
        
        for target in targets:
            if os.path.exists(target):
                files.append(target)
        
        return files
    
    def run(self):
        # ===== SIDEBAR =====
        with st.sidebar:
            st.markdown("## 🔧 INFORMASI SISTEM")
            st.write(f"**Folder program:**")
            st.code(self.script_dir)
            
            # Cek file
            st.markdown("### 📋 STATUS FILE")
            images = self.get_image_files()
            if images:
                st.success(f"✅ {len(images)} file ditemukan")
                for img in images:
                    st.write(f"• {img}")
            else:
                st.error("❌ File gambar tidak ditemukan")
            
            st.markdown("---")
            st.markdown("### 📌 PANDUAN")
            st.markdown("""
            1. Isi form dengan lengkap
            2. Pilih grup dan jabatan
            3. Tekan tombol **TAMPILKAN JADWAL**
            4. Untuk **Managerial** akan ditolak aksesnya
            5. Untuk **Protech/Mekanik** akan tampil jadwal
            """)
        
        # ===== HEADER UTAMA =====
        st.markdown("<h1 style='text-align: center;'>📅 JADWAL SHIFT 4G MAINLINE</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>PHILIP MORRIS INTERNATIONAL</h3>", unsafe_allow_html=True)
        
        # ===== FORM INPUT =====
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown("### 📝 INPUT DATA KARYAWAN")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("NAMA LENGKAP", placeholder="Masukkan nama Anda")
        
        with col2:
            group = st.selectbox("GRUP SHIFT", ["PILIH GRUP"] + self.groups)
        
        with col3:
            position = st.selectbox("JABATAN", ["PILIH JABATAN"] + self.positions)
        
        # Tombol submit
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.button("🚀 TAMPILKAN JADWAL", type="primary", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== PROCESS DATA =====
        if submit:
            if not name or group == "PILIH GRUP" or position == "PILIH JABATAN":
                st.error("❌ HARAP LENGKAPI SEMUA FIELD!")
                return
            
            if position == "Managerial":
                st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
                st.markdown("## ⚠️ AKSES DITOLAK")
                st.markdown("### Jabatan anda terlalu tinggi untuk program sederhana ini")
                st.markdown("""
                **SILAKAN HUBUNGI TIM IT UNTUK AKSES YANG SESUAI**
                """)
                st.markdown("</div>", unsafe_allow_html=True)
                return
            
            if position in ["Protech", "Mekanik"]:
                self.show_schedule(name, group, position)
            else:
                st.error("Jabatan tidak valid!")
    
    def show_schedule(self, name, group, position):
        # Informasi user
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown(f"### 👤 INFORMASI KARYAWAN")
        st.markdown(f"**Nama:** {name}")
        st.markdown(f"**Grup Shift:** {group}")
        st.markdown(f"**Jabatan:** {position}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # LC Info
        lc_name = self.lc_data.get(group, "Tidak Diketahui")
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown(f"### 🎯 LINE COORDINATOR (LC) GRUP {group}")
        st.markdown(f"# {lc_name}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # LS Info
        st.markdown("### 👥 LEADERSHIP TEAM")
        cols = st.columns(3)
        
        for idx, (role, ls_name) in enumerate(self.ls_data.items()):
            with cols[idx]:
                st.markdown(f"""
                <div style='border: 2px solid white; padding: 15px; border-radius: 10px; background-color: #111111;'>
                    <h4 style='text-align: center;'>{role}</h4>
                    <h3 style='text-align: center;'>{ls_name}</h3>
                </div>
                """, unsafe_allow_html=True)
        
        # Tampilkan gambar
        st.markdown("---")
        st.markdown("### 📋 JADWAL SHIFT 2026")
        
        image_files = self.get_image_files()
        order = ["januari", "mei", "september", "libur"]
        sorted_images = []
        
        for keyword in order:
            for img_file in image_files:
                if keyword in img_file.lower():
                    sorted_images.append(img_file)
                    break
        
        for img_file in sorted_images:
            try:
                st.markdown(f"#### 📄 {img_file}")
                img = Image.open(img_file)
                st.image(img)
                st.markdown("---")
            except Exception as e:
                st.error(f"Gagal memuat {img_file}: {str(e)}")
        
        if not image_files:
            st.warning("⚠️ File gambar jadwal tidak ditemukan!")

# ===== JALANKAN APLIKASI =====
if __name__ == "__main__":
    print("\n" + "="*60)
    print("JADWAL SHIFT 4G MAINLINE - WEB VERSION")
    print("="*60)
    
    app = ShiftSchedulerWeb()
    app.run()