import { apiFetch } from './client';

export function logoutAccessToken() {
  return apiFetch<{ message: string }>('/api/v1/login/logout', {
    method: 'POST',
  });
}
