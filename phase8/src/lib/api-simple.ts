// Simple API client for Zomato Restaurant Recommendation System
// Using fetch instead of axios to avoid dependency issues

import {
  RecommendationRequest,
  RecommendationResponse,
  RestaurantSearchRequest,
  RestaurantSearchResponse,
  PreferenceValidationResponse,
  UserPreferences,
  HealthStatus,
  MetricsResponse,
  MetadataResponse,
  ErrorResponse
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Generic API request function
async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const error: ErrorResponse = {
        error: errorData.error || 'ApiError',
        message: errorData.message || `HTTP ${response.status}: ${response.statusText}`,
        details: errorData.details,
        timestamp: new Date().toISOString(),
        request_id: errorData.request_id,
      };
      throw error;
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw {
        error: 'NetworkError',
        message: error.message,
        timestamp: new Date().toISOString(),
      };
    }
    throw error;
  }
}

// Health API
export const healthApi = {
  getHealth: (): Promise<HealthStatus> => 
    apiRequest<HealthStatus>('/health'),
  
  getComponentHealth: (): Promise<HealthStatus['components']> => 
    apiRequest<HealthStatus['components']>('/health/components'),
  
  ping: (): Promise<{ status: string; timestamp: string; message: string }> => 
    apiRequest<{ status: string; timestamp: string; message: string }>('/health/ping'),
};

// Recommendation API
export const recommendationApi = {
  generateRecommendations: (request: RecommendationRequest): Promise<RecommendationResponse> => 
    apiRequest<RecommendationResponse>('/recommendations', {
      method: 'POST',
      body: JSON.stringify(request),
    }),
  
  getRecommendation: (id: string): Promise<RecommendationResponse> => 
    apiRequest<RecommendationResponse>(`/recommendations/${id}`),
  
  getHistory: (): Promise<RecommendationResponse[]> => 
    apiRequest<RecommendationResponse[]>('/recommendations/history'),
};

// Restaurant API
export const restaurantApi = {
  search: (params: RestaurantSearchRequest): Promise<RestaurantSearchResponse> => {
    const queryString = new URLSearchParams(
      Object.entries(params).reduce((acc, [key, value]) => {
        if (value !== undefined && value !== null) {
          acc[key] = String(value);
        }
        return acc;
      }, {} as Record<string, string>)
    ).toString();
    
    return apiRequest<RestaurantSearchResponse>(`/restaurants/search?${queryString}`);
  },
};

// Preference API
export const preferenceApi = {
  validate: (preferences: UserPreferences): Promise<PreferenceValidationResponse> => 
    apiRequest<PreferenceValidationResponse>('/preferences/validate', {
      method: 'POST',
      body: JSON.stringify({ preferences }),
    }),
};

// Metadata API
export const metadataApi = {
  getMetadata: (): Promise<MetadataResponse> => 
    apiRequest<MetadataResponse>('/metadata'),
  
  getMetrics: (hours: number = 24): Promise<MetricsResponse> => 
    apiRequest<MetricsResponse>(`/metrics?hours=${hours}`),
  
  getStats: (): Promise<any> => 
    apiRequest<any>('/stats'),
  
  getConfig: (): Promise<any> => 
    apiRequest<any>('/config'),
};

export const handleApiError = (error: any): ErrorResponse => {
  if (error && typeof error === 'object' && 'error' in error) {
    return error as ErrorResponse;
  }
  return {
    error: 'NetworkError',
    message: 'Network error occurred',
    timestamp: new Date().toISOString(),
  };
};
