import duckdb
import pandas as pd

# Path to your duckdb file
duckdb_file = "data/company_master_data_2025_06_30.duckdb"

# Connect and export
con = duckdb.connect(duckdb_file, read_only=True)

# Export to CSV
con.execute("""
    COPY (
        SELECT * FROM company_master_data
    ) TO 'company_master_data_2025_06_30.csv' 
    (FORMAT CSV, HEADER TRUE)
""")

con.close()

print("✅ Conversion completed! File saved as: company_master_data_2025_06_30.csv")
