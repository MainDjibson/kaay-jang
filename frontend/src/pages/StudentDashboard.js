import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { FileText, Users, TrendingUp, BookOpen } from 'lucide-react';
import api from '../utils/api';
import { AdBanner } from '../components/AdBanner';
import i18n from '../i18n';

export const StudentDashboard = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, assignmentsRes] = await Promise.all([
        api.get('/student/stats'),
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 py-8 px-4">
      <div className="max-w-7xl mx-auto" data-testid="student-dashboard">
        <AdBanner />
        
        <h1 className="text-4xl font-bold mb-8 text-gray-800" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          {i18n.language === 'fr' ? 'Tableau de bord Élève' : 'Student Dashboard'}
        </h1>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200" data-testid="stat-total-assignments">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 font-medium">{i18n.language === 'fr' ? 'Devoirs totaux' : 'Total Assignments'}</p>
                <p className="text-3xl font-bold text-blue-900">{stats?.total_assignments || 0}</p>
              </div>
              <FileText className="w-12 h-12 text-blue-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-green-50 to-green-100 border-green-200" data-testid="stat-completed">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 font-medium">{i18n.language === 'fr' ? 'Complétés' : 'Completed'}</p>
                <p className="text-3xl font-bold text-green-900">{stats?.completed_assignments || 0}</p>
              </div>
              <FileText className="w-12 h-12 text-green-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200" data-testid="stat-average">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600 font-medium">{i18n.language === 'fr' ? 'Moyenne' : 'Average'}</p>
                <p className="text-3xl font-bold text-purple-900">{stats?.average_score || 0}%</p>
              </div>
              <TrendingUp className="w-12 h-12 text-purple-600" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200" data-testid="stat-following">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600 font-medium">{t('following')}</p>
                <p className="text-3xl font-bold text-orange-900">{stats?.following || 0}</p>
              </div>
              <Users className="w-12 h-12 text-orange-600" />
            </div>
          </Card>
        </div>

        {/* Available Assignments */}
        <Card className="p-6">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">
            {i18n.language === 'fr' ? 'Devoirs disponibles' : 'Available Assignments'}
          </h2>
          {assignments.length === 0 ? (
            <p className="text-gray-600">{i18n.language === 'fr' ? 'Aucun devoir disponible' : 'No assignments available'}</p>
          ) : (
            <div className="space-y-4">
              {assignments.map((assignment) => (
                <Link key={assignment.id} to={`/assignments/${assignment.id}`}>
                  <div className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors" data-testid={`assignment-${assignment.id}`}>
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-semibold text-gray-800">{assignment.title}</h3>
                        <p className="text-sm text-gray-600">{assignment.description.substring(0, 100)}...</p>
                        <p className="text-xs text-gray-500 mt-2">
                          {i18n.language === 'fr' ? 'Date limite: ' : 'Due: '}
                          {new Date(assignment.due_date).toLocaleDateString()}
                        </p>
                      </div>
                      <Button size="sm" className="bg-emerald-600 hover:bg-emerald-700">
                        {i18n.language === 'fr' ? 'Commencer' : 'Start'}
                      </Button>
                    </div>
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