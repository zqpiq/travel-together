# 🌍 Travel Together

**Travel Together** is a web platform for organizing shared travel experiences, helping travelers find companions and share costs for their adventures.
<img width="709" height="923" alt="Снимок экрана 2025-08-26 в 14 57 51" src="https://github.com/user-attachments/assets/adc891e2-9441-4986-b754-1c3057a12290" />

## ✨ Features

### 🔐 User Management
- User registration and authentication
- Detailed user profiles with avatars
- Contact information (phone, Telegram)
- Comment and rating system

### 🗺️ Travel Management
- Browse countries and popular destinations
- Create detailed travel plans with:
  - Date and duration
  - Budget ranges
  - Number of available seats
  - Descriptions
- Search trips by location

### 🤝 Request System
- Submit requests to join trips
- Manage requests (approve/reject)
- Access contact details after approval
- Post-trip comment system

### 📱 Responsive Design
- Bootstrap 5 interface
- Mobile-friendly layout
- Dark navigation bar

## 🛠️ Technologies

### Backend
- **Django 5.2.5** - web framework
- **SQLite** - database (default)
- **Cloudinary** - image storage
- **django-phonenumber-field** - phone number validation

### Frontend
- **Bootstrap 5** - CSS framework
- **Crispy Forms** - form styling
- **HTML/CSS/JavaScript**

### Dependencies
- **python-decouple** - configuration management
- **django-crispy-forms** - enhanced forms
- **pillow** - image processing

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Step by Step

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/travel-together.git
cd travel-together
```

2. **Create virtual environment**
```bash
python -m venv travel_env
source travel_env/bin/activate  # Linux/Mac
# or
travel_env\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
# .env
SECRET_KEY=your-secret-key-here
CLOUD_NAME=your-cloudinary-name
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Load initial data**
```bash
python manage.py loaddata countries.json
python manage.py loaddata locations.json
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Run development server**
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## ⚙️ Configuration

### Cloudinary Setup
1. Create account at [Cloudinary](https://cloudinary.com/)
2. Get your API credentials
3. Add them to your `.env` file

### Gmail SMTP Setup
1. Enable 2-factor authentication in Gmail
2. Create an app password
3. Add credentials to your `.env` file

### Database Configuration (Optional)
By default, the project uses SQLite. For PostgreSQL or MySQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travel_together_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎯 Usage

### For Travelers
1. **Sign Up** - Create an account
2. **Complete Profile** - Add contact information
3. **Browse Trips** - Explore available journeys
4. **Join Trips** - Submit participation requests
5. **Connect** - Get contacts after approval

### For Trip Organizers
1. **Create Trip** - Describe your travel plan
2. **Manage Requests** - Approve participants
3. **Communicate** - Connect with approved travelers
4. **Receive Feedback** - Get comments after trip completion

## 📁 Project Structure

```
travel_together/
├── account/                 # User management app
│   ├── models.py           # User and Profile models
│   ├── views.py            # Authentication views
│   ├── forms.py            # Registration and profile forms
│   └── admin.py            # Admin panel configuration
├── travels/                # Main travel app
│   ├── models.py           # Trip, Location, Country models
│   ├── views.py            # Travel and request views
│   ├── forms.py            # Trip creation forms
│   └── admin.py            # Admin panel configuration
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── registration/       # Authentication templates
│   └── travels/            # Travel-related templates
├── static/                 # Static files (CSS, images)
│   └── css/               # Custom stylesheets
├── travel_together/        # Project settings
│   ├── settings.py         # Django configuration
│   └── urls.py             # URL routing
├── countries.json          # Country fixtures
├── locations.json          # Location fixtures
├── requirements.txt        # Python dependencies
└── manage.py              # Django management utility
```

## 🔗 API Routes

### Main URL Patterns

- `/` - Homepage
- `/countries/` - Countries list
- `/locations/` - Locations list  
- `/trips/` - All trips list
- `/create-trip/` - Create new trip
- `/my-trips/` - User's trips
- `/requests/` - Manage requests
- `/account/register/` - User registration
- `/account/login/` - User login
- `/account/profile/` - User profile

### Data Models

**Trip** - main travel model
- `owner` - trip organizer
- `location` - destination
- `date` - travel date
- `budget` - budget range
- `duration_trip` - trip duration
- `number_of_seats` - available seats

**TripRequest** - participation request
- `trip` - related trip
- `user` - requesting user
- `status` - request status (pending/approved/rejected)

**Profile** - extended user information
- `phone_number` - contact phone
- `telegram` - Telegram username
- `avatar` - profile picture
- `date_birth` - birth date
- `about_me` - user description

## 🚢 Deployment

### Production Settings
1. Set `DEBUG = False` in settings.py
2. Configure allowed hosts
3. Set up a production database (PostgreSQL recommended)
4. Configure static files serving
5. Set up proper email backend

### Environment Variables
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@localhost/dbname
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🎉 Acknowledgments

- Django team for the amazing framework
- Bootstrap for responsive design
- Cloudinary for image storage
- All project contributors

## 📊 Project Statistics

- **Models**: 7 (User, Profile, Trip, TripRequest, Country, Location, Commentary)
- **Views**: 12+ (including class-based and function-based views)
- **Templates**: 15+ responsive HTML templates
- **Languages Supported**: English interface, timezone support for Europe/Kiev

---

**Travel Together** - Connect, Explore, Share! 🌟

Made with ❤️ using Django and Bootstrap
