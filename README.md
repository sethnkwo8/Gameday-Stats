# 🏟️ Gameday Stats

**Gameday Stats** is a full-stack web application built with **Django** that provides live football (soccer) data — including fixtures, scores, standings, and player statistics — for the **top five European leagues**:  
**Premier League**, **La Liga**, **Serie A**, **Bundesliga**, and **Ligue 1**. The reason I decided to develop this project is to be able to keep up with the ongoing football season and always stay up to date.

This project was developed as the **Final Project** for **CS50’s Web Programming with Python and JavaScript (CS50W)**.

---

## 🚀 Features

- ⚽ **Fixtures & Live Scores** — view current and upcoming matches across the top 5 leagues  
- 📊 **League Standings** — real-time league tables  
- 👤 **Player & Team Stats** — goals, assists, appearances, and more  
- 🌍 **Multi-API Integration** — powered by **API-Football** and **Football-Data.org**  
- 🧠 **Smart Data Handling** — uses different APIs for different endpoints for maximum accuracy  
- 🌙 **Responsive UI** — designed with Bootstrap and custom CSS  

---

## 🧰 Technologies Used

| Category | Tools |
|-----------|--------|
| **Frontend** | HTML, CSS, Bootstrap, JavaScript |
| **Backend** | Django (Python) |
| **Task Queue** | Celery + Celery Beat |
| **Broker** | Redis |
| **Database** | SQLite (Development) |
| **APIs** | [API-Football](https://www.api-football.com/) and [Football-Data.org](https://www.football-data.org/) |
| **Version Control** | Git & GitHub |

---

## ⚙️ Installation

Follow these steps to set up and run the project locally.

**Step 1 – Clone the Repository**
```bash
git clone https://github.com/sethnkwo8/Gameday-Stats.git
cd gameday-stats
```

---

**Step 2 – Create and Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

---

**Step 3 – Install Dependencies**
```bash
pip install -r requirements.txt        
```

---

**Step 4 – Set Up Environment Variables**
Create a .env file in your project root and add:
```bash
API_FOOTBALL_KEY=your_api_football_key
FOOTBALL_DATA_KEY=your_football_data_key
```

---

**Step 5 – Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

**Step 6 – Start Redis (for Celery)**
Make sure Redis is installed, then run:
```bash
redis-server    
```

---

**Step 7 – Start Celery and Celery Beat**
Open two new terminals in your project folder 

Terminal 1:
```bash
celery -A gameday_stats worker -l info
```

Terminal 2:
```bash
celery -A gameday_stats beat -l info
```

---

**Step 8 – Start the Development Server**
```bash
python manage.py runserver
```
Visit your app at:
http://127.0.0.1:8000/

---

## 🧠 How It Works

Gameday Stats integrates **two football APIs** and uses **Celery Beat** to automatically update data on a schedule.

| Function | Data Source | Update Method |
|-----------|--------------|----------------|
| Fixtures & Live Scores | **API-Football** | Periodically updated with Celery Beat |
| Player & Team Stats | **API-Football** | Fetched on demand or scheduled |
| League Standings | **Football-Data.org** | Updated daily with Celery task |
| Historical Data | **Football-Data.org** | Optional background fetch |

**Celery Beat** runs background tasks at set intervals (e.g., every 30 minutes) to refresh scores and standings.  
This ensures users always see updated data without manually refreshing API calls.  

---

## 🖼️ Project Screenshots

Below are key screenshots showcasing the main features of the Football Web App:

| Feature | Screenshot | Description |
|---------|------------|-------------|
| Home Page | ![Homepage](screenshots/Homepage.png) | The landing page with navigation and overview of leagues. |
| Fixtures | ![Fixtures](screenshots/Matches_Section.png) | Displays upcoming and past matches for selected leagues and matchdays. |
| Standings | ![Standings](screenshots/Standings_Section.png) | Shows league table with team positions, points, and stats. |
| Team Fixtures | ![Team Fixtures](screenshots/Team_Matches.png) | Fixtures specific to a selected team. |
| Top Scorers | ![Top Scorers](screenshots/Top_Scorers_Section.png) | Lists the top goal scorers with goals, assists, and penalties. |
| Team Players | ![Team Players](screenshots/Team_players.png) | Shows squad details for a selected team, including coach and venue. |
| League Teams | ![League Teams](screenshots/Teams_Section.png) | Shows all the teams in a particular league |

## Distinctiveness and Complexity

This project satisfies all CS50W Final Project requirements:

- ✅ Django-based web application  
- ✅ Database models and migrations  
- ✅ Dynamic routes and templates  
- ✅ Integration with multiple external APIs  
- ✅ Implementation of background tasks using Celery Beat  
- ✅ Includes a video demonstration  

---

## 🎥 Video Demo

🎬 Watch the project walkthrough here:  
👉 [YouTube Link](https://youtu.be/bofClOn7viM) 

---

## 👨‍💻 Author

**Seth Nkwo**  
📧 [sethnkwocool@gmail.com]  
🔗 [GitHub Profile](https://github.com/sethnkwo8)  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/seth-nkwo/)  

---

## 🏁 Acknowledgements

Special thanks to:
- The **CS50 Team** for an incredible course and guidance  
- **API-Football** and **Football-Data.org** for providing reliable football data APIs  
- **Celery** and **Redis** for simplifying background scheduling and asynchronous tasks  

---


