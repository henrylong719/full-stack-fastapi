'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect } from 'react';

import { Button } from '@/components/ui/button';
import {
  isAuthError,
  useCurrentUserQuery,
  useLogoutMutation,
} from '@/hooks/use-auth';
import { ThemeToggle } from '@/components/common/theme-toggle';
import { useHasMounted } from '@/hooks/use-has-mounted';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const hasMounted = useHasMounted();

  const meQuery = useCurrentUserQuery({ enabled: hasMounted });
  const logoutMutation = useLogoutMutation();

  useEffect(() => {
    if (hasMounted && meQuery.isError && isAuthError(meQuery.error)) {
      router.replace('/login');
    }
  }, [hasMounted, meQuery.error, meQuery.isError, router]);

  const handleLogout = async () => {
    try {
      await logoutMutation.mutateAsync();
    } finally {
      router.replace('/login');
    }
  };

  if (!hasMounted) {
    return (
      <div className="flex min-h-screen items-center justify-center p-6">
        <p className="text-sm text-muted-foreground">Loading app...</p>
      </div>
    );
  }

  if (meQuery.isPending) {
    return (
      <div className="flex min-h-screen items-center justify-center p-6">
        <p className="text-sm text-muted-foreground">Loading user...</p>
      </div>
    );
  }

  if (meQuery.isError) {
    return (
      <div className="flex min-h-screen items-center justify-center p-6">
        <p className="text-sm text-muted-foreground">
          {isAuthError(meQuery.error)
            ? 'Redirecting to login...'
            : 'Unable to load your session.'}
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <header className="border-b">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <div className="space-y-1">
            <p className="text-lg font-semibold">Dashboard</p>
            <p className="text-sm text-muted-foreground">
              {meQuery.data.email}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href="/"
              className={
                pathname === '/' ? 'font-medium' : 'text-muted-foreground'
              }
            >
              Home
            </Link>
            <Link
              href="/items"
              className={
                pathname === '/items'
                  ? 'rounded px-2 py-1 text-sm font-medium bg-muted'
                  : 'rounded px-2 py-1 text-sm text-muted-foreground hover:text-foreground'
              }
            >
              Items
            </Link>
            <Link
              href="/users"
              className={
                pathname === '/users'
                  ? 'rounded px-2 py-1 text-sm font-medium bg-muted'
                  : 'rounded px-2 py-1 text-sm text-muted-foreground hover:text-foreground'
              }
            >
              Users
            </Link>
            <Link
              href="/settings"
              className={
                pathname === '/settings'
                  ? 'rounded bg-muted px-2 py-1 text-sm font-medium'
                  : 'rounded px-2 py-1 text-sm text-muted-foreground hover:text-foreground'
              }
            >
              Settings
            </Link>

            <ThemeToggle />
            <Button
              variant="outline"
              onClick={() => void handleLogout()}
              disabled={logoutMutation.isPending}
            >
              {logoutMutation.isPending ? 'Logging out...' : 'Logout'}
            </Button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-5xl p-6">{children}</main>
    </div>
  );
}
