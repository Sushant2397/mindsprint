# Shared Finance OS Backend

A comprehensive Django REST API backend for Shared Finance OS - A platform for expense sharing, settlement calculations, and payment processing.

## Features

- **User Management**: Custom user model with KYC status, phone, and locale support
- **Group Management**: Create and manage expense sharing groups with different roles
- **Expense Tracking**: Track shared expenses with receipt upload and OCR processing
- **Fair Settlement**: Multiple fairness policies with networkx-based settlement algorithms
- **Payment Processing**: UPI integration with webhook support (simulated)
- **Consent Management**: Account Aggregator-style data sharing consent system
- **Audit Logging**: Immutable audit trail for all operations
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shared_finance_backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed demo data (optional)**
   ```bash
   python manage.py seed_demo
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Documentation

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **API Schema**: `http://localhost:8000/api/schema/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile

### Groups
- `GET /api/groups/groups/` - List user's groups
- `POST /api/groups/groups/` - Create new group
- `GET /api/groups/groups/{id}/` - Get group details
- `POST /api/groups/groups/{id}/add_member/` - Add member to group
- `POST /api/groups/groups/{id}/remove_member/` - Remove member from group

### Expenses
- `GET /api/expenses/expenses/` - List expenses
- `POST /api/expenses/expenses/` - Create new expense
- `GET /api/expenses/expenses/{id}/` - Get expense details
- `POST /api/expenses/expenses/{id}/mark_settled/` - Mark expense as settled

### Payments
- `GET /api/payments/ledger/` - List ledger entries
- `POST /api/payments/initiate/` - Initiate payment
- `POST /api/payments/webhook/` - Payment webhook
- `GET /api/payments/status/{id}/` - Get payment status

### Fairness & Settlement
- `POST /api/fairness/groups/{id}/compute_settlement/` - Compute settlement
- `GET /api/fairness/groups/{id}/settlement_graph/` - Get settlement graph

### OCR
- `POST /api/ocr/expenses/{id}/upload_receipt/` - Upload and process receipt

### Consents
- `POST /api/consents/` - Create consent
- `GET /api/consents/{id}/` - Get consent details
- `POST /api/consents/{id}/share/` - Share data based on consent

## Sample API Calls

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+919876543210"
  }'
```

### 2. Create Group
```bash
curl -X POST http://localhost:8000/api/groups/groups/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Roommates",
    "description": "Shared expenses for our apartment",
    "group_type": "roommates",
    "currency": "INR"
  }'
```

### 3. Compute Settlement
```bash
curl -X POST http://localhost:8000/api/fairness/groups/1/compute_settlement/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "policy_type": "equal_split"
  }'
```

### 4. Upload Receipt
```bash
curl -X POST http://localhost:8000/api/ocr/expenses/1/upload_receipt/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "receipt=@receipt.jpg"
```

### 5. Initiate Payment
```bash
curl -X POST http://localhost:8000/api/payments/initiate/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ledger_entry_id": 1,
    "method": "UPI_DEEPLINK"
  }'
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Run linting
flake8 .

# Run type checking
mypy .
```

### Database
The project uses SQLite by default for development. For production, configure PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shared_finance',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Production Deployment

### Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/shared_finance
```

### Docker Deployment
```bash
docker-compose up -d
```

## Architecture

### Models
- **User**: Custom user model with additional fields
- **Group**: Expense sharing groups with settings
- **GroupMember**: Group membership with roles and share factors
- **Expense**: Individual expenses with OCR data
- **ExpenseSplit**: How expenses are divided among members
- **LedgerEntry**: Debt tracking between users
- **Payment**: Payment processing and status
- **Consent**: Data sharing consent management
- **AuditLog**: Immutable audit trail

### Services
- **SettlementService**: Networkx-based settlement algorithms
- **PaymentService**: Payment processing and webhook handling
- **OCRService**: Receipt processing with pytesseract

### Fairness Policies
- **Equal Split**: Divide expenses equally among all members
- **Income Based**: Adjust based on member income brackets
- **Custom Share**: Use custom share factors
- **Proportional**: Based on individual expense contributions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.