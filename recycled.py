import pandas as pd

df = pd.read_csv("recycled_volume.csv")

# Drops the first row and makes first index become zero index
df1 = df.iloc[1:].reset_index(drop = True)
df1

# Change column from Object to Numeric
# df1["304L_090319.1"].apply(type)
# df1["304L_090319.1"] = pd.to_numeric(df1["304L_090319.1"])

# Change column to only look at Volume Density % that is greater than 0
# df1 = df1[(df1["304L_090319.1"]) > 0]
# df1

# Get Volume Density column names and length
df.columns
volume_density = ["304L_090319.1", "304L_081519.1", "304L_090219.1",
                  "304L_090519.1", "304L_090619.1", "304L_082819.1",
                  "304L_083019.1", "304L_081619.1", "304L_082919.1",
                  "304L_081319.1"]
volume_density
length = len(volume_density)


for i in range(length):
    column_name = volume_density[i]
    df1[column_name] = pd.to_numeric(df1[column_name], errors = "coerce")
df1 = df1.dropna()
df1.apply(type)

df1 = df1([df1[volume_density]] > 0)