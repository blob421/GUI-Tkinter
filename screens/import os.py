import os

for k in ("PGUSER","PGPASSWORD","PGHOST","PGSERVICE","PGSERVICEFILE","PGPASSFILE"):
    print(k, os.getenv(k))