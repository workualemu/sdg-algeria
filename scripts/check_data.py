from sdg.open_sdg import open_sdg_check
from build_data import _clean_data  # or duplicate the function

validation_successful = open_sdg_check(config="config_data.yml", alter_data=_clean_data)
# Validate the indicators.
# validation_successful = open_sdg_check(config='config_data.yml')

# If everything was valid, perform the build.
if not validation_successful:
    print("Validation errors found (proceeding anyway).")
    # raise Exception('There were validation errors. See output above.')
