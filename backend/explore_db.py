"""
Script pour explorer et visualiser la base de données MongoDB
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

async def explore_database():
    """Explore all collections and show data structure"""
    
    print("=" * 80)
    print(f"📊 EXPLORATION DE LA BASE DE DONNÉES: {db_name}")
    print(f"🔗 URL: {mongo_url}")
    print("=" * 80)
    
    # Get all collections
    collections = await db.list_collection_names()
    
    print(f"\n📁 Collections disponibles ({len(collections)}):")
    for coll in collections:
        print(f"   - {coll}")
    
    print("\n" + "=" * 80)
    
    # Explore each collection
    for collection_name in sorted(collections):
        print(f"\n📦 COLLECTION: {collection_name}")
        print("-" * 80)
        
        # Count documents
        count = await db[collection_name].count_documents({})
        print(f"Nombre d'enregistrements: {count}")
        
        if count > 0:
            # Get first document as example
            example = await db[collection_name].find_one({}, {"_id": 0})
            
            # Show structure
            print("\n📋 Structure (champs):")
            for key in example.keys():
                value = example[key]
                value_type = type(value).__name__
                
                # Show preview of value
                if isinstance(value, str):
                    preview = value[:50] + "..." if len(value) > 50 else value
                elif isinstance(value, list):
                    preview = f"[{len(value)} éléments]"
                elif isinstance(value, dict):
                    preview = f"{{...}}"
                else:
                    preview = str(value)
                
                print(f"   {key:25} : {value_type:15} = {preview}")
            
            # Show all documents for small collections
            if count <= 10:
                print(f"\n📄 Tous les enregistrements ({count}):")
                all_docs = await db[collection_name].find({}, {"_id": 0}).to_list(1000)
                for i, doc in enumerate(all_docs, 1):
                    print(f"\n   Document {i}:")
                    print(f"   {json.dumps(doc, indent=6, ensure_ascii=False, default=str)}")
            else:
                print(f"\n📄 Exemples d'enregistrements (5 premiers sur {count}):")
                examples = await db[collection_name].find({}, {"_id": 0}).limit(5).to_list(5)
                for i, doc in enumerate(examples, 1):
                    print(f"\n   Document {i}:")
                    # Show compact version
                    if "name" in doc:
                        print(f"      name: {doc.get('name')}")
                    if "email" in doc:
                        print(f"      email: {doc.get('email')}")
                    if "title" in doc:
                        print(f"      title: {doc.get('title')}")
                    if "id" in doc:
                        print(f"      id: {doc.get('id')}")
        
        print("\n" + "-" * 80)
    
    print("\n" + "=" * 80)
    print("✅ Exploration terminée!")
    print("=" * 80)

async def show_relationships():
    """Show relationships between collections"""
    
    print("\n\n" + "=" * 80)
    print("🔗 RELATIONS ENTRE LES COLLECTIONS")
    print("=" * 80)
    
    # Branches -> Levels
    branches = await db.branches.find({}, {"_id": 0, "id": 1, "name": 1}).to_list(100)
    print("\n📊 Branches -> Levels:")
    for branch in branches:
        levels = await db.levels.find({"branch_id": branch["id"]}, {"_id": 0, "name": 1}).to_list(100)
        print(f"\n   {branch['name']} ({branch['id'][:8]}...):")
        for level in levels:
            print(f"      - {level['name']}")
    
    # Subjects
    print("\n\n📚 Matières disponibles:")
    subjects = await db.subjects.find({}, {"_id": 0, "name": 1, "name_en": 1}).to_list(100)
    for subject in subjects:
        print(f"   - {subject['name']} / {subject['name_en']}")
    
    # Assignments -> Questions
    print("\n\n📝 Devoirs et leurs questions:")
    assignments = await db.assignments.find({}, {"_id": 0, "id": 1, "title": 1, "assignment_type": 1}).to_list(100)
    for assignment in assignments:
        questions = await db.questions.find({"assignment_id": assignment["id"]}, {"_id": 0}).to_list(100)
        print(f"\n   {assignment['title']} ({assignment['assignment_type']}):")
        print(f"      Questions: {len(questions)}")
        for i, q in enumerate(questions, 1):
            print(f"         {i}. {q.get('question_text', 'N/A')[:60]}...")
    
    # Users by role
    print("\n\n👥 Utilisateurs par rôle:")
    for role in ["admin", "teacher", "student"]:
        count = await db.users.count_documents({"role": role})
        print(f"   {role.capitalize()}: {count}")
        if count > 0 and count <= 5:
            users = await db.users.find({"role": role}, {"_id": 0, "name": 1, "email": 1}).to_list(10)
            for user in users:
                print(f"      - {user['name']} ({user['email']})")
    
    # Topics
    print("\n\n💬 Posts du forum:")
    topics = await db.topics.find({}, {"_id": 0, "title": 1, "author_name": 1, "visibility": 1}).to_list(100)
    for topic in topics:
        visibility_icon = "🌍" if topic['visibility'] == "public" else "🔒"
        print(f"   {visibility_icon} {topic['title']} - par {topic['author_name']}")
    
    print("\n" + "=" * 80)

async def export_schema():
    """Export schema to a JSON file"""
    
    schema = {}
    collections = await db.list_collection_names()
    
    for collection_name in collections:
        count = await db[collection_name].count_documents({})
        if count > 0:
            example = await db[collection_name].find_one({}, {"_id": 0})
            schema[collection_name] = {
                "count": count,
                "fields": {key: type(value).__name__ for key, value in example.items()}
            }
    
    # Save to file
    schema_file = ROOT_DIR / "database_schema.json"
    with open(schema_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n💾 Schéma exporté vers: {schema_file}")

async def main():
    await explore_database()
    await show_relationships()
    await export_schema()
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
