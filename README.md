# EduPath AI

**Catatan project capstone PIJAK / IBM SkillBuild**

EduPath AI adalah project Machine Learning untuk membantu melihat apakah pengguna sudah memahami materi atau masih perlu remedial.

Project ini dibuat sebagai MVP. Jadi fokusnya bukan membuat aplikasi besar dulu, tetapi membuktikan alur utama:

```text
Data belajar pengguna
↓
Diolah menjadi fitur
↓
Model Machine Learning memprediksi kebutuhan remedial
↓
Sistem memberi arah rekomendasi belajar
```

---

## Tujuan Project

Tujuan sederhana dari EduPath AI:

1. Mengolah data belajar.
2. Melihat pola dari nilai dan aktivitas pengguna.
3. Memprediksi apakah pengguna perlu remedial.
4. Menyiapkan dasar untuk rekomendasi materi penguatan.

Output utama model:

```text
0 = Tidak Perlu Remedial
1 = Perlu Remedial
```

---

## Gambaran Alur Project

Alur kerja project ini dibuat bertahap:

```text
1. Data Understanding
2. EDA
3. Data Preparation
4. Feature Engineering
5. Training Model
6. Evaluasi Model
7. Simulasi Topic Accuracy
8. Save Model
9. Demo Aplikasi
```

Saat ini project sudah sampai tahap modeling dan simulasi `topic_accuracy`.

---

## Dataset yang Dipakai

Project ini memakai dua jenis dataset.

### 1. OULAD Dataset

OULAD dipakai sebagai dataset awal atau baseline.

Dataset ini berisi data seperti:

- informasi siswa,
- nilai assessment,
- aktivitas belajar,
- hasil akhir pembelajaran.

File OULAD yang dibutuhkan secara lokal:

```text
dataset/raw/studentInfo.csv
dataset/raw/studentAssessment.csv
dataset/raw/studentVle.csv
dataset/raw/vle.csv
```

Catatan:

File mentah OULAD tidak di-upload ke GitHub karena ukurannya besar. File tersebut tetap disimpan di komputer masing-masing pada folder:

```text
dataset/raw/
```

---

### 2. EduPath Dummy Dataset v2

Dataset dummy v2 dipakai untuk simulasi data ideal EduPath AI.

Dataset ini lebih dekat dengan tujuan utama project karena memiliki kolom:

```text
topic_accuracy
correct_answers
wrong_answers
attempt_count
study_duration_minutes
pre_test_score
needs_remedial
recommended_action
```

Dataset ini membantu menunjukkan bahwa sistem bisa membaca pemahaman per topik, bukan hanya nilai akhir.

---

## Struktur Folder

```text
EduPath-AI/
│
├── dataset/
│   ├── raw/
│   │   └── .gitkeep
│   │
│   └── processed/
│       ├── edupath_dataset_v1.csv
│       └── edupath_dataset_v2_dummy_topic_accuracy.csv
│
├── notebooks/
│   ├── 01_data_understanding_preparation.ipynb
│   ├── 01_data_preparation.py
│   ├── 02_train_baseline_model.py
│   ├── 03_random_forest_model.py
│   └── 04_train_dummy_topic_accuracy_model.ipynb
│
├── models/
│   ├── edupath_topic_accuracy_model.pkl
│   └── edupath_topic_accuracy_encoders.pkl
│
├── backend/
├── docs/
├── screenshots/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Penjelasan File Penting

### `01_data_understanding_preparation.ipynb`

Notebook ini dipakai untuk memahami dataset.

Isinya:

- membaca dataset OULAD,
- melihat isi data,
- EDA sederhana,
- penjelasan variabel,
- persiapan awal dataset.

---

### `01_data_preparation.py`

Script ini dipakai untuk membuat dataset hasil olahan.

Yang dilakukan:

- membaca `studentInfo.csv`, `studentAssessment.csv`, dan `studentVle.csv`,
- membuat `avg_score`,
- membuat `total_click`,
- menggabungkan data,
- membuat target `needs_remedial`,
- menyimpan hasil ke `dataset/processed/edupath_dataset_v1.csv`.

---

### `02_train_baseline_model.py`

Script ini dipakai untuk model baseline menggunakan Logistic Regression.

Tujuannya untuk membuat pembanding awal sebelum model lain dicoba.

---

### `03_random_forest_model.py`

Script ini dipakai untuk training Random Forest.

Di sini kita melihat:

- accuracy,
- confusion matrix,
- classification report,
- feature importance.

---

### `04_train_dummy_topic_accuracy_model.ipynb`

Notebook ini dipakai untuk simulasi model berbasis `topic_accuracy`.

Notebook ini penting karena arah akhir EduPath AI adalah melihat pemahaman pengguna per topik.

---

## Feature Engineering

Pada OULAD, beberapa fitur tidak langsung tersedia, jadi kita buat fitur baru.

### `avg_score`

Rata-rata nilai assessment siswa.

```text
avg_score = rata-rata score
```

Fitur ini dipakai untuk melihat performa akademik.

### `total_click`

Total aktivitas belajar siswa di platform.

```text
total_click = jumlah seluruh sum_click
```

Fitur ini dipakai untuk melihat aktivitas belajar.

### `needs_remedial`

Target yang ingin diprediksi.

Aturan awal:

```text
Fail        = 1
Withdrawn   = 1
Pass        = 0
Distinction = 0
```

---

## Hasil Model Sementara

### Baseline OULAD

Model awal dibuat menggunakan dataset OULAD hasil olahan `edupath_dataset_v1.csv`.

| Model               | Accuracy | Catatan                                          |
| ------------------- | -------: | ------------------------------------------------ |
| Logistic Regression |   73.92% | Accuracy sedikit lebih tinggi pada baseline awal |
| Random Forest       |   73.13% | Recall remedial lebih baik pada baseline awal    |

Catatan:

Pada tahap baseline, fitur yang digunakan masih sederhana, seperti `avg_score`, `total_click`, data demografi, dan riwayat percobaan belajar.

Untuk EduPath AI, mendeteksi pengguna yang perlu remedial lebih penting daripada hanya mengejar accuracy tinggi.

---

### Eksperimen Model Improved OULAD

Setelah baseline selesai, dilakukan eksperimen tambahan dengan menambahkan feature baru dari data assessment dan aktivitas belajar.

Feature tambahan yang digunakan:

```text
assessment_count
avg_date_submitted
banked_count
active_days
avg_click_per_day
max_click_day
```

Hasil eksperimen:

| Model                        | Accuracy | Catatan                                   |
| ---------------------------- | -------: | ----------------------------------------- |
| Logistic Regression Baseline |   73.92% | Model awal                                |
| Random Forest Baseline       |   73.13% | Model pembanding awal                     |
| Random Forest Improved       |   89.92% | Hasil terbaik setelah feature engineering |
| Gradient Boosting            |   89.61% | Hasil mendekati Random Forest Improved    |

Catatan:

Random Forest Improved menjadi model terbaik pada eksperimen OULAD karena accuracy naik menjadi 89.92%.

Peningkatan ini terjadi karena model mendapat informasi tambahan, seperti jumlah assessment yang dikerjakan, rata-rata waktu submit, jumlah hari aktif belajar, dan pola klik pengguna.

Model improved ini cocok untuk dokumentasi eksperimen modeling dan pengembangan lanjutan.

---

### Simulasi Topic Accuracy

Selain OULAD, project ini juga menggunakan dataset dummy v2 berbasis `topic_accuracy`.

Pada dataset dummy v2, fitur paling penting adalah:

1. `topic_accuracy`
2. `pre_test_score`
3. `wrong_answers`
4. `correct_answers`

Catatan:

Hasil dari dataset dummy tidak dianggap sebagai performa dunia nyata. Dataset ini hanya dipakai untuk simulasi alur ideal EduPath AI.

Untuk demo aplikasi berbasis course dan quiz, model `topic_accuracy` tetap lebih cocok digunakan karena alurnya sesuai dengan:

```text
course
↓
materi
↓
quiz
↓
topic_accuracy
↓
prediksi remedial
```

Jadi pembagian penggunaannya:

```text
Model Improved OULAD:
dipakai untuk dokumentasi eksperimen peningkatan model.

Model Topic Accuracy:
dipakai untuk demo aplikasi pembelajaran berbasis course dan quiz.
```

---


## Cara Menjalankan Project

### 1. Clone repository

```bash
git clone https://github.com/ZeroB7/EduPath-AI.git
cd EduPath-AI
```

### 2. Buat virtual environment

```bash
python -m venv venv
```

Aktifkan di Git Bash:

```bash
source venv/Scripts/activate
```

Atau di CMD Windows:

```bash
venv\Scripts\activate
```

### 3. Install library

```bash
pip install -r requirements.txt
```

### 4. Siapkan dataset OULAD

Masukkan file OULAD ke folder:

```text
dataset/raw/
```

Minimal file yang dibutuhkan:

```text
studentInfo.csv
studentAssessment.csv
studentVle.csv
vle.csv
```

### 5. Buat dataset hasil olahan

```bash
python notebooks/01_data_preparation.py
```

Output:

```text
dataset/processed/edupath_dataset_v1.csv
```

### 6. Jalankan model baseline

```bash
python notebooks/02_train_baseline_model.py
```

### 7. Jalankan Random Forest

```bash
python notebooks/03_random_forest_model.py
```

### 8. Jalankan simulasi topic accuracy

Buka notebook:

```text
notebooks/04_train_dummy_topic_accuracy_model.ipynb
```

Lalu jalankan cell dari atas sampai bawah.

---

## Status Project Saat Ini

Yang sudah selesai:

- Struktur folder project.
- GitHub repository.
- EDA dan data understanding.
- Dataset preparation OULAD.
- Dataset processed EduPath v1.
- Baseline model Logistic Regression.
- Random Forest model.
- Dataset dummy EduPath v2 berbasis `topic_accuracy`.
- Notebook simulasi topic accuracy.
- Model dan encoder untuk simulasi topic accuracy.

Yang belum dikerjakan:

- Demo aplikasi Streamlit.
- Integrasi model ke tampilan aplikasi.
- Screenshot demo.
- Dokumentasi final untuk presentasi.

---

## Catatan Penting untuk Tim

1. Jangan upload isi folder `dataset/raw/` ke GitHub.
2. Kalau ingin menjalankan OULAD, file mentah harus ada di komputer lokal.
3. Dataset dummy v2 sudah ada di `dataset/processed/`.
4. Modeling sudah cukup untuk MVP, jangan tambah model baru dulu.
5. Fokus berikutnya adalah membuat demo aplikasi sederhana.

---
## Rencana Alur Aplikasi Demo

Setelah tahap dataset dan modeling selesai, langkah berikutnya adalah membuat demo aplikasi sederhana.

Untuk MVP, aplikasi tidak langsung dibuat besar. Kita mulai dari alur kecil terlebih dahulu agar mudah dipahami dan bisa didemokan.

Alur demo yang akan dibuat:

```text
Pilih Course
↓
Baca Materi
↓
Kerjakan Quiz
↓
Sistem menghitung hasil quiz
↓
Model memprediksi perlu remedial atau tidak
↓
Aplikasi menampilkan rekomendasi belajar
```

---

### Course Demo Awal

Untuk demo pertama, kita cukup memakai satu course.

```text
Course:
Programming Basic

Topik:
Loops
```

Isi course:

```text
- Materi singkat tentang Loops
- Contoh kode sederhana
- Link video pembelajaran
- Quiz 5 soal
- Hasil prediksi remedial
- Rekomendasi belajar
```

Tujuannya agar alur aplikasi selesai terlebih dahulu sebelum menambah course lain.

---

### Data yang Perlu Disiapkan

Agar aplikasi bisa berjalan, tim perlu menyiapkan data sederhana seperti:

```text
course
topic
materi
video pembelajaran
quiz
pilihan jawaban
jawaban benar
pembahasan soal
materi remedial
topik berikutnya
```

Untuk tahap awal, data ini bisa disimpan di file JSON:

```text
data/courses.json
```

Nanti jika project berkembang, data ini bisa dipindahkan ke database.

---

### Peran Model Machine Learning

Model tidak membuat materi secara otomatis.

Model hanya membantu menentukan:

```text
Apakah pengguna perlu remedial atau tidak?
```

Input model berasal dari hasil quiz, seperti:

```text
subject
topic
difficulty_level
total_questions
correct_answers
wrong_answers
topic_accuracy
attempt_count
study_duration_minutes
pre_test_score
```

Output model:

```text
0 = Tidak Perlu Remedial
1 = Perlu Remedial
```

---

### Alur Jika Pengguna Perlu Remedial

Jika hasil model adalah:

```text
needs_remedial = 1
```

maka aplikasi menampilkan rekomendasi seperti:

```text
Status:
Perlu Remedial

Rekomendasi:
- Pelajari ulang materi pada topik tersebut
- Tonton video penguatan
- Baca pembahasan soal yang salah
- Kerjakan quiz remedial
```

---

### Alur Jika Pengguna Tidak Perlu Remedial

Jika hasil model adalah:

```text
needs_remedial = 0
```

maka aplikasi menampilkan:

```text
Status:
Tidak Perlu Remedial

Rekomendasi:
- Lanjut ke topik berikutnya
```

---

### File yang Akan Ditambahkan

Untuk membuat demo aplikasi, file yang akan ditambahkan adalah:

```text
app.py
data/courses.json
```

Penjelasan:

```text
app.py
```

Digunakan untuk membuat tampilan aplikasi menggunakan Streamlit.

```text
data/courses.json
```

Digunakan untuk menyimpan course, materi, quiz, video, pembahasan, dan rekomendasi remedial.

---

### Target Demo MVP

Target demo MVP adalah:

```text
User bisa memilih course
User bisa membaca materi
User bisa mengerjakan quiz
Sistem menghitung topic_accuracy
Model memprediksi kebutuhan remedial
Aplikasi menampilkan rekomendasi belajar
```

Jika alur ini sudah berjalan, maka EduPath AI sudah bisa ditunjukkan sebagai prototype pembelajaran adaptif sederhana.

## Next Step

Tahap berikutnya:

```text
Buat app.py
↓
Load model topic_accuracy
↓
User input data belajar
↓
Prediksi perlu remedial atau tidak
↓
Tampilkan rekomendasi
↓
Ambil screenshot demo
```

Untuk demo, rencana paling sederhana adalah memakai Streamlit.

---

## Kesimpulan Singkat

EduPath AI adalah project untuk membantu membaca pemahaman pengguna dari data belajar.

Tahap awal memakai OULAD sebagai baseline. Setelah itu dibuat dataset dummy berbasis `topic_accuracy` agar alur EduPath AI lebih dekat dengan tujuan utama, yaitu mendeteksi topik yang belum dikuasai dan memberi arah remedial.

Project ini menjadi fondasi awal untuk membangun sistem pembelajaran yang lebih personal, adaptif, dan berbasis data.
