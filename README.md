# 🚌 RedBus JourneyForge

A Django-based bus ticket booking web application inspired by redBus. The project provides a simple interface for searching buses, selecting seats, entering passenger details, and following the ticket booking workflow.

## ✨ Features

- 🔍 **Bus Search** — Search buses by departure city, destination city, and journey date.
- 🚌 **Bus Type Filter** — Filter available buses by seater or sleeper type.
- 💺 **Seat Selection** — Select seats for your journey.
- 👤 **Passenger Details** — Enter passenger information during booking.
- 🎟️ **Booking Workflow** — Navigate through the bus booking process.
- 🎨 **Responsive Interface** — Clean and user-friendly design.
- 🖼️ **Custom Favicon** — Bus icon for browser-tab branding.

## 🛠️ Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (if configured as the default Django database)
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
redbus-journeyforge-1912/
├── bookings/
│   ├── migrations/
│   ├── static/
│   │   └── bookings/
│   │       └── bus-icon.png
│   ├── templates/
│   │   └── bookings/
│   │       ├── home.html
│   │       ├── search_results.html
│   │       ├── seat_selection.html
│   │       └── passenger_details.html
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shri-mini-coder/redbus-journeyforge-1912.git
cd redbus-journeyforge-1912
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Django

```bash
python -m pip install django
```

If a `requirements.txt` file is available, install the project's dependencies instead:

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

### 6. Open the application

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## 🚀 Future Improvements

- User registration and login
- Online payment gateway integration
- Booking confirmation and ticket generation
- Booking history and cancellation
- Email or SMS notifications
- Improved mobile responsiveness

## 🎯 Project Purpose

This project is developed as a learning and portfolio project to practise Django web development, database integration, URL routing, templates, and Git-based version control.

## 👩‍💻 Author

**Shrinithi**

GitHub: [@Shri-mini-coder](https://github.com/Shri-mini-coder)

## 📄 License

This project is intended for educational and portfolio purposes. Add a license if you wish to specify the terms under which others may use or distribute it.

