# 📊 DDR Generator

A Streamlit-based web application that automatically generates structured **Daily Defect Reports (DDR)** from inspection and thermal data.

The system processes input data, generates organized reports, and visualizes severity statistics to support efficient defect analysis.

---

## 🚀 Features

- 📂 Upload inspection and thermal reports
- 🤖 Automatic DDR generation
- 📄 Structured Markdown report output
- 📊 Severity-based defect analysis
- 📁 JSON metadata generation
- 📈 Visual severity chart generation

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Matplotlib**
- **JSON**
- **Markdown**

---
## 🌐 Live Demo

The application is deployed on Streamlit Cloud and can be accessed here:

🔗 https://ddrgenerator-cuhch3uqkslelm5yuhvhvp.streamlit.app/


## 📁 Project Structure

```bash
DDR_GENERATOR/
│
├── app.py              # Streamlit frontend
├── main.py             # Core DDR generation logic
├── visualize.py        # Visualization logic
├── test_ddr.py         # Test script
├── requirements.txt    # Project dependencies
├── input/              # Input files
├── output/             # Generated reports and charts
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/DDR_GENERATOR.git
cd DDR_GENERATOR
```

Replace `YOUR-USERNAME` with your actual GitHub username.

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it (Windows):

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python -m streamlit run app.py
```

Then open your browser and visit:

```
http://localhost:8501
```

---

## 📊 Output Generated

The application generates the following files inside the `output/` directory:

- `generated_ddr.md`
- `metadata.json`
- `statistics.json`
- `severity_chart.png`

---

## 🌟 Future Enhancements

- PDF export functionality
- Cloud deployment (Streamlit Cloud)
- Advanced analytics dashboard
- Multi-user support

---

## 👩‍💻 Author

**Prachi Mishra**
