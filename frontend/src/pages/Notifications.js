import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Switch } from '../components/ui/switch';
import { Label } from '../components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Bell, Check } from 'lucide-react';
import api from '../utils/api';
import { toast } from 'sonner';
import i18n from '../i18n';

export const Notifications = () => {
  const { t } = useTranslation();
  const [notifications, setNotifications] = useState([]);
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [notifsRes, settingsRes] = await Promise.all([
        api.get('/notifications'),
        api.get('/notification-settings')
      ]);
      setNotifications(notifsRes.data);
      setSettings(settingsRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      await api.put(`/notifications/${notificationId}/read`);
      setNotifications(notifications.map(n => 
        n.id === notificationId ? { ...n, read: true } : n
      ));
    } catch (error) {
      console.error('Failed to mark as read:', error);
    }
  };

  const updateSettings = async (key, value) => {
    try {
      const newSettings = { ...settings, [key]: value };
      await api.put('/notification-settings', newSettings);
      setSettings(newSettings);
      toast.success(i18n.language === 'fr' ? 'Paramètres mis à jour' : 'Settings updated');
    } catch (error) {
      toast.error(i18n.language === 'fr' ? 'Erreur' : 'Error');
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">{t('loading')}</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 py-8 px-4">
      <div className="max-w-4xl mx-auto" data-testid="notifications-page">
        <h1 className="text-4xl font-bold mb-8 text-gray-800" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          {t('notifications')}
        </h1>

        <Tabs defaultValue="list" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="list" data-testid="tab-list">{i18n.language === 'fr' ? 'Liste' : 'List'}</TabsTrigger>
            <TabsTrigger value="settings" data-testid="tab-settings">{i18n.language === 'fr' ? 'Paramètres' : 'Settings'}</TabsTrigger>
          </TabsList>

          <TabsContent value="list">
            <Card className="p-6">
              {notifications.length === 0 ? (
                <p className="text-center text-gray-600 py-12">{t('noNotifications')}</p>
              ) : (
                <div className="space-y-4">
                  {notifications.map((notif) => (
                    <div 
                      key={notif.id} 
                      className={`p-4 rounded-lg border-2 transition-colors ${
                        notif.read ? 'bg-gray-50 border-gray-200' : 'bg-emerald-50 border-emerald-200'
                      }`}
                      data-testid={`notification-${notif.id}`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="text-gray-800">
                            {i18n.language === 'fr' ? notif.message : notif.message_en}
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            {new Date(notif.created_at).toLocaleString()}
                          </p>
                        </div>
                        {!notif.read && (
                          <Button 
                            size="sm" 
                            variant="ghost"
                            onClick={() => markAsRead(notif.id)}
                            data-testid={`mark-read-${notif.id}`}
                          >
                            <Check className="w-4 h-4" />
                          </Button>
                        )}
                      </div>
                      {notif.link && (
                        <Link to={notif.link} className="text-sm text-emerald-600 hover:text-emerald-700 mt-2 inline-block">
                          {i18n.language === 'fr' ? 'Voir' : 'View'} →
                        </Link>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </TabsContent>

          <TabsContent value="settings">
            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-6 text-gray-800">
                {i18n.language === 'fr' ? 'Paramètres de notification' : 'Notification Settings'}
              </h2>
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <Label htmlFor="email_enabled">
                    {i18n.language === 'fr' ? 'Notifications par email' : 'Email notifications'}
                  </Label>
                  <Switch 
                    id="email_enabled"
                    checked={settings?.email_enabled}
                    onCheckedChange={(checked) => updateSettings('email_enabled', checked)}
                    data-testid="toggle-email"
                  />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="in_app_enabled">
                    {i18n.language === 'fr' ? 'Notifications dans l\'app' : 'In-app notifications'}
                  </Label>
                  <Switch 
                    id="in_app_enabled"
                    checked={settings?.in_app_enabled}
                    onCheckedChange={(checked) => updateSettings('in_app_enabled', checked)}
                    data-testid="toggle-in-app"
                  />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="new_posts">
                    {i18n.language === 'fr' ? 'Nouveaux posts' : 'New posts'}
                  </Label>
                  <Switch 
                    id="new_posts"
                    checked={settings?.new_posts}
                    onCheckedChange={(checked) => updateSettings('new_posts', checked)}
                    data-testid="toggle-new-posts"
                  />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="new_assignments">
                    {i18n.language === 'fr' ? 'Nouveaux devoirs' : 'New assignments'}
                  </Label>
                  <Switch 
                    id="new_assignments"
                    checked={settings?.new_assignments}
                    onCheckedChange={(checked) => updateSettings('new_assignments', checked)}
                    data-testid="toggle-new-assignments"
                  />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="new_followers">
                    {i18n.language === 'fr' ? 'Nouveaux abonnés' : 'New followers'}
                  </Label>
                  <Switch 
                    id="new_followers"
                    checked={settings?.new_followers}
                    onCheckedChange={(checked) => updateSettings('new_followers', checked)}
                    data-testid="toggle-new-followers"
                  />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="forum_replies">
                    {i18n.language === 'fr' ? 'Réponses forum' : 'Forum replies'}
                  </Label>
                  <Switch 
                    id="forum_replies"
                    checked={settings?.forum_replies}
                    onCheckedChange={(checked) => updateSettings('forum_replies', checked)}
                    data-testid="toggle-forum-replies"
                  />
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};