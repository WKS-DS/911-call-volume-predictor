import pandas as pd
from sqlalchemy import create_engine

# Database connection
DATABASE_URL = "postgresql://williamscott@localhost:5432/dispatch_911"
engine = create_engine(DATABASE_URL)

# Load CSV
print("Loading CSV...")
df = pd.read_csv('data/seattle_fire_911.csv')

# Clean column names (lowercase, no spaces)
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Convert datetime
df['datetime'] = pd.to_datetime(df['datetime'])

# Load to PostgreSQL
print("Loading to PostgreSQL...")
df.to_sql('calls', engine, if_exists='replace', index=False)

print(f"Done! Loaded {len(df)} rows to 'calls' table.")