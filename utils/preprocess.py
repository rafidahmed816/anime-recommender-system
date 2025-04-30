import pandas as pd
def combine_features(row):
    return f"{row['Synopsis']} {row['Genres'] if pd.notna(row['Genres']) else ''} {row['Themes'] if pd.notna(row['Themes']) else ''}"
