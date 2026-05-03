import type { Metadata } from 'next';
import { Toaster } from '@/components/ui/sonner';

import './globals.css';
import Providers from './providers';

export const metadata: Metadata = {
  title: 'Full Stack FastAPI (Next.js Frontend)',
  description: 'Next.js frontend for a FastAPI backend',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen font-sans antialiased">
        <Providers>{children}</Providers>
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
