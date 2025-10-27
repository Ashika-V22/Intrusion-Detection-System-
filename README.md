
**🛡️ Intrusion Detection System (IDS) using NSL-KDD Dataset**

 **📘 Overview**

This project implements a Machine Learning–based Intrusion Detection System (IDS) using the NSL-KDD dataset. The system detects and classifies network connections as normal or attack.
It combines data preprocessing, Random Forest classification, and two user interfaces — a Tkinter-based GUI and a Streamlit web app.

---

## 🧩 Project Structure

| File                                                               | Description                                                                         |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| `train_model.py`                                                   | Trains the Random Forest model on the NSL-KDD dataset and generates `nsl_model.pkl` |
| `ids_model.py`                                                     | Handles model loading, preprocessing, and prediction logic                          |
| `idu_gui.py`                                                       | Provides a desktop GUI interface built using Tkinter                                |
| `app.py`                                                           | Streamlit web application for browser-based intrusion detection                     |
| `le_flag.pkl`, `le_label.pkl`, `le_protocol.pkl`, `le_service.pkl` | Label encoder files used during feature transformation                              |
| `rf_model.pkl` / `nsl_model.pkl`                                   | Trained Random Forest model files                                                   |

---

## ⚙️ Technologies Used

**Programming Language:**

* Python 3.11

**Libraries & Frameworks:**

* `numpy`
* `pandas`
* `scikit-learn`
* `imbalanced-learn`
* `joblib`
* `streamlit`
* `tkinter`

---

## 🧠 Machine Learning Details

* **Algorithm Used:** Random Forest Classifier
* **Dataset:** NSL-KDD
* **Objective:** Classify incoming network data as *Normal* or *Attack*
* **Model Persistence:** Models and encoders are serialized using `joblib`

---

## 🧾 Setup and Execution

### Step 1: Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### Step 2: Install dependencies

```bash
pip install numpy pandas scikit-learn imbalanced-learn streamlit joblib
```

### Step 3: Train the model

```bash
python train_model.py
```

This will generate the model file `nsl_model.pkl`.

### Step 4: Run the Tkinter GUI application

```bash
python idu_gui.py
```

### Step 5: Run the Streamlit web application

```bash
streamlit run app.py
```
**🖼️ Input & Output Examples**
🧩 GUI Interface (Tkinter)
INPUT:
<img width="1920" height="1008" alt="Screenshot 2025-10-27 163509" src="https://github.com/user-attachments/assets/7182a0b5-a926-4ad1-b924-91798d893c73" />

OUTPUT:
<img width="1920" height="1008" alt="Screenshot 2025-10-27 163525" src="https://github.com/user-attachments/assets/dcab9d96-d769-4c3e-b610-6151797910d4" />

**🌐 Web Interface (Streamlit)**
INPUT:
<img width="930" height="481" alt="image" src="https://github.com/user-attachments/assets/94bd316a-50d2-4cda-a7ba-1a66841d6b70" />

OUTPUT:
<img width="930" height="480" alt="image" src="https://github.com/user-attachments/assets/f2d20740-ddde-4e1b-b141-bf73643b9b26" />


---

## 📦 Output Files

| File                             | Purpose                                 |
| -------------------------------- | --------------------------------------- |
| `rf_model.pkl` / `nsl_model.pkl` | Trained Random Forest model             |
| `le_*.pkl`                       | Label encoders for categorical features |
| GUI Interface                    | Tkinter desktop application             |
| Web App                          | Streamlit-based web application         |

---

## 🔍 Key Features

* Preprocessing and encoding of NSL-KDD dataset
* Training and evaluation using Random Forest Classifier
* Dual interfaces: GUI (Tkinter) and Web (Streamlit)
* Serialized model and encoders for efficient reuse
* Clear separation between training, modeling, and deployment

---

## 💡 Future Enhancements

* Integration with real-time network traffic monitoring
* Advanced model comparison (e.g., XGBoost, Neural Networks)
* Visualization dashboard for attack statistics
* Cloud deployment via Streamlit Community Cloud or Heroku

---

## 👩‍💻 Author

**Ashika V**
Bachelor of Engineering in Artificial Intelligence & Machine Learning


