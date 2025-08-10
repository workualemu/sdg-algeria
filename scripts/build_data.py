# scripts/build_data.py
from sdg.open_sdg import open_sdg_build
import pandas as pd

def _clean_data(df, context):
    if "Value" in df.columns:
        s = df["Value"].astype(str)
        s = s.replace({"NaN":"", "nan":"", "N/A":"", "n/a":"", "..":""}, regex=False)
        s = s.str.replace(r"[,\u00A0]", "", regex=True)        # commas, NBSP
        s = s.str.replace(r"[<>~≈≤≥%]", "", regex=True)        # symbols/% signs
        df["Value"] = pd.to_numeric(s, errors="coerce")        # bad -> NaN

    for col in df.columns:
        low = col.strip().lower()
        if low in {"comment_obs","observation-level footnotes","source_detail","source details"}:
            df[col] = df[col].astype(str).str.strip().replace({"nan": ""})
    return df

if __name__ == "__main__":
    ok = open_sdg_build(
        config="config_data.yml",
        alter_data=_clean_data,          # <-- this wires your function in
    )
    if not ok:
        print("Build completed with validation warnings.")
