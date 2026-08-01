import axios from 'axios';
import { env } from '@/config/env';
import { applyAuthInterceptor } from './interceptors/auth.interceptor';
import { applyErrorInterceptor } from './interceptors/error.interceptor';
import { applyRetryInterceptor } from './interceptors/retry.interceptor';

/**
 * Enterprise Axios client.
 * All API modules use this single instance — never create ad-hoc instances.
 */
const apiClient = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 30_000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Apply interceptors in order
applyAuthInterceptor(apiClient);
applyRetryInterceptor(apiClient);
applyErrorInterceptor(apiClient);

export default apiClient;
