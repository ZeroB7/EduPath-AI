import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# =========================
# 1. Load Dataset
# =========================
df = pd.read_csv("dataset/processed/edupath_dataset_v1.csv")

print("Dataset Preview:")
print(df.head())

print("\nShape Awal:")
print(df.shape)


# =========================
# 2. Cek Missing Value
# =========================
print("\nMissing Values Sebelum Cleaning:")
print(df.isnull().sum())


# =========================
# 3. Hapus Missing Value
# =========================
df = df.dropna()

print("\nMissing Values Setelah Cleaning:")
print(df.isnull().sum())

print("\nShape Setelah Cleaning:")
print(df.shape)


# =========================
# 4. Cek Distribusi Target
# =========================
print("\nTarget Distribution:")
print(df["needs_remedial"].value_counts())


# =========================
# 5. Encoding Data Kategori
# =========================
categorical_columns = [
    "gender",
    "highest_education",
    "age_band"
]

encoder = LabelEncoder()

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col])


print("\nDataset Setelah Encoding:")
print(df.head())


# =========================
# 6. Pilih Feature dan Target
# =========================
features = [
    "gender",
    "highest_education",
    "age_band",
    "num_of_prev_attempts",
    "studied_credits",
    "avg_score",
    "total_click"
]

target = "needs_remedial"

X = df[features]
y = df[target]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y, 
    test_size=0.2, 
    random_state=42
)

# Model
model = LogisticRegression(max_iter=1000)

# Training
model.fit(X_train, y_train)

# Prediksi
y_pred = model.predict(X_test)

# Akurasi
accuracy = accuracy_score(y_test, y_pred)

cm = confusion_matrix(y_test, y_pred)


print("\nFeature X:")
print(X.head())

print("\nTarget y:")
print(y.head())

print("\nX Train Shape:")
print(X_train.shape)

print("\nX Test Shape:")
print(X_test.shape)

print("\ny Train Shape:")
print(y_train.shape)

print("\ny Test Shape:")
print(y_test.shape)

print("\nAccuracy:")
print(round(accuracy * 100, 2), "%")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =========================
# Catatan penting:
# final_result tidak dipakai sebagai feature
# karena needs_remedial dibuat dari final_result
# jika dipakai, akan terjadi data leakage
# =========================