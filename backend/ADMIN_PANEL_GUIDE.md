# CodeAura Admin Panel - Documentation

## 🎛️ Admin Panel Overview

Complete web-based admin dashboard for managing CodeAura educational platform with students, courses, batches, enrollments, payments, and notifications.

---

## 🚀 Features

### Dashboard
- ✅ Real-time statistics
- ✅ Student count
- ✅ Course count
- ✅ Enrollment status
- ✅ Payment statistics with revenue
- ✅ Charts and analytics
- ✅ Recent activities feed

### Student Management
- ✅ View all students
- ✅ Search students (name, email, phone)
- ✅ Student detail page
- ✅ View enrollments
- ✅ View payment history
- ✅ Delete students
- ✅ Pagination

### Course Management
- ✅ View all courses
- ✅ Create new courses
- ✅ Edit courses
- ✅ Delete courses
- ✅ Course grid view
- ✅ Add images, descriptions, syllabus

### Batch Management
- ✅ View all batches
- ✅ Filter by course
- ✅ Create batches
- ✅ Edit batches
- ✅ Delete batches
- ✅ Manage timing, faculty, start date

### Enrollment Management
- ✅ View all enrollments
- ✅ Filter by status (Active, Completed, Dropped)
- ✅ Update enrollment status
- ✅ Student-Batch relationship tracking
- ✅ Pagination

### Payment Management
- ✅ View all payments
- ✅ Filter by status (Success, Pending, Failed)
- ✅ Update payment status
- ✅ Payment amount tracking
- ✅ Payment method display
- ✅ Pagination

### Notifications
- ✅ Send notifications to specific student
- ✅ Broadcast notifications to all
- ✅ View all notifications
- ✅ Mark read/unread
- ✅ Delete notifications
- ✅ Notifications list with pagination

---

## 📂 File Structure

```
backend/
├── routes/
│   └── admin.py                 # Admin routes (40+ endpoints)
├── templates/
│   └── admin/
│       ├── base.html           # Base template with sidebar
│       ├── login.html          # Login page
│       ├── dashboard.html      # Dashboard with stats
│       ├── students.html       # Students list
│       ├── student_detail.html # Student profile
│       ├── courses.html        # Courses grid
│       ├── course_form.html    # Create/Edit course
│       ├── batches.html        # Batches list
│       ├── batch_form.html     # Create/Edit batch
│       ├── enrollments.html    # Enrollments list
│       ├── payments.html       # Payments list
│       ├── notifications.html  # Notifications list
│       ├── notification_form.html # Send notification
│       └── settings.html       # Settings page
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles
│   └── js/
│       └── script.js           # JavaScript utilities
└── app.py                      # Main app (blueprint registered)
```

---

## 🔐 Authentication

### Default Admin Credentials
```
Username: admin
Password: admin123
```

**Change this immediately in production!**

### How to Change:
1. Access the database
2. Find the admin record
3. Hash the new password:
```python
from werkzeug.security import generate_password_hash
hashed = generate_password_hash('new_password')
```
4. Update the admin record

---

## 📊 Admin Routes

### Authentication
- `GET /admin/login` - Login page
- `POST /admin/login` - Process login
- `GET /admin/logout` - Logout

### Dashboard
- `GET /admin/dashboard` - Main dashboard with stats

### Students
- `GET /admin/students` - Students list with search & pagination
- `GET /admin/students/<student_id>` - Student detail page
- `POST /admin/students/<student_id>/delete` - Delete student

### Courses
- `GET /admin/courses` - Courses list (grid view)
- `GET /admin/courses/create` - Create course form
- `POST /admin/courses/create` - Create course
- `GET /admin/courses/<course_id>/edit` - Edit course form
- `POST /admin/courses/<course_id>/edit` - Update course
- `POST /admin/courses/<course_id>/delete` - Delete course

### Batches
- `GET /admin/batches` - Batches list with filters
- `GET /admin/batches/create` - Create batch form
- `POST /admin/batches/create` - Create batch
- `GET /admin/batches/<batch_id>/edit` - Edit batch form
- `POST /admin/batches/<batch_id>/edit` - Update batch
- `POST /admin/batches/<batch_id>/delete` - Delete batch

### Enrollments
- `GET /admin/enrollments` - Enrollments list with status filter
- `POST /admin/enrollments/<enrollment_id>/update` - Update status

### Payments
- `GET /admin/payments` - Payments list with status filter
- `POST /admin/payments/<payment_id>/update` - Update status

### Notifications
- `GET /admin/notifications` - Notifications list
- `GET /admin/notifications/send` - Send notification form
- `POST /admin/notifications/send` - Send notification
- `POST /admin/notifications/<notification_id>` - Delete notification

### Settings
- `GET /admin/settings` - Settings page

---

## 🎨 UI Features

### Design System
- **Colors**: Primary (#667eea), Secondary (#764ba2), Success, Danger, Warning
- **Framework**: Bootstrap 5
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js
- **Responsive**: Mobile-friendly sidebar navigation

### Key Components
1. **Navigation Bar** - Logo, user dropdown, logout
2. **Sidebar** - Navigation menu with active indicator
3. **Content Area** - Main dashboard content
4. **Footer** - Copyright and info
5. **Alerts** - Flash messages (auto-dismiss after 5s)
6. **Tables** - Sortable, paginated with hover effects
7. **Forms** - Clean forms with validation
8. **Cards** - Statistics cards with gradients
9. **Charts** - Doughnut charts for data visualization

---

## 🔧 Customization

### Change Primary Color
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;  /* Change this */
    --secondary-color: #764ba2;
}
```

### Add New Menu Item
1. Edit `templates/admin/base.html`
2. Add to sidebar navigation:
```html
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('admin.your_route') }}">
        <i class="bi bi-icon-name"></i> Your Menu
    </a>
</li>
```

### Create New Admin Page
1. Create route in `routes/admin.py`:
```python
@admin_bp.route('/your-page')
@admin_login_required
def your_page():
    return render_template('admin/your_page.html')
```

2. Create template `templates/admin/your_page.html`:
```html
{% extends "admin/base.html" %}
{% block title %}Your Page - CodeAura Admin{% endblock %}
{% block content %}
    <h1>Your Content Here</h1>
{% endblock %}
```

---

## 📱 Responsive Design

- **Desktop**: Full sidebar + content
- **Tablet**: Collapsible sidebar
- **Mobile**: Hamburger menu, stacked layout

---

## 🔒 Security Features

- ✅ Login required (session-based)
- ✅ Password hashing (Werkzeug)
- ✅ CSRF protection ready
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation on forms
- ✅ Confirmation dialogs for delete operations

---

## 🚀 How to Run

### 1. Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database
```bash
cp .env.example .env
# Edit .env with your database credentials
mysql -u root -p < database/schema.sql
```

### 3. Run Server
```bash
python app.py
```

### 4. Access Admin Panel
```
http://localhost:5000/admin
```

Login with:
- **Username**: admin
- **Password**: admin123

---

## 📈 Next Steps

1. **Customize** - Add your logo, change colors
2. **Deploy** - Deploy to Render/Railway
3. **SSL** - Setup HTTPS in production
4. **Email** - Setup email notifications
5. **Reports** - Add export to CSV/PDF
6. **Analytics** - Add more advanced charts
7. **Two-Factor Auth** - Add 2FA login

---

## 🐛 Troubleshooting

### Can't login?
- Check database connection
- Verify admin user exists
- Check password hash

### Templates not found?
- Ensure template folder structure is correct
- Check Flask app.py has correct template_folder path
- Restart Flask server

### Styles not loading?
- Clear browser cache
- Check static folder path in app.py
- Verify CSS file exists

### Charts not showing?
- Check Chart.js is loaded from CDN
- Verify chart canvas elements exist
- Check browser console for errors

---

## 📞 Support

For issues:
1. Check Flask logs
2. Check browser console (F12)
3. Verify database connection
4. Check environment variables

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Change default admin password
- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Setup HTTPS/SSL
- [ ] Configure production database
- [ ] Setup logging
- [ ] Add rate limiting
- [ ] Backup database regularly
- [ ] Monitor admin panel usage
- [ ] Setup email for notifications
- [ ] Configure environment variables
- [ ] Setup automated backups

---

## 📝 License

CodeAura Admin Panel - Educational App Management System

---

Ready to manage your CodeAura app? 🚀
