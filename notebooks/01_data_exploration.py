import pandas as pd


def load_data():
    student_info = pd.read_csv("dataset/raw/studentInfo.csv")
    student_assessment = pd.read_csv("dataset/raw/studentAssessment.csv")
    student_vle = pd.read_csv("dataset/raw/studentVle.csv")

    return student_info, student_assessment, student_vle


def create_features(student_assessment, student_vle):
    avg_score = (
        student_assessment
        .groupby("id_student")["score"]
        .mean()
        .reset_index()
        .rename(columns={"score": "avg_score"})
    )

    total_click = (
        student_vle
        .groupby("id_student")["sum_click"]
        .sum()
        .reset_index()
        .rename(columns={"sum_click": "total_click"})
    )

    return avg_score, total_click


def build_edupath_dataset(student_info, avg_score, total_click):
    student_master = student_info[
        [
            "id_student",
            "gender",
            "highest_education",
            "age_band",
            "num_of_prev_attempts",
            "studied_credits",
            "final_result"
        ]
    ]

    edupath_df = student_master.merge(
        avg_score,
        on="id_student",
        how="inner"
    )

    edupath_df = edupath_df.merge(
        total_click,
        on="id_student",
        how="inner"
    )

    edupath_df["needs_remedial"] = edupath_df["final_result"].apply(
        lambda x: 1 if x in ["Fail", "Withdrawn"] else 0
    )

    return edupath_df


def main():
    student_info, student_assessment, student_vle = load_data()

    print("Data Loaded")
    print("student_info:", student_info.shape)
    print("student_assessment:", student_assessment.shape)
    print("student_vle:", student_vle.shape)

    avg_score, total_click = create_features(
        student_assessment,
        student_vle
    )

    edupath_df = build_edupath_dataset(
        student_info,
        avg_score,
        total_click
    )

    print("\nEduPath Dataset Preview:")
    print(edupath_df.head())

    print("\nDataset Shape:")
    print(edupath_df.shape)

    print("\nDistribusi needs_remedial:")
    print(edupath_df["needs_remedial"].value_counts())

    edupath_df.to_csv(
        "dataset/processed/edupath_dataset_v1.csv",
        index=False
    )

    print("\nDataset berhasil disimpan ke:")
    print("dataset/processed/edupath_dataset_v1.csv")


if __name__ == "__main__":
    main()