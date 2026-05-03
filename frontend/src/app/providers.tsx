'use client';

import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState, type ReactNode } from 'react';

import { makeQueryClient } from '@/lib/query-client';
import { ThemeProvider } from '@/components/common/theme-provider';

type Props = {
  children: ReactNode;
};

export default function Providers({ children }: Props) {
  const [queryClient] = useState(() => makeQueryClient());
  const showDevtools = process.env.NODE_ENV === 'development';

  return (
    <ThemeProvider>
      <QueryClientProvider client={queryClient}>
        {children}
        {showDevtools ? <ReactQueryDevtools initialIsOpen={false} /> : null}
      </QueryClientProvider>
    </ThemeProvider>
  );
}
