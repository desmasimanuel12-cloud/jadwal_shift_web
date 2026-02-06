import streamlit as st
import os
from PIL import Image
import sys
import base64

# ===== KONFIGURASI HALAMAN =====
st.set_page_config(
    page_title="Jadwal Shift 4G Mainline - PMI",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== META TAGS UNTUK ZOOM & COLOR SCHEME =====
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover">
<meta name="color-scheme" content="light only">
<meta name="theme-color" content="#000000">
""", unsafe_allow_html=True)

# ===== CSS LENGKAP DENGAN ZOOM GAMBAR =====
st.markdown("""
<style>
    /* COMPLETE RESET - FORCE COLORS */
    * {
        --st-selectbox-bg: #FFFFFF !important;
        --st-selectbox-text: #000000 !important;
    }
    
    /* BLACK BACKGROUND */
    .stApp, .main, .block-container {
        background-color: #000000 !important;
    }
    
    /* ALL TEXT WHITE BY DEFAULT */
    * {
        color: #FFFFFF !important;
    }
    
    /* EXCEPTIONS FOR INPUT ELEMENTS */
    input, 
    [data-baseweb="select"],
    [data-baseweb="select"] *,
    [role="listbox"],
    [role="listbox"] *,
    [role="option"],
    [role="option"] * {
        background-color: white !important;
        color: black !important;
        -webkit-text-fill-color: black !important;
    }
    
    /* SPECIFIC FOR SELECTBOX TEXT */
    [data-baseweb="select"] div,
    [data-baseweb="select"] span,
    [role="option"] div,
    [role="option"] span {
        color: black !important !important;
    }
    
    /* BUTTON */
    .stButton > button {
        background-color: black !important;
        color: white !important;
        border: 2px solid white !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    .stButton > button:hover {
        background-color: white !important;
        color: black !important;
        border: 2px solid white !important;
    }
    
    /* OVERRIDE ANY DARK/LIGHT MODE */
    @media (prefers-color-scheme: dark) {
        input, 
        [data-baseweb="select"],
        [data-baseweb="select"] * {
            background-color: white !important;
            color: black !important;
        }
    }
    
    @media (prefers-color-scheme: light) {
        input, 
        [data-baseweb="select"],
        [data-baseweb="select"] * {
            background-color: white !important;
            color: black !important;
        }
    }
    
    /* ===== GAMBAR: AGAR DAPAT DI ZOOM ===== */
    /* Container gambar Streamlit */
    .stImage, .stImage > div {
        overflow: visible !important;
        position: relative !important;
        touch-action: auto !important;
        margin: 20px 0 !important;
    }
    
    /* Gambar itu sendiri */
    .stImage img,
    .stImage > div > img,
    img[src*=".png"],
    img[src*=".jpg"],
    img[src*=".jpeg"] {
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
        
        /* Izinkan interaksi */
        pointer-events: auto !important;
        touch-action: auto !important;
        -webkit-user-select: none !important;
        user-select: none !important;
        
        /* Efek visual dan zoom */
        cursor: zoom-in !important;
        transition: transform 0.3s ease !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
        object-fit: contain !important;
    }
    
    /* Efek hover desktop */
    .stImage img:hover,
    img[src*=".png"]:hover,
    img[src*=".jpg"]:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Saat gambar di-klik/di-tap (ZOOM IN) */
    .stImage img.zoomed,
    img.zoomed {
        transform: scale(2) !important;
        cursor: zoom-out !important;
        z-index: 9999 !important;
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) scale(2) !important;
        max-width: 90vw !important;
        max-height: 90vh !important;
        border: 3px solid white !important;
        box-shadow: 0 0 50px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Overlay saat gambar di-zoom */
    .zoom-overlay {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background: rgba(0, 0, 0, 0.95) !important;
        z-index: 9998 !important;
        display: none;
    }
    
    /* Khusus untuk mobile devices */
    @media (max-width: 768px) {
        .stImage img,
        img[src*=".png"],
        img[src*=".jpg"] {
            min-height: 250px !important;
            min-width: 250px !important;
            touch-action: auto !important;
        }
        
        /* Tombol close untuk mobile */
        .zoom-close {
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            background: white !important;
            color: black !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 30px !important;
            z-index: 10000 !important;
            display: none;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            border: 2px solid black;
        }
    }
    
    /* Label gambar */
    .image-caption {
        text-align: center !important;
        color: white !important;
        font-weight: bold !important;
        margin-top: 10px !important;
        margin-bottom: 30px !important;
        font-size: 16px !important;
    }
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* CUSTOM BOX */
    .custom-box {
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin: 20px 0 !important;
        background-color: #111111 !important;
    }
</style>

<script>
// JavaScript untuk zoom gambar dan fix colors
document.addEventListener('DOMContentLoaded', function() {
    // 1. Fix warna selectbox
    function fixSelectboxColors() {
        document.querySelectorAll('[data-baseweb="select"], [role="option"]').forEach(el => {
            el.style.color = 'black';
            el.style.backgroundColor = 'white';
            el.querySelectorAll('*').forEach(child => {
                child.style.color = 'black';
                child.style.backgroundColor = 'white';
            });
        });
    }
    
    // 2. Fungsi zoom gambar
    function enableImageZoom() {
        const images = document.querySelectorAll('.stImage img, img[src*=".png"], img[src*=".jpg"]');
        
        images.forEach(img => {
            // Hapus event listener lama
            img.removeEventListener('click', toggleZoom);
            img.removeEventListener('touchstart', handleTouch);
            
            // Tambah event listener baru
            img.addEventListener('click', toggleZoom);
            img.addEventListener('touchstart', handleTouch, { passive: true });
            
            // Tambah class untuk styling
            img.classList.add('zoomable-image');
        });
    }
    
    // Variabel untuk touch handling
    let touchStartTime = 0;
    
    function handleTouch(e) {
        touchStartTime = Date.now();
        
        // Jika double tap (dalam 300ms), trigger zoom
        if (e.touches.length === 1) {
            setTimeout(() => {
                if (Date.now() - touchStartTime < 300) {
                    toggleZoom(e.target);
                }
            }, 300);
        }
    }
    
    function toggleZoom(imgElement) {
        const img = imgElement;
        
        if (img.classList.contains('zoomed')) {
            // Zoom out
            img.classList.remove('zoomed');
            document.body.style.overflow = 'auto';
            
            // Sembunyikan overlay
            const overlay = document.querySelector('.zoom-overlay');
            if (overlay) overlay.style.display = 'none';
            
            // Sembunyikan tombol close di mobile
            const closeBtn = document.querySelector('.zoom-close');
            if (closeBtn) closeBtn.style.display = 'none';
        } else {
            // Zoom in
            img.classList.add('zoomed');
            document.body.style.overflow = 'hidden';
            
            // Tampilkan overlay
            let overlay = document.querySelector('.zoom-overlay');
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.className = 'zoom-overlay';
                overlay.onclick = function() {
                    const zoomedImages = document.querySelectorAll('.zoomed');
                    zoomedImages.forEach(img => img.classList.remove('zoomed'));
                    this.style.display = 'none';
                    document.body.style.overflow = 'auto';
                    
                    // Sembunyikan tombol close
                    const closeBtn = document.querySelector('.zoom-close');
                    if (closeBtn) closeBtn.style.display = 'none';
                };
                document.body.appendChild(overlay);
            }
            overlay.style.display = 'block';
            
            // Tambah tombol close untuk mobile
            if (window.innerWidth <= 768) {
                let closeBtn = document.querySelector('.zoom-close');
                if (!closeBtn) {
                    closeBtn = document.createElement('div');
                    closeBtn.className = 'zoom-close';
                    closeBtn.innerHTML = '×';
                    closeBtn.onclick = function() {
                        const zoomedImages = document.querySelectorAll('.zoomed');
                        zoomedImages.forEach(img => img.classList.remove('zoomed'));
                        document.querySelector('.zoom-overlay').style.display = 'none';
                        this.style.display = 'none';
                        document.body.style.overflow = 'auto';
                    };
                    document.body.appendChild(closeBtn);
                }
                closeBtn.style.display = 'flex';
            }
        }
    }
    
    // 3. Inisialisasi fungsi
    fixSelectboxColors();
    enableImageZoom();
    
    // 4. Jalankan periodik untuk menangkap perubahan dinamis
    setInterval(() => {
        fixSelectboxColors();
        enableImageZoom();
    }, 1000);
    
    // 5. Mutation observer untuk perubahan DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                setTimeout(() => {
                    fixSelectboxColors();
                    enableImageZoom();
                }, 100);
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // 6. Reset zoom saat resize window
    window.addEventListener('resize', function() {
        const zoomedImages = document.querySelectorAll('.zoomed');
        zoomedImages.forEach(img => img.classList.remove('zoomed'));
        
        const overlay = document.querySelector('.zoom-overlay');
        if (overlay) overlay.style.display = 'none';
        
        const closeBtn = document.querySelector('.zoom-close');
        if (closeBtn) closeBtn.style.display = 'none';
        
        document.body.style.overflow = 'auto';
    });
});
</script>
""", unsafe_allow_html=True)

# ===== KELAS UTAMA =====
class ShiftSchedulerWeb:
    def __init__(self):
        # Tentukan folder script
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
        """Mendapatkan file gambar"""
        files = []
        targets = ["SS januari.png", "SS mei.png", "SS september.png", "SS libur.png"]
        
        for target in targets:
            if os.path.exists(target):
                files.append(target)
        
        return files
    
    def display_zoomable_image(self, image_path, caption=""):
        """Menampilkan gambar yang bisa di-zoom"""
        try:
            from PIL import Image
            
            # Buka gambar untuk mendapatkan ukuran
            img = Image.open(image_path)
            width, height = img.size
            
            # Tampilkan dengan width yang optimal
            max_display_width = 1000
            if width > max_display_width:
                # Hitung rasio resize
                ratio = max_display_width / width
                new_height = int(height * ratio)
                
                # Tampilkan gambar dengan ukuran yang sesuai
                st.image(img, width=max_display_width, caption=caption)
            else:
                # Tampilkan ukuran asli
                st.image(img, caption=caption)
            
            # Tambahkan info ukuran
            st.markdown(f"<div class='image-caption'>{caption} | Ukuran: {width} × {height} px</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Gagal memuat gambar {image_path}: {str(e)}")
    
    def run(self):
        # ===== SIDEBAR =====
        with st.sidebar:
            st.markdown("## 🔧 INFORMASI SISTEM")
            
            # Informasi folder
            st.write(f"**Folder program:**")
            st.code(self.script_dir)
            
            # Status file gambar
            st.markdown("### 📋 STATUS FILE")
            images = self.get_image_files()
            if images:
                st.success(f"✅ {len(images)} file ditemukan")
                for img in images:
                    st.write(f"• {os.path.basename(img)}")
            else:
                st.error("❌ File gambar tidak ditemukan")
            
            st.markdown("---")
            st.markdown("### 📌 PANDUAN PENGGUNAAN")
            st.markdown("""
            1. Isi **Nama Lengkap**
            2. Pilih **Grup Shift** (A, B, C, atau D)
            3. Pilih **Jabatan**
            4. Klik **TAMPILKAN JADWAL**
            
            **Fitur Zoom Gambar:**
            - Desktop: Klik gambar untuk zoom, klik lagi untuk keluar
            - Mobile: Double tap untuk zoom, tap luar gambar untuk keluar
            """)
        
        # ===== HEADER UTAMA =====
        st.markdown("<h1 style='text-align: center;'>📅 JADWAL SHIFT 4G MAINLINE</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>PHILIP MORRIS INTERNATIONAL</h3>", unsafe_allow_html=True)
        
        # ===== FORM INPUT =====
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("### 📝 INPUT DATA KARYAWAN")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input(
                "NAMA LENGKAP",
                placeholder="Masukkan nama lengkap",
                help="Contoh: Ahmad Supriyadi"
            )
        
        with col2:
            group = st.selectbox(
                "GRUP SHIFT",
                ["PILIH GRUP"] + self.groups,
                help="Pilih grup shift A, B, C, atau D"
            )
        
        with col3:
            position = st.selectbox(
                "JABATAN",
                ["PILIH JABATAN"] + self.positions,
                help="Pilih jabatan Anda"
            )
        
        # Tombol submit
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.button(
                "🚀 TAMPILKAN JADWAL",
                type="primary",
                use_container_width=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== PROCESS DATA =====
        if submit:
            # Validasi input
            if not name or group == "PILIH GRUP" or position == "PILIH JABATAN":
                st.error("❌ HARAP LENGKAPI SEMUA FIELD!")
                return
            
            # Cek jabatan Managerial
            if position == "Managerial":
                st.markdown("<div class='custom-box' style='border-color: #ff4444;'>", unsafe_allow_html=True)
                st.markdown("## ⚠️ AKSES DITOLAK")
                st.markdown("### Jabatan anda terlalu tinggi untuk program sederhana ini")
                st.markdown("""
                **Silakan hubungi tim IT untuk akses yang sesuai dengan jabatan Anda.**
                """)
                st.markdown("</div>", unsafe_allow_html=True)
                return
            
            # Cek jabatan valid
            if position in ["Protech", "Mekanik"]:
                self.show_schedule(name, group, position)
            else:
                st.error("Jabatan tidak valid!")
    
    def show_schedule(self, name, group, position):
        # ===== INFORMASI KARYAWAN =====
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("### 👤 INFORMASI KARYAWAN")
        st.markdown(f"**Nama:** {name}")
        st.markdown(f"**Grup Shift:** {group}")
        st.markdown(f"**Jabatan:** {position}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== LINE COORDINATOR =====
        lc_name = self.lc_data.get(group, "Tidak Diketahui")
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown(f"### 🎯 LINE COORDINATOR (LC) GRUP {group}")
        st.markdown(f"# {lc_name}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== LEADERSHIP TEAM =====
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("### 👥 LEADERSHIP TEAM")
        
        cols = st.columns(3)
        for idx, (role, ls_name) in enumerate(self.ls_data.items()):
            with cols[idx]:
                st.markdown(f"""
                <div style='
                    border: 2px solid white;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #222222;
                    text-align: center;
                '>
                    <h4 style='margin-bottom: 5px;'>{role}</h4>
                    <h3 style='margin-top: 5px;'>{ls_name}</h3>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== TAMPILKAN GAMBAR JADWAL =====
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("### 📋 JADWAL SHIFT 2026")
        st.markdown("**Klik gambar untuk zoom • Double tap di mobile**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        image_files = self.get_image_files()
        
        if image_files:
            # Urutkan gambar sesuai urutan yang diinginkan
            order = ["januari", "mei", "september", "libur"]
            sorted_images = []
            
            for keyword in order:
                for img_file in image_files:
                    if keyword in img_file.lower():
                        sorted_images.append(img_file)
                        break
            
            # Tampilkan gambar
            for img_file in sorted_images:
                try:
                    # Tampilkan dengan fungsi zoomable
                    self.display_zoomable_image(img_file, f"📄 {os.path.basename(img_file)}")
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Gagal memuat {img_file}: {str(e)}")
        else:
            st.warning("⚠️ File gambar jadwal tidak ditemukan!")
            st.info("Pastikan file berikut ada di folder program:")
            st.code("""
            SS januari.png
            SS mei.png
            SS september.png
            SS libur.png
            """)

# ===== JALANKAN APLIKASI =====
if __name__ == "__main__":
    print("🚀 Menjalankan Jadwal Shift 4G Mainline...")
    print(f"📁 Folder: {os.getcwd()}")
    
    # Jalankan aplikasi
    try:
        app = ShiftSchedulerWeb()
        app.run()
    except Exception as e:
        st.error(f"Terjadi error: {str(e)}")
        st.info("Pastikan semua file gambar ada di folder yang sama dengan program ini.")
