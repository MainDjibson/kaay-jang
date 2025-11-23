import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { BookOpen, Users, GraduationCap, MessageSquare, TrendingUp, Award } from 'lucide-react';
import i18n from '../i18n';

export const Home = () => {
  const { t } = useTranslation();
  const { user } = useAuth();

  const features = [
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: i18n.language === 'fr' ? 'Forum Éducatif' : 'Educational Forum',
      description: i18n.language === 'fr' 
        ? 'Discutez par branche, niveau et matière avec des professeurs et élèves' 
        : 'Discuss by branch, level and subject with teachers and students'
    },
    {
      icon: <GraduationCap className="w-8 h-8" />,
      title: i18n.language === 'fr' ? 'Devoirs en Ligne' : 'Online Assignments',
      description: i18n.language === 'fr' 
        ? 'Créez et complétez des devoirs avec correction automatique' 
        : 'Create and complete assignments with automatic grading'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: i18n.language === 'fr' ? 'Réseau Social' : 'Social Network',
      description: i18n.language === 'fr' 
        ? 'Suivez vos professeurs et élèves préférés' 
        : 'Follow your favorite teachers and students'
    },
    {
      icon: <MessageSquare className="w-8 h-8" />,
      title: i18n.language === 'fr' ? 'Publications Privées' : 'Private Posts',
      description: i18n.language === 'fr' 
        ? 'Partagez du contenu exclusif avec vos abonnés' 
        : 'Share exclusive content with your followers'
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: i18n.language === 'fr' ? 'Statistiques' : 'Statistics',
      description: i18n.language === 'fr' 
        ? 'Suivez vos progrès et performances' 
        : 'Track your progress and performance'
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: i18n.language === 'fr' ? 'Validation Professeurs' : 'Teacher Validation',
      description: i18n.language === 'fr' 
        ? 'Les professeurs validés par des administrateurs' 
        : 'Teachers validated by administrators'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 to-teal-500/5" />
        <div className="max-w-6xl mx-auto relative z-10">
          <div className="text-center space-y-8">
            <h1 
              className="text-5xl sm:text-6xl lg:text-7xl font-bold bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 bg-clip-text text-transparent"
              style={{ fontFamily: 'Space Grotesk, sans-serif' }}
              data-testid="hero-title"
            >
              {t('welcomeTitle')}
            </h1>
            <p 
              className="text-xl sm:text-2xl text-gray-600 max-w-3xl mx-auto"
              style={{ fontFamily: 'Inter, sans-serif' }}
              data-testid="hero-subtitle"
            >
              {t('welcomeSubtitle')}
            </p>
            {!user && (
              <div className="flex gap-4 justify-center flex-wrap">
                <Link to="/register">
                  <Button 
                    size="lg" 
                    className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-8 py-6 text-lg rounded-full shadow-lg hover:shadow-xl transition-all"
                    data-testid="get-started-btn"
                  >
                    {t('getStarted')}
                  </Button>
                </Link>
                <Link to="/login">
                  <Button 
                    size="lg" 
                    variant="outline" 
                    className="px-8 py-6 text-lg rounded-full border-2 border-emerald-600 text-emerald-600 hover:bg-emerald-50"
                    data-testid="login-btn-hero"
                  >
                    {t('login')}
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white/50 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto">
          <h2 
            className="text-4xl font-bold text-center mb-12 text-gray-800"
            style={{ fontFamily: 'Space Grotesk, sans-serif' }}
          >
            {i18n.language === 'fr' ? 'Fonctionnalités Principales' : 'Key Features'}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <Card 
                key={index} 
                className="p-6 hover:shadow-xl transition-all duration-300 border-2 border-transparent hover:border-emerald-200 bg-white group"
                data-testid={`feature-card-${index}`}
              >
                <div className="w-16 h-16 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-2xl flex items-center justify-center mb-4 text-emerald-600 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!user && (
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Card className="p-12 bg-gradient-to-r from-emerald-600 to-teal-600 text-white border-none shadow-2xl">
              <h2 className="text-4xl font-bold mb-4">
                {i18n.language === 'fr' ? 'Rejoignez-nous aujourd\'hui!' : 'Join us today!'}
              </h2>
              <p className="text-xl mb-8 text-emerald-50">
                {i18n.language === 'fr' 
                  ? 'Commencez votre parcours éducatif avec KAAY-JANG' 
                  : 'Start your educational journey with KAAY-JANG'}
              </p>
              <Link to="/register">
                <Button 
                  size="lg" 
                  className="bg-white text-emerald-600 hover:bg-emerald-50 px-8 py-6 text-lg rounded-full shadow-lg"
                  data-testid="cta-register-btn"
                >
                  {t('register')}
                </Button>
              </Link>
            </Card>
          </div>
        </section>
      )}
    </div>
  );
};