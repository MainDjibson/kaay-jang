import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { LogIn } from 'lucide-react';
import i18n from '../i18n';

export const Login = () => {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await login(formData.email, formData.password);
      toast.success(t('login') + ' ' + (i18n.language === 'fr' ? 'réussi!' : 'successful!'));
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || (i18n.language === 'fr' ? 'Erreur de connexion' : 'Login failed'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 shadow-2xl border-2 border-emerald-100">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <LogIn className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            {t('login')}
          </h1>
          <p className="text-gray-600 mt-2">
            {i18n.language === 'fr' ? 'Bienvenue sur KAAY-JANG' : 'Welcome to KAAY-JANG'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6" data-testid="login-form">
          <div className="space-y-2">
            <Label htmlFor="email">{t('email')}</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              className="border-2 border-gray-200 focus:border-emerald-500"
              data-testid="email-input"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">{t('password')}</Label>
            <Input
              id="password"
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              className="border-2 border-gray-200 focus:border-emerald-500"
              data-testid="password-input"
            />
          </div>

          <Button 
            type="submit" 
            className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 py-6 text-lg rounded-full"
            disabled={loading}
            data-testid="login-submit-btn"
          >
            {loading ? t('loading') : t('login')}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            {i18n.language === 'fr' ? 'Pas encore de compte?' : "Don't have an account?"}{' '}
            <Link to="/register" className="text-emerald-600 hover:text-emerald-700 font-semibold" data-testid="register-link">
              {t('register')}
            </Link>
          </p>
        </div>
      </Card>
    </div>
  );
};