import os
import sys


REQUIRED_VARIABLES = (
    "APP_ENV",
    "INVENTORY_REGION",
)


missing = [name for name in REQUIRED_VARIABLES if not os.getenv(name)]

if missing:
    print(
        "Configuration error: required environment variable(s) missing: "
        + ", ".join(missing),
        file=sys.stderr,
    )
    raise SystemExit(1)

print(
    "Configuration valid: "
    f"APP_ENV={os.environ['APP_ENV']}, "
    f"INVENTORY_REGION={os.environ['INVENTORY_REGION']}"
)
