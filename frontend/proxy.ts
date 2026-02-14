// Proxy configuration for Vercel deployment
// Since we're using client-side authentication with localStorage,
// actual auth checks happen in the components themselves
// This proxy handles route protection patterns

import { NextRequest, NextResponse } from 'next/server';

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Public routes that don't require authentication
  const publicRoutes = ['/', '/auth/login', '/auth/signup'];

  // For this application, we're allowing all routes to pass through
  // since authentication is handled client-side in the components
  // This proxy is primarily for route matching patterns
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};