import os
import re
<<<<<<< HEAD
<<<<<<< HEAD
from datetime import date
=======
>>>>>>> dd65c14 (Updating all my assets to use dagster dbt handler, cleaning up the logic)
=======
from datetime import date
>>>>>>> 21c38e0 (Updating another Dagster Asset to use IO Manager)


def sanitize_filename(value: str) -> str:
    # Replace all non-word characters (anything other than letters, digits, underscore) with underscore
    no_whitespace = ''.join(value.split())
    ascii_only = no_whitespace.encode("ascii", errors="ignore").decode()
    return re.sub(r"[^\w\-_\.]", "_", ascii_only)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 21c38e0 (Updating another Dagster Asset to use IO Manager)


def json_converter(o):
    if isinstance(o, date):
        return o.isoformat()
    return str(o)
<<<<<<< HEAD
=======
>>>>>>> dd65c14 (Updating all my assets to use dagster dbt handler, cleaning up the logic)
=======
>>>>>>> 21c38e0 (Updating another Dagster Asset to use IO Manager)
