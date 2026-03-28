import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/AllData_PreEDM_Virgin_RowColIDs_correcteddates.csv")

# Convert BuildDate column to date time
df["BuildDate"] = pd.to_datetime(df["BuildDate"], format="%m/%d/%y", errors="coerce")

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
# print(summary)

# filter out scraps
tolerances_boundaries = {
    "B3_DATUM_B_LOC": (0.415, 0.435),
    "B3_REF_OD": (0.445, 0.469),
    "C1_LOC_INSIDE_PLN": (0.049, 0.06),
    "C4_LOC_TOP_PLN": (0.261, 0.281),
    "B3_THICK1_WALL": (0.010, 0.017),
    "B3_THICK2_WALL": (0.010, 0.017),
    "B3_THICK3_WALL": (0.010, 0.017),
    "B3_THICK4_WALL": (0.010, 0.017),
}

def filter_within_tolerance(dataframe, tolerances):
    df_copy = dataframe.copy()
    within_tol_all = np.ones(len(df_copy), dtype=bool)
    for col, (lo, hi) in tolerances.items():
        if col in df_copy.columns:
            within_tol = (df_copy[col] >= lo) & (df_copy[col] <= hi)
            within_tol_all &= within_tol
    
    # remove rows within tolerance (keeping the scraps)
    return df_copy[~within_tol_all].copy()

# cups that are scraps
df_scraps = filter_within_tolerance(df_clean, tolerances_boundaries)
print(df_scraps.columns)
# print("Total rows:", len(df_clean))
# print("Scraps rows:", len(df_scraps))

# bar plot: number of scraps vs build plate layout
counts = df_scraps.groupby("Layout").size()
sns.barplot(x=counts.index, y=counts.values)
plt.title("Scrap Count by Build Plate Type for Virgin Powder")
plt.ylabel("Scrap Count")
plt.xlabel("Build Playe Type (Layout)")
plt.show()

# bar plot: percentage of scraps vs build plate layout
counts_total = df_clean.groupby("Layout").size()
sns.barplot(x=counts.index, y=counts.values/counts_total.values)
plt.title("Scrap Rate by Build Plate Type for Virgin Powder")
plt.ylabel("Scrap Rate (%)")
plt.xlabel("Build Playe Type (Layout)")
plt.show()

# heatmap
def plot_scrap_count_heatmap(dataframe, layouts=("6X6", "6X6TA", "11X11TA")):
    df_copy = dataframe.copy()

    for layout in layouts:
        df_subset = df_copy[df_copy["Layout"] == layout]

        # scrap count per location
        count = (df_subset.groupby(["RowID","ColID"])
                    .size()
                    .unstack(fill_value=0)
                    .sort_index(axis=0)
                    .sort_index(axis=1))

         # set grid size
        if layout.startswith("6X6"):
            n = 6
            # map observed row/col indices to 1-6
            row_vals = list(count.index)
            col_vals = list(count.columns)
            row_map = {v: i+1 for i, v in enumerate(sorted(row_vals)[:6])}
            col_map = {v: i+1 for i, v in enumerate(sorted(col_vals)[:6])}
            count = count.rename(index=row_map, columns=col_map)
        else:
            n = 11

        # ensure a full n×n canvas
        count = count.reindex(index=range(1, n+1), columns=range(1, n+1), fill_value=0)

        # plot
        plt.figure()
        plt.imshow(count.values)
        plt.title(f"Scrap Count by Location — {layout}")
        plt.xlabel("ColID")
        plt.ylabel("RowID")

        # tick labels
        plt.xticks(ticks=np.arange(n), labels=range(1, n+1))
        plt.yticks(ticks=np.arange(n), labels=range(1, n+1))

        # annotate each cell
        for i in range(n):
            for j in range(n):
                val = count.values[i, j]
                plt.text(j, i, f"{int(val)}", ha="center", va="center")

        plt.colorbar()
        plt.tight_layout()
        plt.show()

# plot heatmaps
plot_scrap_count_heatmap(df_scraps)

