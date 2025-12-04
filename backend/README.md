# CodeAura Backend - Flask API

Complete Flask backend for CodeAura educational app with authentication, courses, enrollment, payments, and notifications.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL/PostgreSQL
- pip

### Installation

1. **Clone/Setup the project:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup database:**
```bash
# Create .env file
cp .env.example .env

# Update DATABASE_URL in .env with your credentials
# Then run:
mysql -u root -p < backend/database/schema.sql
```

5. **Run the server:**
```bash
python app.py
```

Server will start at `http://localhost:5000`

---

## 📚 API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new student
- `POST /login` - Login with email & password
- `POST /login-phone` - Login with phone number
- `POST /verify-otp` - Verify OTP
- `POST /refresh` - Refresh JWT token
- `GET /profile` - Get student profile (JWT required)
- `PUT /profile` - Update profile (JWT required)
- `POST /change-password` - Change password (JWT required)

### Courses (`/api/courses`)
- `GET /` - Get all courses (with filters)
- `GET /<course_id>` - Get course details
- `GET /<course_id>/videos` - Get course videos
- `GET /<course_id>/notes` - Get course notes
- `GET /<course_id>/tests` - Get course tests
- `POST /` - Create course (Admin)
- `PUT /<course_id>` - Update course (Admin)
- `DELETE /<course_id>` - Delete course (Admin)

### Admission & Enrollment (`/api/admission`)
- `POST /enroll` - Enroll in a batch (JWT required)
- `GET /my-enrollments` - Get my enrollments (JWT required)
- `GET /enrollments/<enrollment_id>` - Get enrollment details
- `DELETE /enrollments/<enrollment_id>` - Unenroll
- `GET /admin/enrollments` - Get all enrollments (Admin)
- `GET /admin/batches` - Get all batches (Admin)
- `POST /admin/batches` - Create batch (Admin)
- `PUT /admin/batches/<batch_id>` - Update batch (Admin)

### Payments (`/api/payments`)
- `POST /create` - Create payment order (JWT required)
- `POST /verify` - Verify payment (JWT required)
- `GET /history` - Get payment history (JWT required)
- `GET /<payment_id>` - Get payment details
- `GET /admin/all` - Get all payments (Admin)
- `GET /admin/dashboard` - Payment statistics (Admin)
- `PUT /admin/<payment_id>/update-status` - Update payment status (Admin)

### Notifications (`/api/notifications`)
- `GET /` - Get notifications (JWT required)
- `GET /<notification_id>` - Get single notification
- `PUT /<notification_id>/mark-read` - Mark as read
- `PUT /mark-all-read` - Mark all as read
- `DELETE /<notification_id>` - Delete notification
- `POST /admin/send` - Send notification (Admin)
- `POST /admin/broadcast` - Broadcast notification (Admin)
- `GET /admin/all` - Get all notifications (Admin)

---

## 🔑 Environment Variables

Create `.env` file with:

```env
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://root:password@localhost/codeaura
JWT_SECRET_KEY=your-secret-key
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_secret
```

---

## 📊 Database Schema

### Main Tables:
- `students` - Student information
- `courses` - Course details
- `batches` - Course batches
- `enrollments` - Student enrollments
- `payments` - Payment records
- `videos` - Course videos
- `notes` - Course notes
- `tests` - Course tests
- `notifications` - User notifications
- `admins` - Admin users

---

## 🔐 Authentication

Uses JWT (JSON Web Tokens):

1. **Register/Login** to get `access_token` and `refresh_token`
2. **Include token** in Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```
3. **Refresh token** expires in 90 days
4. **Access token** expires in 30 days

---

## 💳 Payment Integration

### Razorpay Setup:
1. Create Razorpay account
2. Get API keys from dashboard
3. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=xxx
   RAZORPAY_KEY_SECRET=xxx
   ```

---

## 📝 Sample Requests

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "phone": "9876543210",
    "password": "password123",
    "stream": "Engineering"
  }'
```

### Get Courses
```bash
curl http://localhost:5000/api/courses?type=Engineering&page=1
```

### Get Profile
```bash
curl http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Enroll in Course
```bash
curl -X POST http://localhost:5000/api/admission/enroll \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"batch_id": 1}'
```

---

## 🚀 Deployment

### Deploy on Render:

1. **Create Render account** at render.com
2. **Connect GitHub** repository
3. **Create Web Service** with:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:create_app()`
4. **Add environment variables** in Render dashboard
5. **Deploy!**

### Deploy on Railway:

1. **Create Railway account**
2. **Connect GitHub**
3. **Deploy from GitHub**
4. **Set environment variables**
5. **Done!**

---

## 🐛 Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify credentials in `.env`
- Ensure database exists

### JWT Token Error
- Token might be expired - use refresh endpoint
- Check `Authorization` header format
- Verify `JWT_SECRET_KEY` in `.env`

### CORS Error
- Check if Flask-CORS is installed
- Verify frontend URL in CORS configuration

---

## 📞 Support

For issues, check:
- Database logs
- Flask debug output
- Network requests in browser dev tools

---

## 📄 License

CodeAura - Educational App Backend

---

## 🔥 What's Next?

- [ ] Implement admin panel (Step 3)
- [ ] Build Flutter frontend
- [ ] Deploy backend
- [ ] Launch on Play Store

Ready? Let's build! 🚀
