import joblib
import os

# Load your existing model
model = joblib.load("rf_model.pkl")

# Save it in a compressed form
joblib.dump(model, "rf_model_compressed.pkl", compress=3)

# Show size comparison
old_size = os.path.getsize("rf_model.pkl") / (1024 * 1024)
new_size = os.path.getsize("rf_model_compressed.pkl") / (1024 * 1024)

print("✅ Model compressed successfully!")
print(f"Original size: {old_size:.2f} MB")
print(f"Compressed size: {new_size:.2f} MB")
