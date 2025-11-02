import tkinter as tk
from tkinter import messagebox
import pickle

# -----------------------------
# Load model and encoders (must exist in same folder)
# -----------------------------
try:
    clf = pickle.load(open("rf_model.pkl", "rb"))
    le_protocol = pickle.load(open("le_protocol.pkl", "rb"))
    le_service = pickle.load(open("le_service.pkl", "rb"))
    le_flag = pickle.load(open("le_flag.pkl", "rb"))
    le_label = pickle.load(open("le_label.pkl", "rb"))
except FileNotFoundError:
    tk.Tk().withdraw()
    messagebox.showerror("Missing files",
                         "Model/encoder files (rf_model.pkl, le_*.pkl) not found.\nRun ids_model.py first.")
    raise SystemExit

# -----------------------------
# All 41 features used by model
# -----------------------------
features = [
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
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

# -----------------------------
# Example inputs (normal + attack)
# -----------------------------
normal_example = {
    'duration': 10, 'protocol_type': 'tcp', 'service': 'http', 'flag': 'SF',
    'src_bytes': 181, 'dst_bytes': 5450, 'land': 0, 'wrong_fragment': 0, 'urgent': 0,
    'hot': 0, 'num_failed_logins': 0, 'logged_in': 1, 'num_compromised': 0,
    'root_shell': 0, 'su_attempted': 0, 'num_root': 0, 'num_file_creations': 0,
    'num_shells': 0, 'num_access_files': 0, 'num_outbound_cmds': 0, 'is_host_login': 0,
    'is_guest_login': 0, 'count': 5, 'srv_count': 3, 'serror_rate': 0.0,
    'srv_serror_rate': 0.0, 'rerror_rate': 0.0, 'srv_rerror_rate': 0.0,
    'same_srv_rate': 1.0, 'diff_srv_rate': 0.0, 'srv_diff_host_rate': 0.0,
    'dst_host_count': 255, 'dst_host_srv_count': 3, 'dst_host_same_srv_rate': 1.0,
    'dst_host_diff_srv_rate': 0.0, 'dst_host_same_src_port_rate': 1.0,
    'dst_host_srv_diff_host_rate': 0.0, 'dst_host_serror_rate': 0.0,
    'dst_host_srv_serror_rate': 0.0, 'dst_host_rerror_rate': 0.0,
    'dst_host_srv_rerror_rate': 0.0
}

attack_example = normal_example.copy()
attack_example.update({
    'duration': 2000, 'protocol_type': 'udp', 'service': 'private', 'flag': 'REJ',
    'src_bytes': 0, 'dst_bytes': 0, 'wrong_fragment': 2, 'hot': 5,
    'num_failed_logins': 2, 'logged_in': 0, 'count': 500, 'srv_count': 300,
    'serror_rate': 1.0, 'srv_serror_rate': 1.0, 'same_srv_rate': 0.1, 'diff_srv_rate': 0.9
})

# -----------------------------
# GUI functions
# -----------------------------
def fill_values(example_dict):
    # Fill each entry with example values (string)
    for f in features:
        entries[f].delete(0, tk.END)
        entries[f].insert(0, str(example_dict.get(f, "")))

def predict():
    # Read values, validate, encode categoricals and predict
    try:
        input_values = []
        for f in features:
            val = entries[f].get().strip()
            if val == "":
                messagebox.showwarning("Input missing", f"Please fill value for: {f}")
                return

            # categorical encoders
            if f == 'protocol_type':
                # transform if known, else map to -1 (unseen)
                if val in le_protocol.classes_:
                    val_enc = le_protocol.transform([val])[0]
                else:
                    # make a fallback numeric not seen before
                    val_enc = -1
                input_values.append(val_enc)
            elif f == 'service':
                if val in le_service.classes_:
                    val_enc = le_service.transform([val])[0]
                else:
                    val_enc = -1
                input_values.append(val_enc)
            elif f == 'flag':
                if val in le_flag.classes_:
                    val_enc = le_flag.transform([val])[0]
                else:
                    val_enc = -1
                input_values.append(val_enc)
            else:
                # numeric field
                try:
                    num = float(val)
                except ValueError:
                    messagebox.showerror("Type error", f"Field {f} needs a numeric value.")
                    return
                input_values.append(num)

        # model predict
        pred = clf.predict([input_values])[0]
        pred_label = le_label.inverse_transform([pred])[0]
        # Show result
        if pred_label.lower() in ("normal", "benign", "normal."):
            msg = f"✅ Result: NORMAL traffic ({pred_label})"
        else:
            msg = f"⚠ Result: ATTACK detected ({pred_label})"
        messagebox.showinfo("Prediction Result", msg)
    except Exception as e:
        messagebox.showerror("Error during prediction", str(e))

# -----------------------------
# Build the GUI: scrollable area + fixed bottom buttons
# -----------------------------
root = tk.Tk()
root.title("AI-based Intrusion Detection System (Demo)")
root.geometry("700x700")
root.configure(bg="#f7f7f7")

# Main frame holds canvas + scrollbar
main_frame = tk.Frame(root, bg="#f7f7f7")
main_frame.pack(fill="both", expand=True, padx=8, pady=8)

canvas = tk.Canvas(main_frame, bg="#f7f7f7")
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f7f7f7")

# configure scroll region
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# entries dictionary
entries = {}

# Add input rows inside scrollable frame
for i, f in enumerate(features):
    lbl = tk.Label(scrollable_frame, text=f, anchor='w', bg="#f7f7f7")
    lbl.grid(row=i, column=0, sticky='w', padx=6, pady=4)
    ent = tk.Entry(scrollable_frame, width=30)
    ent.grid(row=i, column=1, padx=6, pady=4)
    entries[f] = ent

# Bottom fixed frame for buttons (always visible)
bottom = tk.Frame(root, bg="#e9e9e9")
bottom.pack(fill="x", padx=8, pady=(0,8))

btn_normal = tk.Button(bottom, text="Fill Normal Traffic", command=lambda: fill_values(normal_example),
                       bg="#2E8B57", fg="white", width=20)
btn_attack = tk.Button(bottom, text="Fill Attack Traffic", command=lambda: fill_values(attack_example),
                       bg="#B22222", fg="white", width=20)
btn_check = tk.Button(bottom, text="Check Network Status", command=predict,
                      bg="#1E90FF", fg="white", width=25)

btn_normal.pack(side="left", padx=10, pady=10)
btn_attack.pack(side="left", padx=10, pady=10)
btn_check.pack(side="right", padx=10, pady=10)

# Helpful tip label
tip = tk.Label(bottom, text="Tip: use Fill buttons to auto-populate then click Check Network Status", bg="#e9e9e9")
tip.pack(side="left", padx=6)

root.mainloop()