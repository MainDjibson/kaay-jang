import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { FileText, Users, BookOpen, Plus } from 'lucide-react';
import api from '../utils/api';
import { AdBanner } from '../components/AdBanner';
import i18n from '../i18n';

export const TeacherDashboard = () => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, assignmentsRes] = await Promise.all([
        api.get('/teacher/stats'),
        api.get('/assignments')
      ]);
      setStats(statsRes.data);
      setAssignments(assignmentsRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">{t('loading')}</div>;
  }

  if (!user.is_validated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="p-12 text-center">
            <h1 className="text-3xl font-bold mb-4 text-gray-800">
              {i18n.language === 'fr' ? 'Compte en attente de validation' : 'Account Pending Validation'}
            </h1>
            <p className="text-gray-600">
              {i18n.language === 'fr' 
                ? 'Votre compte professeur est en attente de validation par un administrateur. Vous recevrez une notification une fois validé.'
                : 'Your teacher account is pending validation by an administrator. You will receive a notification once validated.'}
            </p>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 py-8 px-4">
      <div className="max-w-7xl mx-auto" data-testid="teacher-dashboard">
        <AdBanner />
        
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            {i18n.language === 'fr' ? 'Tableau de bord Professeur' : 'Teacher Dashboard'}
          </h1>
          <Link to="/assignments/create">
            <Button className="bg-emerald-600 hover:bg-emerald-700" data-testid="create-assignment-btn">
              <Plus className="w-4 h-4 mr-2" />
              {t('createAssignment')}
            </Button>
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="p-6 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200" data-testid="stat-assignments">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 font-medium">{t('assignments')}</p>
                <p className="text-3xl font-bold text-blue-900">{stats?.total_assignments || 0}</p>
              </div>
              <FileText className="w-12 h-12 text-blue-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-green-50 to-green-100 border-green-200" data-testid="stat-followers">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 font-medium">{t('followers')}</p>
                <p className="text-3xl font-bold text-green-900">{stats?.followers || 0}</p>
              </div>
              <Users className="w-12 h-12 text-green-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200" data-testid="stat-topics">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600 font-medium">{t('topics')}</p>
                <p className="text-3xl font-bold text-purple-900">{stats?.total_topics || 0}</p>
              </div>
              <BookOpen className="w-12 h-12 text-purple-600" />
            </div>
          </Card>
        </div>

        {/* Recent Assignments */}
        <Card className="p-6">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">
            {i18n.language === 'fr' ? 'Devoirs récents' : 'Recent Assignments'}
          </h2>
          {assignments.length === 0 ? (
            <p className="text-gray-600">{i18n.language === 'fr' ? 'Aucun devoir' : 'No assignments'}</p>
          ) : (
            <div className="space-y-4">
              {assignments.slice(0, 5).map((assignment) => (
                <Link key={assignment.id} to={`/assignments/${assignment.id}`}>
                  <div className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors" data-testid={`assignment-${assignment.id}`}>
                    <h3 className="font-semibold text-gray-800">{assignment.title}</h3>
                    <p className="text-sm text-gray-600">{assignment.description.substring(0, 100)}...</p>
                    <p className="text-xs text-gray-500 mt-2">
                      {i18n.language === 'fr' ? 'Date limite: ' : 'Due: '}
                      {new Date(assignment.due_date).toLocaleDateString()}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};