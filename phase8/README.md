# Phase 8: Frontend Application (Next.js)

This folder contains the implementation of Phase 8 - the frontend web application for the restaurant recommendation system using Next.js 14 with TypeScript.

## Features

### 🎯 Core Features
- **Modern Next.js 14 App** with TypeScript support
- **Responsive Design** with Tailwind CSS
- **Component Library** with reusable UI components
- **State Management** with Zustand
- **API Integration** with custom fetch client
- **Form Handling** with validation
- **Loading States** and error handling
- **Restaurant Search** and filtering
- **Recommendation Display** with detailed information
- **User Dashboard** with history and favorites

### 📁 Project Structure

```
phase8/
├── package.json              # Dependencies and scripts
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Root layout component
│   │   ├── page.tsx        # Home page
│   │   └── globals.css      # Global styles
│   ├── components/            # Reusable UI components
│   ├── lib/                 # Utility functions and API client
│   ├── types/               # TypeScript type definitions
│   ├── hooks/               # Custom React hooks
│   ├── store/               # State management
│   └── utils/               # Helper functions
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn package manager

### Installation

```bash
# Navigate to phase8 directory
cd phase8

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start
```

### Environment Setup

Create a `.env.local` file for environment variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 📱 Pages

### Home Page (/)
- Hero section with app introduction
- Quick recommendation form
- Feature highlights
- Call-to-action buttons

### Recommendations Page (/recommendations)
- Comprehensive preference form
- Real-time validation
- Results display with loading states
- Filtering and sorting options
- Save to favorites functionality

### Restaurant Search (/restaurants)
- Advanced search interface
- Filter by location, cuisine, rating, price
- Search results grid/list view
- Restaurant detail modal

### Restaurant Details (/restaurants/[id])
- Complete restaurant information
- Photos gallery
- Menu preview
- Reviews and ratings
- Similar recommendations

### Dashboard (/dashboard)
- User recommendation history
- Favorite restaurants
- Search statistics
- Preference management

### System Status (/status)
- Live system health monitoring
- API performance metrics
- Service status indicators

## 🧩 Components

### UI Components
- **RestaurantCard** - Restaurant display with actions
- **RecommendationForm** - Preference input form
- **SearchFilters** - Advanced search filters
- **LoadingSpinner** - Loading state indicator
- **ErrorMessage** - Error display component
- **HealthStatus** - System health dashboard

### Forms
- **PreferenceForm** - User preferences with validation
- **SearchForm** - Restaurant search with filters

### Layout Components
- **Header** - Navigation and branding
- **Footer** - Site information and links
- **Sidebar** - Navigation menu
- **Container** - Responsive layout wrapper

## 🎨 Design System

### Colors
- **Primary**: Blue-600 (#3b82f6)
- **Secondary**: Orange-500 (#f97316)
- **Success**: Green-500 (#10b981)
- **Warning**: Yellow-500 (#eab308)
- **Error**: Red-500 (#ef4444)
- **Neutral**: Gray shades

### Typography
- **Headings**: Inter font, bold weights
- **Body**: Inter font, regular/medium weights
- **Monospace**: JetBrains Mono for code/IDs

### Responsive Design
- **Mobile-first** approach
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Grid system**: 12-column grid with Tailwind

## 🔧 State Management

### Zustand Store Structure
```typescript
interface AppState {
  user: {
    preferences: UserPreferences | null;
    favorites: RestaurantInfo[];
    history: RecommendationResponse[];
  };
  ui: {
    theme: 'light' | 'dark';
    sidebarOpen: boolean;
    notifications: Notification[];
  };
}
```

## 🌐 API Integration

### API Client
- Custom fetch-based client with error handling
- Request/response type safety
- Automatic retry logic
- Response caching

### Endpoints
- `GET /api/health` - System health check
- `POST /api/recommendations` - Generate recommendations
- `GET /api/restaurants/search` - Search restaurants
- `POST /api/preferences/validate` - Validate preferences
- `GET /api/metadata` - System metadata

## ♿ Accessibility

### WCAG 2.1 AA Compliance
- Semantic HTML elements
- ARIA labels and descriptions
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- Color contrast ratios (4.5:1 minimum)

### Features
- Skip to main content link
- Focus visible indicators
- Alt text for images
- Descriptive link text
- Form labels and descriptions

## 🧪 Testing

### Unit Tests
- Component rendering tests
- Form validation tests
- Utility function tests
- Hook behavior tests

### Integration Tests
- API integration tests
- User flow tests
- Navigation tests
- State management tests

### E2E Tests
- Critical user journeys
- Form submission flows
- Search functionality
- Recommendation generation

## 📊 Performance

### Optimization
- Image optimization with Next.js Image
- Code splitting with dynamic imports
- Client-side caching of API responses
- Infinite scroll for search results
- Debounced search inputs
- Optimistic updates for favorites

### SEO
- Meta tags for all pages
- Structured data for restaurants
- Open Graph tags for sharing
- Sitemap generation
- robots.txt configuration

## 🚀 Deployment

### Build Configuration
```bash
# Production build
npm run build

# Start production server
npm run start
```

### Environment Variables
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NODE_ENV` - Environment (development/production)

### Platform Deployment
- **Vercel**: Recommended for Next.js apps
- **Netlify**: Static site deployment
- **AWS Amplify**: Full-stack deployment
- **Docker**: Containerized deployment

## 🔧 Development

### Code Quality
- ESLint configuration for code consistency
- Prettier for code formatting
- TypeScript strict mode for type safety
- Husky for git hooks

### Development Scripts
```json
{
  "dev": "next dev",
  "build": "next build", 
  "start": "next start",
  "lint": "next lint",
  "type-check": "tsc --noEmit",
  "test": "jest",
  "test:watch": "jest --watch"
}
```

## 🔄 Integration with Backend

### API Configuration
- Base URL: `http://localhost:8000/api`
- Request/response models match Phase 7 API
- Error handling with user-friendly messages
- Loading states and retry logic

### Data Flow
1. User input → Form validation
2. Form submission → API request
3. API response → State update
4. State update → UI re-render
5. Error handling → User feedback

## 🎯 Key Features Implemented

### ✅ Completed
- [x] Project structure and configuration
- [x] TypeScript types and interfaces
- [x] API client with error handling
- [x] Basic layout and styling
- [x] Home page with hero section
- [x] Form components and validation
- [x] Restaurant card components

### 🚧 In Progress
- [ ] Complete React component integration
- [ ] Implement state management with Zustand
- [ ] Add TanStack Query for data fetching
- [ ] Complete all pages (recommendations, search, dashboard)
- [ ] Add responsive design with Tailwind
- [ ] Implement accessibility features
- [ ] Add loading states and error handling

### 📋 Next Steps
1. Install dependencies: `npm install`
2. Fix TypeScript configuration for React/Next.js
3. Complete component implementations
4. Add state management and data fetching
5. Implement remaining pages
6. Add testing and deployment configuration

## 🐛 Troubleshooting

### Common Issues
- **TypeScript errors**: Ensure React types are installed
- **Import errors**: Check file paths and module resolution
- **Styling issues**: Verify Tailwind CSS configuration
- **API errors**: Check backend server is running on port 8000

### Solutions
- Run `npm install` to install all dependencies
- Check `tsconfig.json` paths configuration
- Verify environment variables are set
- Ensure backend API is accessible

---

Phase 8 provides a modern, responsive frontend application that seamlessly integrates with the Phase 7 FastAPI backend, delivering a complete full-stack restaurant recommendation system.
