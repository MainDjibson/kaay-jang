"""
Script to create demo data: users, posts, assignments
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_demo_users():
    """Create demo teachers and students"""
    
    # Get branches and levels
    branches = await db.branches.find({}, {"_id": 0}).to_list(10)
    levels = await db.levels.find({}, {"_id": 0}).to_list(100)
    
    lycee_branch = next((b for b in branches if "Lycée" in b["name"]), branches[0])
    college_branch = next((b for b in branches if "Collège" in b["name"]), branches[1])
    licence_branch = next((b for b in branches if "Licence" in b["name"]), branches[2])
    
    lycee_levels = [l for l in levels if l["branch_id"] == lycee_branch["id"]]
    college_levels = [l for l in levels if l["branch_id"] == college_branch["id"]]
    licence_levels = [l for l in levels if l["branch_id"] == licence_branch["id"]]
    
    # Create 4 teachers
    teachers = [
        {
            "id": str(uuid.uuid4()),
            "email": "prof.math@kaayjang.com",
            "password": pwd_context.hash("prof123"),
            "name": "Sophie Diop",
            "role": "teacher",
            "branch_id": lycee_branch["id"],
            "level_id": lycee_levels[0]["id"] if lycee_levels else None,
            "filiere": "Scientifique",
            "bio": "Professeure de mathématiques avec 10 ans d'expérience. Passionnée par l'enseignement des sciences.",
            "establishment": "Lycée Blaise Diagne",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "email": "prof.francais@kaayjang.com",
            "password": pwd_context.hash("prof123"),
            "name": "Amadou Ba",
            "role": "teacher",
            "branch_id": college_branch["id"],
            "level_id": college_levels[0]["id"] if college_levels else None,
            "bio": "Enseignant de français et littérature. J'aime partager ma passion pour les lettres.",
            "establishment": "Collège Kennedy",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "email": "prof.physique@kaayjang.com",
            "password": pwd_context.hash("prof123"),
            "name": "Fatou Sall",
            "role": "teacher",
            "branch_id": lycee_branch["id"],
            "level_id": lycee_levels[1]["id"] if len(lycee_levels) > 1 else lycee_levels[0]["id"],
            "filiere": "Scientifique",
            "bio": "Docteure en physique, enseignante passionnée de sciences expérimentales.",
            "establishment": "Lycée Limamou Laye",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "email": "prof.info@kaayjang.com",
            "password": pwd_context.hash("prof123"),
            "name": "Moussa Ndiaye",
            "role": "teacher",
            "branch_id": licence_branch["id"],
            "level_id": licence_levels[0]["id"] if licence_levels else None,
            "bio": "Ingénieur informaticien et formateur. Spécialisé en développement web et algorithmique.",
            "establishment": "Université Cheikh Anta Diop",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Create 10 students
    students = [
        {
            "id": str(uuid.uuid4()),
            "email": f"eleve{i+1}@kaayjang.com",
            "password": pwd_context.hash("eleve123"),
            "name": name,
            "role": "student",
            "branch_id": branch["id"],
            "level_id": level["id"],
            "filiere": filiere,
            "objectives": objective,
            "establishment": establishment,
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        for i, (name, branch, level, filiere, objective, establishment) in enumerate([
            ("Awa Faye", lycee_branch, lycee_levels[2] if len(lycee_levels) > 2 else lycee_levels[0], "S", "Réussir le bac et devenir médecin", "Lycée Blaise Diagne"),
            ("Ibrahima Sarr", lycee_branch, lycee_levels[2] if len(lycee_levels) > 2 else lycee_levels[0], "S", "Préparer le concours d'ingénieur", "Lycée Limamou Laye"),
            ("Mariama Diallo", college_branch, college_levels[2] if len(college_levels) > 2 else college_levels[0], None, "Passer en seconde", "Collège Kennedy"),
            ("Cheikh Fall", lycee_branch, lycee_levels[1] if len(lycee_levels) > 1 else lycee_levels[0], "L", "Étudier les lettres", "Lycée Blaise Diagne"),
            ("Aissatou Thiam", college_branch, college_levels[3] if len(college_levels) > 3 else college_levels[0], None, "Obtenir le BFEM", "Collège Kennedy"),
            ("Omar Sow", lycee_branch, lycee_levels[0], "S", "Devenir ingénieur", "Lycée Limamou Laye"),
            ("Ndeye Sy", lycee_branch, lycee_levels[2] if len(lycee_levels) > 2 else lycee_levels[0], "L", "Devenir journaliste", "Lycée Blaise Diagne"),
            ("Mamadou Gueye", college_branch, college_levels[1] if len(college_levels) > 1 else college_levels[0], None, "Améliorer mes notes", "Collège Kennedy"),
            ("Khady Niang", licence_branch, licence_levels[0] if licence_levels else lycee_levels[0], "Informatique", "Devenir développeuse", "UCAD"),
            ("Alioune Badara", lycee_branch, lycee_levels[1] if len(lycee_levels) > 1 else lycee_levels[0], "G", "Devenir économiste", "Lycée Limamou Laye")
        ])
    ]
    
    # Check if demo users already exist
    existing = await db.users.find_one({"email": "prof.math@kaayjang.com"})
    if not existing:
        await db.users.insert_many(teachers + students)
        print(f"Created {len(teachers)} teachers and {len(students)} students")
        
        # Create notification settings for all users
        notif_settings = []
        for user in teachers + students:
            notif_settings.append({
                "id": str(uuid.uuid4()),
                "user_id": user["id"],
                "email_enabled": True,
                "in_app_enabled": True,
                "new_posts": True,
                "new_assignments": True,
                "new_followers": True,
                "forum_replies": True
            })
        await db.notification_settings.insert_many(notif_settings)
    else:
        print("Demo users already exist")
        # Fetch existing users for later use
        teachers = await db.users.find({"role": "teacher", "email": {"$regex": "@kaayjang.com"}}, {"_id": 0}).to_list(10)
        students = await db.users.find({"role": "student", "email": {"$regex": "@kaayjang.com"}}, {"_id": 0}).to_list(20)
    
    return teachers, students

async def create_follows(teachers, students):
    """Create follow relationships"""
    follows = []
    
    # Students follow teachers
    for student in students[:7]:
        for teacher in teachers[:2]:
            follows.append({
                "id": str(uuid.uuid4()),
                "follower_id": student["id"],
                "followed_id": teacher["id"],
                "created_at": datetime.now(timezone.utc).isoformat()
            })
    
    # Some students follow each other
    for i in range(0, min(5, len(students)), 2):
        if i + 1 < len(students):
            follows.append({
                "id": str(uuid.uuid4()),
                "follower_id": students[i]["id"],
                "followed_id": students[i+1]["id"],
                "created_at": datetime.now(timezone.utc).isoformat()
            })
    
    existing = await db.follows.count_documents({})
    if existing == 0:
        await db.follows.insert_many(follows)
        print(f"Created {len(follows)} follow relationships")
    else:
        print("Follows already exist")

async def create_forum_posts(teachers, students):
    """Create forum topics and posts"""
    subjects = await db.subjects.find({}, {"_id": 0}).to_list(100)
    branches = await db.branches.find({}, {"_id": 0}).to_list(10)
    levels = await db.levels.find({}, {"_id": 0}).to_list(100)
    
    math_subject = next((s for s in subjects if "Math" in s["name"]), subjects[0])
    francais_subject = next((s for s in subjects if "Fran" in s["name"]), subjects[1])
    
    topics = [
        {
            "id": str(uuid.uuid4()),
            "branch_id": teachers[0]["branch_id"],
            "level_id": teachers[0]["level_id"],
            "subject_id": math_subject["id"],
            "title": "Comment résoudre les équations du second degré ?",
            "content": "Bonjour à tous ! Je propose une méthode simple pour résoudre les équations du second degré. N'hésitez pas à poser vos questions !",
            "author_id": teachers[0]["id"],
            "author_name": teachers[0]["name"],
            "author_role": "teacher",
            "visibility": "public",
            "views_count": 45,
            "replies_count": 5,
            "created_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "branch_id": students[0]["branch_id"],
            "level_id": students[0]["level_id"],
            "subject_id": math_subject["id"],
            "title": "Aide pour les dérivées",
            "content": "Bonjour, j'ai du mal à comprendre les dérivées. Quelqu'un peut m'expliquer ?",
            "author_id": students[0]["id"],
            "author_name": students[0]["name"],
            "author_role": "student",
            "visibility": "public",
            "views_count": 23,
            "replies_count": 3,
            "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "branch_id": teachers[1]["branch_id"],
            "level_id": teachers[1]["level_id"],
            "subject_id": francais_subject["id"],
            "title": "Analyse de texte - Méthode",
            "content": "Pour mes abonnés : voici ma méthode complète d'analyse de texte avec exemples concrets.",
            "author_id": teachers[1]["id"],
            "author_name": teachers[1]["name"],
            "author_role": "teacher",
            "visibility": "followers_only",
            "views_count": 12,
            "replies_count": 2,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "branch_id": teachers[2]["branch_id"],
            "level_id": teachers[2]["level_id"],
            "subject_id": subjects[3]["id"],
            "title": "Expériences de physique amusantes",
            "content": "Partageons des expériences simples à faire à la maison pour comprendre la physique !",
            "author_id": teachers[2]["id"],
            "author_name": teachers[2]["name"],
            "author_role": "teacher",
            "visibility": "public",
            "views_count": 67,
            "replies_count": 8,
            "created_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "branch_id": students[2]["branch_id"],
            "level_id": students[2]["level_id"],
            "subject_id": francais_subject["id"],
            "title": "Mes notes de cours - Français 3ème",
            "content": "Je partage mes notes de cours de français pour ceux qui sont intéressés. Réservé à mes abonnés !",
            "author_id": students[2]["id"],
            "author_name": students[2]["name"],
            "author_role": "student",
            "visibility": "followers_only",
            "views_count": 8,
            "replies_count": 1,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat()
        }
    ]
    
    existing = await db.topics.count_documents({})
    if existing == 0:
        await db.topics.insert_many(topics)
        print(f"Created {len(topics)} forum topics")
    else:
        print("Forum topics already exist")

async def create_assignments(teachers, students):
    """Create sample assignments"""
    subjects = await db.subjects.find({}, {"_id": 0}).to_list(100)
    
    math_subject = next((s for s in subjects if "Math" in s["name"]), subjects[0])
    francais_subject = next((s for s in subjects if "Fran" in s["name"]), subjects[1])
    
    # Assignment 1: Quiz automatique (QCM)
    assignment1_id = str(uuid.uuid4())
    assignment1 = {
        "id": assignment1_id,
        "title": "QCM - Équations du second degré",
        "description": "Quiz de 5 questions sur les équations du second degré. Correction automatique.",
        "subject_id": math_subject["id"],
        "branch_id": teachers[0]["branch_id"],
        "level_id": teachers[0]["level_id"],
        "teacher_id": teachers[0]["id"],
        "assignment_type": "quiz",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        "allow_files": False,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    }
    
    # Questions for assignment 1
    questions1 = [
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment1_id,
            "question_type": "mcq",
            "question_text": "Quelle est la forme générale d'une équation du second degré ?",
            "options": ["ax + b = 0", "ax² + bx + c = 0", "ax³ + bx² + c = 0", "ax² + b = 0"],
            "correct_answer": "ax² + bx + c = 0",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment1_id,
            "question_type": "mcq",
            "question_text": "Le discriminant d'une équation ax² + bx + c = 0 est :",
            "options": ["b² - 4ac", "b² + 4ac", "2b - 4ac", "b - 4ac"],
            "correct_answer": "b² - 4ac",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Assignment 2: Devoir à rendre (dissertation)
    assignment2 = {
        "id": str(uuid.uuid4()),
        "title": "Dissertation - Le romantisme",
        "description": "Rédigez une dissertation sur le romantisme en littérature française. Vous pouvez joindre des images et documents. Longueur : 3-4 pages.",
        "subject_id": francais_subject["id"],
        "branch_id": teachers[1]["branch_id"],
        "level_id": teachers[1]["level_id"],
        "teacher_id": teachers[1]["id"],
        "assignment_type": "submission",
        "due_date": None,  # Pas de limite de temps
        "allow_files": True,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
    }
    
    # Assignment 3: Étude de cas
    assignment3 = {
        "id": str(uuid.uuid4()),
        "title": "Étude de cas - Chute libre",
        "description": "Analysez le mouvement de chute libre d'un objet. Incluez calculs et graphiques. Vous pouvez ajouter des photos de vos schémas.",
        "subject_id": subjects[3]["id"],  # Physique
        "branch_id": teachers[2]["branch_id"],
        "level_id": teachers[2]["level_id"],
        "teacher_id": teachers[2]["id"],
        "assignment_type": "submission",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat(),
        "allow_files": True,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    }
    
    existing = await db.assignments.count_documents({})
    if existing == 0:
        await db.assignments.insert_many([assignment1, assignment2, assignment3])
        await db.questions.insert_many(questions1)
        print(f"Created 3 assignments (1 quiz, 2 submissions)")
    else:
        print("Assignments already exist")

async def main():
    print("Creating demo data...")
    teachers, students = await create_demo_users()
    await create_follows(teachers, students)
    await create_forum_posts(teachers, students)
    await create_assignments(teachers, students)
    print("\nDemo data creation complete!")
    print("\n" + "="*60)
    print("COMPTES DE DÉMONSTRATION")
    print("="*60)
    print("\n📚 ADMINISTRATEUR:")
    print("  Email: admin@kaayjang.com")
    print("  Mot de passe: admin123")
    print("\n👨‍🏫 PROFESSEURS:")
    print("  1. Sophie Diop (Maths)")
    print("     Email: prof.math@kaayjang.com")
    print("     Mot de passe: prof123")
    print("\n  2. Amadou Ba (Français)")
    print("     Email: prof.francais@kaayjang.com")
    print("     Mot de passe: prof123")
    print("\n  3. Fatou Sall (Physique)")
    print("     Email: prof.physique@kaayjang.com")
    print("     Mot de passe: prof123")
    print("\n  4. Moussa Ndiaye (Informatique)")
    print("     Email: prof.info@kaayjang.com")
    print("     Mot de passe: prof123")
    print("\n👨‍🎓 ÉLÈVES (10 comptes):")
    for i in range(1, 11):
        print(f"  {i}. Email: eleve{i}@kaayjang.com")
        print(f"     Mot de passe: eleve123")
    print("\n" + "="*60)
    print("Données créées:")
    print("  - Posts publics et privés sur le forum")
    print("  - Relations de follow entre utilisateurs")
    print("  - 1 devoir QCM (correction automatique)")
    print("  - 2 devoirs à rendre (dissertation + étude de cas)")
    print("="*60)
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
