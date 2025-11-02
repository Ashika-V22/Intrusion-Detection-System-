# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# -----------------------------
# 1️⃣ Load dataset
# -----------------------------
# Replace with the path to your NSL-KDD training dataset
df = pd.read_csv("KDDTrain+.txt", header=None)

# -----------------------------
# 2️⃣ Assign column names (NSL-KDD standard)
columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label', 'difficulty_level'
]

df.columns = columns

# -----------------------------
# 3️⃣ Preprocess features
# -----------------------------
# Select features for training (you can add more if needed)
X = df[['duration', 'src_bytes', 'dst_bytes', 'count', 'srv_count']]  # example features

# Encode label: normal = 0, attack = 1
df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)
y = df['label']

# -----------------------------
# 4️⃣ Split dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -----------------------------
# 5️⃣ Train model
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# 6️⃣ Save trained model
# -----------------------------
with open("nsl_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as nsl_model.pkl")
