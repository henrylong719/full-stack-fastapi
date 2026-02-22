'use client';

import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import {
  CheckCircle2,
  XCircle,
  Loader2,
  Package,
  Users,
  Settings,
  ShieldCheck,
  ArrowRight,
} from 'lucide-react';

import { useCurrentUserQuery } from '@/hooks/use-auth';
import { getAccessToken } from '@/lib/api/auth';
import { getItems } from '@/lib/api/items';
import { getUsers } from '@/lib/api/users';
import { getHealthCheck } from '@/lib/api/health';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PageHeader } from '@/components/common/page-header';

function useStats() {
  const token = getAccessToken() ?? '';

  const itemsQuery = useQuery({
    queryKey: ['items', 0, 1],
    queryFn: () => getItems(token, { skip: 0, limit: 1 }),
    enabled: !!token,
    retry: false,
  });

  const usersQuery = useQuery({
    queryKey: ['users', 0, 1],
    queryFn: () => getUsers(token, { skip: 0, limit: 1 }),
    enabled: !!token,
    retry: false,
  });

  const healthQuery = useQuery({
    queryKey: ['health-check'],
    queryFn: getHealthCheck,
  });

  return { itemsQuery, usersQuery, healthQuery };
}

function StatCard({
  label,
  value,
  isLoading,
  isError,
  icon: Icon,
}: {
  label: string;
  value: number | undefined;
  isLoading: boolean;
  isError: boolean;
  icon: React.ElementType;
}) {
  return (
    <Card>
      <CardContent className="flex items-center gap-4 pt-6">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-muted">
          <Icon className="h-5 w-5 text-muted-foreground" />
        </div>
        <div>
          <p className="text-sm text-muted-foreground">{label}</p>
          {isLoading ? (
            <Loader2 className="mt-1 h-4 w-4 animate-spin text-muted-foreground" />
          ) : isError ? (
            <p className="text-sm text-muted-foreground">—</p>
          ) : (
            <p className="text-2xl font-semibold tabular-nums">{value ?? 0}</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

const NAV_LINKS = [
  {
    href: '/items',
    icon: Package,
    label: 'Items',
    description: 'Create, view, and manage your items.',
  },
  {
    href: '/users',
    icon: Users,
    label: 'Users',
    description: 'Admin panel for managing user accounts.',
  },
  {
    href: '/settings',
    icon: Settings,
    label: 'Settings',
    description: 'Edit your profile and change your password.',
  },
];

export default function DashboardHomePage() {
  const meQuery = useCurrentUserQuery();
  const { itemsQuery, usersQuery, healthQuery } = useStats();

  const user = meQuery.data;
  const backendOk = healthQuery.isSuccess;

  return (
    <div className="page-container space-y-8">
      {/* Header */}
      <PageHeader
        title={
          meQuery.isSuccess
            ? `Welcome back${user?.full_name ? `, ${user.full_name}` : ''}!`
            : 'Dashboard'
        }
        description={
          meQuery.isSuccess ? user?.email ?? '' : 'Loading your profile…'
        }
      />

      {/* Stats */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <StatCard
          label="Total items"
          value={itemsQuery.data?.count}
          isLoading={itemsQuery.isPending}
          isError={itemsQuery.isError}
          icon={Package}
        />
        <StatCard
          label="Total users"
          value={usersQuery.data?.count}
          isLoading={usersQuery.isPending}
          isError={usersQuery.isError}
          icon={Users}
        />
        <Card>
          <CardContent className="flex items-center gap-4 pt-6">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-muted">
              {healthQuery.isPending ? (
                <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
              ) : backendOk ? (
                <CheckCircle2 className="h-5 w-5 text-green-500" />
              ) : (
                <XCircle className="h-5 w-5 text-red-500" />
              )}
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Backend</p>
              {healthQuery.isPending ? (
                <p className="text-sm text-muted-foreground">Checking…</p>
              ) : (
                <p
                  className={`text-2xl font-semibold ${backendOk ? 'text-green-600' : 'text-red-600'}`}
                >
                  {backendOk ? 'Online' : 'Offline'}
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Profile + Role */}
      {meQuery.isSuccess && user && (
        <Card>
          <CardHeader>
            <CardTitle>Your account</CardTitle>
            <CardDescription>Account details and role.</CardDescription>
          </CardHeader>
          <CardContent>
            <dl className="grid grid-cols-1 gap-4 text-sm sm:grid-cols-3">
              <div className="space-y-1">
                <dt className="text-muted-foreground">Email</dt>
                <dd className="font-medium">{user.email}</dd>
              </div>
              <div className="space-y-1">
                <dt className="text-muted-foreground">Full name</dt>
                <dd className="font-medium">{user.full_name || '—'}</dd>
              </div>
              <div className="space-y-1">
                <dt className="text-muted-foreground">Role</dt>
                <dd className="flex items-center gap-1.5 font-medium">
                  {user.is_superuser ? (
                    <>
                      <ShieldCheck className="h-4 w-4 text-amber-500" />
                      Superuser
                    </>
                  ) : (
                    'Regular user'
                  )}
                </dd>
              </div>
            </dl>
          </CardContent>
        </Card>
      )}

      {/* Quick links */}
      <div>
        <h2 className="mb-3 text-sm font-medium text-muted-foreground uppercase tracking-wide">
          Quick links
        </h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {NAV_LINKS.map(({ href, icon: Icon, label, description }) => (
            <Card
              key={href}
              className="transition-colors hover:border-foreground/30"
            >
              <CardContent className="flex items-start justify-between pt-6">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Icon className="h-4 w-4 text-muted-foreground" />
                    <p className="font-medium">{label}</p>
                  </div>
                  <p className="text-sm text-muted-foreground">{description}</p>
                </div>
                <Button variant="ghost" size="icon" asChild className="shrink-0">
                  <Link href={href}>
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
