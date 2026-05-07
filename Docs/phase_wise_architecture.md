## Phase-wise Architecture: AI-Powered Restaurant Recommendation System

### Phase 0 — Project Setup (Foundation)

- **Repo structure**: `Docs/`, `src/`, `data/` (or `storage/`)
- **Configuration**: dataset source/path, model provider + API key, runtime environment variables
- **Logging**: basic request + error logs

**Deliverable**: runnable skeleton (CLI or minimal UI) with configs wired.

---

### Phase 1 — Data Ingestion & Preparation (Offline/Batch)

- **Dataset loader**: pulls Zomato dataset from Hugging Face
- **Preprocessor/cleaner**: missing values, duplicates, normalization (city/cuisine/cost/rating)
- **Schema mapping**: standardize fields like:
  - restaurant name
  - city/location
  - cuisine(s)
  - average cost / price range
  - rating
  - other useful metadata (if available)
- **Storage layer (choose one)**:
  - simple: CSV/Parquet
  - query-friendly: SQLite/Postgres

**Data flow**: Hugging Face dataset → preprocess/normalize → stored restaurant dataset.

**Deliverable**: clean, queryable dataset with consistent schema.

---

### Phase 2 — User Preference Collection & Validation (Online)

- **Input UI**: capture location, budget, cuisine, minimum rating, extra preferences
- **Validator/normalizer**:
  - budget mapping (low/medium/high → numeric range)
  - city/cuisine standardization (case, synonyms, typos if needed)

**Deliverable**: validated `UserPreferences` object ready for retrieval + prompting.

---

### Phase 3 — Candidate Retrieval (Deterministic Layer)

- **Filter engine**: applies hard constraints (city, min rating, budget range, cuisine)
- **Scoring/heuristics (optional)**: tie-break scoring (rating, budget match, cuisine match)
- **Shortlist builder**: select top \(N\) candidates for the LLM (e.g., 20–50)

**Data flow**: stored dataset + user preferences → filter/score → candidate shortlist (structured).

**Deliverable**: compact, high-quality candidate list (cost-controlled, relevant).

---

### Phase 4 — LLM Recommendation & Explanation (AI Layer)

- **Prompt builder**: formats user preferences + candidate shortlist + strict output rules
- **LLM gateway**: model call (timeouts, retries, rate-limit handling)
- **Structured output parser**: enforce JSON output (ranked list + explanations)
- **Quality/safety checks**:
  - ensure recommendations come only from the provided shortlist
  - handle malformed outputs safely

**Deliverable**: ranked recommendations with concise, human-like explanations.

---

### Phase 5 — Presentation Layer (User Output) ✅ COMPLETED

- **Renderer**: show top \(K\) results with:
  - restaurant name, cuisine, rating, estimated cost, location
  - AI-generated explanation with word wrapping
  - Multiple output formats: Console, JSON, Markdown, Enhanced
- **UX enhancements**:
  - **Sorting**: By rank, rating (high/low), cost (high/low), name (A/Z)
  - **Filtering**: By minimum rating, maximum cost, cuisine, location
  - **Comparison tools**: Side-by-side restaurant analysis with statistics
  - **Preference refinement**: AI-powered suggestions for better results
  - **Filter suggestions**: Context-aware filtering recommendations

**Deliverable**: user-friendly output for comparison and decision-making.

**Implementation Details**:
- `phase5/renderer.py`: Core rendering functionality
- `phase5/ux_enhancements.py`: Advanced UX features
- `phase5/main_simple.py`: Standalone CLI interface
- Supports Unicode-safe console output for cross-platform compatibility

---

### Phase 6 — Evaluation, Monitoring & Iteration (Quality Loop)

- **Golden test queries**: repeatable preference cases to validate behavior
- **Metrics**:
  - constraint satisfaction (location/budget/cuisine/rating match)
  - diversity of results
  - latency and token/cost tracking
- **Logging/monitoring**: input stats (anonymized), shortlist size, parse success, error rates

**Deliverable**: measurable quality improvements over time (prompt + retrieval tuning).

---

### Phase 7 — Backend API Layer (Web Services)

- **FastAPI Application**: Production-ready web server with async support
- **RESTful Endpoints**:
  - `GET /api/health` - System health check and status
  - `POST /api/recommendations` - Generate restaurant recommendations
  - `GET /api/recommendations/{id}` - Retrieve previous recommendations
  - `GET /api/restaurants/search` - Restaurant search and filtering
  - `POST /api/preferences/validate` - Preference validation and normalization
  - `GET /api/metadata` - System metadata and statistics
  - `GET /api/metrics` - Performance and quality metrics
- **Service Layer**: Orchestrates Phases 1-5 pipeline with proper error handling
- **Data Integration**: SQLite database with Redis caching layer
- **Authentication**: JWT-based user authentication (optional)
- **Rate Limiting**: API abuse prevention and cost management

**Deliverable**: Production-ready REST API with full CRUD operations.

---

### Phase 8 — Frontend Application (User Interface)

- **React.js Application**: Modern single-page application with TypeScript
- **User Interface Components**:
  - Preference collection forms with validation
  - Restaurant recommendation display with filtering/sorting
  - Comparison tools and detailed restaurant views
  - User dashboard with history and favorites
- **Real-time Features**: WebSocket integration for live updates
- **State Management**: React Query + Zustand for data management
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Performance**: Code splitting, lazy loading, caching

**Deliverable**: User-friendly web interface for restaurant recommendations.

---

## Google Stitch Frontend Generation Prompt

### Next.js Frontend Generation Prompt

Copy and paste the following prompt into Google Stitch to generate the complete Next.js frontend for the restaurant recommendation system:

```
Create a modern, responsive restaurant recommendation web application using Next.js 14 with TypeScript. The application should integrate with a FastAPI backend that provides RESTful endpoints for restaurant recommendations, health monitoring, and system metadata.

## Backend API Integration

### Base URL: http://localhost:8000/api

### Available Endpoints:
- GET /health - System health check
- POST /recommendations - Generate restaurant recommendations
- GET /recommendations/{id} - Retrieve previous recommendations
- GET /restaurants/search - Search restaurants with filters
- POST /preferences/validate - Validate user preferences
- GET /metadata - System metadata and capabilities
- GET /metrics - System performance metrics

### API Request/Response Models:

#### Recommendation Request:
```typescript
interface RecommendationRequest {
  preferences: {
    location: string;
    budget: { min: number; max: number };
    minimum_rating: number;
    cuisines: string[];
    additional_preferences?: string;
  };
  top_k?: number; // default 5, max 20
  include_explanations?: boolean; // default true
}
```

#### Recommendation Response:
```typescript
interface RecommendationResponse {
  request_id: string;
  preferences: UserPreferences;
  recommendations: RestaurantInfo[];
  metadata: {
    processing_time: number;
    candidates_considered: number;
    model_used: string;
    top_k_requested: number;
    recommendations_generated: number;
    include_explanations: boolean;
    pipeline_version: string;
  };
  created_at: string;
}
```

#### Restaurant Info:
```typescript
interface RestaurantInfo {
  name: string;
  city: string;
  cuisines: string[];
  rating: number;
  cost_estimate: number;
  reason: string;
}
```

## Frontend Requirements

### Technology Stack:
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form with Zod validation
- **UI Components**: Headless UI + custom components
- **Icons**: Lucide React
- **Routing**: Next.js App Router (built-in)

### Pages Required:

#### 1. Home Page (/)
- Hero section with app introduction
- Quick recommendation form (location, budget, rating)
- Featured restaurants carousel
- Call-to-action to get personalized recommendations

#### 2. Recommendations Page (/recommendations)
- Comprehensive preference form with all options
- Real-time form validation
- Loading states during recommendation generation
- Results display with restaurant cards
- Filtering and sorting options
- Save to favorites functionality
- Share recommendations feature

#### 3. Restaurant Search Page (/restaurants)
- Advanced search interface with filters
- Search results grid/list view toggle
- Restaurant detail modal/overlay
- Search history
- Filter chips for quick filtering

#### 4. Restaurant Details Page (/restaurants/[id])
- Complete restaurant information
- Photos gallery
- Menu preview
- Reviews and ratings
- Similar recommendations
- Map integration (if available)
- Book/call-to-action buttons

#### 5. Dashboard Page (/dashboard)
- User recommendation history
- Favorite restaurants
- Search statistics
- Preference management
- Account settings

#### 6. System Status Page (/status)
- Live system health monitoring
- API performance metrics
- Service status indicators
- System statistics

### Components Required:

#### Recommendation Form:
```typescript
interface RecommendationFormProps {
  onSubmit: (preferences: UserPreferences) => void;
  loading?: boolean;
}
```

#### Restaurant Card:
```typescript
interface RestaurantCardProps {
  restaurant: RestaurantInfo;
  showReason?: boolean;
  onSaveFavorite?: (restaurant: RestaurantInfo) => void;
  onViewDetails?: (restaurant: RestaurantInfo) => void;
}
```

#### Search Filters:
```typescript
interface SearchFiltersProps {
  filters: SearchFilters;
  onFiltersChange: (filters: SearchFilters) => void;
}
```

#### Health Status Dashboard:
```typescript
interface HealthStatusProps {
  refreshInterval?: number;
}
```

### Design Requirements:

#### Color Scheme:
- Primary: Blue (Blue-600)
- Secondary: Orange (Orange-500)
- Success: Green (Green-500)
- Warning: Yellow (Yellow-500)
- Error: Red (Red-500)
- Neutral: Gray shades (Gray-50 to Gray-900)

#### Typography:
- Headings: Inter font, bold weights
- Body: Inter font, regular/medium weights
- Monospace: JetBrains Mono for code/IDs

#### Layout:
- Responsive design (mobile-first)
- Max width container (1280px)
- Consistent spacing (4px base unit)
- Card-based layouts for content
- Sticky navigation on desktop
- Bottom navigation on mobile

#### Interactive Elements:
- Smooth transitions (200ms)
- Hover states on all interactive elements
- Loading skeletons for async operations
- Toast notifications for user feedback
- Modal dialogs for complex interactions
- Tooltips for additional information

### State Management:

#### Global State (Zustand):
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

#### Server State (React Query):
- Recommendations cache
- Restaurant search cache
- System metrics cache
- User preferences cache

### Performance Requirements:

#### Optimization:
- Image optimization with Next.js Image component
- Code splitting with dynamic imports
- Client-side caching of API responses
- Infinite scroll for search results
- Debounced search inputs
- Optimistic updates for favorites

#### SEO:
- Meta tags for all pages
- Structured data for restaurants
- Open Graph tags for sharing
- Sitemap generation
- robots.txt configuration

### Error Handling:

#### Global Error Boundaries:
- Catch and log runtime errors
- User-friendly error messages
- Retry mechanisms for failed requests
- Offline support with service workers

#### Form Validation:
- Real-time validation with Zod schemas
- Clear error messages
- Validation on blur and submit
- Accessibility-friendly error display

### Accessibility:

#### WCAG 2.1 AA Compliance:
- Semantic HTML elements
- ARIA labels and descriptions
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- Color contrast ratios (4.5:1 minimum)

#### Features:
- Skip to main content link
- Focus visible indicators
- Alt text for images
- Descriptive link text
- Form labels and descriptions

### Testing:

#### Unit Tests:
- Component rendering tests
- Form validation tests
- Utility function tests
- Hook behavior tests

#### Integration Tests:
- API integration tests
- User flow tests
- Navigation tests
- State management tests

#### E2E Tests:
- Critical user journeys
- Form submission flows
- Search functionality
- Recommendation generation

### Deployment:

#### Build Configuration:
- Production optimizations
- Environment variable management
- Asset optimization
- Bundle analysis

#### Environment Setup:
- Development (localhost:3000)
- Staging environment
- Production deployment

### Additional Features:

#### Progressive Web App:
- Service worker for offline support
- App manifest for installability
- Push notifications for recommendations

#### Analytics:
- User interaction tracking
- Performance monitoring
- Error reporting
- Usage statistics

#### Internationalization:
- Multi-language support
- Currency formatting
- Date/time localization
- RTL language support

## Implementation Notes:

1. Use TypeScript strict mode for type safety
2. Follow Next.js 14 App Router conventions
3. Implement proper error boundaries
4. Use environment variables for API configuration
5. Implement proper loading states and skeleton screens
6. Add comprehensive error handling and user feedback
7. Ensure mobile responsiveness across all breakpoints
8. Implement proper SEO optimization
9. Add accessibility features for WCAG compliance
10. Include comprehensive testing strategy

The application should provide a seamless, modern user experience for discovering and exploring restaurant recommendations with AI-powered personalization.
```

---

## Backend Architecture

### Core Backend Components

#### API Layer
- **FastAPI Application** (`src/zomato_rec/web_ui/app.py`)
- **RESTful Endpoints**:
  - `POST /api/recommendations` - Generate recommendations
  - `GET /api/recommendations/{id}` - Retrieve previous recommendations
  - `GET /api/restaurants/search` - Restaurant search
  - `POST /api/preferences/validate` - Preference validation
- **Request/Response Models**: Pydantic schemas for type safety
- **Error Handling**: Structured error responses with proper HTTP status codes

#### Service Layer
- **Recommendation Service**: Orchestrates Phases 1-5 pipeline
- **Data Service**: Manages dataset operations and caching
- **LLM Service**: Handles Groq API integration with retry logic
- **Validation Service**: Input validation and normalization

#### Data Layer
- **Primary Storage**: SQLite database for user data and recommendations
- **Cache Layer**: Redis for frequent queries and session data
- **File Storage**: JSON files for phase outputs and datasets
- **Database Schema**:
  ```sql
  users (id, preferences, created_at, updated_at)
  recommendations (id, user_id, preferences, results, created_at)
  restaurants (id, name, city, cuisines, rating, cost, metadata)
  ```

#### Configuration & Security
- **Environment Variables**: API keys, database URLs, feature flags
- **Authentication**: JWT-based user authentication (optional)
- **Rate Limiting**: Prevent API abuse and manage costs
- **Logging**: Structured logging with correlation IDs

---

## Frontend Architecture

### Web Application Structure

#### Technology Stack
- **Framework**: React.js with TypeScript
- **UI Library**: Tailwind CSS + Headless UI components
- **State Management**: React Query + Zustand
- **Routing**: React Router v6
- **Build Tool**: Vite

#### Component Architecture
```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   ├── forms/           # Preference input forms
│   ├── recommendations/  # Result display components
│   └── layout/          # Layout components
├── pages/
│   ├── Home.tsx         # Main recommendation interface
│   ├── History.tsx      # Previous recommendations
│   └── Settings.tsx     # User preferences
├── hooks/
│   ├── useRecommendations.ts
│   ├── usePreferences.ts
│   └── useRestaurantSearch.ts
├── services/
│   ├── api.ts           # API client
│   └── types.ts         # TypeScript types
└── utils/
    ├── validation.ts    # Form validation
    └── formatting.ts    # Data formatting
```

#### Key Features
- **Progressive Enhancement**: Works without JavaScript initially
- **Real-time Updates**: WebSocket integration for live recommendations
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Code splitting, lazy loading, caching

#### User Interface Flow
1. **Preference Collection**: Multi-step form with validation
2. **Loading States**: Skeleton screens during processing
3. **Results Display**: Card-based layout with filtering/sorting
4. **Comparison Mode**: Side-by-side restaurant comparison
5. **History**: Previous recommendations with save/favorite options

---

## Integration Architecture

### API Specification

#### Generate Recommendations
```http
POST /api/recommendations
Content-Type: application/json

{
  "location": "Bellandur",
  "budget": {"min": 0, "max": 2000},
  "minimum_rating": 4.0,
  "cuisines": ["North Indian", "Chinese"],
  "additional_preferences": "Family-friendly"
}

Response:
{
  "id": "rec_123",
  "preferences": {...},
  "recommendations": [...],
  "metadata": {
    "processing_time": 2.3,
    "candidates_considered": 30,
    "model_used": "llama-3.3-70b-versatile"
  }
}
```

#### Restaurant Search
```http
GET /api/restaurants/search?location=Bellandur&cuisine=NorthIndian&limit=10

Response:
{
  "restaurants": [...],
  "total": 25,
  "page": 1
}
```

### Data Flow Architecture

```
Frontend (React) → API Gateway → Service Layer → Data Layer
                    ↓
              Phase 1-5 Pipeline → LLM (Groq) → Results
                    ↓
              Caching Layer → Database → Storage
```

### Deployment Architecture

#### Backend Deployment
- **Container**: Docker with multi-stage builds
- **Orchestration**: Kubernetes or Docker Compose
- **Load Balancer**: Nginx or cloud load balancer
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK stack (Elasticsearch, Logstash, Kibana)

#### Frontend Deployment
- **Static Hosting**: Vercel, Netlify, or S3 + CloudFront
- **CDN**: Global content delivery
- **CI/CD**: GitHub Actions with automated testing
- **Environment Management**: Development, staging, production

---

## Updated Project Structure

```
zomato-restaurant-recommendation/
├── backend/
│   ├── src/
│   │   ├── zomato_rec/
│   │   │   ├── phase[1-5]/     # Phase implementations
│   │   │   ├── web_ui/         # FastAPI application
│   │   │   ├── config.py       # Configuration
│   │   │   └── models.py       # Data models
│   │   └── tests/              # Backend tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/                # Database migrations
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # API services
│   │   └── utils/              # Utilities
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── phase5/                     # Standalone presentation layer
├── storage/                    # Data storage
├── docs/                       # Documentation
├── tests/                      # Integration tests
├── docker-compose.yml
├── .github/workflows/          # CI/CD pipelines
└── README.md
```

---

## End-to-End Flow (Updated)

### CLI Flow:
User Preferences → Phase 1-5 Pipeline → Enhanced Console/JSON Output

### Web Flow:
User Interface → API Gateway → Phase 1-5 Pipeline → Database → Frontend Display

### Complete Architecture:
```
User (Web/CLI) → Validation → Data Processing → LLM Integration → 
Structured Output → Presentation Layer → Storage/Cache → Monitoring
```

---

## End-to-End Flow (High-level)

User Preferences → Validation → Candidate Retrieval (Dataset) → Prompt Builder → LLM → Parse/Validate → Display Results → Logs/Metrics

