# scripts/check_data.py
from sdg.open_sdg import open_sdg_check
from build_data import _clean_data

if __name__ == "__main__":
    ok = open_sdg_check(
        config="config_data.yml",
        alter_data=_clean_data,   # run the same cleaner during validation
    )
    if not ok:
        print("Validation errors found (proceeding anyway).")
