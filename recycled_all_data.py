import pandas as pd


df = pd.read_csv("AllData_PreEDM_Recycled_RowColIDs_correcteddates.csv")

df.BuildDate.dtype  # BuildDate type is Object
df["BuildDate"] = pd.to_datetime(df["BuildDate"], format = "%m/%d/%y", errors = "coerce")
df.BuildDate.dtype # BuildDate type is date-time

# Filters by the correct dates (8/29-8/30, 9/2-9/6)
df11x11TA = df[(df.Layout == "11X11TA")]
df11x11TA["BuildDate"]

correct_key = {
    "L": {"date": "2019-08-29"},
    "M": {"date": "2019-08-30"},
    "N": {"date": "2019-09-02"},
    "O": {"date": "2019-09-03"},
    "P": {"date": "2019-09-04"},
    "Q": {"date": "2019-09-05"},
    "R": {"date": "2019-09-06"},
}
df11x11TA
df_correct = pd.DataFrame(columns = df11x11TA.columns.tolist())
df_correct
for i, row in df11x11TA.iterrows():
    plateID = row["PlateID"].strip().upper()

    if plateID in correct_key and pd.notnull(row["BuildDate"]):
        if row["BuildDate"].strftime("%Y-%m-%d") == correct_key[plateID]["date"]:
            df_correct = pd.concat([df_correct, pd.DataFrame([row])], ignore_index = True)
        else:
            print(row["BuildDate"].strftime("%Y-%m-%d"), " not equal to ", correct_key[plateID]["date"])
df_correct
df_scraps = df_correct.copy()

df_correct = df_correct[((df_correct["B3_DATUM_B_LOC"] >= 0.415) & (df_correct["B3_DATUM_B_LOC"] <= 0.435)) &
                        ((df_correct["B3_REF_OD"] >= 0.445) & (df_correct["B3_REF_OD"] <= 0.469)) &
                        ((df_correct["C1_LOC_INSIDE_PLN"] >= 0.049) & (df_correct["C1_LOC_INSIDE_PLN"] <= 0.060)) &
                        ((df_correct["C4_LOC_TOP_PLN"] >= 0.261) & (df_correct["C4_LOC_TOP_PLN"] <= 0.281)) &
                        ((df_correct["B3_THICK1_WALL"] >= 0.010) & (df_correct["B3_THICK1_WALL"] <= 0.017)) &
                        ((df_correct["B3_THICK2_WALL"] >= 0.010) & (df_correct["B3_THICK2_WALL"] <= 0.017)) &
                        ((df_correct["B3_THICK3_WALL"] >= 0.010) & (df_correct["B3_THICK3_WALL"] <= 0.017)) &
                        ((df_correct["B3_THICK4_WALL"] >= 0.010) & (df_correct["B3_THICK4_WALL"] <= 0.017))]
df_correct

df_scraps = df_scraps.drop(df_correct.index)
df_scraps