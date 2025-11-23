"""
Script to initialize database with default branches, levels, subjects, and ad banners
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def init_branches():
    """Initialize branches"""
    branches = [
        {"id": str(uuid.uuid4()), "name": "Primaire", "name_en": "Primary", "is_active": True, "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Secondaire", "name_en": "Secondary", "is_active": True, "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Coll\u00e8ge", "name_en": "Middle School", "is_active": True, "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Lyc\u00e9e", "name_en": "High School", "is_active": True, "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "BTS", "name_en": "BTS", "is_active": True, "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Licence", "name_en": "Bachelor", "is_active": True, "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Ing\u00e9nieur", "name_en": "Engineering", "is_active": True, "created_at": datetime.now(timezone.utc).isoformat()},
    ]
    
    existing = await db.branches.count_documents({})
    if existing == 0:
        await db.branches.insert_many(branches)
        print(f"Inserted {len(branches)} branches")
    else:
        print("Branches already exist")
    
    return branches

async def init_levels(branches):
    """Initialize levels for each branch"""
    levels = []
    
    # Primaire levels
    primaire_branch = next(b for b in branches if b["name"] == "Primaire")
    for level_name in ["CI (Cours d'Initiation)", "CP (Cours Pr\u00e9paratoire)", "CE1", "CE2", "CM1", "CM2"]:
        levels.append({
            "id": str(uuid.uuid4()),
            "branch_id": primaire_branch["id"],
            "name": level_name,
            "name_en": level_name,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    # Coll\u00e8ge levels
    college_branch = next(b for b in branches if b["name"] == "Coll\u00e8ge")
    for level_name in ["6\u00e8me", "5\u00e8me", "4\u00e8me", "3\u00e8me"]:
        levels.append({
            "id": str(uuid.uuid4()),
            "branch_id": college_branch["id"],
            "name": level_name,
            "name_en": level_name,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    # Lyc\u00e9e levels
    lycee_branch = next(b for b in branches if b["name"] == "Lyc\u00e9e")
    for level_name in ["Seconde", "Premi\u00e8re", "Terminale"]:
        levels.append({
            "id": str(uuid.uuid4()),
            "branch_id": lycee_branch["id"],
            "name": level_name,
            "name_en": level_name,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    # Licence levels
    licence_branch = next(b for b in branches if b["name"] == "Licence")
    for level_name in ["L1", "L2", "L3"]:
        levels.append({
            "id": str(uuid.uuid4()),
            "branch_id": licence_branch["id"],
            "name": level_name,
            "name_en": level_name,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    existing = await db.levels.count_documents({})
    if existing == 0:
        await db.levels.insert_many(levels)
        print(f"Inserted {len(levels)} levels")
    else:
        print("Levels already exist")

async def init_subjects():
    """Initialize subjects"""
    subjects = [
        {"id": str(uuid.uuid4()), "name": "Math\u00e9matiques", "name_en": "Mathematics", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Fran\u00e7ais", "name_en": "French", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Anglais", "name_en": "English", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Physique-Chimie", "name_en": "Physics-Chemistry", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "SVT (Sciences de la Vie et de la Terre)", "name_en": "Life and Earth Sciences", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Histoire-G\u00e9ographie", "name_en": "History-Geography", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Philosophie", "name_en": "Philosophy", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Informatique", "name_en": "Computer Science", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "\u00c9conomie", "name_en": "Economics", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Espagnol", "name_en": "Spanish", "created_at": datetime.now(timezone.utc).isoformat()},
    ]
    
    existing = await db.subjects.count_documents({})
    if existing == 0:
        await db.subjects.insert_many(subjects)
        print(f"Inserted {len(subjects)} subjects")
    else:
        print("Subjects already exist")

async def init_ad_banners():
    """Initialize sample ad banners"""
    banners = [
        {
            "id": str(uuid.uuid4()),
            "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400",
            "title": "Librairie Scolaire Dakar",
            "text": "Tous vos manuels scolaires au meilleur prix!",
            "phone": "+221 33 123 45 67",
            "email": "contact@librairie-dakar.sn",
            "link": "https://example.com",
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "image_url": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=400",
            "title": "Cours de Soutien",
            "text": "Cours particuliers pour tous les niveaux",
            "phone": "+221 77 987 65 43",
            "email": "info@soutien-scolaire.sn",
            "link": "https://example.com",
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400",
            "title": "Orientation Acad\u00e9mique",
            "text": "Trouvez votre voie avec nos conseillers exp\u00e9riment\u00e9s",
            "phone": "+221 70 456 78 90",
            "email": "contact@orientation.sn",
            "link": "https://example.com",
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    existing = await db.ad_banners.count_documents({})
    if existing == 0:
        await db.ad_banners.insert_many(banners)
        print(f"Inserted {len(banners)} ad banners")
    else:
        print("Ad banners already exist")

async def create_admin_user():
    """Create default admin user"""
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    admin_email = "admin@kaayjang.com"
    existing_admin = await db.users.find_one({"email": admin_email})
    
    if not existing_admin:
        admin_user = {
            "id": str(uuid.uuid4()),
            "email": admin_email,
            "password": pwd_context.hash("admin123"),
            "name": "Admin KAAY-JANG",
            "role": "admin",
            "is_validated": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(admin_user)
        print(f"Created admin user: {admin_email} / password: admin123")
    else:
        print("Admin user already exists")

async def main():
    print("Initializing database...")
    branches = await init_branches()
    await init_levels(branches)
    await init_subjects()
    await init_ad_banners()
    await create_admin_user()
    print("Database initialization complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
