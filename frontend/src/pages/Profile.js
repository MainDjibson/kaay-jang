import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { User, Users, UserPlus, UserMinus } from 'lucide-react';
import api from '../utils/api';
import { toast } from 'sonner';
import i18n from '../i18n';

export const Profile = () => {
  const { t } = useTranslation();
  const { user: currentUser, updateUser } = useAuth();
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isFollowing, setIsFollowing] = useState(false);
  const [followers, setFollowers] = useState({ count: 0 });
  const [following, setFollowing] = useState({ count: 0 });
  const [formData, setFormData] = useState({});

  const isOwnProfile = !userId || userId === currentUser?.id;

  useEffect(() => {
    if (isOwnProfile) {
      setUser(currentUser);
      setFormData(currentUser || {});
    } else {
      fetchUser();
      checkFollowStatus();
    }
    fetchFollowStats();
  }, [userId, currentUser]);

  const fetchUser = async () => {
    try {
      const response = await api.get(`/users/${userId}`);
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
    }
  };

  const checkFollowStatus = async () => {
    try {
      const response = await api.get(`/follows/is-following/${userId}`);
      setIsFollowing(response.data.is_following);
    } catch (error) {
      console.error('Failed to check follow status:', error);
    }
  };

  const fetchFollowStats = async () => {
    try {
      const targetUserId = userId || currentUser?.id;
      const [followersRes, followingRes] = await Promise.all([
        api.get(`/follows/followers/${targetUserId}`),
        api.get(`/follows/following/${targetUserId}`)
      ]);
      setFollowers(followersRes.data);
      setFollowing(followingRes.data);
    } catch (error) {
      console.error('Failed to fetch follow stats:', error);
    }
  };

  const handleFollow = async () => {
    try {
      if (isFollowing) {
        await api.delete(`/follows/${userId}`);
        setIsFollowing(false);
        toast.success(i18n.language === 'fr' ? 'Désabonné' : 'Unfollowed');
      } else {
        await api.post(`/follows?followed_id=${userId}`);
        setIsFollowing(true);
        toast.success(i18n.language === 'fr' ? 'Abonné' : 'Followed');
      }
      fetchFollowStats();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error');
    }
  };

  const handleSave = async () => {
    try {
      await api.put('/auth/me', formData);
      updateUser(formData);
      setIsEditing(false);
      toast.success(i18n.language === 'fr' ? 'Profil mis à jour' : 'Profile updated');
    } catch (error) {
      toast.error(i18n.language === 'fr' ? 'Erreur' : 'Error');
    }
  };

  if (!user) {
    return <div className="flex items-center justify-center min-h-screen">{t('loading')}</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 py-8 px-4">
      <div className="max-w-4xl mx-auto" data-testid="profile-page">
        <Card className="p-8">
          {/* Header */}
          <div className="flex items-start justify-between mb-8">
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-full flex items-center justify-center">
                {user.avatar_url ? (
                  <img src={user.avatar_url} alt={user.name} className="w-24 h-24 rounded-full" />
                ) : (
                  <User className="w-12 h-12 text-white" />
                )}
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-800" data-testid="profile-name">{user.name}</h1>
                <p className="text-gray-600" data-testid="profile-role">{t(user.role)}</p>
                <div className="flex gap-4 mt-2 text-sm">
                  <span data-testid="followers-count">
                    <strong>{followers.count}</strong> {t('followers')}
                  </span>
                  <span data-testid="following-count">
                    <strong>{following.count}</strong> {t('following')}
                  </span>
                </div>
              </div>
            </div>
            <div>
              {isOwnProfile ? (
                <Button 
                  onClick={() => setIsEditing(!isEditing)}
                  variant="outline"
                  data-testid="edit-profile-btn"
                >
                  {isEditing ? t('cancel') : t('edit')}
                </Button>
              ) : (
                <Button 
                  onClick={handleFollow}
                  className={isFollowing ? '' : 'bg-emerald-600 hover:bg-emerald-700'}
                  variant={isFollowing ? 'outline' : 'default'}
                  data-testid="follow-btn"
                >
                  {isFollowing ? (
                    <><UserMinus className="w-4 h-4 mr-2" /> {t('unfollow')}</>
                  ) : (
                    <><UserPlus className="w-4 h-4 mr-2" /> {t('follow')}</>
                  )}
                </Button>
              )}
            </div>
          </div>

          {/* Profile Info */}
          {isEditing && isOwnProfile ? (
            <div className="space-y-6">
              <div>
                <Label>{t('name')}</Label>
                <Input 
                  value={formData.name || ''}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  data-testid="edit-name"
                />
              </div>
              <div>
                <Label>{i18n.language === 'fr' ? 'Bio' : 'Bio'}</Label>
                <Textarea 
                  value={formData.bio || ''}
                  onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  rows={4}
                  data-testid="edit-bio"
                />
              </div>
              <Button onClick={handleSave} className="bg-emerald-600 hover:bg-emerald-700" data-testid="save-profile-btn">
                {t('save')}
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-gray-700">{i18n.language === 'fr' ? 'Bio' : 'Bio'}</h3>
                <p className="text-gray-600" data-testid="profile-bio">{user.bio || (i18n.language === 'fr' ? 'Aucune bio' : 'No bio')}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h3 className="font-semibold text-gray-700">{t('email')}</h3>
                  <p className="text-gray-600" data-testid="profile-email">{user.email}</p>
                </div>
                {user.establishment && (
                  <div>
                    <h3 className="font-semibold text-gray-700">{i18n.language === 'fr' ? 'Établissement' : 'Institution'}</h3>
                    <p className="text-gray-600">{user.establishment}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};