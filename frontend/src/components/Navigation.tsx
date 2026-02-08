'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="bg-white shadow-md border-b border-gray-200">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <div className="text-xl font-bold text-blue-600">
              ERP Dashboard
            </div>
            <div className="flex space-x-6">
              <Link
                href="/dashboard"
                className={`py-2 px-4 font-medium transition-colors ${
                  pathname === '/dashboard'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Invoice Priority
              </Link>
              <Link
                href="/inventory"
                className={`py-2 px-4 font-medium transition-colors ${
                  pathname === '/inventory'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Inventory
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
