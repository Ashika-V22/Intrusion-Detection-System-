import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import pickle

# -----------------------------
# 1. Load NSL-KDD dataset
# -----------------------------
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

train_data = pd.read_csv("KDDTrain+.txt", names=columns)
test_data = pd.read_csv("KDDTest+.txt", names=columns)

# Drop 'difficulty_level'
train_data.drop(['difficulty_level'], axis=1, inplace=True)
test_data.drop(['difficulty_level'], axis=1, inplace=True)

print("Train shape:", train_data.shape)
print("Test shape:", test_data.shape)

# -----------------------------
# 2. Separate features and labels
# -----------------------------
X_train = train_data.drop('label', axis=1)
y_train = train_data['label']
X_test = test_data.drop('label', axis=1)
y_test = test_data['label']

# -----------------------------
# 3. Encode categorical features
# -----------------------------
cat_cols = ['protocol_type', 'service', 'flag']

# Create label encoders for each categorical column
le_protocol = LabelEncoder()
le_service = LabelEncoder()
le_flag = LabelEncoder()

X_train['protocol_type'] = le_protocol.fit_transform(X_train['protocol_type'])
X_train['service'] = le_service.fit_transform(X_train['service'])
X_train['flag'] = le_flag.fit_transform(X_train['flag'])

# Handle unseen test values
for col, le in zip(cat_cols, [le_protocol, le_service, le_flag]):
    X_test[col] = X_test[col].map(lambda s: le.transform([s])[0] if s in le.classes_ else -1)

# -----------------------------
# 4. Encode labels & handle unseen attacks
# -----------------------------
le_label = LabelEncoder()
y_train = le_label.fit_transform(y_train)
y_test = y_test.apply(lambda x: x if x in le_label.classes_ else 'normal')

# Ensure 'normal' is in classes_
if 'normal' not in le_label.classes_:
    le_label.classes_ = np.append(le_label.classes_, 'normal')

y_test = le_label.transform(y_test)

# -----------------------------
# 5. Balance dataset using SMOTE
# -----------------------------
class_counts = np.bincount(y_train)
min_class_count = class_counts[class_counts > 0].min()
k_neighbors = min(5, min_class_count - 1)

smote = SMOTE(k_neighbors=k_neighbors, random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)
print("Balanced training set shape:", X_train_bal.shape)

# -----------------------------
# 6. Train RandomForest
# -----------------------------
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_bal, y_train_bal)

# -----------------------------
# 7. Predict & evaluate
# -----------------------------
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# -----------------------------
# 8. Save model & encoders
# -----------------------------
print("\n💾 Saving model and encoders...")

pickle.dump(clf, open("rf_model.pkl", "wb"))
pickle.dump(le_protocol, open("le_protocol.pkl", "wb"))
pickle.dump(le_service, open("le_service.pkl", "wb"))
pickle.dump(le_flag, open("le_flag.pkl", "wb"))
pickle.dump(le_label, open("le_label.pkl", "wb"))

print("\n✅ All model and encoder files saved successfully!")