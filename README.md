# ✈️ Aviation Navigation Data
*A portfolio project simulating the work of an Aviation Data Analyst*


![airways-chart](/aviation_chart.jpg)


---

## 🌍 Live Demo  
👉 [View Interactive Dashboard (GitHub Pages)](https://YOUR_USERNAME.github.io/aviation-navigation-data)  

This interactive map displays airports, navigation aids, and obstructions. It simulates how aviation data analysts process and visualise aeronautical information for safe flight operations.  

---

## 📌 Project Overview
This project explores how aeronautical information can be processed, validated, and transformed into digital maps and navigation charts that support safe flight operations.  

Using open dataset from **OpenAIP**, I built tools to:  
- ✅ Clean and validate navigation data for accuracy and flight safety  
- ✅ Create an **interactive cockpit-style dashboard** showing airports, airways, and obstructions  
- ✅ Generate **paper-style navigation charts** for mission planning and low-level flying  
- ✅ Develop a **mission route planner** that plots routes between airports using real navigation data  

The goal is to mirror the responsibilities of an **Aviation Data Analyst**, where navigation data is critical to ensuring safe and effective air operations.

---

## 🛠️ Tools & Technologies
- **Python** – Data processing and automation  
- **Pandas / GeoPandas** – Data cleaning and geospatial processing  
- **Folium** – Interactive mapping  
- **Matplotlib + Cartopy** – Paper-style navigation charts
- **GitHub Pages** – Hosting interactive maps  

---

## 🌍 Data Source
- [OpenAIP](https://openaip.net) – Airports, airspaces, obstructions and navaids

---

## 📂 Project Structure
```
│
├── data/
│   ├── raw/                  # Unprocessed datasets
│   ├── processed/            # Cleaned datasets
│
├── notebooks/
│   ├── 01_data_validation.ipynb
│   ├── 02_interactive_map.ipynb
│   ├── 03_paper_chart.ipynb
│   ├── 04_route_planner.ipynb
│
├── outputs/
│   ├── charts/               # PNG/PDF charts
│   ├── reports/              # Validation reports
│
├── scripts/
│   ├── validate_data.py
│   ├── generate_chart.py
│
├── requirements.txt
├── README.md
```

---

## 🚀 Features
- **Data Validation:** Automated checks for missing or invalid coordinates, unrealistic elevations, and outdated entries  
- **Interactive Dashboard:** A Folium-based map with airports, airways, and obstructions layered and filterable  
- **Paper-Style Charts:** High-resolution charts with airways, airports, and hazard markers for mission planning  
- **Route Planner:** Input departure & destination ICAO codes → outputs route with distance and chart visualization  

---

## 📸 Screenshots / Examples
*(Add here once charts and maps are ready)*  

---

## ⚙️ Setup Guide

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository
```
git clone https://github.com/YOUR_USERNAME/aviation-navigation-data.git
cd aviation-navigation-data
```

### 2. Create a Virtual Environment (Recommended)
```
# Create environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Requirements
```
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook
```
jupyter notebook
```

This will open Jupyter in your browser. Navigate to the notebooks/ folder and start with `01_data_validation.ipynb.`

✅ If everything installs without errors, you’re ready to explore the project!
