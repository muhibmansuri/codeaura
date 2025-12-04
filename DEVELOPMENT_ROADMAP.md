# CodeAura App - Complete Development Roadmap

## 📋 Project Overview
Full-stack educational app with Android + iOS + Admin Panel

**Tech Stack:**
- Mobile: Flutter (Android + iOS)
- Backend: Python Flask
- Database: MySQL / PostgreSQL
- Admin Panel: Flask + Bootstrap
- Hosting: Render / Railway / AWS

---

## 🏗️ STEP 1 — Project Structure

```
codeaura/
├── backend/                    # Flask Backend
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py            # Login, Register, JWT
│   │   ├── courses.py         # Course APIs
│   │   ├── admission.py       # Enrollment
│   │   ├── payments.py        # Fee payments
│   │   ├── notifications.py   # Notifications
│   │   └── admin.py           # Admin panel
│   ├── models/
│   │   ├── student.py
│   │   ├── course.py
│   │   ├── batch.py
│   │   ├── enrollment.py
│   │   ├── payment.py
│   │   └── notification.py
│   ├── database/
│   │   ├── db.py             # DB Connection
│   │   └── schema.sql        # Database schema
│   ├── templates/            # Admin Panel HTML
│   └── static/              # CSS, JS, Images
│
├── flutter_app/              # Flutter Frontend
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/
│   │   │   ├── splash_screen.dart
│   │   │   ├── login_screen.dart
│   │   │   ├── register_screen.dart
│   │   │   ├── dashboard_screen.dart
│   │   │   ├── courses_screen.dart
│   │   │   ├── course_details_screen.dart
│   │   │   ├── admission_form_screen.dart
│   │   │   ├── fees_screen.dart
│   │   │   ├── video_player_screen.dart
│   │   │   ├── notes_viewer_screen.dart
│   │   │   ├── tests_screen.dart
│   │   │   ├── profile_screen.dart
│   │   │   └── notifications_screen.dart
│   │   ├── widgets/
│   │   ├── services/
│   │   │   ├── api_service.dart
│   │   │   ├── auth_service.dart
│   │   │   └── firebase_service.dart
│   │   ├── models/
│   │   │   ├── student.dart
│   │   │   ├── course.dart
│   │   │   └── payment.dart
│   │   └── theme/
│   │       └── app_theme.dart
│   ├── pubspec.yaml
│   └── android/ / ios/
│
└── docs/
    ├── API_DOCUMENTATION.md
    ├── DATABASE_SCHEMA.md
    └── DEPLOYMENT_GUIDE.md
```

---

## 📊 STEP 2 — Database Schema

### Students Table
```sql
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    photo_url VARCHAR(255),
    stream VARCHAR(100),
    age INT,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'graduated')
);
```

### Courses Table
```sql
CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    type VARCHAR(100),
    fee DECIMAL(10, 2),
    duration VARCHAR(50),
    image_url VARCHAR(255),
    description TEXT,
    syllabus TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Batches Table
```sql
CREATE TABLE batches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_name VARCHAR(255),
    course_id INT,
    timing VARCHAR(100),
    faculty VARCHAR(255),
    start_date DATE,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

### Enrollments Table
```sql
CREATE TABLE enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    batch_id INT,
    status ENUM('active', 'completed', 'dropped'),
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (batch_id) REFERENCES batches(id)
);
```

### Payments Table
```sql
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    amount DECIMAL(10, 2),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method ENUM('razorpay', 'cashfree', 'bank_transfer'),
    receipt_url VARCHAR(255),
    status ENUM('success', 'pending', 'failed'),
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

### Videos Table
```sql
CREATE TABLE videos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT,
    title VARCHAR(255),
    video_url VARCHAR(255),
    duration INT,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

### Notes Table
```sql
CREATE TABLE notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT,
    title VARCHAR(255),
    pdf_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

### Tests Table
```sql
CREATE TABLE tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT,
    title VARCHAR(255),
    questions_json LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

### Notifications Table
```sql
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    message TEXT,
    student_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

---

## 🔧 STEP 3 — Development Sequence

### Phase 1: Setup & Authentication (Week 1)
- [ ] Flask project initialization
- [ ] Database setup & schema creation
- [ ] JWT authentication system
- [ ] Login/Register API endpoints
- [ ] Flutter project initialization
- [ ] Login & Register screens

### Phase 2: Core Features (Week 2-3)
- [ ] Course listing API
- [ ] Course details API
- [ ] Flutter course screens
- [ ] Admission form API & screen
- [ ] Student profile system

### Phase 3: Payment & Enrollment (Week 4)
- [ ] Razorpay integration
- [ ] Payment API endpoints
- [ ] Enrollment tracking
- [ ] Payment history

### Phase 4: Learning Features (Week 5)
- [ ] Video upload API
- [ ] PDF notes system
- [ ] Online tests API
- [ ] Video player screen
- [ ] Notes viewer screen
- [ ] Tests screen

### Phase 5: Advanced Features (Week 6)
- [ ] Firebase push notifications
- [ ] WhatsApp Cloud API integration
- [ ] Referral system
- [ ] Wallet system

### Phase 6: Admin Panel (Week 7)
- [ ] Admin login
- [ ] Courses management
- [ ] Student list & filters
- [ ] Payments tracking
- [ ] Analytics dashboard

### Phase 7: Deployment (Week 8)
- [ ] Backend deployment on Render
- [ ] Flutter APK build
- [ ] Play Store deployment
- [ ] iOS deployment

---

## 🚀 API Endpoints (Flask)

### Authentication
- `POST /api/auth/register` - Register new student
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh-token` - Refresh JWT

### Courses
- `GET /api/courses` - Get all courses
- `GET /api/courses/<id>` - Get course details
- `GET /api/courses/<id>/videos` - Get course videos
- `GET /api/courses/<id>/notes` - Get course notes

### Enrollment
- `POST /api/enroll` - Enroll in course
- `GET /api/enrollments/<student_id>` - Get student enrollments

### Payments
- `POST /api/payments/create` - Create payment
- `GET /api/payments/<student_id>` - Get payment history
- `POST /api/payments/verify` - Verify payment

### Admin Panel
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/students` - All students list
- `POST /admin/courses` - Add course
- `POST /admin/push-notification` - Send notification

---

## 📝 Next Steps

**Ready to start building?**

1. **Reply with:** "Start Flask Backend"
   - I'll create complete Flask boilerplate with all endpoints
   
2. **Reply with:** "Start Flutter App"
   - I'll create Flutter project structure with all screens
   
3. **Reply with:** "Create Admin Panel"
   - I'll create Flask admin panel with Bootstrap
   
4. **Reply with:** "Database Setup"
   - I'll create complete MySQL schema file

---

## ✅ Checklist
- [ ] Tech stack selected ✅
- [ ] Project structure created
- [ ] Database schema designed ✅
- [ ] Development sequence planned ✅
- [ ] API endpoints documented ✅
- [ ] Ready to code!
