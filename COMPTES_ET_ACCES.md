# 🎓 KAAY-JANG - Guide d'Accès et Comptes de Démonstration

## 🌐 URL de l'Application
**https://scholar-network.preview.emergentagent.com**

---

## 📊 BASE DE DONNÉES MongoDB

### Connexion
- **URL**: mongodb://localhost:27017
- **Database**: kaay_jang_db

### Comment explorer la base de données?

1. **Via le script Python d'exploration**:
```bash
cd /app/backend
python explore_db.py
```
Ce script affiche:
- Toutes les collections
- La structure de chaque collection
- Les relations entre collections
- Des exemples de données

2. **Via MongoDB Shell** (dans le conteneur):
```bash
mongosh mongodb://localhost:27017/kaay_jang_db
```

Commandes utiles:
```javascript
// Lister toutes les collections
show collections

// Voir tous les utilisateurs
db.users.find({}, {password: 0}).pretty()

// Voir toutes les branches
db.branches.find().pretty()

// Voir tous les devoirs
db.assignments.find().pretty()

// Compter les documents
db.users.countDocuments()
```

---

## 🗄️ STRUCTURE DE LA BASE DE DONNÉES

### Collections (Tables) et Relations:

```
┌─────────────────┐
│   branches      │ ← Filières (Primaire, Collège, Lycée, etc.)
│  (7 branches)   │
└────────┬────────┘
         │ 1:N
         │
┌────────▼────────┐
│    levels       │ ← Niveaux (CI, CP, CE1, 6ème, Seconde, etc.)
│  (16 levels)    │
└─────────────────┘

┌─────────────────┐
│   subjects      │ ← Matières (Maths, Français, Physique, etc.)
│  (14 subjects)  │   Certaines sont liées à des branches
│                 │   Ex: "Mathématiques (Primaire)" avec branch_id
└────────┬────────┘
         │
         │ M:N via teacher_subjects (à créer)
         │
┌────────▼────────┐
│     users       │ ← Utilisateurs (Admin, Professeurs, Élèves)
│   (22 users)    │   - role: admin/teacher/student
└────────┬────────┘   - branch_id: lien vers filière
         │            - level_id: lien vers niveau
         │
         │ 1:N
         │
┌────────▼────────┐
│  assignments    │ ← Devoirs
│ (7 assignments) │   - assignment_type: "quiz" ou "submission"
└────────┬────────┘   - branch_id + level_id + subject_id
         │            - teacher_id
         │ 1:N
         │
┌────────▼────────┐
│   questions     │ ← Questions (pour quiz uniquement)
│  (8 questions)  │   - assignment_id
└─────────────────┘   - correct_answer pour correction auto

┌─────────────────┐
│  submissions    │ ← Soumissions des élèves (devoirs à rendre)
│                 │   - assignment_id
└─────────────────┘   - student_id
                      - grade (note)
                      - teacher_comment

┌─────────────────┐
│    topics       │ ← Posts du forum
│   (5 topics)    │   - branch_id + level_id + subject_id
└─────────────────┘   - author_id
                      - visibility: "public" ou "followers_only"

┌─────────────────┐
│     posts       │ ← Réponses aux topics
└─────────────────┘   - topic_id

┌─────────────────┐
│    follows      │ ← Relations de follow
└─────────────────┘   - follower_id
                      - followed_id

┌─────────────────┐
│ notifications   │ ← Notifications in-app
└─────────────────┘   - user_id

┌─────────────────┐
│  ad_banners     │ ← Bannières publicitaires
│  (3 banners)    │
└─────────────────┘
```

### Modèle relationnel adapté:

**Votre suggestion de modèle:**
```
Filière (branches)
   └── 1:N → Niveau (levels)
              └── 1:N → Matière (subjects avec branch_id)
                         └── 1:N → Devoir (assignments)
                                    └── 1:N → Question
                                               └── 1:N → Réponse (answers/submissions)
```

---

## 👥 COMPTES DE DÉMONSTRATION

### 📚 ADMINISTRATEUR
- **Email**: admin@kaayjang.com
- **Password**: admin123
- **Accès**: Validation profs, gestion branches/niveaux/matières, stats globales

---

### 👨‍🏫 PROFESSEURS (5 comptes)

#### 1. Sophie Diop - Mathématiques (Lycée)
- **Email**: prof.math@kaayjang.com
- **Password**: prof123
- **Établissement**: Lycée Blaise Diagne
- **Niveau**: Terminale
- **Devoirs créés**: QCM Équations du second degré

#### 2. Amadou Ba - Français (Collège)
- **Email**: prof.francais@kaayjang.com
- **Password**: prof123
- **Établissement**: Collège Kennedy
- **Niveau**: 6ème
- **Devoirs créés**: Dissertation sur le romantisme

#### 3. Fatou Sall - Physique (Lycée)
- **Email**: prof.physique@kaayjang.com
- **Password**: prof123
- **Établissement**: Lycée Limamou Laye
- **Niveau**: Première
- **Devoirs créés**: Étude de cas - Chute libre

#### 4. Moussa Ndiaye - Informatique (Licence)
- **Email**: prof.info@kaayjang.com
- **Password**: prof123
- **Établissement**: Université Cheikh Anta Diop
- **Niveau**: L1

#### 5. Aminata Mbaye - Primaire ⭐ NOUVEAU
- **Email**: prof.primaire@kaayjang.com
- **Password**: prof123
- **Établissement**: École Primaire Diamniadio
- **Niveaux**: CI à CM2
- **Devoirs créés**:
  - Quiz - Les additions (CE1)
  - Rédaction - Mon animal préféré (CE2)
  - Quiz - Tables de multiplication (CM1)
  - Poésie à réciter - Les saisons (CE2, sans limite)

---

### 👨‍🎓 ÉLÈVES (13 comptes)

#### Lycée (7 élèves)
1. **Awa Faye** (Terminale S) - eleve1@kaayjang.com
2. **Ibrahima Sarr** (Terminale S) - eleve2@kaayjang.com
3. **Cheikh Fall** (Première L) - eleve4@kaayjang.com
4. **Omar Sow** (Seconde S) - eleve6@kaayjang.com
5. **Ndeye Sy** (Terminale L) - eleve7@kaayjang.com
6. **Alioune Badara** (Première G) - eleve10@kaayjang.com

#### Collège (2 élèves)
7. **Mariama Diallo** (4ème) - eleve3@kaayjang.com
8. **Aissatou Thiam** (3ème) - eleve5@kaayjang.com
9. **Mamadou Gueye** (5ème) - eleve8@kaayjang.com

#### Licence (1 élève)
10. **Khady Niang** (L1 Info) - eleve9@kaayjang.com

#### Primaire (3 élèves) ⭐ NOUVEAUX
11. **Samba Gueye** (CE1) - eleve.primaire1@kaayjang.com
12. **Fatoumata Diagne** (CE2) - eleve.primaire2@kaayjang.com
13. **Modou Ndiaye** (CM1) - eleve.primaire3@kaayjang.com

**Tous les élèves ont le mot de passe**: eleve123

---

## 📝 DEVOIRS CRÉÉS (7 devoirs)

### Type "quiz" (correction automatique - 4 devoirs):
1. **QCM - Équations du second degré** (Lycée Terminale - Maths)
   - 2 questions
   - Prof: Sophie Diop

2. **Quiz - Les additions** (Primaire CE1 - Maths)
   - 3 questions (5+3, 12+8, 7+9)
   - Prof: Aminata Mbaye

3. **Quiz - Tables de multiplication** (Primaire CM1 - Maths)
   - 3 questions (6×7, 9×8, 5×12)
   - Prof: Aminata Mbaye

### Type "submission" (à rendre avec correction manuelle - 3 devoirs):
4. **Dissertation - Le romantisme** (Collège - Français)
   - Sans limite de temps
   - Upload de fichiers autorisé
   - Prof: Amadou Ba

5. **Étude de cas - Chute libre** (Lycée - Physique)
   - Date limite: 14 jours
   - Upload de fichiers autorisé
   - Prof: Fatou Sall

6. **Rédaction - Mon animal préféré** (Primaire CE2 - Français)
   - Date limite: 10 jours
   - Upload de fichiers autorisé (dessins!)
   - Prof: Aminata Mbaye

7. **Poésie à réciter - Les saisons** (Primaire CE2 - Français)
   - **SANS LIMITE DE TEMPS** ✨
   - Upload audio/vidéo autorisé
   - Prof: Aminata Mbaye

---

## 💬 POSTS DU FORUM (5 posts)

### Posts Publics (3):
1. **Comment résoudre les équations du second degré?** 🌍
   - Par: Sophie Diop (prof)
   - Lycée Terminale - Maths

2. **Aide pour les dérivées** 🌍
   - Par: Awa Faye (élève)
   - Lycée - Maths

3. **Expériences de physique amusantes** 🌍
   - Par: Fatou Sall (prof)
   - Lycée - Physique

### Posts Privés (2):
4. **Analyse de texte - Méthode** 🔒
   - Par: Amadou Ba (prof)
   - Visible uniquement par ses followers
   - Collège - Français

5. **Mes notes de cours - Français 3ème** 🔒
   - Par: Mariama Diallo (élève)
   - Visible uniquement par ses followers
   - Collège - Français

---

## 🎨 BANNIÈRES PUBLICITAIRES (3)

Rotation automatique toutes les 5 secondes:
1. **Librairie Scolaire Dakar**
   - Tous vos manuels scolaires au meilleur prix!
   - ☎️ +221 33 123 45 67

2. **Cours de Soutien**
   - Cours particuliers pour tous les niveaux
   - ☎️ +221 77 987 65 43

3. **Orientation Académique**
   - Trouvez votre voie avec nos conseillers expérimentés
   - ☎️ +221 70 456 78 90

---

## 🗂️ FILIÈRES, NIVEAUX ET MATIÈRES

### Branches (Filières):
1. **Primaire** - 6 niveaux
   - CI (Cours d'Initiation)
   - CP (Cours Préparatoire)
   - CE1, CE2, CM1, CM2

2. **Secondaire** - 0 niveau (à compléter)

3. **Collège** - 4 niveaux
   - 6ème, 5ème, 4ème, 3ème

4. **Lycée** - 3 niveaux
   - Seconde, Première, Terminale

5. **BTS** - 0 niveau (à compléter)

6. **Licence** - 3 niveaux
   - L1, L2, L3

7. **Ingénieur** - 0 niveau (à compléter)

### Matières (14 matières):

#### Générales:
- Mathématiques
- Français
- Anglais
- Physique-Chimie
- SVT (Sciences de la Vie et de la Terre)
- Histoire-Géographie
- Philosophie
- Informatique
- Économie
- Espagnol

#### Spécifiques Primaire (avec branch_id):
- Mathématiques (Primaire)
- Français (Primaire)
- Éveil Scientifique
- Dessin et Arts

---

## 🔧 SCRIPTS UTILES

### Explorer la base de données:
```bash
cd /app/backend
python explore_db.py
```

### Créer des données de test:
```bash
cd /app/backend
python create_demo_data.py
```

### Ajouter des devoirs primaire:
```bash
cd /app/backend
python add_primary_assignments.py
```

### Réinitialiser complètement la DB:
```bash
mongosh mongodb://localhost:27017/kaay_jang_db
db.dropDatabase()
cd /app/backend
python init_data.py
python create_demo_data.py
python add_primary_assignments.py
```

---

## 🎯 FONCTIONNALITÉS PRINCIPALES

✅ Authentification JWT
✅ 3 rôles (Admin/Prof/Élève)
✅ Dashboards personnalisés par rôle
✅ Forum avec filtres (branche/niveau/matière)
✅ Posts publics et privés (followers only)
✅ Système de follow
✅ **Devoirs QCM avec correction automatique**
✅ **Devoirs à rendre avec correction manuelle**
✅ **Upload de fichiers (PDF, images, audio, vidéo)**
✅ **Devoirs sans limite de temps**
✅ Notifications in-app configurables
✅ Bannière publicitaire rotative (5 sec)
✅ Multilingue FR/EN
✅ Design futuriste et responsive

---

## 📱 COMMENT TESTER?

1. **En tant qu'Admin**:
   - Connexion avec admin@kaayjang.com / admin123
   - Voir stats globales
   - Valider/refuser des professeurs
   - Gérer branches/niveaux/matières

2. **En tant que Professeur**:
   - Connexion avec prof.primaire@kaayjang.com / prof123
   - Créer des devoirs (quiz ou à rendre)
   - Corriger les soumissions des élèves
   - Publier sur le forum

3. **En tant qu'Élève**:
   - Connexion avec eleve.primaire1@kaayjang.com / eleve123
   - Voir les devoirs disponibles
   - Faire les quiz (correction automatique)
   - Soumettre les devoirs (avec upload de fichiers)
   - Participer au forum

---

## 💡 NOTES IMPORTANTES

1. **Matières liées aux filières**: Les matières peuvent avoir un `branch_id` pour être spécifiques à une filière (ex: "Mathématiques (Primaire)")

2. **Devoirs flexibles**: 
   - `assignment_type = "quiz"` → correction automatique
   - `assignment_type = "submission"` → correction manuelle
   - `due_date = null` → sans limite de temps

3. **Upload de fichiers**: Activé avec `allow_files = true`

4. **Relations**: 
   - Devoir → branch_id + level_id + subject_id
   - Matière → peut avoir branch_id (optionnel)
   - Niveau → obligatoirement lié à branch_id

---

**Version**: 1.1
**Date**: 23 Novembre 2025
