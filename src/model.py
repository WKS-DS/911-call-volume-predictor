import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

DATABASE_URL = "postgresql://williamscott@localhost:5432/dispatch_911"
engine = create_engine(DATABASE_URL)

# Load data
print("Loading data...")
df = pd.read_sql("SELECT * FROM hourly_calls", engine)

# Features and target
X = df[['year', 'month', 'day_of_week', 'hour']]
y = df['call_count']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set: {len(X_train)} rows")
print(f"Test set: {len(X_test)} rows")

# Train
print("Training model...")
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nResults:")
print(f"MAE: {mae:.2f} calls")
print(f"R2 Score: {r2:.3f}")

# Save model
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("\nModel saved to models/model.pkl")