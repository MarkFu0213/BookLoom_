# BookLoom

An AI‑powered mobile reading application that lets users reimagine book stories by editing them in different styles while preserving the author’s original voice.

---

## 🚀 Features

* **Library Browse**: Explore books by title, author, and cover image.
* **Story Editing**: Choose from various stylistic presets (e.g., fantasy, mystery, modern) and let the AI rewrite selected chapters.
* **User Accounts**: Secure login, registration, password reset, and profile management (view, edit, delete).
* **Generated Story Viewer**: Read and compare AI‑edited chapters; note that AI rewrites may take a few seconds.
* **Persistent Data**: MySQL for user/auth and book metadata; MongoDB for book content and editing history.

## 📋 Prerequisites

* **Python 3.9+**
* **Node.js & npm**
* **MySQL** (for user/auth data)
* **MongoDB Atlas** (for book content)
* **Expo CLI** (for React Native frontend)
* **OpenAI API Key**

## 🛠 Environment Setup

> Full instructions are in the `Documents/` folder. Below is a quickstart.

### 1. Backend

1. **Clone repo**

   ```bash
   git clone git@github.com:MarkFu0213/Bookloom.git
   cd Bookloom/backend
   ```

2. **Create virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   * Copy and update `backend/app/config/mysql_db.py` with your MySQL credentials.
   * Set your MongoDB Atlas URI in `backend/app/config/mongodb_db.py`:

     ```python
     MONGO_URI = "mongodb+srv://<user>:<password>@bookloommongodb..."
     ```
   * Export OpenAI key:

     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     ```

5. **Initialize MySQL schema**

   1. Open MySQL Workbench and run `backend/database/BookLoomMySQL.sql`.

6. **Start server**

   ```bash
   python app/main.py
   ```

   You should see:

   * Running on [http://127.0.0.1:5001](http://127.0.0.1:5001)
   * Connected to MongoDB & available databases

### 2. Frontend

1. **Go to frontend directory**

   ```bash
   cd ../frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start Expo**

   ```bash
   npx expo start
   ```

   * Press `i` for iOS simulator, `a` for Android emulator, or scan QR for Expo Go.

## ✅ Running Tests

1. Ensure backend server is running.
2. In the `backend/` folder, run:

   ```bash
   pytest --cov=backend/app/controllers --cov=backend/app/services --cov-report=term-missing
   ```
3. All tests should pass (53/53) and coverage should be 100%.

## 📁 Project Structure

```
BookLoom/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── services/
│   │   └── config/
│   ├── database/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/           # Expo React Native source
│   └── package.json
├── Documents/              # Detailed documentation
└── README.md
```

## 💡 Future Features

* User-submitted story uploads & deletion
* Friend system: share and comment on rewrites
* Ratings, comments, and sorting by popularity

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push (`git push origin feature/name`)
5. Open a Pull Request


---

*For full setup and deployment details, please see the `Documents/` folder.*
