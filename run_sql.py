#!/usr/bin/env python3
import sys
import duckdb

sql_file = sys.argv[1] if len(sys.argv) > 1 else 'queries.sql'

with open(sql_file, 'r') as f:
    query = f.read().strip()

con = duckdb.connect()
result = con.execute(query)
print(result.df().to_string(index=False))
con.close()
