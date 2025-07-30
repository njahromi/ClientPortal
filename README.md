# ClientPortal - Multi-Tenant Client Management System

A comprehensive Django-based SaaS application for small businesses, freelancers, and agencies to manage their clients, tasks, and documents in an isolated multi-tenant environment.

## 🚀 Features

### Core Functionality
- **Multi-Tenant Architecture**: Each business/organization has isolated data
- **User Management**: Role-based access (Admin, Staff, Regular User)
- **Client Management**: Complete CRUD operations with search and filtering
- **Task Tracking**: Create, assign, and track tasks with priorities and due dates
- **Document Management**: Upload and organize client documents
- **Dashboard**: At-a-glance overview with statistics and recent activity

### Advanced Features
- **Search & Filtering**: Advanced search across all entities
- **Pagination**: Efficient data loading for large datasets
- **File Upload**: Secure document storage with validation
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Admin Interface**: Custom Django admin with tenant isolation
- **Activity Logging**: Track all user actions and changes

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Forms**: Django Crispy Forms with Bootstrap 5
- **File Storage**: Django Storages (S3 ready)
- **Authentication**: Django's built-in auth system
- **Environment**: Python 3.11+, Virtual Environment

## 📋 Requirements

- Python 3.11 or higher
- pip (Python package manager)
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ClientPortal
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\Activate.ps1
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and configure it:
```bash
cp env.example .env
# Edit .env with your settings
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Load Demo Data (Optional)
```bash
python manage.py setup_demo_data
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 👥 Demo Credentials

After running the demo data setup:
- **Username**: admin
- **Password**: admin123
- **URL**: http://localhost:8000

## 🏗️ Project Structure

```
ClientPortal/
├── accounts/                 # User and tenant management
│   ├── models.py            # Tenant and UserProfile models
│   ├── admin.py             # Custom admin configurations
│   └── management/          # Management commands
├── clients/                 # Client management app
│   ├── models.py            # Client model
│   ├── views.py             # Client CRUD views
│   ├── forms.py             # Client forms
│   └── admin.py             # Client admin
├── tasks/                   # Task management app
│   ├── models.py            # Task and TaskComment models
│   ├── views.py             # Task CRUD views
│   ├── forms.py             # Task forms
│   └── admin.py             # Task admin
├── documents/               # Document management app
│   ├── models.py            # Document model
│   ├── views.py             # Document CRUD views
│   ├── forms.py             # Document forms
│   └── admin.py             # Document admin
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── dashboard.html       # Dashboard template
│   ├── clients/             # Client templates
│   ├── tasks/               # Task templates
│   └── documents/           # Document templates
├── static/                  # Static files (CSS, JS)
├── media/                   # Uploaded files
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── clientportal/           # Main project settings
    ├── settings.py         # Django settings
    └── urls.py             # Main URL configuration
```

## �� Configuration

### Environment Variables
Create a `.env` file with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
For production, update the database settings in `clientportal/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎯 Key Features Explained

### Multi-Tenancy
- Each tenant (business) has isolated data
- Users are associated with specific tenants
- All queries are automatically filtered by tenant
- Admin interface respects tenant boundaries

### Client Management
- Complete client profiles with contact information
- Status tracking (Active, Inactive, Prospect, Former)
- Company association and notes
- Task and document relationships

### Task Management
- Create and assign tasks to clients
- Priority levels (Low, Medium, High, Urgent)
- Status tracking (Pending, In Progress, Completed, Cancelled)
- Due date management with overdue detection
- Comment system for collaboration

### Document Management
- Secure file upload with validation
- File type and size restrictions
- Organized by client and document type
- Download functionality

## 🔒 Security Features

- **Tenant Isolation**: Data is automatically filtered by tenant
- **Authentication**: Django's secure authentication system
- **Authorization**: Role-based access control
- **File Validation**: Secure file upload with type checking
- **CSRF Protection**: Built-in CSRF protection
- **SQL Injection Protection**: Django ORM protection

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Clean Bootstrap 5 design
- **Intuitive Navigation**: Easy-to-use sidebar navigation
- **Visual Feedback**: Success/error messages and loading states
- **Search & Filter**: Advanced search capabilities
- **Pagination**: Efficient data loading

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in production
2. Use a strong `SECRET_KEY`
3. Configure PostgreSQL database
4. Set up static file serving
5. Configure media file storage (S3 recommended)
6. Set up HTTPS
7. Configure proper `ALLOWED_HOSTS`

### Heroku Deployment
```bash
# Install Heroku CLI
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t clientportal .
docker run -p 8000:8000 clientportal
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📝 API Documentation

The application includes a REST API (planned feature):
- Client endpoints for CRUD operations
- Task management endpoints
- Document upload/download endpoints
- Authentication and authorization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the Django documentation

## 🎉 Acknowledgments

- Django team for the excellent framework
- Bootstrap team for the UI components
- All contributors and users

---

**ClientPortal** - Empowering businesses to manage their client relationships effectively.
