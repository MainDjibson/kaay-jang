import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Users, BookOpen, FileText, CheckCircle, XCircle } from 'lucide-react';
import api from '../utils/api';
import { toast } from 'sonner';
import { AdBanner } from '../components/AdBanner';
import i18n from '../i18n';

export const AdminDashboard = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [pendingTeachers, setPendingTeachers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, teachersRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get('/admin/pending-teachers')
      ]);
      setStats(statsRes.data);
      setPendingTeachers(teachersRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleValidateTeacher = async (teacherId) => {
    try {
      await api.put(`/admin/validate-teacher/${teacherId}`);
      toast.success(i18n.language === 'fr' ? 'Professeur validé' : 'Teacher validated');
      fetchData();
    } catch (error) {
      toast.error(i18n.language === 'fr' ? 'Erreur' : 'Error');
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">{t('loading')}</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 py-8 px-4">
      <div className="max-w-7xl mx-auto" data-testid="admin-dashboard">
        <AdBanner />
        
        <h1 className="text-4xl font-bold mb-8 text-gray-800" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          {i18n.language === 'fr' ? 'Tableau de bord Admin' : 'Admin Dashboard'}
        </h1>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="p-6 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200" data-testid="stat-users">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 font-medium">{i18n.language === 'fr' ? 'Utilisateurs' : 'Users'}</p>
                <p className="text-3xl font-bold text-blue-900">{stats?.total_users || 0}</p>
              </div>
              <Users className="w-12 h-12 text-blue-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-green-50 to-green-100 border-green-200" data-testid="stat-teachers">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 font-medium">{t('teacher')}s</p>
                <p className="text-3xl font-bold text-green-900">{stats?.total_teachers || 0}</p>
              </div>
              <Users className="w-12 h-12 text-green-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200" data-testid="stat-students">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600 font-medium">{t('student')}s</p>
                <p className="text-3xl font-bold text-purple-900">{stats?.total_students || 0}</p>
              </div>
              <Users className="w-12 h-12 text-purple-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200" data-testid="stat-topics">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600 font-medium">{t('topics')}</p>
                <p className="text-3xl font-bold text-orange-900">{stats?.total_topics || 0}</p>
              </div>
              <BookOpen className="w-12 h-12 text-orange-600" />
            </div>
          </Card>
        </div>

        {/* Pending Teachers */}
        <Card className="p-6" data-testid="pending-teachers-section">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">
            {i18n.language === 'fr' ? 'Professeurs en attente de validation' : 'Pending Teacher Validations'}
          </h2>
          {pendingTeachers.length === 0 ? (
            <p className="text-gray-600">{i18n.language === 'fr' ? 'Aucun professeur en attente' : 'No pending teachers'}</p>
          ) : (
            <div className="space-y-4">
              {pendingTeachers.map((teacher) => (
                <div key={teacher.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg" data-testid={`teacher-${teacher.id}`}>
                  <div>
                    <p className="font-semibold text-gray-800">{teacher.name}</p>
                    <p className="text-sm text-gray-600">{teacher.email}</p>
                  </div>
                  <Button
                    onClick={() => handleValidateTeacher(teacher.id)}
                    className="bg-emerald-600 hover:bg-emerald-700"
                    data-testid={`validate-btn-${teacher.id}`}
                  >
                    <CheckCircle className="w-4 h-4 mr-2" />
                    {i18n.language === 'fr' ? 'Valider' : 'Validate'}
                  </Button>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};