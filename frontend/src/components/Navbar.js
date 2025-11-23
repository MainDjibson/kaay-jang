import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Bell, Globe, User, LogOut, Menu, X } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import api from '../utils/api';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const { t, i18n } = useTranslation();
  const location = useLocation();
  const [unreadCount, setUnreadCount] = useState(0);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    if (user) {
      fetchUnreadCount();
      const interval = setInterval(fetchUnreadCount, 30000);
      return () => clearInterval(interval);
    }
  }, [user]);

  const fetchUnreadCount = async () => {
    try {
      const response = await api.get('/notifications/unread-count');
      setUnreadCount(response.data.count);
    } catch (error) {
      console.error('Failed to fetch unread count:', error);
    }
  };

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    localStorage.setItem('language', lng);
  };

  const isActive = (path) => location.pathname === path;

  const NavLinks = () => (
    <>
      <Link to="/" onClick={() => setMobileOpen(false)}>
        <Button 
          variant={isActive('/') ? 'default' : 'ghost'} 
          className="font-medium"
          data-testid="nav-home"
        >
          {t('home')}
        </Button>
      </Link>
      {user && (
        <>
          <Link to="/forum" onClick={() => setMobileOpen(false)}>
            <Button 
              variant={isActive('/forum') ? 'default' : 'ghost'} 
              className="font-medium"
              data-testid="nav-forum"
            >
              {t('forum')}
            </Button>
          </Link>
          <Link to="/dashboard" onClick={() => setMobileOpen(false)}>
            <Button 
              variant={isActive('/dashboard') ? 'default' : 'ghost'} 
              className="font-medium"
              data-testid="nav-dashboard"
            >
              {t('dashboard')}
            </Button>
          </Link>
        </>
      )}
    </>
  );

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 backdrop-blur-lg bg-opacity-90">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">K</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              KAAY-JANG
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-2">
            <NavLinks />
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-2">
            {/* Language Selector */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" data-testid="language-selector">
                  <Globe className="w-5 h-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem onClick={() => changeLanguage('fr')} data-testid="lang-fr">
                  Français
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => changeLanguage('en')} data-testid="lang-en">
                  English
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {user ? (
              <>
                {/* Notifications */}
                <Link to="/notifications">
                  <Button variant="ghost" size="icon" className="relative" data-testid="notifications-btn">
                    <Bell className="w-5 h-5" />
                    {unreadCount > 0 && (
                      <Badge 
                        className="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center p-0 bg-red-500"
                        data-testid="unread-badge"
                      >
                        {unreadCount}
                      </Badge>
                    )}
                  </Button>
                </Link>

                {/* User Menu */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" data-testid="user-menu">
                      {user.avatar_url ? (
                        <img src={user.avatar_url} alt={user.name} className="w-8 h-8 rounded-full" />
                      ) : (
                        <User className="w-5 h-5" />
                      )}
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuItem asChild>
                      <Link to="/profile" className="w-full" data-testid="user-menu-profile">
                        <User className="w-4 h-4 mr-2" /> {t('profile')}
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={logout} data-testid="user-menu-logout">
                      <LogOut className="w-4 h-4 mr-2" /> {t('logout')}
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </>
            ) : (
              <div className="hidden md:flex items-center space-x-2">
                <Link to="/login">
                  <Button variant="ghost" data-testid="login-btn">{t('login')}</Button>
                </Link>
                <Link to="/register">
                  <Button data-testid="register-btn">{t('register')}</Button>
                </Link>
              </div>
            )}

            {/* Mobile Menu */}
            <div className="md:hidden">
              <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
                <SheetTrigger asChild>
                  <Button variant="ghost" size="icon" data-testid="mobile-menu-btn">
                    {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                  </Button>
                </SheetTrigger>
                <SheetContent side="right">
                  <div className="flex flex-col space-y-4 mt-8">
                    <NavLinks />
                    {!user && (
                      <>
                        <Link to="/login" onClick={() => setMobileOpen(false)}>
                          <Button variant="ghost" className="w-full" data-testid="mobile-login-btn">
                            {t('login')}
                          </Button>
                        </Link>
                        <Link to="/register" onClick={() => setMobileOpen(false)}>
                          <Button className="w-full" data-testid="mobile-register-btn">
                            {t('register')}
                          </Button>
                        </Link>
                      </>
                    )}
                  </div>
                </SheetContent>
              </Sheet>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};