import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Plus, MessageSquare, Eye } from 'lucide-react';
import api from '../utils/api';
import { AdBanner } from '../components/AdBanner';
import i18n from '../i18n';

export const Forum = () => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [branches, setBranches] = useState([]);
  const [levels, setLevels] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [topics, setTopics] = useState([]);
  const [filters, setFilters] = useState({ branch_id: '', level_id: '', subject_id: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    if (filters.branch_id) {
      fetchLevels(filters.branch_id);
    }
  }, [filters.branch_id]);

  useEffect(() => {
    fetchTopics();
  }, [filters]);

  const fetchInitialData = async () => {
    try {
      const [branchesRes, subjectsRes] = await Promise.all([
        api.get('/branches'),
        api.get('/subjects')
      ]);
      setBranches(branchesRes.data);
      setSubjects(subjectsRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
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

  const fetchTopics = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.branch_id) params.append('branch_id', filters.branch_id);
      if (filters.level_id) params.append('level_id', filters.level_id);
      if (filters.subject_id) params.append('subject_id', filters.subject_id);
      
      const response = await api.get(`/topics?${params.toString()}`);
      setTopics(response.data);
    } catch (error) {
      console.error('Failed to fetch topics:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 py-8 px-4">
      <div className="max-w-7xl mx-auto" data-testid="forum-page">
        <AdBanner />
        
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            {t('forum')}
          </h1>
          {user && (
            <Link to="/forum/create">
              <Button className="bg-emerald-600 hover:bg-emerald-700" data-testid="create-topic-btn">
                <Plus className="w-4 h-4 mr-2" />
                {t('createTopic')}
              </Button>
            </Link>
          )}
        </div>

        {/* Filters */}
        <Card className="p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">{t('branch')}</label>
              <Select value={filters.branch_id || 'all'} onValueChange={(value) => setFilters({ ...filters, branch_id: value === 'all' ? '' : value, level_id: '' })}>
                <SelectTrigger data-testid="filter-branch">
                  <SelectValue placeholder={i18n.language === 'fr' ? 'Toutes les branches' : 'All branches'} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{i18n.language === 'fr' ? 'Toutes' : 'All'}</SelectItem>
                  {branches.map((branch) => (
                    <SelectItem key={branch.id} value={branch.id}>
                      {i18n.language === 'fr' ? branch.name : branch.name_en}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">{t('level')}</label>
              <Select value={filters.level_id || 'all'} onValueChange={(value) => setFilters({ ...filters, level_id: value === 'all' ? '' : value })} disabled={!filters.branch_id}>
                <SelectTrigger data-testid="filter-level">
                  <SelectValue placeholder={i18n.language === 'fr' ? 'Tous les niveaux' : 'All levels'} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{i18n.language === 'fr' ? 'Tous' : 'All'}</SelectItem>
                  {levels.map((level) => (
                    <SelectItem key={level.id} value={level.id}>
                      {i18n.language === 'fr' ? level.name : level.name_en}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">{t('subjects')}</label>
              <Select value={filters.subject_id || 'all'} onValueChange={(value) => setFilters({ ...filters, subject_id: value === 'all' ? '' : value })}>
                <SelectTrigger data-testid="filter-subject">
                  <SelectValue placeholder={i18n.language === 'fr' ? 'Toutes les matières' : 'All subjects'} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{i18n.language === 'fr' ? 'Toutes' : 'All'}</SelectItem>
                  {subjects.map((subject) => (
                    <SelectItem key={subject.id} value={subject.id}>
                      {i18n.language === 'fr' ? subject.name : subject.name_en}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </Card>

        {/* Topics List */}
        {loading ? (
          <div className="text-center py-12">{t('loading')}</div>
        ) : topics.length === 0 ? (
          <Card className="p-12 text-center">
            <p className="text-gray-600">{i18n.language === 'fr' ? 'Aucun sujet trouvé' : 'No topics found'}</p>
          </Card>
        ) : (
          <div className="space-y-4">
            {topics.map((topic) => (
              <Link key={topic.id} to={`/forum/topic/${topic.id}`}>
                <Card className="p-6 hover:shadow-lg transition-shadow" data-testid={`topic-${topic.id}`}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-800 mb-2">{topic.title}</h3>
                      <p className="text-gray-600 mb-3">{topic.content.substring(0, 200)}...</p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>{topic.author_name} ({topic.author_role})</span>
                        <span>•</span>
                        <span>{new Date(topic.created_at).toLocaleDateString()}</span>
                        <span className="flex items-center gap-1">
                          <Eye className="w-4 h-4" /> {topic.views_count}
                        </span>
                        <span className="flex items-center gap-1">
                          <MessageSquare className="w-4 h-4" /> {topic.replies_count}
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};