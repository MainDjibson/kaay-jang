from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import aiosmtplib
from email.message import EmailMessage
import shutil

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT & Password
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# File upload directory
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# ============= Models =============
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    role: str  # admin, teacher, student
    branch_id: Optional[str] = None
    level_id: Optional[str] = None
    filiere: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    establishment: Optional[str] = None
    objectives: Optional[str] = None
    is_validated: bool = False  # For teacher validation
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str
    branch_id: Optional[str] = None
    level_id: Optional[str] = None
    filiere: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Branch(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    name_en: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Level(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    branch_id: str
    name: str
    name_en: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Subject(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    name_en: str
    branch_id: Optional[str] = None
    level_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TeacherSubject(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    teacher_id: str
    subject_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Topic(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    branch_id: str
    level_id: str
    subject_id: Optional[str] = None
    title: str
    content: str
    author_id: str
    author_name: Optional[str] = None
    author_role: Optional[str] = None
    visibility: str = "public"  # public or followers_only
    views_count: int = 0
    replies_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Post(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic_id: str
    author_id: str
    author_name: Optional[str] = None
    author_role: Optional[str] = None
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Assignment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    subject_id: str
    branch_id: str
    level_id: str
    teacher_id: str
    due_date: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Question(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assignment_id: str
    question_type: str  # mcq, text, true_false
    question_text: str
    options: Optional[List[str]] = None  # For MCQ
    correct_answer: str
    points: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StudentAnswer(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assignment_id: str
    question_id: str
    student_id: str
    answer_value: str
    is_correct: Optional[bool] = None
    score: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Follow(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    follower_id: str
    followed_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Notification(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: str  # new_post, new_assignment, new_follower, etc.
    message: str
    message_en: str
    link: Optional[str] = None
    read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NotificationSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    email_enabled: bool = True
    in_app_enabled: bool = True
    new_posts: bool = True
    new_assignments: bool = True
    new_followers: bool = True
    forum_replies: bool = True

class AdBanner(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    image_url: str
    title: str
    text: str
    phone: Optional[str] = None
    email: Optional[str] = None
    link: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FileUpload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_url: str
    uploaded_by: str
    file_type: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ============= Helper Functions =============
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"id": user_id}, {"_id": 0})
    if user is None:
        raise credentials_exception
    return User(**user)

async def send_email_notification(to_email: str, subject: str, body: str):
    # Placeholder for email sending
    # In production, configure SMTP settings
    pass

# ============= Routes =============

@api_router.post("/auth/register", response_model=Token)
async def register(user_create: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_create.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = hash_password(user_create.password)
    user_dict = user_create.model_dump(exclude={"password"})
    user = User(**user_dict)
    
    # Teachers need validation
    if user.role == "teacher":
        user.is_validated = False
    else:
        user.is_validated = True
    
    user_doc = user.model_dump()
    user_doc["password"] = hashed_password
    user_doc["created_at"] = user_doc["created_at"].isoformat()
    
    await db.users.insert_one(user_doc)
    
    # Create default notification settings
    notif_settings = NotificationSettings(user_id=user.id)
    await db.notification_settings.insert_one(notif_settings.model_dump())
    
    # Create token
    access_token = create_access_token(data={"sub": user.id})
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_login: UserLogin):
    user_doc = await db.users.find_one({"email": user_login.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user_login.password, user_doc["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Convert datetime string back to datetime if needed
    if isinstance(user_doc.get("created_at"), str):
        user_doc["created_at"] = datetime.fromisoformat(user_doc["created_at"])
    
    user = User(**{k: v for k, v in user_doc.items() if k != "password"})
    
    access_token = create_access_token(data={"sub": user.id})
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.put("/auth/me", response_model=User)
async def update_profile(user_update: dict, current_user: User = Depends(get_current_user)):
    # Remove sensitive fields
    user_update.pop("password", None)
    user_update.pop("role", None)
    user_update.pop("is_validated", None)
    
    await db.users.update_one({"id": current_user.id}, {"$set": user_update})
    
    updated_user = await db.users.find_one({"id": current_user.id}, {"_id": 0, "password": 0})
    if isinstance(updated_user.get("created_at"), str):
        updated_user["created_at"] = datetime.fromisoformat(updated_user["created_at"])
    
    return User(**updated_user)

# Branches
@api_router.get("/branches", response_model=List[Branch])
async def get_branches():
    branches = await db.branches.find({}, {"_id": 0}).to_list(100)
    for branch in branches:
        if isinstance(branch.get("created_at"), str):
            branch["created_at"] = datetime.fromisoformat(branch["created_at"])
    return branches

@api_router.post("/branches", response_model=Branch)
async def create_branch(branch: Branch, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    branch_doc = branch.model_dump()
    branch_doc["created_at"] = branch_doc["created_at"].isoformat()
    await db.branches.insert_one(branch_doc)
    return branch

# Levels
@api_router.get("/levels", response_model=List[Level])
async def get_levels(branch_id: Optional[str] = None):
    query = {"branch_id": branch_id} if branch_id else {}
    levels = await db.levels.find(query, {"_id": 0}).to_list(100)
    for level in levels:
        if isinstance(level.get("created_at"), str):
            level["created_at"] = datetime.fromisoformat(level["created_at"])
    return levels

@api_router.post("/levels", response_model=Level)
async def create_level(level: Level, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    level_doc = level.model_dump()
    level_doc["created_at"] = level_doc["created_at"].isoformat()
    await db.levels.insert_one(level_doc)
    return level

# Subjects
@api_router.get("/subjects", response_model=List[Subject])
async def get_subjects():
    subjects = await db.subjects.find({}, {"_id": 0}).to_list(100)
    for subject in subjects:
        if isinstance(subject.get("created_at"), str):
            subject["created_at"] = datetime.fromisoformat(subject["created_at"])
    return subjects

@api_router.post("/subjects", response_model=Subject)
async def create_subject(subject: Subject, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    subject_doc = subject.model_dump()
    subject_doc["created_at"] = subject_doc["created_at"].isoformat()
    await db.subjects.insert_one(subject_doc)
    return subject

# Teacher Subjects
@api_router.post("/teacher-subjects", response_model=TeacherSubject)
async def add_teacher_subject(teacher_subject: TeacherSubject, current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher" or current_user.id != teacher_subject.teacher_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    ts_doc = teacher_subject.model_dump()
    ts_doc["created_at"] = ts_doc["created_at"].isoformat()
    await db.teacher_subjects.insert_one(ts_doc)
    return teacher_subject

@api_router.get("/teacher-subjects/{teacher_id}", response_model=List[TeacherSubject])
async def get_teacher_subjects(teacher_id: str):
    ts_list = await db.teacher_subjects.find({"teacher_id": teacher_id}, {"_id": 0}).to_list(100)
    for ts in ts_list:
        if isinstance(ts.get("created_at"), str):
            ts["created_at"] = datetime.fromisoformat(ts["created_at"])
    return ts_list

# Topics (Forum)
@api_router.get("/topics", response_model=List[Topic])
async def get_topics(
    branch_id: Optional[str] = None,
    level_id: Optional[str] = None,
    subject_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = {}
    if branch_id:
        query["branch_id"] = branch_id
    if level_id:
        query["level_id"] = level_id
    if subject_id:
        query["subject_id"] = subject_id
    
    topics = await db.topics.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    # Filter visibility
    filtered_topics = []
    for topic in topics:
        if isinstance(topic.get("created_at"), str):
            topic["created_at"] = datetime.fromisoformat(topic["created_at"])
        
        if topic["visibility"] == "public":
            filtered_topics.append(topic)
        elif topic["visibility"] == "followers_only":
            # Check if current user follows the author
            is_following = await db.follows.find_one({
                "follower_id": current_user.id,
                "followed_id": topic["author_id"]
            })
            if is_following or topic["author_id"] == current_user.id:
                filtered_topics.append(topic)
    
    return filtered_topics

@api_router.post("/topics", response_model=Topic)
async def create_topic(topic: Topic, current_user: User = Depends(get_current_user)):
    topic.author_id = current_user.id
    topic.author_name = current_user.name
    topic.author_role = current_user.role
    
    topic_doc = topic.model_dump()
    topic_doc["created_at"] = topic_doc["created_at"].isoformat()
    await db.topics.insert_one(topic_doc)
    
    # Notify followers
    followers = await db.follows.find({"followed_id": current_user.id}, {"_id": 0}).to_list(1000)
    for follower in followers:
        notif = Notification(
            user_id=follower["follower_id"],
            type="new_post",
            message=f"{current_user.name} a créé un nouveau sujet: {topic.title}",
            message_en=f"{current_user.name} created a new topic: {topic.title}",
            link=f"/forum/topic/{topic.id}"
        )
        await db.notifications.insert_one(notif.model_dump())
    
    return topic

@api_router.get("/topics/{topic_id}", response_model=Topic)
async def get_topic(topic_id: str, current_user: User = Depends(get_current_user)):
    topic = await db.topics.find_one({"id": topic_id}, {"_id": 0})
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    if isinstance(topic.get("created_at"), str):
        topic["created_at"] = datetime.fromisoformat(topic["created_at"])
    
    # Check visibility
    if topic["visibility"] == "followers_only":
        if topic["author_id"] != current_user.id:
            is_following = await db.follows.find_one({
                "follower_id": current_user.id,
                "followed_id": topic["author_id"]
            })
            if not is_following:
                raise HTTPException(status_code=403, detail="Access denied")
    
    # Increment views
    await db.topics.update_one({"id": topic_id}, {"$inc": {"views_count": 1}})
    
    return Topic(**topic)

# Posts (Replies)
@api_router.get("/posts/{topic_id}", response_model=List[Post])
async def get_posts(topic_id: str):
    posts = await db.posts.find({"topic_id": topic_id}, {"_id": 0}).sort("created_at", 1).to_list(1000)
    for post in posts:
        if isinstance(post.get("created_at"), str):
            post["created_at"] = datetime.fromisoformat(post["created_at"])
    return posts

@api_router.post("/posts", response_model=Post)
async def create_post(post: Post, current_user: User = Depends(get_current_user)):
    post.author_id = current_user.id
    post.author_name = current_user.name
    post.author_role = current_user.role
    
    post_doc = post.model_dump()
    post_doc["created_at"] = post_doc["created_at"].isoformat()
    await db.posts.insert_one(post_doc)
    
    # Increment replies count
    await db.topics.update_one({"id": post.topic_id}, {"$inc": {"replies_count": 1}})
    
    # Notify topic author
    topic = await db.topics.find_one({"id": post.topic_id}, {"_id": 0})
    if topic and topic["author_id"] != current_user.id:
        notif = Notification(
            user_id=topic["author_id"],
            type="forum_reply",
            message=f"{current_user.name} a répondu à votre sujet",
            message_en=f"{current_user.name} replied to your topic",
            link=f"/forum/topic/{post.topic_id}"
        )
        await db.notifications.insert_one(notif.model_dump())
    
    return post

# Assignments
@api_router.get("/assignments", response_model=List[Assignment])
async def get_assignments(
    level_id: Optional[str] = None,
    subject_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = {}
    if current_user.role == "teacher":
        query["teacher_id"] = current_user.id
    elif current_user.role == "student":
        if current_user.level_id:
            query["level_id"] = current_user.level_id
    
    if level_id:
        query["level_id"] = level_id
    if subject_id:
        query["subject_id"] = subject_id
    
    assignments = await db.assignments.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    for assignment in assignments:
        if isinstance(assignment.get("created_at"), str):
            assignment["created_at"] = datetime.fromisoformat(assignment["created_at"])
        if isinstance(assignment.get("due_date"), str):
            assignment["due_date"] = datetime.fromisoformat(assignment["due_date"])
    return assignments

@api_router.post("/assignments", response_model=Assignment)
async def create_assignment(assignment: Assignment, current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher" or not current_user.is_validated:
        raise HTTPException(status_code=403, detail="Only validated teachers can create assignments")
    
    assignment.teacher_id = current_user.id
    
    assignment_doc = assignment.model_dump()
    assignment_doc["created_at"] = assignment_doc["created_at"].isoformat()
    assignment_doc["due_date"] = assignment_doc["due_date"].isoformat()
    await db.assignments.insert_one(assignment_doc)
    
    # Notify students in the level
    students = await db.users.find({"role": "student", "level_id": assignment.level_id}, {"_id": 0}).to_list(1000)
    for student in students:
        notif = Notification(
            user_id=student["id"],
            type="new_assignment",
            message=f"Nouveau devoir: {assignment.title}",
            message_en=f"New assignment: {assignment.title}",
            link=f"/assignments/{assignment.id}"
        )
        await db.notifications.insert_one(notif.model_dump())
    
    return assignment

@api_router.get("/assignments/{assignment_id}", response_model=Assignment)
async def get_assignment(assignment_id: str):
    assignment = await db.assignments.find_one({"id": assignment_id}, {"_id": 0})
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if isinstance(assignment.get("created_at"), str):
        assignment["created_at"] = datetime.fromisoformat(assignment["created_at"])
    if isinstance(assignment.get("due_date"), str):
        assignment["due_date"] = datetime.fromisoformat(assignment["due_date"])
    
    return Assignment(**assignment)

# Questions
@api_router.get("/questions/{assignment_id}", response_model=List[Question])
async def get_questions(assignment_id: str):
    questions = await db.questions.find({"assignment_id": assignment_id}, {"_id": 0}).to_list(100)
    for question in questions:
        if isinstance(question.get("created_at"), str):
            question["created_at"] = datetime.fromisoformat(question["created_at"])
    return questions

@api_router.post("/questions", response_model=Question)
async def create_question(question: Question, current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teachers only")
    
    question_doc = question.model_dump()
    question_doc["created_at"] = question_doc["created_at"].isoformat()
    await db.questions.insert_one(question_doc)
    return question

# Student Answers
@api_router.post("/answers", response_model=StudentAnswer)
async def submit_answer(answer: StudentAnswer, current_user: User = Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Students only")
    
    answer.student_id = current_user.id
    
    # Get question to check correct answer
    question = await db.questions.find_one({"id": answer.question_id}, {"_id": 0})
    if question:
        answer.is_correct = (answer.answer_value.strip().lower() == question["correct_answer"].strip().lower())
        answer.score = question["points"] if answer.is_correct else 0
    
    answer_doc = answer.model_dump()
    answer_doc["created_at"] = answer_doc["created_at"].isoformat()
    await db.answers.insert_one(answer_doc)
    return answer

@api_router.get("/answers/{assignment_id}/{student_id}", response_model=List[StudentAnswer])
async def get_student_answers(assignment_id: str, student_id: str):
    answers = await db.answers.find({"assignment_id": assignment_id, "student_id": student_id}, {"_id": 0}).to_list(100)
    for answer in answers:
        if isinstance(answer.get("created_at"), str):
            answer["created_at"] = datetime.fromisoformat(answer["created_at"])
    return answers

# Follows
@api_router.post("/follows")
async def follow_user(followed_id: str, current_user: User = Depends(get_current_user)):
    if current_user.id == followed_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    existing = await db.follows.find_one({"follower_id": current_user.id, "followed_id": followed_id})
    if existing:
        raise HTTPException(status_code=400, detail="Already following")
    
    follow = Follow(follower_id=current_user.id, followed_id=followed_id)
    follow_doc = follow.model_dump()
    follow_doc["created_at"] = follow_doc["created_at"].isoformat()
    await db.follows.insert_one(follow_doc)
    
    # Notify followed user
    notif = Notification(
        user_id=followed_id,
        type="new_follower",
        message=f"{current_user.name} vous suit maintenant",
        message_en=f"{current_user.name} is now following you",
        link=f"/profile/{current_user.id}"
    )
    await db.notifications.insert_one(notif.model_dump())
    
    return {"message": "Followed successfully"}

@api_router.delete("/follows/{followed_id}")
async def unfollow_user(followed_id: str, current_user: User = Depends(get_current_user)):
    result = await db.follows.delete_one({"follower_id": current_user.id, "followed_id": followed_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not following")
    return {"message": "Unfollowed successfully"}

@api_router.get("/follows/followers/{user_id}")
async def get_followers(user_id: str):
    followers = await db.follows.find({"followed_id": user_id}, {"_id": 0}).to_list(1000)
    return {"count": len(followers), "followers": followers}

@api_router.get("/follows/following/{user_id}")
async def get_following(user_id: str):
    following = await db.follows.find({"follower_id": user_id}, {"_id": 0}).to_list(1000)
    return {"count": len(following), "following": following}

@api_router.get("/follows/is-following/{followed_id}")
async def is_following(followed_id: str, current_user: User = Depends(get_current_user)):
    follow = await db.follows.find_one({"follower_id": current_user.id, "followed_id": followed_id})
    return {"is_following": follow is not None}

# Notifications
@api_router.get("/notifications", response_model=List[Notification])
async def get_notifications(current_user: User = Depends(get_current_user)):
    notifications = await db.notifications.find({"user_id": current_user.id}, {"_id": 0}).sort("created_at", -1).limit(50).to_list(50)
    for notif in notifications:
        if isinstance(notif.get("created_at"), str):
            notif["created_at"] = datetime.fromisoformat(notif["created_at"])
    return notifications

@api_router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, current_user: User = Depends(get_current_user)):
    await db.notifications.update_one({"id": notification_id, "user_id": current_user.id}, {"$set": {"read": True}})
    return {"message": "Marked as read"}

@api_router.get("/notifications/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_user)):
    count = await db.notifications.count_documents({"user_id": current_user.id, "read": False})
    return {"count": count}

# Notification Settings
@api_router.get("/notification-settings", response_model=NotificationSettings)
async def get_notification_settings(current_user: User = Depends(get_current_user)):
    settings = await db.notification_settings.find_one({"user_id": current_user.id}, {"_id": 0})
    if not settings:
        # Create default settings
        settings = NotificationSettings(user_id=current_user.id)
        await db.notification_settings.insert_one(settings.model_dump())
    return NotificationSettings(**settings)

@api_router.put("/notification-settings", response_model=NotificationSettings)
async def update_notification_settings(settings_update: dict, current_user: User = Depends(get_current_user)):
    await db.notification_settings.update_one({"user_id": current_user.id}, {"$set": settings_update}, upsert=True)
    updated = await db.notification_settings.find_one({"user_id": current_user.id}, {"_id": 0})
    return NotificationSettings(**updated)

# Ad Banners
@api_router.get("/ad-banners", response_model=List[AdBanner])
async def get_ad_banners():
    banners = await db.ad_banners.find({"is_active": True}, {"_id": 0}).to_list(100)
    for banner in banners:
        if isinstance(banner.get("created_at"), str):
            banner["created_at"] = datetime.fromisoformat(banner["created_at"])
    return banners

@api_router.post("/ad-banners", response_model=AdBanner)
async def create_ad_banner(banner: AdBanner, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    banner_doc = banner.model_dump()
    banner_doc["created_at"] = banner_doc["created_at"].isoformat()
    await db.ad_banners.insert_one(banner_doc)
    return banner

# Admin routes
@api_router.get("/admin/pending-teachers", response_model=List[User])
async def get_pending_teachers(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    teachers = await db.users.find({"role": "teacher", "is_validated": False}, {"_id": 0, "password": 0}).to_list(100)
    for teacher in teachers:
        if isinstance(teacher.get("created_at"), str):
            teacher["created_at"] = datetime.fromisoformat(teacher["created_at"])
    return teachers

@api_router.put("/admin/validate-teacher/{teacher_id}")
async def validate_teacher(teacher_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    await db.users.update_one({"id": teacher_id}, {"$set": {"is_validated": True}})
    return {"message": "Teacher validated"}

@api_router.get("/admin/stats")
async def get_admin_stats(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    total_users = await db.users.count_documents({})
    total_teachers = await db.users.count_documents({"role": "teacher"})
    total_students = await db.users.count_documents({"role": "student"})
    total_topics = await db.topics.count_documents({})
    total_assignments = await db.assignments.count_documents({})
    
    return {
        "total_users": total_users,
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_topics": total_topics,
        "total_assignments": total_assignments
    }

# Teacher stats
@api_router.get("/teacher/stats")
async def get_teacher_stats(current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teachers only")
    
    total_assignments = await db.assignments.count_documents({"teacher_id": current_user.id})
    total_topics = await db.topics.count_documents({"author_id": current_user.id})
    followers = await db.follows.count_documents({"followed_id": current_user.id})
    
    return {
        "total_assignments": total_assignments,
        "total_topics": total_topics,
        "followers": followers
    }

# Student stats
@api_router.get("/student/stats")
async def get_student_stats(current_user: User = Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Students only")
    
    # Get assignments completed
    assignments_in_level = await db.assignments.find({"level_id": current_user.level_id}, {"_id": 0}).to_list(1000)
    assignment_ids = [a["id"] for a in assignments_in_level]
    
    completed_assignments = set()
    all_answers = await db.answers.find({"student_id": current_user.id}, {"_id": 0}).to_list(10000)
    for answer in all_answers:
        if answer["assignment_id"] in assignment_ids:
            completed_assignments.add(answer["assignment_id"])
    
    # Calculate average score
    total_score = sum([a.get("score", 0) for a in all_answers if a.get("score") is not None])
    total_possible = len(all_answers)
    avg_score = (total_score / total_possible * 100) if total_possible > 0 else 0
    
    following = await db.follows.count_documents({"follower_id": current_user.id})
    
    return {
        "total_assignments": len(assignment_ids),
        "completed_assignments": len(completed_assignments),
        "average_score": round(avg_score, 2),
        "following": following
    }

# File upload
@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # Save file
    file_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{file_id}.{file_extension}"
    file_path = UPLOAD_DIR / new_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Save file info to DB
    file_upload = FileUpload(
        filename=file.filename,
        file_url=f"/uploads/{new_filename}",
        uploaded_by=current_user.id,
        file_type=file.content_type or "unknown"
    )
    
    file_doc = file_upload.model_dump()
    file_doc["created_at"] = file_doc["created_at"].isoformat()
    await db.files.insert_one(file_doc)
    
    return {"file_url": file_upload.file_url, "file_id": file_upload.id}

# User search
@api_router.get("/users/search", response_model=List[User])
async def search_users(q: str, role: Optional[str] = None):
    query = {"name": {"$regex": q, "$options": "i"}}
    if role:
        query["role"] = role
    
    users = await db.users.find(query, {"_id": 0, "password": 0}).limit(20).to_list(20)
    for user in users:
        if isinstance(user.get("created_at"), str):
            user["created_at"] = datetime.fromisoformat(user["created_at"])
    return users

@api_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id}, {"_id": 0, "password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if isinstance(user.get("created_at"), str):
        user["created_at"] = datetime.fromisoformat(user["created_at"])
    
    return User(**user)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()