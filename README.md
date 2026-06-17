# 📊 Bale Price Bot

A bot for **Bale Messenger** that provides real‑time prices for:

- Gold
- USD
- EUR
- Coin

The project is built using **Django** and **python‑telegram‑bot** with an **async‑friendly architecture** .

The bot also records **user interactions and command statistics** which can be viewed from the **Django Admin panel**.

---

# ✨ Features

- Real‑time **Gold, USD, EUR, and Coin prices**
- **Inline keyboard UI**
- **Refresh prices without sending new messages**
- **Single‑asset price view**
- **User tracking**
- **Command usage statistics**
- **Admin analytics dashboard**
- **Async‑safe Django ORM usage**
- **Unit tests using pytest**

---

# 🧰 Requirements

- Python **3.14+**
- Django **6+**
- SQLite (default) or any Django supported database

---

# 📦 Download the Project

Instead of cloning the repository, download the project as a **ZIP file**.

1. Download the ZIP archive of the project.
2. Extract it:

Linux / macOS
```bash
unzip bale-price-bot.zip
cd bale-price-bot
```
Windows

Right click the ZIP file → Extract All

# 📥 Install Dependencies

Using uv


```bash
uv sync
```

# ⚙️ Environment Variables
Create a .env file in the root of the project:

```bash
DEBUG=True
SECRET_KEY=your_secret_key_here

ALLOWED_HOSTS=

PRICEBOT_TOKEN=your_bale_bot_token
BOT_NAME=your_bale_bot_name

PRICE_API_URL=https://api.nerkh.io/v1/prices/json/all
PRICE_API_KEY=

```

# 🗄 Database Setup
Run migrations to create database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

# 👤 Create Admin User
Create a superuser for the admin panel:

```bash
python manage.py createsuperuser
```

Then start the server and open the admin panel:

```bash
python manage.py runserver
```

http://127.0.0.1:8000/admin


- Registered users
- User interaction history
- Command statistics
- Bot analytics

# ▶️ Run the Bot

Start the bot with:

```bash
python manage.py run_pricebot
```


Users can interact with the bot using commands:

```bash
/start
/price
```


The bot will display the current prices and provide inline buttons for:

- Viewing individual asset prices
- Refreshing prices
- Returning to the full list

# 🧪 Run Tests

This project uses pytest and pytest‑django.

Run all tests:

```bash
pytest
```

### wish you the best !!!
