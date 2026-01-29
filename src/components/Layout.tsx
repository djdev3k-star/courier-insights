import { Outlet, Link, useLocation } from 'react-router-dom'
import { BarChart3, Calendar, DollarSign, TrendingUp, FileText, Menu, X } from 'lucide-react'
import { useState } from 'react'

export function Layout() {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3 },
    { path: '/schedule', label: 'Schedule', icon: Calendar },
    { path: '/expenses', label: 'Expenses', icon: DollarSign },
    { path: '/performance', label: 'Performance', icon: TrendingUp },
    { path: '/reports', label: 'Reports', icon: FileText },
  ]

  return (
    <div className="min-h-screen">
      <nav className="bg-white border-b-4 border-black sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-600 border-3 border-black flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-black text-blue-600 uppercase tracking-tight">HustleReport</span>
            </Link>

            <div className="hidden md:flex space-x-2">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-4 py-2 border-3 border-black font-bold uppercase text-sm transition-all duration-200 ${
                      isActive
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-black hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>

            <button
              className="md:hidden border-3 border-black p-2 bg-white hover:bg-gray-100"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {mobileMenuOpen && (
            <div className="md:hidden py-4 space-y-2 border-t-3 border-black">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center space-x-3 px-4 py-3 border-3 border-black font-bold uppercase transition-all duration-200 ${
                      isActive
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-black hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>
          )}
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      <footer className="text-center bg-black text-white py-8 mt-12 border-t-4 border-black">
        <p className="font-black uppercase tracking-wide">HustleReport Analytics System</p>
        <p className="mt-2 text-sm font-bold">
          Built for optimization and efficiency • Last updated: January 29, 2026
        </p>
      </footer>
    </div>
  )
}
