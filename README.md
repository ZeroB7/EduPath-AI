# EduPath AI

**Personalized Remedial & Adaptive Learning Platform**

EduPath AI adalah project capstone yang dikembangkan untuk membantu menganalisis pemahaman pengguna terhadap materi pembelajaran berdasarkan data evaluasi dan aktivitas belajar. Sistem ini bertujuan mendeteksi apakah pengguna sudah memahami materi atau masih membutuhkan remedial, kemudian memberikan rekomendasi penguatan materi yang sesuai.

Project ini dikembangkan sebagai bagian dari program Capstone PIJAK / IBM SkillBuild dengan fokus pada penerapan Machine Learning dalam bidang pendidikan.

---

## Project Overview

Banyak platform pembelajaran hanya menampilkan nilai akhir setelah pengguna mengerjakan evaluasi. Namun, nilai akhir saja belum cukup untuk mengetahui apakah pengguna benar-benar memahami materi yang dipelajari.

EduPath AI mencoba menyelesaikan masalah tersebut dengan cara:

1. Menganalisis hasil evaluasi pengguna.
2. Mengidentifikasi kemungkinan kebutuhan remedial.
3. Melihat indikator pembelajaran seperti nilai, aktivitas belajar, dan akurasi per topik.
4. Memberikan rekomendasi penguatan materi secara lebih personal.

Dengan demikian, EduPath AI tidak hanya berfungsi sebagai sistem penilaian, tetapi juga sebagai sistem diagnosis pembelajaran.

---

## Problem Statement

Dalam proses pembelajaran, pengguna sering kali hanya mendapatkan hasil akhir berupa nilai tanpa mengetahui bagian materi mana yang belum dikuasai.

Permasalahan utama yang ingin diselesaikan:

> Bagaimana sistem dapat membantu mengidentifikasi apakah pengguna sudah memahami materi dan menentukan apakah pengguna membutuhkan remedial berdasarkan data pembelajaran?

---

## Proposed Solution

EduPath AI menggunakan pendekatan Machine Learning untuk menganalisis data pembelajaran pengguna.

Sistem memanfaatkan indikator seperti:

* rata-rata nilai assessment,
* aktivitas belajar,
* hasil evaluasi,
* jumlah jawaban benar,
* jumlah jawaban salah,
* akurasi per topik,
* jumlah percobaan,
* durasi belajar.

Output utama sistem:

```text
0 = Tidak Perlu Remedial
1 = Perlu Remedial
```

---

## Main Features

Pada tahap MVP, fitur yang dikembangkan meliputi:

1. **Data Understanding**

   * Memahami struktur dataset OULAD.
   * Melakukan eksplorasi data awal.
   * Mengecek missing value dan distribusi data.

2. **Feature Engineering**

   * Membuat fitur `avg_score`.
   * Membuat fitur `total_click`.
   * Membuat dataset hasil olahan EduPath v1.

3. **Baseline Machine Learning Model**

   * Logistic Regression.
   * Random Forest.
   * Evaluasi menggunakan accuracy, confusion matrix, classification report.

4. **Topic Accuracy Simulation**

   * Menggunakan dataset dummy EduPath v2.
   * Menganalisis pemahaman pengguna berdasarkan `topic_accuracy`.
   * Melatih model simulasi untuk prediksi kebutuhan remedial.

5. **Model Export**

   * Menyimpan model Machine Learning.
   * Menyimpan encoder untuk kebutuhan integrasi backend.

---

## Dataset

Project ini menggunakan dua jenis dataset:

### 1. OULAD Dataset

OULAD digunakan sebagai baseline dataset karena memiliki data pembelajaran nyata seperti:

* informasi siswa,
* hasil assessment,
* aktivitas pembelajaran,
* final result.

Dataset OULAD digunakan untuk membangun model awal prediksi kebutuhan remedial.

File utama yang digunakan:

```text
studentInfo.csv
studentAssessment.csv
studentVle.csv
vle.csv
```

Catatan:

Dataset mentah tidak disertakan di repository karena ukuran file cukup besar. Dataset mentah disimpan secara lokal di folder:

```text
dataset/raw/
```

---

### 2. EduPath Dummy Dataset v2

Dataset dummy EduPath v2 digunakan untuk mensimulasikan struktur data ideal EduPath AI.

Dataset ini berisi fitur seperti:

```text
user_id
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
post_test_score
improvement_score
mastery_level
needs_remedial
recommended_action
remediation_material_id
interaction_date
```

Dataset dummy ini digunakan untuk membuktikan bahwa indikator `topic_accuracy` dapat menjadi dasar dalam mendeteksi kebutuhan remedial pengguna.

---

## Project Structure

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
│
├── docs/
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Machine Learning Workflow

Alur pemodelan Machine Learning pada project ini:

```text
Raw Dataset
↓
Data Understanding
↓
Data Cleaning
↓
Feature Engineering
↓
Dataset Preparation
↓
Train-Test Split
↓
Model Training
↓
Model Evaluation
↓
Feature Importance Analysis
↓
Model Export
```

---

## Feature Engineering

Pada dataset OULAD, dilakukan pembuatan fitur baru:

### avg_score

Rata-rata nilai assessment setiap siswa.

```text
avg_score = mean(score)
```

Fitur ini digunakan untuk merepresentasikan performa akademik pengguna.

### total_click

Jumlah aktivitas belajar pengguna pada Virtual Learning Environment.

```text
total_click = sum(sum_click)
```

Fitur ini digunakan untuk merepresentasikan keterlibatan pengguna dalam proses pembelajaran.

### needs_remedial

Target klasifikasi yang dibuat dari `final_result`.

Aturan:

```text
Fail       → 1
Withdrawn  → 1
Pass       → 0
Distinction → 0
```

---

## Baseline Model

Model baseline yang digunakan:

1. Logistic Regression
2. Random Forest

Hasil baseline pada dataset OULAD:

| Model               | Accuracy | Catatan                          |
| ------------------- | -------: | -------------------------------- |
| Logistic Regression |   73.92% | Accuracy lebih tinggi            |
| Random Forest       |   73.13% | Recall kelas remedial lebih baik |

Pada konteks EduPath AI, recall untuk kelas `needs_remedial = 1` penting karena sistem perlu mendeteksi pengguna yang membutuhkan bantuan belajar.

---

## Topic Accuracy Model

Dataset dummy EduPath v2 digunakan untuk simulasi model berbasis `topic_accuracy`.

Hasil model menunjukkan bahwa fitur paling berpengaruh adalah:

1. `topic_accuracy`
2. `pre_test_score`
3. `wrong_answers`
4. `correct_answers`

Temuan ini mendukung konsep utama EduPath AI bahwa pemahaman per topik lebih relevan untuk mendeteksi kebutuhan remedial dibandingkan hanya melihat nilai akhir.

Catatan penting:

Hasil akurasi pada dataset dummy tidak diklaim sebagai performa dunia nyata. Dataset dummy digunakan sebagai proof of concept untuk menunjukkan struktur data ideal EduPath AI.

---

## How to Run

### 1. Clone Repository

```bash
git clone https://github.com/ZeroB7/EduPath-AI.git
cd EduPath-AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Aktifkan environment:

```bash
source venv/Scripts/activate
```

atau pada CMD Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Siapkan Dataset Mentah

Masukkan file OULAD ke folder:

```text
dataset/raw/
```

Contoh:

```text
dataset/raw/studentInfo.csv
dataset/raw/studentAssessment.csv
dataset/raw/studentVle.csv
dataset/raw/vle.csv
```

### 5. Jalankan Data Preparation

```bash
python notebooks/01_data_preparation.py
```

Output:

```text
dataset/processed/edupath_dataset_v1.csv
```

### 6. Jalankan Baseline Model

```bash
python notebooks/02_train_baseline_model.py
```

### 7. Jalankan Random Forest Model

```bash
python notebooks/03_random_forest_model.py
```

### 8. Jalankan Notebook Topic Accuracy

Buka dan jalankan:

```text
notebooks/04_train_dummy_topic_accuracy_model.ipynb
```

---

## Current Status

Status project saat ini:

* Dataset OULAD berhasil diproses.
* Dataset EduPath v1 berhasil dibuat.
* Baseline model berhasil dilatih.
* Random Forest berhasil dievaluasi.
* Dataset dummy EduPath v2 berbasis `topic_accuracy` berhasil dibuat.
* Model simulasi berbasis `topic_accuracy` berhasil dilatih.
* Model dan encoder berhasil disimpan ke folder `models/`.

---

## Limitations

Project ini masih berada pada tahap MVP dan proof of concept.

Beberapa keterbatasan:

1. Dataset OULAD belum memiliki informasi akurasi per topik.
2. Dataset dummy v2 masih berupa simulasi, bukan data pengguna nyata.
3. Model belum terintegrasi penuh dengan backend aplikasi.
4. Sistem rekomendasi materi masih dirancang sebagai tahap lanjutan.
5. Continuous learning belum diterapkan pada tahap MVP.

---

## Future Development

Pengembangan berikutnya:

1. Integrasi model dengan backend.
2. Pembuatan API prediksi remedial.
3. Pembuatan dashboard pengguna.
4. Pengumpulan data pengguna nyata.
5. Perhitungan `topic_accuracy` dari hasil quiz real.
6. Rekomendasi materi berdasarkan topik lemah.
7. Continuous model improvement berdasarkan data pengguna baru.

---

## Conclusion

EduPath AI merupakan platform pembelajaran adaptif berbasis Machine Learning yang bertujuan membantu mengidentifikasi kebutuhan remedial pengguna berdasarkan data pembelajaran.

Pada tahap awal, project menggunakan OULAD sebagai baseline dataset dan dataset dummy EduPath v2 sebagai simulasi data ideal berbasis `topic_accuracy`.

Hasil eksperimen menunjukkan bahwa indikator pemahaman per topik memiliki peran penting dalam menentukan apakah pengguna membutuhkan remedial.

Project ini menjadi fondasi awal untuk membangun sistem pembelajaran yang lebih personal, adaptif, dan berbasis data.
