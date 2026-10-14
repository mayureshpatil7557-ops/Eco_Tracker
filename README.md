# 🌿 EcoTrack — Personal Carbon Footprint Estimator

**Understand your impact. Make greener choices. Build a sustainable future.**

EcoTrack is a web-based carbon footprint estimation application built using Python and Flask. It helps users understand the estimated environmental impact of their everyday lifestyle, including transportation, household electricity consumption, and dietary habits.

The application converts user inputs into estimated carbon emissions and presents the results through visual charts, comparison metrics, and practical eco-friendly recommendations.

## ✨ Features

- 🌍 **Carbon Footprint Estimation** — Estimate daily, monthly, and annual emissions.
- 🚗 **Transportation Analysis** — Calculate estimated emissions based on travel mode and daily distance.
- ⚡ **Electricity Analysis** — Estimate household electricity emissions while accounting for household size.
- 🥗 **Food Habit Analysis** — Include dietary choices in the overall footprint estimate.
- 📊 **Visual Results Dashboard** — View the contribution of different lifestyle activities.
- 🌱 **Eco Action Plan** — Receive practical suggestions for reducing everyday environmental impact.
- 🌙 **Modern Dark UI** — A dark, green-accented interface designed for a clean and engaging experience.
- 📱 **Responsive Design** — Designed to adapt to different screen sizes.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and calculations |
| Flask | Web framework and routing |
| HTML5 | Page structure |
| CSS3 | Styling, responsive layouts, and animations |
| JavaScript | Client-side interactivity where applicable |
| Chart.js | Visualizing footprint results |

## 📂 Project Structure

```text
Eco_Tracker/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── lifestyle.html
│   └── results.html
└── static/
    └── style.css
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/mayureshpatil7557-ops/Eco_Tracker.git
```

### 2. Open the project directory

```bash
cd Eco_Tracker
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

### 6. Open EcoTrack

Visit the following address in your browser:

```text
http://127.0.0.1:5000
```

## 🧮 How It Works

1. Open the EcoTrack home page.
2. Enter lifestyle information on the calculator page.
3. Provide transportation type, daily travel distance, electricity consumption, household size, and diet type.
4. Submit the form to calculate the estimated carbon footprint.
5. Review the daily, monthly, and annual estimates.
6. Explore the visual breakdown and suggested sustainability actions.

## 📈 Emission Calculation

EcoTrack estimates emissions using illustrative emission factors for transportation, electricity, and diet.

**Daily footprint:**

```text
Daily Footprint =
Transport Emissions
+ Electricity Emissions
+ Food Emissions
```

Monthly and annual estimates are calculated as:

```text
Monthly Footprint = Daily Footprint × 30

Annual Footprint = Daily Footprint × 365
```

For car travel, estimated transport emissions are adjusted by the number of passengers. Household electricity emissions are divided by the number of people sharing the household electricity use.

**Note:** The current factors are illustrative estimates intended for educational demonstration. Results are not precise measurements or official carbon-accounting assessments.

## 🎯 Project Objectives

- Build an interactive web application for estimating personal carbon footprints.
- Demonstrate how everyday lifestyle choices contribute to estimated emissions.
- Present numerical results in an understandable visual format.
- Encourage sustainable habits through practical recommendations.
- Apply Python, Flask, frontend development, and data visualization skills in a complete project.

## 🔮 Future Scope

- Integrate region-specific and verified emission-factor datasets.
- Add user accounts and historical footprint tracking.
- Compare footprint estimates across different periods.
- Include more lifestyle categories, such as waste and shopping.
- Deploy the application online for public access.

## 👨‍💻 Author

**Mayuresh Patil**

GitHub: [@mayureshpatil7557-ops](https://github.com/mayureshpatil7557-ops)

## 📄 License

This project is intended for educational and demonstration purposes. A formal open-source license can be added if the project is to be distributed or reused by others.
