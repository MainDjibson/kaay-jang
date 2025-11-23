import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';
import { UserPlus } from 'lucide-react';
import api from '../utils/api';
import i18n from '../i18n';

export const Register = () => {
  const { t } = useTranslation();
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [branches, setBranches] = useState([]);
  const [levels, setLevels] = useState([]);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    role: 'student',
    branch_id: '',
    level_id: '',
    filiere: ''
  });

  useEffect(() => {
    fetchBranches();
  }, []);

  useEffect(() => {
    if (formData.branch_id) {
      fetchLevels(formData.branch_id);
    }
  }, [formData.branch_id]);

  const fetchBranches = async () => {
    try {
      const response = await api.get('/branches');
      setBranches(response.data);
    } catch (error) {
      console.error('Failed to fetch branches:', error);
    }
  };

  const fetchLevels = async (branchId) => {
    try {
      const response = await api.get(`/levels?branch_id=${branchId}`);
      setLevels(response.data);
    } catch (error) {
      console.error('Failed to fetch levels:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await registerUser(formData);
      toast.success(i18n.language === 'fr' ? 'Inscription réussie!' : 'Registration successful!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || (i18n.language === 'fr' ? "Erreur d'inscription" : 'Registration failed'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-2xl p-8 shadow-2xl border-2 border-emerald-100">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <UserPlus className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            {t('register')}
          </h1>
          <p className="text-gray-600 mt-2">
            {i18n.language === 'fr' ? 'Créez votre compte KAAY-JANG' : 'Create your KAAY-JANG account'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6" data-testid="register-form">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="name">{t('name')}</Label>
              <Input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                className="border-2 border-gray-200 focus:border-emerald-500"
                data-testid="name-input"
              />
            </div>

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

            <div className="space-y-2">
              <Label htmlFor="role">{t('role')}</Label>
              <Select value={formData.role} onValueChange={(value) => setFormData({ ...formData, role: value })}>
                <SelectTrigger className="border-2 border-gray-200" data-testid="role-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="student" data-testid="role-student">{t('student')}</SelectItem>
                  <SelectItem value="teacher" data-testid="role-teacher">{t('teacher')}</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="branch">{t('branch')}</Label>
              <Select value={formData.branch_id} onValueChange={(value) => setFormData({ ...formData, branch_id: value, level_id: '' })}>
                <SelectTrigger className="border-2 border-gray-200" data-testid="branch-select">
                  <SelectValue placeholder={i18n.language === 'fr' ? 'Sélectionnez' : 'Select'} />
                </SelectTrigger>
                <SelectContent>
                  {branches.map((branch) => (
                    <SelectItem key={branch.id} value={branch.id}>
                      {i18n.language === 'fr' ? branch.name : branch.name_en}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="level">{t('level')}</Label>
              <Select value={formData.level_id} onValueChange={(value) => setFormData({ ...formData, level_id: value })} disabled={!formData.branch_id}>
                <SelectTrigger className="border-2 border-gray-200" data-testid="level-select">
                  <SelectValue placeholder={i18n.language === 'fr' ? 'Sélectionnez' : 'Select'} />
                </SelectTrigger>
                <SelectContent>
                  {levels.map((level) => (
                    <SelectItem key={level.id} value={level.id}>
                      {i18n.language === 'fr' ? level.name : level.name_en}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="filiere">{i18n.language === 'fr' ? 'Filière / Spécialité' : 'Field / Specialty'} ({i18n.language === 'fr' ? 'optionnel' : 'optional'})</Label>
              <Input
                id="filiere"
                type="text"
                value={formData.filiere}
                onChange={(e) => setFormData({ ...formData, filiere: e.target.value })}
                placeholder={i18n.language === 'fr' ? 'Ex: S, L, G, etc.' : 'Ex: S, L, G, etc.'}
                className="border-2 border-gray-200 focus:border-emerald-500"
                data-testid="filiere-input"
              />
            </div>
          </div>

          <Button 
            type="submit" 
            className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 py-6 text-lg rounded-full"
            disabled={loading}
            data-testid="register-submit-btn"
          >
            {loading ? t('loading') : t('register')}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            {i18n.language === 'fr' ? 'Déjà un compte?' : 'Already have an account?'}{' '}
            <Link to="/login" className="text-emerald-600 hover:text-emerald-700 font-semibold" data-testid="login-link">
              {t('login')}
            </Link>
          </p>
        </div>
      </Card>
    </div>
  );
};