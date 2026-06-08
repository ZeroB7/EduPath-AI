import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# =========================
# 1. Load Dataset
# =========================
df = pd.read_csv("dataset/processed/edupath_dataset_v1.csv")

#==========================
# 2. Hapus Missing Value
# =========================
df = df.dropna()

# =========================
# 3. Encoding Data Kategori
# =========================
categorical_columns = [
    "gender",
    "highest_education",
    "age_band"
]

encoder = LabelEncoder()

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col])
    

# =========================
# 4. Fitur dan Target
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

# =========================
# 5. Split Dataset
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 6. Train Random Forest Classifier
# =========================
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

#==========================
# 7. Prediksi dan Evaluasi
# =========================
y_pred = rf_model.predict(X_test)

#==========================
# 8. Evaluasi Model
# =========================
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("\nRandom Forest Classifier Evaluation:")
print("Accuracy:", round(accuracy * 100, 2), "%")
print("\nConfusion Matrix:")
print(cm)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

#==========================
# 9. Feature Importance
# =========================
feature_importance = pd.DataFrame({
    "Feature": features,
    "Importance": rf_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(feature_importance)
