import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;
  
  // Define which paths are "Protected"
  const isProtectedRoute = path.startsWith('/dashboard');
  
  // Check for an auth token (for the hackathon, we simulate this with a cookie)
  const token = request.cookies.get('aura_token')?.value;

  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL('/auth', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};