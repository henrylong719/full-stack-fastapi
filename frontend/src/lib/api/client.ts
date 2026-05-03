import { config } from '@/lib/config';

type ApiFetchOptions = RequestInit & {
  token?: string;
  timeoutMs?: number;
};

const API_BASE_URL = config.apiBaseUrl;
const CSRF_COOKIE_NAME = config.csrfCookieName;
const DEFAULT_TIMEOUT_MS = 10_000;
const UNSAFE_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

export class ApiError extends Error {
  status: number;
  body: unknown;

  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null;

  const cookies = document.cookie.split('; ');
  const prefix = `${encodeURIComponent(name)}=`;
  const match = cookies.find((cookie) => cookie.startsWith(prefix));
  if (!match) return null;

  return decodeURIComponent(match.slice(prefix.length));
}

async function parseResponse(response: Response) {
  const contentType = response.headers.get('content-type') ?? '';
  if (contentType.includes('application/json')) {
    return response.json();
  }
  return response.text();
}

export async function apiFetch<T>(
  path: string,
  init?: ApiFetchOptions,
): Promise<T> {
  const {
    token,
    headers,
    timeoutMs = DEFAULT_TIMEOUT_MS,
    signal,
    ...rest
  } = init ?? {};

  const url = `${API_BASE_URL}${path}`;
  const method = (rest.method ?? 'GET').toUpperCase();
  const requestHeaders = new Headers(headers);
  const timeoutController = new AbortController();
  const timeoutId = setTimeout(() => timeoutController.abort(), timeoutMs);

  if (
    rest.body &&
    !(rest.body instanceof FormData) &&
    !(rest.body instanceof URLSearchParams) &&
    !requestHeaders.has('Content-Type')
  ) {
    requestHeaders.set('Content-Type', 'application/json');
  }

  const csrfToken = UNSAFE_METHODS.has(method)
    ? getCookie(CSRF_COOKIE_NAME)
    : null;
  if (csrfToken && !requestHeaders.has('X-CSRF-Token')) {
    requestHeaders.set('X-CSRF-Token', csrfToken);
  }

  if (token) {
    requestHeaders.set('Authorization', `Bearer ${token}`);
  }

  let response: Response;
  try {
    response = await fetch(url, {
      ...rest,
      credentials: rest.credentials ?? 'include',
      headers: requestHeaders,
      signal: signal ?? timeoutController.signal,
      cache: 'no-store',
    });
  } catch (error) {
    if (timeoutController.signal.aborted) {
      throw new ApiError('Request timed out', 408, null);
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }

  const body = await parseResponse(response);

  if (!response.ok) {
    throw new ApiError(
      `Request failed: ${response.status} ${response.statusText}`,
      response.status,
      body,
    );
  }

  return body as T;
}
