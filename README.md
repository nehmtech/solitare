# Django Solitaire Game - Setup Guide

A fully functional Solitaire (Klondike) card game built with Django and vanilla JavaScript.

![Solitaire Game](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 Features

- **Classic Solitaire Gameplay**: Standard Klondike rules
- **Beautiful UI**: Modern gradient design with smooth animations
- **Drag & Drop**: Intuitive card movement
- **Auto Move**: Automatically move cards to foundations when possible
- **Win Detection**: Celebrates when you complete the game
- **Responsive Design**: Works on different screen sizes
- **Session-Based**: Game state persists across page refreshes

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer - comes with Python)
- **Git** (to clone the repository) - [Download Git](https://git-scm.com/downloads)

To check if Python is installed:
```bash
python --version
# or
python3 --version
```

To check if pip is installed:
```bash
pip --version
# or
pip3 --version
```

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/yourusername/django-solitaire.git
cd django-solitaire
```

If you downloaded the ZIP file instead, extract it and navigate to the folder:
```bash
cd path/to/django-solitaire
```

---

### Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies isolated from other Python projects.

**On Windows:**
```bash
python -m venv venv
```

**On macOS/Linux:**
```bash
python3 -m venv venv
```

---

### Step 3: Activate the Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your terminal prompt, indicating the virtual environment is active.

---

### Step 4: Install Django

With the virtual environment activated, install Django:

```bash
pip install django
```

To verify Django is installed:
```bash
python -m django --version
```

---

### Step 5: Run Database Migrations

Django needs to set up its database tables:

```bash
python manage.py migrate
```

You should see output showing migrations being applied:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

### Step 6: Start the Development Server

Run the Django development server:

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Step 7: Open the Game in Your Browser

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

or

```
http://localhost:8000/
```

🎉 **You should now see the Solitaire game running!**

---

## 🎴 How to Play

1. **New Game**: Click the "New Game" button to start a fresh game
2. **Draw Cards**: Click the "DECK" pile to draw cards to the "WASTE" pile
3. **Move Cards**: Drag and drop cards between piles:
   - From waste to tableau or foundations
   - Between tableau columns
   - From tableau to foundations
4. **Auto Move**: Click "Auto Move" to automatically place any available cards to foundations
5. **Win**: Complete all four foundation piles (Ace through King for each suit) to win!

### Game Rules

- Build foundation piles (top right) from Ace to King, separated by suit
- In the tableau (bottom), build down by alternating colors (red on black, black on red)
- Only Kings can be placed in empty tableau columns
- Click the deck to draw cards - when empty, it resets automatically

---

## 📁 Project Structure

```
django-solitaire/
├── game/                          # Main game application
│   ├── __init__.py
│   ├── apps.py
│   ├── solitaire.py              # Game logic (Card, SolitaireGame classes)
│   ├── views.py                  # Django views for API endpoints
│   ├── urls.py                   # URL routing
│   └── templates/
│       └── game/
│           └── index.html        # Game interface (HTML/CSS/JS)
├── solitaire_project/            # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py
├── manage.py                     # Django management script
├── db.sqlite3                    # Database (created after migrations)
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

---

## 🔧 Troubleshooting

### Issue: "Command not found: python"
**Solution**: Try using `python3` instead of `python` on macOS/Linux:
```bash
python3 manage.py runserver
```

### Issue: "Port already in use"
**Solution**: Use a different port:
```bash
python manage.py runserver 8080
```
Then access the game at `http://127.0.0.1:8080/`

### Issue: "Module not found: django"
**Solution**: Make sure your virtual environment is activated and Django is installed:
```bash
# Activate venv first
pip install django
```

### Issue: Cards won't drag/drop
**Solution**: 
- Ensure JavaScript is enabled in your browser
- Try refreshing the page (Ctrl+F5 or Cmd+Shift+R)
- Check browser console for errors (F12)

### Issue: "Invalid move" message
**Solution**: Make sure you're following Solitaire rules:
- Cards in tableau must alternate colors
- Cards must be in descending order in tableau
- Only Kings can start empty tableau columns
- Foundations must be built up from Ace to King in the same suit

### Issue: Session errors
**Solution**: 
- Clear your browser cookies
- Restart the Django server

---

## 🛠️ Development

### Creating a Superuser (Optional)

To access Django's admin panel:
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account, then access at `http://127.0.0.1:8000/admin/`

### Running in Production

**Important**: This project uses default Django settings suitable for development only. Before deploying to production:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use a production database (PostgreSQL, MySQL)
5. Collect static files
6. Use a production server (Gunicorn, uWSGI)

---

## 📦 Dependencies

This project uses:
- **Django 4.0+** - Web framework
- **Python 3.8+** - Programming language

All dependencies are listed in `requirements.txt` (if provided):
```bash
pip install -r requirements.txt
```

---

## 🎯 API Endpoints

The game uses these API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main game page |
| `/api/new-game/` | GET | Start a new game |
| `/api/game-state/` | GET | Get current game state |
| `/api/draw-card/` | GET | Draw a card from deck |
| `/api/move-card/` | POST | Move a card |
| `/api/auto-move/` | GET | Auto-move cards to foundations |

---

## 🌟 Future Enhancements

Potential improvements:
- Score tracking system
- Timer to track game duration
- Move counter
- Undo/Redo functionality
- Different difficulty levels
- Save/load game state to database
- User accounts and leaderboards
- Sound effects and music
- Multiple card draw options (draw 1 vs draw 3)
- Hint system
- Statistics and analytics

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Created with ❤️ by [Your Name]

---

## 🙏 Acknowledgments

- Built with Django and pure JavaScript - no external JavaScript libraries required!
- Card game logic inspired by classic Klondike Solitaire
- Modern UI design with CSS gradients and animations

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an issue on GitHub
3. Contact: your.email@example.com

---

## 🎓 Educational Use

This project is perfect for:
- Learning Django framework basics
- Understanding session management
- Practicing JavaScript DOM manipulation
- Implementing drag-and-drop functionality
- Building game logic in Python

Feel free to use this project for educational purposes!

---

**Enjoy playing Solitaire! 🎴**

To stop the server, press `CTRL+C` in the terminal.

To deactivate the virtual environment when you're done:
```bash
deactivate
```