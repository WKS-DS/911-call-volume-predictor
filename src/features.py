import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://williamscott@localhost:5432/dispatch_911"
engine = create_engine(DATABASE_URL)

query = """
SELECT 
    DATE(datetime) as date,
    year,
    month,
    day_of_week,
    hour,
    COUNT(*) as call_count
FROM calls
GROUP BY DATE(datetime), year, month, day_of_week, hour
ORDER BY date, hour
"""

print("Aggregating calls by hour...")
df = pd.read_sql(query, engine)

print(f"Created {len(df)} hourly records")
print(df.head(10))

df.to_sql('hourly_calls', engine, if_exists='replace', index=False)
print("Saved to 'hourly_calls' table")