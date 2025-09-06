# Shared Finance OS

A comprehensive expense splitting and settlement platform for modern groups, built with Django REST Framework and React.

## 🚀 Features

### Core Functionality
- **Smart Expense Splitting**: Multiple fairness algorithms (equal, income-based, proportional)
- **Receipt OCR**: Automatic data extraction from receipt images
- **Settlement Optimization**: Network flow algorithms for minimal transactions
- **Payment Integration**: UPI deep-links and webhook processing
- **Audit & Compliance**: Complete audit trails and consent management

### Technical Highlights
- **Backend**: Django 4.2 + DRF with JWT authentication
- **Frontend**: React 18 + TypeScript + Vite
- **Database**: PostgreSQL (production) / SQLite (development)
- **PWA**: Offline-first with service worker
- **Testing**: Comprehensive test suite with pytest
- **Deployment**: Docker + Docker Compose

## 📁 Project Structure

```
shared_finance_os/
├── shared_finance_backend/     # Django REST API
│   ├── shared_finance/         # Main Django project
│   ├── users/                  # User management
│   ├── groups/                 # Group management
│   ├── expenses/               # Expense tracking
│   ├── payments/               # Payment processing
│   ├── fairness/               # Settlement algorithms
│   ├── ocr/                    # Receipt processing
│   ├── audits/                 # Audit logging
│   └── notifications/          # Notification system
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/         # Reusable components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   ├── stores/             # State management
│   │   └── ui/                 # Design system
│   └── public/                 # Static assets
└── docs/                       # Documentation
```

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (for production)
- Git

### Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd shared_finance_os

# Set up Python environment
cd shared_finance_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
```

### Using Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

### Backend Environment Variables

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/shared_finance
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend Environment Variables

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Shared Finance OS
VITE_DEMO_MODE=true
```

## 📊 API Documentation

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `GET /api/auth/profile/` - User profile
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Groups
- `GET /api/groups/groups/` - List groups
- `POST /api/groups/groups/` - Create group
- `GET /api/groups/groups/{id}/` - Get group details
- `PATCH /api/groups/groups/{id}/` - Update group
- `DELETE /api/groups/groups/{id}/` - Delete group

### Expenses
- `GET /api/expenses/expenses/` - List expenses
- `POST /api/expenses/expenses/` - Create expense
- `GET /api/expenses/expenses/{id}/` - Get expense details
- `POST /api/expenses/expenses/{id}/upload_receipt/` - Upload receipt

### Settlements
- `POST /api/fairness/groups/{id}/compute_settlement/` - Compute settlement
- `GET /api/fairness/groups/{id}/settlement_graph/` - Get settlement graph

### Payments
- `POST /api/payments/initiate/` - Initiate payment
- `GET /api/payments/status/{id}/` - Get payment status
- `POST /api/payments/webhook/` - Payment webhook

## 🧪 Testing

### Backend Tests
```bash
cd shared_finance_backend
pytest
pytest --cov=.
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Integration Tests
```bash
# Run all tests
pytest tests/
```

## 🚀 Deployment

### Production Setup

1. **Database**: Set up PostgreSQL
2. **Environment**: Configure production environment variables
3. **Static Files**: Collect and serve static files
4. **SSL**: Set up SSL certificates
5. **Monitoring**: Configure logging and monitoring

### Docker Deployment

```bash
# Build images
docker-compose build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-Specific Configurations

- **Development**: SQLite, debug enabled, CORS open
- **Staging**: PostgreSQL, debug disabled, limited CORS
- **Production**: PostgreSQL, debug disabled, strict CORS, SSL

## 📈 Performance

### Backend Optimizations
- Database query optimization
- Redis caching for frequent operations
- Async task processing with Celery
- API response compression

### Frontend Optimizations
- Code splitting and lazy loading
- Image optimization
- Service worker caching
- Bundle size optimization

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control
- API rate limiting
- CORS configuration

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

### Privacy & Compliance
- GDPR compliance features
- Data encryption at rest
- Audit logging
- Consent management

## 🌐 Internationalization

- English and Hindi support
- RTL language support ready
- Localized date/time formats
- Currency formatting

## 📱 PWA Features

- Offline functionality
- Install prompts
- Background sync
- Push notifications
- App-like experience

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend
- Write comprehensive tests
- Update documentation
- Follow conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django and Django REST Framework
- React and the React ecosystem
- Tailwind CSS for styling
- Cytoscape.js for graph visualization
- All open-source contributors

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**Built with ❤️ for modern group finance management**