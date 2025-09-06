# Shared Finance OS Demo Script

This script demonstrates the complete functionality of the Shared Finance OS application.

## Prerequisites

1. **Backend Server**: Ensure the Django backend is running on `http://localhost:8000`
2. **Frontend Server**: Ensure the React frontend is running on `http://localhost:3000`
3. **Demo Data**: Use the "Load Demo Data" button to populate sample data

## Demo Flow

### 1. Authentication (2 minutes)
- **Login**: Use any credentials (demo mode enabled)
- **Registration**: Create a new account with email/password
- **Auto-redirect**: After login, redirect to dashboard

### 2. Dashboard Overview (3 minutes)
- **Groups List**: View all groups you're part of
- **Statistics**: See total groups, expenses, and pending settlements
- **Demo Data**: Click "Load Demo Data" to populate sample groups
- **Group Cards**: Each group shows member count, currency, and status

### 3. Group Management (5 minutes)
- **Group Details**: Click on any group to view details
- **Group Info**: See group type, currency, billing cycle, GST mode
- **Members**: View group members and their roles
- **Settings**: Access group configuration options

### 4. Expense Management (8 minutes)
- **Add Expense**: Create new expenses with manual entry
- **Receipt Upload**: Upload receipt images for OCR processing
- **Voice Input**: Use Web Speech API for hands-free data entry
- **Categories**: Organize expenses by category (food, transport, etc.)
- **GST Handling**: Automatic GST calculation and invoice number extraction

### 5. Fairness & Settlement (10 minutes)
- **Policy Selection**: Choose from multiple fairness policies:
  - Equal Split: Everyone pays the same amount
  - Income-based: Proportional to income brackets
  - Custom Share: Manual share factors
  - Proportional: Based on usage patterns
- **Settlement Calculation**: Compute optimal settlement plan
- **Visualization**: Interactive settlement graph with Cytoscape.js
- **Explanation**: Step-by-step human-readable settlement breakdown
- **Envy Score**: Visual indicator of fairness

### 6. Payment Processing (5 minutes)
- **Payment Initiation**: Generate UPI deep-links for payments
- **Mock UPI**: Simulated payment flow for demo purposes
- **Webhook Simulation**: Test payment status updates
- **Payment History**: Track all payment attempts and statuses

### 7. Consent & Privacy (3 minutes)
- **Consent Center**: Manage data sharing permissions
- **Account Aggregator**: Mock AA-style consent flows
- **Data Sharing**: Share exports with accountants
- **Revocation**: Revoke consents when needed

### 8. Audit & Exports (4 minutes)
- **CSV Export**: Download expense data as CSV
- **PDF Reports**: Generate formatted PDF reports
- **Audit Trail**: View all system activities
- **Compliance**: Ensure regulatory compliance

### 9. PWA Features (2 minutes)
- **Offline Mode**: Test offline functionality
- **Install Prompt**: "Add to Home Screen" functionality
- **Background Sync**: Sync pending changes when online
- **Push Notifications**: Real-time updates (simulated)

### 10. Advanced Features (5 minutes)
- **Internationalization**: Switch between English and Hindi
- **Theme Toggle**: Light/dark mode switching
- **Responsive Design**: Test on different screen sizes
- **Accessibility**: Keyboard navigation and ARIA attributes

## Key Demo Points

### Technical Highlights
- **Modern Stack**: React 18, TypeScript, Vite
- **State Management**: Zustand for global state
- **API Integration**: Axios with automatic token refresh
- **Form Validation**: React Hook Form + Zod
- **Data Visualization**: Cytoscape.js for settlement graphs
- **PWA Support**: Offline-first with service worker

### Business Value
- **Smart Splitting**: AI-powered expense distribution
- **Fairness Algorithms**: Multiple policy options
- **Compliance**: Built-in audit trails and consent management
- **Scalability**: Handles groups from 2 to 100+ members
- **Integration**: UPI, GST, and accounting system ready

### User Experience
- **Intuitive UI**: Clean, modern interface
- **Accessibility**: WCAG 2.1 compliant
- **Performance**: Fast loading and smooth animations
- **Mobile-First**: Responsive design for all devices
- **Offline Support**: Works without internet connection

## Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure backend CORS is configured for localhost:3000
2. **Token Expiry**: Refresh tokens are handled automatically
3. **Demo Data**: Use the "Load Demo Data" button if no groups appear
4. **PWA Issues**: Clear browser cache and reinstall if needed

### Performance Tips
1. **Large Groups**: Settlement calculation may take longer for 50+ members
2. **Receipt OCR**: Large images may take time to process
3. **Offline Mode**: Some features require internet connection

## Success Metrics

- **User Onboarding**: < 2 minutes from login to first expense
- **Expense Creation**: < 30 seconds per expense
- **Settlement Calculation**: < 5 seconds for groups up to 20 members
- **Payment Processing**: < 10 seconds for UPI deep-link generation
- **Export Generation**: < 15 seconds for PDF reports

## Next Steps

After the demo, consider:
1. **Production Deployment**: Use Docker containers
2. **Database Migration**: Move from SQLite to PostgreSQL
3. **Authentication**: Implement OAuth2 with Google/Microsoft
4. **Payment Integration**: Connect to real UPI providers
5. **Analytics**: Add user behavior tracking
6. **Mobile App**: React Native version for mobile users

---

**Total Demo Time**: ~45 minutes
**Audience**: Technical stakeholders, product managers, potential users
**Focus**: Showcase both technical excellence and business value