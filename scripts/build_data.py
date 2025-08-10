# scripts/build_data.py
from sdg.open_sdg import open_sdg_build
import pandas as pd

def _clean_data(df, context):
    """
    Alteration hook to normalize numeric 'Value' and trim whitespace in text fields.
    Runs for every indicator dataframe during build.
    """
    # Debug so you can confirm the hook is actually running in CI logs
    try:
        ind = (context or {}).get("indicator_id")
        if ind:
            print(f"[alter_data] cleaning {ind}")
    except Exception:
        pass

    # Normalize Value column -> numeric
    if "Value" in df.columns:
        s = df["Value"].astype(str).str.strip()
        # Normalize common "missing" tokens from upstream APIs
        s = s.str.replace(r'^(?i:na|nan|null|n/a)$', '', regex=True)
        s = s.replace({"NaN": "", "nan": "", "N/A": "", "n/a": "", "..": ""}, regex=False)
        # Remove formatting characters/symbols
        s = s.str.replace(r"[,\u00A0]", "", regex=True)        # commas, NBSP
        s = s.str.replace(r"[<>~≈≤≥%]", "", regex=True)        # symbols and percent signs
        # Coerce to numeric (bad values -> NaN)
        df["Value"] = pd.to_numeric(s, errors="coerce")

    # Trim whitespace in all object/text columns (helps avoid trailing/leading warnings)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip().replace({"nan": ""})

    return df


if __name__ == "__main__":
    ok = open_sdg_build(
        config="config_data.yml",
        alter_data=_clean_data,   # <-- wire the alteration hook
    )
    if not ok:
        print("Build completed with validation warnings.")
