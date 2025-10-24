# StreamBase

**StreamBase** is a YouTube-like backend application built with **FastAPI**, **SQLAlchemy (async)**.  
It demonstrates a production-ready backend structure with complex database relationships, role-based access, and a robust API architecture.

---

## 🌟 Features (Implemented)

- **User Management & Roles**
  - Users can register and log in.
  - Roles include `viewer`, `creator`, and `admin`.
  - Role-based access control for endpoints.

- **Video Management**
  - CRUD operations for videos.
  - Public/private video settings.
  - Video metadata (title, description, duration, thumbnail, tags, category).
  - Like/Dislike functionality with toggle system.
  - View count tracking.

- **Comments**
  - Nested comments and replies.
  - Users can edit/delete their own comments.
  - Admins can moderate all comments.

- **Playlists**
  - Users can create public/private playlists.
  - Add/remove videos in playlists.

- **Subscriptions**
  - Subscribe/unsubscribe to creators.
  - Track subscribers and subscriptions per user.

- **Database**
  - Fully modeled with **SQLAlchemy ORM**.
  - Complex relationships: many-to-many, one-to-many, self-referencing.
  - Cascading deletes for proper data integrity.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (async)  
- **Database:** PostgreSQL (SQLite for local dev optional)  
- **ORM:** SQLAlchemy 2.0 (async)  
- **Authentication:** JWT, Bcrypt password hashing  
- **Testing:** Pytest + httpx (async tests)  
- **Version Control:** Git + GitHub  

---

## 🚀 Installation

1. **Clone the repo**

```bash
git clone https://github.com/Anantshukla007/StreamBase.git
cd StreamBase
````

2. **Create virtual environment**

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   Create a `.env` file in the project root:

```text
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/streambase
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

5. **Run the app**

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API with Swagger UI.

---

## 🧩 Project Structure

```
StreamBase/
├─ app/
│  ├─ main.py               # FastAPI entrypoint
│  ├─ core/                 # Configs, settings
│  ├─ db/                   # Database setup, AsyncSession
│  ├─ models/               # SQLAlchemy models
│  ├─ schemas/              # Pydantic request/response schemas
│  ├─ api/                  # Route modules
│  ├─ services/             # Business logic
│  ├─ tests/                # Pytest test cases
├─ requirements.txt
├─ README.md
├─ .gitignore
└─ .env.example
```

---

## 🔮 Future Plans (Advanced Features)

* **Analytics**

  * Video watch time and engagement metrics.
  * Like/Dislike trends and creator statistics.
  * Subscription-based video feed recommendations.

* **Advanced Features**

  * Video streaming & chunked uploads.
  * Search and filter functionality.
  * Background tasks for video processing (thumbnails, transcoding).
  * Notifications for subscribers when a creator uploads a video.
  * Caching and optimization for large-scale data.

* **Testing Enhancements**

  * More comprehensive Pytest coverage for edge cases.
  * Integration tests for complex query endpoints.

---

## 💡 Why This Project?

* Demonstrates **industry-level backend design** with FastAPI and async SQLAlchemy.
* Includes **complex ORM relationships** and **role-based access control**.
* Fully **testable** with Pytest for real-world reliability.
* Ready to **scale and extend** with advanced analytics and features.
* Excellent **portfolio project** to showcase backend skills to recruiters.

---

## 📄 License

MIT License – feel free to explore and extend this project for learning purposes.
