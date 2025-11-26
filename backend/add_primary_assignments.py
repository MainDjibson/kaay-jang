"""
Script pour ajouter des devoirs pour le primaire avec des matières spécifiques
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone, timedelta

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def create_primary_subjects():
    """Create subjects specific to primary school"""
    
    # Get Primaire branch
    primaire = await db.branches.find_one({"name": "Primaire"}, {"_id": 0})
    if not primaire:
        print("Primaire branch not found!")
        return None
    
    # Create primary-specific subjects (if they don't exist)
    primary_subjects = [
        {
            "id": "primaire_maths",
            "name": "Mathématiques (Primaire)",
            "name_en": "Mathematics (Primary)",
            "branch_id": primaire["id"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "primaire_francais",
            "name": "Français (Primaire)",
            "name_en": "French (Primary)",
            "branch_id": primaire["id"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "primaire_eveil",
            "name": "Éveil Scientifique",
            "name_en": "Science Discovery",
            "branch_id": primaire["id"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "primaire_dessin",
            "name": "Dessin et Arts",
            "name_en": "Drawing and Arts",
            "branch_id": primaire["id"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    for subject in primary_subjects:
        existing = await db.subjects.find_one({"id": subject["id"]})
        if not existing:
            await db.subjects.insert_one(subject)
            print(f"Created subject: {subject['name']}")
    
    return primaire, primary_subjects

async def create_primary_teacher():
    """Create a primary school teacher"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    primaire = await db.branches.find_one({"name": "Primaire"}, {"_id": 0})
    levels = await db.levels.find({"branch_id": primaire["id"]}, {"_id": 0}).to_list(10)
    
    teacher = {
        "id": str(uuid.uuid4()),
        "email": "prof.primaire@kaayjang.com",
        "password": pwd_context.hash("prof123"),
        "name": "Aminata Mbaye",
        "role": "teacher",
        "branch_id": primaire["id"],
        "level_id": levels[0]["id"] if levels else None,
        "bio": "Institutrice avec 15 ans d'expérience en primaire. J'adore enseigner aux enfants!",
        "establishment": "École Primaire Diamniadio",
        "is_validated": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    existing = await db.users.find_one({"email": teacher["email"]})
    if not existing:
        await db.users.insert_one(teacher)
        # Create notification settings
        notif_settings = {
            "id": str(uuid.uuid4()),
            "user_id": teacher["id"],
            "email_enabled": True,
            "in_app_enabled": True,
            "new_posts": True,
            "new_assignments": True,
            "new_followers": True,
            "forum_replies": True
        }
        await db.notification_settings.insert_one(notif_settings)
        print(f"Created teacher: {teacher['name']} ({teacher['email']})")
        return teacher
    else:
        print(f"Teacher {teacher['email']} already exists")
        return existing

async def create_primary_students():
    """Create some primary students"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    primaire = await db.branches.find_one({"name": "Primaire"}, {"_id": 0})
    levels = await db.levels.find({"branch_id": primaire["id"]}, {"_id": 0}).to_list(10)
    
    students = [
        {
            "id": str(uuid.uuid4()),
            "email": "eleve.primaire1@kaayjang.com",
            "password": pwd_context.hash("eleve123"),
            "name": "Samba Gueye",
            "role": "student",
            "branch_id": primaire["id"],
            "level_id": levels[2]["id"] if len(levels) > 2 else levels[0]["id"],  # CE1
            "objectives": "Apprendre à bien lire et compter",
            "establishment": "École Primaire Diamniadio",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "email": "eleve.primaire2@kaayjang.com",
            "password": pwd_context.hash("eleve123"),
            "name": "Fatoumata Diagne",
            "role": "student",
            "branch_id": primaire["id"],
            "level_id": levels[3]["id"] if len(levels) > 3 else levels[0]["id"],  # CE2
            "objectives": "Devenir excellente en maths",
            "establishment": "École Primaire Diamniadio",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "email": "eleve.primaire3@kaayjang.com",
            "password": pwd_context.hash("eleve123"),
            "name": "Modou Ndiaye",
            "role": "student",
            "branch_id": primaire["id"],
            "level_id": levels[4]["id"] if len(levels) > 4 else levels[0]["id"],  # CM1
            "objectives": "Préparer mon entrée au collège",
            "establishment": "École Primaire Diamniadio",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    created_students = []
    for student in students:
        existing = await db.users.find_one({"email": student["email"]})
        if not existing:
            await db.users.insert_one(student)
            notif_settings = {
                "id": str(uuid.uuid4()),
                "user_id": student["id"],
                "email_enabled": True,
                "in_app_enabled": True,
                "new_posts": True,
                "new_assignments": True,
                "new_followers": True,
                "forum_replies": True
            }
            await db.notification_settings.insert_one(notif_settings)
            created_students.append(student)
            print(f"Created student: {student['name']} ({student['email']})")
        else:
            created_students.append(existing)
    
    return created_students

async def create_primary_assignments(teacher, primaire, subjects):
    """Create assignments for primary school"""
    
    levels = await db.levels.find({"branch_id": primaire["id"]}, {"_id": 0}).to_list(10)
    maths_subject = next((s for s in subjects if "Mathématiques" in s["name"]), subjects[0])
    francais_subject = next((s for s in subjects if "Français" in s["name"]), subjects[1])
    
    # Assignment 1: Quiz Maths CE1 - Les additions
    assignment1_id = str(uuid.uuid4())
    assignment1 = {
        "id": assignment1_id,
        "title": "Quiz - Les additions (CE1)",
        "description": "Petit quiz sur les additions simples. Correction automatique!",
        "subject_id": maths_subject["id"],
        "branch_id": primaire["id"],
        "level_id": levels[2]["id"] if len(levels) > 2 else levels[0]["id"],  # CE1
        "teacher_id": teacher["id"],
        "assignment_type": "quiz",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=5)).isoformat(),
        "allow_files": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    questions1 = [
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment1_id,
            "question_type": "mcq",
            "question_text": "Combien font 5 + 3 ?",
            "options": ["6", "7", "8", "9"],
            "correct_answer": "8",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment1_id,
            "question_type": "mcq",
            "question_text": "Combien font 12 + 8 ?",
            "options": ["18", "19", "20", "21"],
            "correct_answer": "20",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment1_id,
            "question_type": "mcq",
            "question_text": "Quelle est la somme de 7 + 9 ?",
            "options": ["14", "15", "16", "17"],
            "correct_answer": "16",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Assignment 2: Rédaction à rendre CE2
    assignment2 = {
        "id": str(uuid.uuid4()),
        "title": "Rédaction - Mon animal préféré",
        "description": "Écris un petit texte sur ton animal préféré (5-10 lignes). Tu peux ajouter un dessin ou une photo!",
        "subject_id": francais_subject["id"],
        "branch_id": primaire["id"],
        "level_id": levels[3]["id"] if len(levels) > 3 else levels[0]["id"],  # CE2
        "teacher_id": teacher["id"],
        "assignment_type": "submission",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
        "allow_files": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Assignment 3: Quiz Maths CM1 - Les multiplications
    assignment3_id = str(uuid.uuid4())
    assignment3 = {
        "id": assignment3_id,
        "title": "Quiz - Tables de multiplication (CM1)",
        "description": "Révisons les tables de multiplication! Correction automatique.",
        "subject_id": maths_subject["id"],
        "branch_id": primaire["id"],
        "level_id": levels[4]["id"] if len(levels) > 4 else levels[0]["id"],  # CM1
        "teacher_id": teacher["id"],
        "assignment_type": "quiz",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        "allow_files": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    questions3 = [
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment3_id,
            "question_type": "mcq",
            "question_text": "Combien font 6 × 7 ?",
            "options": ["40", "41", "42", "43"],
            "correct_answer": "42",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment3_id,
            "question_type": "mcq",
            "question_text": "Combien font 9 × 8 ?",
            "options": ["70", "71", "72", "73"],
            "correct_answer": "72",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "assignment_id": assignment3_id,
            "question_type": "mcq",
            "question_text": "Combien font 5 × 12 ?",
            "options": ["50", "55", "60", "65"],
            "correct_answer": "60",
            "points": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Assignment 4: Poésie à apprendre (sans limite de temps)
    assignment4 = {
        "id": str(uuid.uuid4()),
        "title": "Poésie à réciter - Les saisons",
        "description": "Apprends cette poésie sur les saisons et enregistre-toi en train de la réciter (audio ou vidéo). Pas de limite de temps, prends ton temps!",
        "subject_id": francais_subject["id"],
        "branch_id": primaire["id"],
        "level_id": levels[3]["id"] if len(levels) > 3 else levels[0]["id"],  # CE2
        "teacher_id": teacher["id"],
        "assignment_type": "submission",
        "due_date": None,  # Pas de limite
        "allow_files": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    assignments = [assignment1, assignment2, assignment3, assignment4]
    all_questions = questions1 + questions3
    
    await db.assignments.insert_many(assignments)
    await db.questions.insert_many(all_questions)
    
    print(f"\nCreated {len(assignments)} primary school assignments:")
    for assignment in assignments:
        print(f"   - {assignment['title']} ({assignment['assignment_type']})")

async def main():
    print("=" * 80)
    print("📚 AJOUT DE DEVOIRS POUR LE PRIMAIRE")
    print("=" * 80)
    
    primaire, subjects = await create_primary_subjects()
    teacher = await create_primary_teacher()
    students = await create_primary_students()
    await create_primary_assignments(teacher, primaire, subjects)
    
    print("\n" + "=" * 80)
    print("✅ Devoirs primaire créés avec succès!")
    print("=" * 80)
    print("\n📋 NOUVEAU COMPTE CRÉÉ:")
    print("\n👨‍🏫 PROFESSEUR PRIMAIRE:")
    print("   Nom: Aminata Mbaye")
    print("   Email: prof.primaire@kaayjang.com")
    print("   Mot de passe: prof123")
    print("\n👨‍🎓 ÉLÈVES PRIMAIRE (3 nouveaux):")
    print("   1. Samba Gueye (CE1)")
    print("      Email: eleve.primaire1@kaayjang.com")
    print("      Mot de passe: eleve123")
    print("\n   2. Fatoumata Diagne (CE2)")
    print("      Email: eleve.primaire2@kaayjang.com")
    print("      Mot de passe: eleve123")
    print("\n   3. Modou Ndiaye (CM1)")
    print("      Email: eleve.primaire3@kaayjang.com")
    print("      Mot de passe: eleve123")
    print("\n" + "=" * 80)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
