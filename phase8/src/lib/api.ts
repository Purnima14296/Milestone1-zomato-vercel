// API client for Zomato Restaurant Recommendation System

import axios, { AxiosResponse } from 'axios';
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

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: any) => {
    const errorResponse: ErrorResponse = {
      error: error.response?.data?.error || 'UnknownError',
      message: error.response?.data?.message || error.message || 'An error occurred',
      details: error.response?.data?.details,
      timestamp: new Date().toISOString(),
      request_id: error.response?.data?.request_id,
    };
    
    return Promise.reject(errorResponse);
  }
);

// Health API
export const healthApi = {
  getHealth: (): Promise<AxiosResponse<HealthStatus>> => 
    apiClient.get('/health'),
  
  getComponentHealth: (): Promise<AxiosResponse<HealthStatus['components']>> => 
    apiClient.get('/health/components'),
  
  ping: (): Promise<AxiosResponse<{ status: string; timestamp: string; message: string }>> => 
    apiClient.get('/health/ping'),
};

// Recommendation API
export const recommendationApi = {
  generateRecommendations: (request: RecommendationRequest): Promise<AxiosResponse<RecommendationResponse>> => 
    apiClient.post('/recommendations', request),
  
  getRecommendation: (id: string): Promise<AxiosResponse<RecommendationResponse>> => 
    apiClient.get(`/recommendations/${id}`),
  
  getHistory: (): Promise<AxiosResponse<RecommendationResponse[]>> => 
    apiClient.get('/recommendations/history'),
};

// Restaurant API
export const restaurantApi = {
  search: (params: RestaurantSearchRequest): Promise<AxiosResponse<RestaurantSearchResponse>> => 
    apiClient.get('/restaurants/search', { params }),
};

// Preference API
export const preferenceApi = {
  validate: (preferences: UserPreferences): Promise<AxiosResponse<PreferenceValidationResponse>> => 
    apiClient.post('/preferences/validate', { preferences }),
};

// Metadata API
export const metadataApi = {
  getMetadata: (): Promise<AxiosResponse<MetadataResponse>> => 
    apiClient.get('/metadata'),
  
  getMetrics: (hours: number = 24): Promise<AxiosResponse<MetricsResponse>> => 
    apiClient.get('/metrics', { params: { hours } }),
  
  getStats: (): Promise<AxiosResponse<any>> => 
    apiClient.get('/stats'),
  
  getConfig: (): Promise<AxiosResponse<any>> => 
    apiClient.get('/config'),
};

// Utility functions
export const createQueryString = (params: Record<string, any>): string => {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, String(value));
    }
  });
  return searchParams.toString();
};

export const handleApiError = (error: any): ErrorResponse => {
  if (error.response) {
    return error.response.data as ErrorResponse;
  }
  return {
    error: 'NetworkError',
    message: 'Network error occurred',
    timestamp: new Date().toISOString(),
  };
};

export default apiClient;
