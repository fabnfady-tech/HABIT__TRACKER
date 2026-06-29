# 🎯 Habit Tracker & Advanced Task Manager API

A production-ready, secure, and feature-rich RESTful API designed to manage daily tasks and track long-term habits. Built using **Django REST Framework (DRF)** and backed by robust relational database design, this system allows users to organize their lives, prevent habit "cheating" with time-cooldown logic, and document endpoints cleanly.

---

## 🚀 Key Features

### 🔒 1. Secure Authentication & User Isolation
* **JWT Authentication:** Powered by `djangorestframework-simplejwt` for secure, stateless login sessions.
* **Token Blacklisting:** Implements secure logout by blacklisting refresh tokens to prevent reuse.
* **Strict Registration Validation:** Enforces built-in Django password strength validators and checks for matching confirmations during signup.
* **Complete Data Isolation:** Every user can only view, edit, or delete their own tasks and categories via enforced Django QuerySet filtering.

### 📊 2. Smart Habit Tracking Engine
* **Incremental Streak Counter:** Tracks how many times a habit/task has been ticked off using a `completed_count` metric.
* **Anti-Cheat Cooldown Logic:** Implements a strict **14-hour cooldown lock** via custom API actions (`/tasks/{id}/complete/`). Users cannot spam the complete button; they must wait until the next calendar day cycles to protect habit authenticity.

### 🎨 3. Dynamic Category Organization
* **Color-Coded Workspaces:** Supports custom Hex color strings (e.g., `#6366f1`) per category for beautiful front-end rendering.
* **Smart Database Constraints:** Enforces a `unique_together` constraint on category names per user—preventing duplicate lists while keeping names reusable across different users.

### 🔍 4. Professional API Capabilities
* **Advanced Query Controls:** Out-of-the-box filtering by `status`, `priority`, and `category`.
* **Full-Text Search:** Instantly query tasks by `title` or `description`.
* **Optimized Sorting:** Default strict ordering based on high priority (`-priority`) and upcoming deadlines (`due_date`).
* **Automated Documentation:** Fully generated OpenAPI 3.0 interactive schemas using `drf_spectacular` (Swagger UI).

---

## 🛠️ Tech Stack & Architecture

* **Framework:** Django 5.x & Django REST Framework (DRF)
* **Database:** PostgreSQL / SQLite
* **Authentication:** SimpleJWT (JSON Web Tokens)
* **API Documentation:** DRF-Spectacular (OpenAPI 3.0 / Swagger UI)

---

## 📂 Database Schema Overview

### 1. Category Model
* `name` (CharField)
* `color` (CharField - Hex format)
* `user` (ForeignKey to User)
* *Constraint:* Unique combination of `name` + `user`.

### 2. Task Model
* `title` & `description` (Text fields)
* `status` (Choices: Todo, In Progress, Done)
* `priority` (Integer Choices: Low = 1, Medium = 2, High = 3)
* `due_date` (DateField)
* `completed_count` (IntegerField - for tracking habit streaks)
* `last_completed` (DateTimeField - enforces the 14-hour lockout)

---

## 🚦 Core API Endpoints

### Authentication
* `POST /api/register/` - Register a new user with strict validation.
* `POST /api/login/` - Authenticate and receive Access + Refresh JWT tokens.
* `POST /api/logout/` - Securely log out and blacklist the token.

### Categories
* `GET /api/categories/` - List user-specific categories.
* `POST /api/categories/` - Create a custom workspace with hex colors.

### Tasks & Habits
* `GET /api/tasks/` - Retrieve, filter, search, and sort your tasks.
* `POST /api/tasks/` - Instantiate a new task or habit.
* `POST /api/tasks/{id}/complete/` - **Custom Trigger:** Increments the habit counter and activates the anti-cheat time lockout.