# EventHive — Event Management System (EMS)

EventHive is a full-featured, responsive Event Management System built using Django 6.0.7 and Bootstrap. It allows users to browse events, register and log in securely, reserve seats via an interactive grid system, and receive real-time email confirmations. Organizers can seamlessly create, track, and modify their own events with rich-text descriptions.
URL:akarshan.pythonanywhere.com
---

##  Key Features

###  Authentication & Security
*   **User Management:** Secure user registration, login, and logout protocols.
*   **Password Reset Pipeline:** Complete, secure password reset and credential recovery system utilizing Gmail SMTP transactional mailers.
*   **Organizer Access Control:** Strict server-side verification ensuring only verified event creators can modify, edit, or update their respective events.

###  Event Management
*   **Rich Text Integration:** Built-in TinyMCE 8.7.0 editor for creating highly customizable and beautiful event descriptions.
*   **Robust Input Validation:** Dual-layer validation (HTML5 frontend constraints and Django form `clean` methods) completely preventing zero or negative values in seat configurations.
*   **Tailored Management Dashboards:**
    *   *My Events:* For coordinators to monitor live seat occupancy meters and access immediate updates.
    *   *My Bookings:* For attendees to track historical logs and active reservations they have committed to.

###  Booking & Seating Pipeline
*   **Interactive Seat Matrix:** A live-updating visual grid mapping out exactly which seats are open, taken, or claimed by the active user.
*   **Email Confirmations:** Automated, real-time dispatch of ticketing profiles (venue, time routing, seat allocations) upon booking or cancellation actions.
*   **Fail-Safe Intercepts:** Integrated jQuery interactive confirmation alerts to prevent accidental bookings or early cancellations.

---

##  Installation & Local Setup

### 1. Clone the Project Workspace
```bash
git clone [https://github.com/yourusername/EMS.git](https://github.com/yourusername/EMS.git)
cd EMS
```
## 2. Set Up a Python Virtual Environment
Bash
python -m venv .venv
Activate on Windows:

PowerShell
.venv\Scripts\activate
Activate on Mac/Linux:

Bash
source .venv/bin/activate
3. Install Required Dependencies
Ensure you have your environment tools, database connectors, and decoupling libraries installed:

Bash
pip install django python-decouple
4. Configure Your Environment Variables (.env)
Create a file named .env in the root project directory (where manage.py lives).

⚠️ CRITICAL FORMATTING: Do NOT use quotation marks around strings or insert empty spaces around the = signs. Google App Passwords must be a solid, contiguous 16-character string without spaces.

Code snippet
SECRET_KEY=your-secret-key-goes-here
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-valid-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-google-app-password
5. Run Database Migrations
Initialize your SQLite architecture and apply user/booking system schemas:

Bash
python manage.py migrate
6. Create an Administrative Superuser
Generate an admin profile to access the primary Django back-office dashboard:

Bash
python manage.py createsuperuser
7. Fire Up the Development Server
Bash
python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/ to explore EventHive!

## Architecture Overview
The system architecture is organized cleanly into modular apps:

EMS/: Main core directory containing structural definitions, global URL routings, and asset pipelines (settings.py, urls.py).

accounts/: Manages operational profile registration, sign-in wrappers, and authentication sequences.

home/: Drives core dashboard views, interactive ticket grid matrices, multi-conditional model filtering, and transactional email triggers.

templates/: Centralized UI storage housing reusable layouts like base wrappers (base.html), authentication pages, custom dashboards, and structural layout grids (event_form.html, event_detail.html).

### Project Structure

```text
EMS/                               # Root Project Directory
│
├── .env                           # Local environment variables (Secrets & SMTP configurations)
├── db.sqlite3                     # SQLite Local Database 
├── manage.py                      # Django administrative management script
│
├── EMS/                           # Core Project Configuration Folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # Main app configurations & secure SMTP stripping logic
│   ├── urls.py                    # Global URL routing
│   └── wsgi.py
│
├── accounts/                      # Authentication Application
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   └── views.py                   # User registration, login, and logout controller logic
│
├── home/                          # Core Event Management Application
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py
│   ├── forms.py                   # EventForm with seat limit min="1" restrictions
│   ├── models.py                  # Event and Bookings schema architectures
│   ├── urls.py                    # Dashboards, update endpoints, and action routes
│   └── views.py                   # CRUD handlers, email triggers, and details code
│
├── templates/                     # Centralized HTML Interface Layouts
│   ├── base.html                  # Global layout skeleton template
│   ├── home.html                  # Core public index dashboard
│   ├── event_form.html            # Context-adaptive Create/Edit event configuration sheet
│   ├── event_detail.html          # Interactive seat matrix & control actions page
│   ├── my_events.html             # Organizer portal equipped with update mappings
│   ├── my_bookings.html           # User booking historical log
│   ├── login.html                 # Login page wrapper
│   ├── register.html              # Sign-up page wrapper
│   │
│   └── registration/              # Django Contrib Auth Native Directory Fallbacks
│       ├── password_reset_form.html
│       ├── password_reset_done.html
│       ├── password_reset_confirm.html
│       └── password_reset_complete.html      
│
└── Screenshots/                   # System UI and Transactional Email Proofs
    ├── forget_password_ui.png     # Password recovery interface
    ├── forget_pasword_mail.png    # Sent password reset token email
    ├── login_ui.png               # User authentication interface
    ├── my_booking_ui.png          # Attendee booking history dashboard
    ├── my_events_ui.png           # Organizer event management portal
    ├── seat_booked.png            # Live updating interactive seating grid
    ├── seat_booking_cancel_mail.png # Booking cancellation email alert
    └── seat_confirmed_mail.png    # Booking confirmation email alert
   ```

 ## System Visuals & Dashboards
Here is a visual run-through of the EventHive application interfaces and automated transactional mail pipelines.

Core User Interfaces (UI)
User Authentication & Account Recovery
Login Gateway (login_ui.png): Secure entry point for organizers and attendees.

Forgot Password Screen (forget_password_ui.png): Form interface where users trigger verification links.

Platform Management Dashboards
Organizer Management Portal (my_events_ui.png): Where organizers track, edit, and modify their hosted events.

User Bookings Log (my_booking_ui.png): A history log displaying all active reservations for an attendee.

Live Seating Matrix (seat_booked.png): The interactive layout showcasing real-time seat tracking and selections.

 Transactional Email Pipelines (Google SMTP)
1. Password Reset Action
Dispatched securely via automated channels when a credential recovery request is initialized.

2. Seat Booking Confirmation
Sent instantly to the attendee upon a successful real-time seat reservation from the grid matrix.

3. Booking Cancellation Notification
Triggers automatically when a user relinquishes an allocated seat, safely releasing the vacancy asset back to the local database.

## Tech Stack
Backend Framework: Python 3.13 + Django 6.0.7

Database: SQLite (Development standard)

Frontend Interface: Bootstrap 5, Bootstrap Icons, jQuery

Environment Configuration: python-decouple

Rich Text System: TinyMCE 8.7.0 Cloud API

Deployment Platform: PythonAnywher
