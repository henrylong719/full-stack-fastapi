function requireEnv(name: string, value: string | undefined): string {
  if (!value || value.trim() === '') {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export const config = {
  apiBaseUrl: requireEnv(
    'NEXT_PUBLIC_API_BASE_URL',
    process.env.NEXT_PUBLIC_API_BASE_URL,
  ),
  csrfCookieName: process.env.NEXT_PUBLIC_CSRF_COOKIE_NAME?.trim() || 'csrf_token',
  appName: process.env.NEXT_PUBLIC_APP_NAME?.trim() || 'App',
};
