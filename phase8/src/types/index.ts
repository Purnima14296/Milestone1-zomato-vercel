// API Types for Zomato Restaurant Recommendation System

export interface BudgetRange {
  min: number;
  max: number;
}

export interface UserPreferences {
  location: string;
  budget: BudgetRange;
  minimum_rating: number;
  cuisines: string[];
  additional_preferences?: string;
}

export interface RestaurantInfo {
  name: string;
  city: string;
  cuisines: string[];
  rating: number;
  cost_estimate: number;
  reason: string;
}

export interface RecommendationRequest {
  preferences: UserPreferences;
  top_k?: number; // default 5, max 20
  include_explanations?: boolean; // default true
}

export interface RecommendationResponse {
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

export interface RecommendationHistory {
  request_id: string;
  preferences: UserPreferences;
  recommendations_count: number;
  created_at: string;
}

export interface RestaurantSearchRequest {
  location?: string;
  cuisine?: string;
  min_rating?: number;
  max_cost?: number;
  limit?: number; // default 20, max 100
  offset?: number; // default 0
}

export interface RestaurantSearchResponse {
  restaurants: RestaurantInfo[];
  total: number;
  limit: number;
  offset: number;
}

export interface ValidationError {
  field: string;
  message: string;
  severity: string;
}

export interface PreferenceValidationResponse {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationError[];
  suggestions: string[];
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy' | 'critical';
  timestamp: string;
  version: string;
  components: ComponentHealth[];
  uptime: number;
}

export interface ComponentHealth {
  name: string;
  status: 'healthy' | 'degraded' | 'unhealthy' | 'critical';
  response_time: number;
  message?: string;
  details: Record<string, any>;
}

export interface SystemMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  active_requests: number;
  total_requests: number;
  avg_response_time: number;
  error_rate: number;
}

export interface QualityMetrics {
  constraint_satisfaction: number;
  diversity_score: number;
  avg_quality_score: number;
  total_recommendations: number;
}

export interface MetricsResponse {
  timestamp: string;
  system: SystemMetrics;
  quality: QualityMetrics;
  period_hours: number;
}

export interface SystemMetadata {
  version: string;
  description: string;
  total_restaurants: number;
  total_recommendations: number;
  supported_cuisines: string[];
  supported_locations: string[];
  features: string[];
}

export interface MetadataResponse {
  system: SystemMetadata;
  timestamp: string;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, any>;
  timestamp: string;
  request_id?: string;
}

export interface SuccessResponse {
  message: string;
  data?: Record<string, any>;
  timestamp: string;
}

// UI Component Types
export interface RecommendationFormProps {
  onSubmit: (preferences: UserPreferences) => void;
  loading?: boolean;
  initialValues?: Partial<UserPreferences>;
}

export interface RestaurantCardProps {
  restaurant: RestaurantInfo;
  showReason?: boolean;
  onSaveFavorite?: (restaurant: RestaurantInfo) => void;
  onViewDetails?: (restaurant: RestaurantInfo) => void;
  isFavorite?: boolean;
}

export interface SearchFiltersProps {
  filters: RestaurantSearchRequest;
  onFiltersChange: (filters: RestaurantSearchRequest) => void;
}

export interface HealthStatusProps {
  refreshInterval?: number;
}

// Store Types
export interface AppState {
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

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: string;
  autoClose?: boolean;
}

// Utility Types
export type SearchFilters = RestaurantSearchRequest;
export type ApiResponse<T> = T & ErrorResponse;
export type PaginatedResponse<T> = {
  data: T[];
  total: number;
  limit: number;
  offset: number;
};
