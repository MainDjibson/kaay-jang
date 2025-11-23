import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  fr: {
    translation: {
      // Navigation
      home: 'Accueil',
      forum: 'Forum',
      dashboard: 'Tableau de bord',
      profile: 'Profil',
      login: 'Connexion',
      logout: 'Déconnexion',
      register: 'Inscription',
      
      // Common
      search: 'Rechercher',
      save: 'Enregistrer',
      cancel: 'Annuler',
      delete: 'Supprimer',
      edit: 'Modifier',
      view: 'Voir',
      submit: 'Soumettre',
      loading: 'Chargement...',
      
      // Auth
      email: 'Email',
      password: 'Mot de passe',
      name: 'Nom',
      role: 'Rôle',
      admin: 'Administrateur',
      teacher: 'Professeur',
      student: 'Élève',
      
      // Forum
      topics: 'Sujets',
      createTopic: 'Créer un sujet',
      replies: 'Réponses',
      views: 'Vues',
      
      // Assignments
      assignments: 'Devoirs',
      createAssignment: 'Créer un devoir',
      dueDate: 'Date limite',
      questions: 'Questions',
      
      // Profile
      branch: 'Branche',
      level: 'Niveau',
      subjects: 'Matières',
      followers: 'Abonnés',
      following: 'Abonnements',
      follow: 'Suivre',
      unfollow: 'Se désabonner',
      
      // Notifications
      notifications: 'Notifications',
      markAllRead: 'Tout marquer comme lu',
      noNotifications: 'Aucune notification',
      
      // Welcome
      welcomeTitle: 'Bienvenue sur KAAY-JANG',
      welcomeSubtitle: 'La plateforme éducative qui connecte professeurs et élèves',
      getStarted: 'Commencer',
      
      // Visibility
      public: 'Public',
      followersOnly: 'Abonnés uniquement',
      visibility: 'Visibilité'
    }
  },
  en: {
    translation: {
      // Navigation
      home: 'Home',
      forum: 'Forum',
      dashboard: 'Dashboard',
      profile: 'Profile',
      login: 'Login',
      logout: 'Logout',
      register: 'Register',
      
      // Common
      search: 'Search',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      view: 'View',
      submit: 'Submit',
      loading: 'Loading...',
      
      // Auth
      email: 'Email',
      password: 'Password',
      name: 'Name',
      role: 'Role',
      admin: 'Administrator',
      teacher: 'Teacher',
      student: 'Student',
      
      // Forum
      topics: 'Topics',
      createTopic: 'Create Topic',
      replies: 'Replies',
      views: 'Views',
      
      // Assignments
      assignments: 'Assignments',
      createAssignment: 'Create Assignment',
      dueDate: 'Due Date',
      questions: 'Questions',
      
      // Profile
      branch: 'Branch',
      level: 'Level',
      subjects: 'Subjects',
      followers: 'Followers',
      following: 'Following',
      follow: 'Follow',
      unfollow: 'Unfollow',
      
      // Notifications
      notifications: 'Notifications',
      markAllRead: 'Mark all as read',
      noNotifications: 'No notifications',
      
      // Welcome
      welcomeTitle: 'Welcome to KAAY-JANG',
      welcomeSubtitle: 'The educational platform connecting teachers and students',
      getStarted: 'Get Started',
      
      // Visibility
      public: 'Public',
      followersOnly: 'Followers Only',
      visibility: 'Visibility'
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: localStorage.getItem('language') || 'fr',
    fallbackLng: 'fr',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;