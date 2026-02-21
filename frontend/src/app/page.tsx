'use client';

import { useCurrentUserQuery } from '@/hooks/use-auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PageHeader } from '@/components/common/page-header';

export default function DashboardHomePage() {
  const meQuery = useCurrentUserQuery();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Frontend Milestone B: login + protected routes"
      />

      <Card>
        <CardHeader>
          <CardTitle>Current User</CardTitle>
        </CardHeader>
        <CardContent>
          {meQuery.isPending && <p>Loading current user...</p>}
          {meQuery.isError && (
            <p className="text-sm text-red-600">
              Could not load current user. Please sign in again.
            </p>
          )}
          {meQuery.isSuccess && (
            <div className="space-y-1 text-sm">
              <p>Email: {meQuery.data.email}</p>
              <p>Full name: {meQuery.data.full_name ?? '-'}</p>
              <p>Superuser: {String(meQuery.data.is_superuser)}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
