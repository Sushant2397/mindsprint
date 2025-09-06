# Development Guide

This document provides detailed information for developers working on the Shared Finance OS backend.

## Project Structure

```
shared_finance_backend/
├── shared_finance/          # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI configuration
├── users/                 # User management app
├── groups/                # Group management app
├── expenses/              # Expense tracking app
├── payments/              # Payment processing app
├── fairness/              # Settlement algorithms app
├── ocr/                   # OCR processing app
├── audits/                # Audit logging app
├── notifications/         # Notification app
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── README.md             # Project documentation
```

## Development Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed demo data
python manage.py seed_demo
```

### 3. Development Server

```bash
python manage.py runserver
```

## API Development

### Adding New Endpoints

1. **Create Serializer**
   ```python
   # app/serializers.py
   class NewModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = NewModel
           fields = '__all__'
   ```

2. **Create ViewSet**
   ```python
   # app/views.py
   class NewModelViewSet(viewsets.ModelViewSet):
       queryset = NewModel.objects.all()
       serializer_class = NewModelSerializer
       permission_classes = [IsAuthenticated]
   ```

3. **Add URL Configuration**
   ```python
   # app/urls.py
   router = DefaultRouter()
   router.register(r'new-models', NewModelViewSet)
   ```

### Authentication

The API uses JWT authentication. Include the token in requests:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/endpoint/
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Database Models

### User Model
- Extends Django's AbstractUser
- Additional fields: phone, locale, kyc_status, avatar
- Custom admin interface

### Group Model
- Expense sharing groups
- JSON settings field for flexibility
- Currency and billing cycle support

### Expense Model
- Individual expenses with OCR data
- GST support for Indian businesses
- Receipt file upload

### Payment Model
- Multiple payment methods
- Webhook integration
- Status tracking

## Services

### SettlementService
- Networkx-based settlement algorithms
- Multiple fairness policies
- Graph visualization support

### PaymentService
- UPI deep link generation
- Webhook processing
- Status management

### OCRService
- Receipt text extraction
- Data parsing and validation
- Error handling

## Production Considerations

### Security
- Use environment variables for secrets
- Enable HTTPS in production
- Implement rate limiting
- Add input validation

### Performance
- Database query optimization
- Caching with Redis
- CDN for static files
- Database indexing

### Monitoring
- Logging configuration
- Error tracking (Sentry)
- Performance monitoring
- Health checks

## Replacing Mock Services

### UPI Integration
Replace mock UPI service with real PSP integration:

1. **Update PaymentService**
   ```python
   def generate_upi_deeplink(self, amount, payer, payee):
       # Integrate with real UPI provider
       # e.g., Razorpay, PayU, etc.
   ```

2. **Configure Webhooks**
   - Set up webhook endpoints
   - Verify webhook signatures
   - Handle payment status updates

### Account Aggregator Integration
Replace mock consent system with real AA integration:

1. **Update Consent Model**
   - Add AA-specific fields
   - Implement consent flow
   - Handle data requests

2. **Integrate with AA APIs**
   - Consent creation
   - Data sharing
   - Status updates

## Database Migrations

### Creating Migrations
```bash
# Create migration for model changes
python manage.py makemigrations app_name

# Create empty migration for data changes
python manage.py makemigrations --empty app_name
```

### Applying Migrations
```bash
# Apply all pending migrations
python manage.py migrate

# Apply specific migration
python manage.py migrate app_name migration_name
```

### Rollback Migrations
```bash
# Rollback to previous migration
python manage.py migrate app_name previous_migration_name

# Rollback all migrations for an app
python manage.py migrate app_name zero
```

## Environment Configuration

### Development
```python
# settings.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Production
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shared_finance',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'db_host',
        'PORT': '5432',
    }
}
```

## Troubleshooting

### Common Issues

1. **Migration Errors**
   - Check model definitions
   - Verify field types
   - Run `python manage.py showmigrations`

2. **Import Errors**
   - Check Python path
   - Verify virtual environment
   - Check for circular imports

3. **Database Errors**
   - Check database connection
   - Verify migrations
   - Check field constraints

### Debugging

1. **Enable Debug Mode**
   ```python
   DEBUG = True
   ```

2. **Use Django Debug Toolbar**
   ```bash
   pip install django-debug-toolbar
   ```

3. **Check Logs**
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': 'debug.log',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['file'],
               'level': 'DEBUG',
               'propagate': True,
           },
       },
   }
   ```

## Contributing

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings
- Add tests

### Git Workflow
1. Create feature branch
2. Make changes
3. Add tests
4. Run tests
5. Submit pull request

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit PR

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [NetworkX Documentation](https://networkx.org/)
- [Pytesseract Documentation](https://pytesseract.readthedocs.io/)