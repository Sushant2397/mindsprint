# Shared Finance OS Frontend

A modern React + TypeScript frontend for the Shared Finance OS application, built with Vite and featuring a comprehensive design system.

## Features

- 🚀 **Modern Stack**: React 18, TypeScript, Vite
- 🎨 **Design System**: Tailwind CSS with custom components
- 🔐 **Authentication**: JWT-based auth with automatic token refresh
- 📱 **PWA Support**: Offline-first with service worker
- 🌐 **Internationalization**: i18next with English and Hindi support
- 📊 **Data Visualization**: Cytoscape.js for settlement graphs
- 🧪 **Testing**: Vitest + Testing Library
- 📚 **Storybook**: Component documentation and development
- 🎯 **State Management**: Zustand for global state
- 📝 **Forms**: React Hook Form with Zod validation

## Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create a `.env.local` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Shared Finance OS
VITE_APP_VERSION=1.0.0
VITE_DEMO_MODE=true
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Auth/           # Authentication components
│   ├── Dashboard/      # Dashboard-specific components
│   ├── Group/          # Group management components
│   ├── Expense/        # Expense tracking components
│   ├── SettlementGraph/ # Settlement visualization
│   ├── Admin/          # Admin panel components
│   └── ConsentCenter/  # Consent management
├── pages/              # Page components
├── hooks/              # Custom React hooks
├── services/           # API services and utilities
├── stores/             # Zustand state stores
├── types/              # TypeScript type definitions
├── ui/                 # Design system components
├── utils/              # Utility functions
└── locales/            # Internationalization files
```

## Key Components

### Authentication
- **LoginForm**: User login with validation
- **RegisterForm**: User registration with validation
- **ProtectedRoute**: Route protection wrapper

### Design System
- **Button**: Variant-based button component
- **Input**: Form input with validation states
- **Card**: Content container component
- **Modal**: Overlay dialog component
- **Badge**: Status indicator component

### State Management
- **authStore**: User authentication state
- **appStore**: Application-wide state (theme, notifications, etc.)

## API Integration

The frontend communicates with the Django REST API through the `apiService`:

```typescript
// Example API usage
import { apiService } from './services/api';

// Get user groups
const groups = await apiService.getGroups();

// Create new expense
const expense = await apiService.createExpense({
  group: groupId,
  amount_subtotal: 100,
  vendor: 'Restaurant',
  // ... other fields
});
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run unit tests
- `npm run test:ui` - Run tests with UI
- `npm run storybook` - Start Storybook
- `npm run build-storybook` - Build Storybook

### Testing

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Storybook

```bash
# Start Storybook development server
npm run storybook

# Build static Storybook
npm run build-storybook
```

## PWA Features

- **Offline Support**: Cached API responses and static assets
- **Install Prompt**: "Add to Home Screen" functionality
- **Background Sync**: Sync pending changes when online
- **Push Notifications**: Real-time updates (when implemented)

## Internationalization

The app supports multiple languages with i18next:

```typescript
// Usage in components
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

## Demo Mode

When `VITE_DEMO_MODE=true`, the app includes:
- Demo data seeding functionality
- Mock payment flows
- Simulated webhook responses
- Placeholder data for development

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow the existing code style
2. Write tests for new components
3. Update Storybook stories
4. Ensure TypeScript types are correct
5. Test PWA functionality

## License

MIT License - see LICENSE file for details.