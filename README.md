# Farm Dashboard 🌾📊

A simple yet powerful **Dash** application to help farmers monitor real-time and historical environmental indicators such as **temperature**, **humidity**, and **soil pH**. This dashboard provides dynamic visualizations and live updates to support better agricultural decision-making.

---

## 📌 Features

- 📈 Real-time chart updates for selected devices and variables.
- 🌡️ Temperature gauge with dynamic coloring.
- 💧 Humidity and pH gauges.
- 📊 Interactive dropdowns to filter data by device and variable.
- 🎨 Responsive layout and custom styles.

---

## 🗂️ Project Structure

```
Smart_Farming/
├── dash_components.py   # Custom components: temperature, humidity, and pH gauges.
├── ra_os.py            # Entry point to run the Dash app.
├── requirements.txt    # Python dependencies.
├── dashboard.py        # Main dashboard layout and logic.
└── assets/             # Folder for CSS and static assets
   └── styles.css # Custom styles to remove white space and style the app.
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/e-Yasmina/Smart_Farming.git
cd farm_dashboard
```

### 2. Install dependencies
It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

```

### 3. Run the app
It's recommended to use a virtual environment:

```bash
python ra_os.py
```
Open your browser and go to: http://127.0.0.1:8050/

---

## 📦 Dependencies

Main libraries used:

- Dash
- Plotly
- Dash DAQ
- pandas
- numpy

See `requirements.txt` for the full list.

---

## 📚 Usage

This dashboard simulates environmental data generation for a farm and presents it visually in real time. You can:

- **Choose a device** (e.g., `ferme anoljdid`).
- **Select a variable** like temperature, humidity, or soil pH.
- **Watch live updates** on the graph and gauges every 5 seconds.

This tool can easily be extended to integrate with actual IoT sensors or backend APIs.

---

## 📌 Notes

- The current version uses randomly generated synthetic data for demonstration.
- You can adapt the `generate_historical_and_real_time_data()` function to pull from a real data source.

---

## 🧑‍🌾 Motivation

This project was built as a simple tool to assist farmers in tracking crucial indicators that affect soil health and crop yield. By making data easy to understand, we aim to empower better farming decisions.

---

## 🙌 Acknowledgements

Thanks to the Dash and Plotly teams for the excellent libraries that made this possible.