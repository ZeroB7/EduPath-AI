from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import joblib
import pandas as pd

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_eduai_SMK_pastibisa'

# ====================================================================
# MULTIMEDIA INTERFACES: MEMUAT MODEL AI DAN ENCODER BINER (.PKL)
# ====================================================================
try:
    model_ai = joblib.load('models/edupath_topic_accuracy_model.pkl')
    encoders = joblib.load('models/edupath_topic_accuracy_encoders.pkl')
    print("AI Core Status: Berhasil memuat Model dan Encoder Pintar.")
except Exception as e:
    model_ai = None
    encoders = None
    print(f"AI Core Status Error: Gagal memuat file model biner. Logika manual diaktifkan. Detail: {e}")

# KONFIGURASI KONEKSI DATABASE MYSQL
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',         # Default XAMPP adalah root
        password='',         # Default XAMPP adalah kosong
        database='eduai_smk',
        cursorclass=pymysql.cursors.DictCursor
    )

# 1. ROUTE LOGIN
@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_siswa')
        password = request.form.get('password')
        
        # VALIDASI KETAT: Password wajib "indonesiamaju"
        if password == "indonesiamaju" and nama_lengkap:
            # Mengambil kata pertama dari nama lengkap siswa sebagai nama panggilan
            nama_panggilan = nama_lengkap.strip().split()[0]
            
            # Simpan nama yang sudah rapi ke dalam session
            session['nama_siswa'] = nama_panggilan.capitalize()
            
            return redirect(url_for('dashboard_siswa'))
        else:
            # Jika password salah, tendang balik ke halaman login dengan alert
            return render_template('login.html', error_alert=True)
            
    return render_template('login.html')

# 2. ROUTE DASHBOARD SISWA (LOGIKA PREDIKSI INTEGRASI MODEL MACHINE LEARNING)
@app.route('/siswa', methods=['GET', 'POST'])
def dashboard_siswa():
    nama = session.get('nama_siswa', 'Siswa')
    
    # Ambil data input dari kuis
    nilai_input = request.form.get('nilai_siswa')
    tipe_kuis = request.form.get('tipe_kuis') # Penanda apakah kuis dasar atau pengayaan
    
    if nilai_input is not None:
        nilai = int(nilai_input)
        
        # Penentuan nama topik string berdasarkan tipe kuis yang dikirim form
        if tipe_kuis == 'pengayaan':
            topik_nama = "Data Structures"  # Menyesuaikan keyword topik yang ada di encoder temanmu
        else:
            topik_nama = "Linear Equations" # Menyesuaikan keyword topik yang ada di encoder temanmu

        # --- EKSEKUSI PREDIKSI CLASSIFICATION MODEL START ---
        status = None
        if model_ai and encoders:
            try:
                # 1. Transformasi Fitur String (Mata Pelajaran & Tingkat Kesulitan Default)
                subject_encoded = encoders['subject'].transform(['Mathematics'])[0]
                topic_encoded = encoders['topic'].transform([topik_nama])[0]
                difficulty_encoded = encoders['difficulty_level'].transform(['easy'])[0]
                
                # 2. Susun data input menjadi DataFrame yang sesuai dengan nama kolom saat training model
                input_df = pd.DataFrame([{
                    'subject': subject_encoded,
                    'topic': topic_encoded,
                    'difficulty_level': difficulty_encoded,
                    'accuracy': nilai  # Nilai kuis dibaca sebagai tingkat akurasi pemahaman
                }])
                
                # 3. Prediksi Klasifikasi Kategori Performa Siswa
                prediksi_angka = model_ai.predict(input_df)[0]
                
                # 4. Ambil representasi string kategori hasil inverse encoder (Rendah/Sedang/Tinggi)
                status = str(prediksi_angka).capitalize()
            except Exception as ml_error:
                print(f"Gagal memproses fitur input model: {ml_error}")
                status = None

        # Fallback Logic: Jika file model tidak sesuai atau gagal menghitung dimensi array
        if status not in ["Rendah", "Sedang", "Tinggi", "Selesai"]:
            if tipe_kuis == 'pengayaan':
                if nilai >= 80: status = "Selesai"
                elif nilai >= 50: status = "Tinggi"
                else: status = "Sedang"
            else:
                if nilai >= 85: status = "Tinggi"
                elif nilai >= 40: status = "Sedang"
                else: status = "Rendah"
        # --- EKSEKUSI PREDIKSI CLASSIFICATION MODEL END ---

        # 5. PEMETAAN REKOMENDASI MULTIMEDIA ADAPTIF BERDASARKAN STATUS AKHIR
        if tipe_kuis == 'pengayaan':
            topik_db_save = "Data Modeling Structures (Pengayaan)"
            if status == "Selesai":
                rekomendasi_materi = "Semua Modul Kompetensi Matematika SMK Telah Diselesaikan! 🎓"
                langkah_belajar = [
                    "Selamat! Anda telah menyelesaikan seluruh rangkaian Jalur Pembelajaran Adaptif.",
                    "Sistem AI menyatakan Anda kompeten dalam seluruh topik Kurikulum SMK.",
                    "Silakan unduh ringkasan laporan belajar untuk evaluasi guru."
                ]
            elif status == "Tinggi":
                rekomendasi_materi = "Data Modeling Structures (Review Pengayaan)"
                langkah_belajar = [
                    "Nilai pengayaan Anda cukup baik. Silakan review kembali soal-soal HOTS untuk mencapai target.",
                    "Coba ulangi kuis kelas pengayaan untuk menyelesaikan modul sepenuhnya."
                ]
            else:
                status = "Sedang"  # Normalisasi status pengayaan terendah ke Sedang
                rekomendasi_materi = 'Penguatan Basis Data & Logika Modeling <br><br> <a href="https://youtu.be/ZwiBGMaVo8s?si=BoxoXy9JKJmVguF_" target="_blank" style="background: #EF4444; color:white; padding: 6px 12px; border-radius:6px; text-decoration:none; font-size:12px; margin-right:6px; font-weight:500;"><i class="fa-brands fa-youtube"></i> Tonton Video</a> <a href="/static/pdf/modeling_sedang.pdf" target="_blank" style="background: #1A56DB; color:white; padding: 6px 12px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:500;"><i class="fa-solid fa-file-pdf"></i> Download PDF</a>'
                langkah_belajar = [
                    "Nilai pengayaan terlalu rendah. Sistem menyarankan untuk review materi dasar.",
                    "Silakan tonton video pembelajaran materi dan pelajari kembali modul PDF di atas sebelum mencoba kuis lagi."
                ]
        else:
            topik_db_save = "Evaluasi Dasar (Tahap 1)"
            if status == "Tinggi":
                rekomendasi_materi = "Data Modeling Structures (Kelas Lanjut)"
                langkah_belajar = [
                    "Selamat! Kemampuanmu sudah sangat baik.",
                    "Silakan akses modul kelas pengayaan yang telah terbuka di atas.",
                    "Ikuti tantangan coding test tingkat lanjut."
                ]
            elif status == "Sedang":
                rekomendasi_materi = 'Fungsi Kuadrat & Grafik (Review) <br><br> <a href="https://youtu.be/IwFQPIdqqqQ?si=ZzBJaiulos-91HWE" target="_blank" style="background: #EF4444; color:white; padding: 6px 12px; border-radius:6px; text-decoration:none; font-size:12px; margin-right:6px; font-weight:500;"><i class="fa-brands fa-youtube"></i> Video Pembahasan</a> <a href="/static/pdf/fungsi_kuadrat.pdf" target="_blank" style="background: #1A56DB; color:white; padding: 6px 12px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:500;"><i class="fa-solid fa-file-pdf"></i> Modul Ringkas</a>'
                langkah_belajar = [
                    "Pertahankan prestasimu! Sedikit lagi mencapai nilai sempurna.",
                    "Review materi Fungsi Kuadrat yang masih keliru menggunakan tautan video atau materi PDF di atas.",
                    "Ikuti kuis pemantapan nilai kembali untuk membuka kelas lanjutan."
                ]
            else:
                status = "Rendah"
                rekomendasi_materi = 'Persamaan Linear (Dasar) - Remedial <br><br> <a href="https://youtu.be/4DPidz3KdEI?si=uBR2vXbFnotE7kKJ" target="_blank" style="background: #EF4444; color:white; padding: 6px 12px; border-radius:6px; text-decoration:none; font-size:12px; margin-right:6px; font-weight:500;"><i class="fa-brands fa-youtube"></i> Video Remedial</a> <a href="/static/pdf/persamaan_linear_dasar.pdf" target="_blank" style="background: #1A56DB; color:white; padding: 6px 12px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:500;"><i class="fa-solid fa-file-pdf"></i> Download PDF Materi</a>'
                langkah_belajar = [
                    "Terus semangat! Sistem mendeteksi kamu berisiko gagal.",
                    "Wajib pelajari ulang materi dasar: Persamaan Linear melalui panduan berkas di atas.",
                    "Kerjakan latihan soal remedial yang disediakan setelah memahami materi."
                ]
            
        # Simpan hasil akhir ke session dashboard utama
        session['terakhir_nilai'] = nilai
        session['terakhir_status'] = status  
        session['terakhir_rekomendasi'] = rekomendasi_materi
        session['terakhir_langkah'] = langkah_belajar
        session['sudah_kuis'] = True

        # ====================================================================
        # PROSES 1: SIMPAN REKAMAN DATA KUIS OTOMATIS KE DATABASE MYSQL
        # ====================================================================
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """INSERT INTO riwayat_nilai (nama_siswa, mapel, topik, nilai, durasi, prediksi) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nama, "Matematika SMK", topik_db_save, nilai, 30, status))
        conn.commit()
        conn.close()

    # Ambil data tracking dari session
    sudah_kuis = session.get('sudah_kuis', False)
    nilai = session.get('terakhir_nilai', 0)
    status = session.get('terakhir_status', 'Belum Ada Data')
    rekomendasi_materi = session.get('terakhir_rekomendasi', 'Silakan kerjakan kuis pertama Anda untuk mendapatkan rekomendasi model AI.')
    langkah_belajar = session.get('terakhir_langkah', [
        "Klik tombol 'Masuk Kelas & Kuis' di atas untuk memulai evaluasi.",
        "Sistem AI akan membaca metrik akurasi jawaban Anda secara real-time."
    ])

    return render_template('siswa.html', 
                           nama=nama, 
                           nilai=nilai, 
                           status=status, 
                           rekomendasi=rekomendasi_materi, 
                           langkah=langkah_belajar,
                           sudah_kuis=sudah_kuis)

# 3. ROUTE HALAMAN KUIS
@app.route('/kuis')
def halaman_kuis():
    return render_template('kuis.html')

# 4. ROUTE INPUT NILAI MANUAL
@app.route('/input_nilai', methods=['GET', 'POST'])
def input_nilai():
    nama = session.get('nama_siswa', 'Siswa')
    pesan_sukses = False

    if request.method == 'POST':
        mapel = request.form.get('mapel')
        topik = request.form.get('topik')
        nilai = int(request.form.get('nilai_siswa'))
        durasi = int(request.form.get('durasi_belajar'))
        
        # --- PROSES MACHINE LEARNING INPUT MANUAL ---
        prediksi_status = None
        if model_ai and encoders:
            try:
                # Normalisasi string input dinamis agar cocok dengan dictionary kategori encoder
                sub_norm = "Mathematics" if mapel.lower() == "matematika smk" else "Science"
                top_norm = "Linear Equations" if "linear" in topik.lower() else "Data Structures"
                
                subject_encoded = encoders['subject'].transform([sub_norm])[0]
                topic_encoded = encoders['topic'].transform([top_norm])[0]
                difficulty_encoded = encoders['difficulty_level'].transform(['easy'])[0]
                
                input_df = pd.DataFrame([{
                    'subject': subject_encoded,
                    'topic': topic_encoded,
                    'difficulty_level': difficulty_encoded,
                    'accuracy': nilai
                }])
                
                prediksi_status = str(model_ai.predict(input_df)[0]).capitalize()
            except:
                prediksi_status = None
                
        if prediksi_status not in ["Rendah", "Sedang", "Tinggi", "Selesai"]:
            if nilai >= 85: prediksi_status = "Tinggi"
            elif nilai >= 40: prediksi_status = "Sedang"
            else: prediksi_status = "Rendah"
        # --- PROSES MACHINE LEARNING INPUT MANUAL END ---
            
        # ====================================================================
        # PROSES 2: SIMPAN DATA INPUTAN MANUAL KE DATABASE MYSQL
        # ====================================================================
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """INSERT INTO riwayat_nilai (nama_siswa, mapel, topik, nilai, durasi, prediksi) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nama, mapel, topik, nilai, durasi, prediksi_status))
        conn.commit()
        conn.close()
        
        pesan_sukses = True

    return render_template('input.html', nama=nama, pesan_sukses=pesan_sukses)

# 5. ROUTE MATERI LANJUTAN (TAHAP 2)
@app.route('/materi_lanjut')
def materi_lanjut():
    status = session.get('terakhir_status', 'Belum Ada Data')
    nama = session.get('nama_siswa', 'Siswa')
    
    # Proteksi: Hanya yang berstatus 'Tinggi' atau 'Selesai' yang boleh masuk ke Tahap 2
    if status != 'Tinggi' and status != 'Selesai':
        return redirect(url_for('dashboard_siswa'))
        
    return render_template('materi_lanjut.html', nama=nama)

# ROUTE LOGOUT (COOKIE TERHAPUS BERSIH)
@app.route('/logout')
def logout():
    session.clear()
    response = redirect(url_for('login_page'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

# 6. ROUTE RIWAYAT SAYA (MEMBACA DATA DINAMIS DARI MYSQL)
@app.route('/riwayat')
def halaman_riwayat():
    nama = session.get('nama_siswa', 'Siswa')
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = """SELECT mapel, topik, nilai, durasi, prediksi 
                 FROM riwayat_nilai 
                 WHERE nama_siswa = %s 
                 ORDER BY id DESC"""
        cursor.execute(sql, (nama,))
        data_riwayat = cursor.fetchall()
    conn.close()
    
    return render_template('riwayat.html', nama=nama, data_riwayat=data_riwayat)

# 7. ROUTE TIPS BELAJAR (DINAMIS BERDASARKAN STATUS)
@app.route('/tips')
def halaman_tips():
    nama = session.get('nama_siswa', 'Siswa')
    status = session.get('terakhir_status', 'Belum Ada Data')
    
    if status == 'Rendah':
        kategori_tips = "Strategi Penguatan Dasar 📉"
        list_tips = [
            "Fokus pada Konsep, Bukan Rumus: Pelajari struktur dasar kenapa rumus itu terbentuk, bukan sekadar menghafal hurufnya.",
            "Metode Pomodoro (25/5): Belajar materi dasar selama 25 minutes secara fokus, lalu istirahat 5 menit agar otak tidak jenuh.",
            "Visualisasi Materi: Coba cari video ilustrasi animasi di YouTube mengenai topik yang sulit agar lebih mudah dibayangkan."
        ]
    elif status == 'Sedang':
        kategori_tips = "Akselerasi & Pemantapan Nilai 📊"
        list_tips = [
            "Analisis Kesalahan Kuis: Buka kembali lembar jawaban kuis kemarin, lalu lacak di baris mana letak keliru hitungmu.",
            "Variasi Angka Soal: Coba ulangi kuis kelas pemantapan dengan mengubah angka-angkanya secara mandiri untuk menguji kefasihan logikamu.",
            "Manajemen Waktu per Soal: Pasang stopwatch saat latihan, targetkan satu soal selesai dalam waktu maksimal 2 menit."
        ]
    elif status == 'Tinggi' or status == 'Selesai':
        kategori_tips = "Tantangan Tingkat Lanjut (HOTS) 🚀"
        list_tips = [
            "Implementasi ke Bahasa Program: Coba konversikan logika rumus matematika tadi ke dalam baris kode Python.",
            "Eksplorasi Logika Modeling: Mulai mengenali struktur pemodelan data (Data Modeling) tingkat lanjut yang sering dipakai di industri IT.",
            "Metode Belajar Feynman: Cobalah jelaskan materi kuis tadi kepada teman sekelompokmu yang belum paham untuk memperkuat ingatanmu."
        ]
    else:
        kategori_tips = "Tips Umum EduAI 💡"
        list_tips = [
            "Silakan ikuti kuis pertama kamu di Beranda atau masukkan nilai manual terlebih dahulu agar AI bisa membaca metrik kemampuanmu!"
        ]
        
    return render_template('tips.html', nama=nama, kategori=kategori_tips, data_tips=list_tips)

# 8. ROUTE HALAMAN TENTANG APLIKASI
@app.route('/tentang')
def halaman_tentang():
    return render_template('tentang.html')

if __name__ == '__main__':
    app.run(debug=True)