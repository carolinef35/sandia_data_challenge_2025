import pandas as pd

df = pd.read_csv("data/AllData_PreEDM_Virgin_RowColIDs_correcteddates.csv")

# Convert BuildDate column to date time
df["BuildDate"] = pd.to_datetime(df["BuildDate"], errors="coerce")

# Keep only virgin power
df = df[df["Powder"].str.lower().str.contains("virgin")]

# Define valid builds
valid_builds = {
    "A": {"date": "2019-08-05", "layout": "6X6"}, 
    "B": {"date": "2019-08-06", "layout": "6X6TA"},
    "C": {"date": "2019-08-07", "layout": "11X11TA"}, 
    "D": {"date": "2019-08-08", "layout": "11X11TA"},
    "E": {"date": "2019-08-09", "layout": "6X6"},
    "F": {"date": "2019-08-12", "layout": "6X6TA"}, 
    "G": {"date": "2019-08-13", "layout": "6X6TA"},
    "H": {"date": "2019-08-14", "layout": "11X11TA"}, 
    "I": {"date": "2019-08-15", "layout": "6X6"},
    "J": {"date": "2019-08-16", "layout": "11X11TA"},
    "K": {"date": "2019-08-28", "layout": "11X11TA"},
}

keep_rows = []
for i, row in df.iterrows():
    plate = str(row["PlateID"]).strip()
    layout = str(row["Layout"]).strip().upper()
    build_date = row["BuildDate"].strftime("%Y-%m-%d") if not pd.isna(row["BuildDate"]) else None
    # print(plate, layout, build_date)

    if plate in valid_builds:
        valid_date = valid_builds[plate]["date"]
        valid_layout = valid_builds[plate]["layout"]
        # print(valid_date, valid_layout)
        if layout == valid_layout and build_date == valid_date:
            keep_rows.append(True)
        else:
            keep_rows.append(False)
    else:
        keep_rows.append(False)

# print(keep_rows)
df_clean = df[keep_rows].copy()
summary = df_clean.groupby(["PlateID", "Layout", "BuildDate"]).size().reset_index(name="Count")
print(summary)

