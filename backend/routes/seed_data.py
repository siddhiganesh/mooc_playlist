from datetime import datetime, timedelta
from extensions import db
from models import (
    User,
    Course,
    Video,
    Enrollment,
    Subtitle,
    Assignment,
    Quiz,
    Test,
    Discussion,
    Certificate,
)
from extensions import bcrypt


def seed():
    if User.query.first():
        return  # already seeded

    # --- Users ---
    admin_pw = bcrypt.generate_password_hash("password123").decode("utf-8")
    admin = User(
        username="admin",
        email="admin@mooc.com",
        password_hash=admin_pw,
        full_name="Admin User",
        bio="Platform administrator",
        role="instructor",
        points=1500,
    )
    student = User(
        username="student",
        email="student@mooc.com",
        password_hash=admin_pw,
        full_name="John Student",
        bio="Eager learner",
        role="student",
        points=850,
    )
    db.session.add_all([admin, student])
    db.session.commit()

    # --- Courses ---
    courses_data = [
        {
            "title": "Complete Python Bootcamp",
            "description": "Master Python from basics to advanced topics including OOP, data structures, and web development.",
            "instructor": "Dr. Angela Yu",
            "category": "Programming",
            "difficulty": "Beginner",
            "duration_hours": 42.5,
            "rating": 4.8,
            "students_count": 12500,
            "thumbnail": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600",
        },
        {
            "title": "Machine Learning A-Z",
            "description": "Hands-on ML with Python, scikit-learn, and TensorFlow. Build real-world models.",
            "instructor": "Kirill Eremenko",
            "category": "Data Science",
            "difficulty": "Intermediate",
            "duration_hours": 38.0,
            "rating": 4.7,
            "students_count": 9800,
            "thumbnail": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=600",
        },
        {
            "title": "Web Development Masterclass",
            "description": "Full-stack web development with HTML, CSS, JS, React, Node.js and databases.",
            "instructor": "Brad Traversy",
            "category": "Web Development",
            "difficulty": "Beginner",
            "duration_hours": 55.0,
            "rating": 4.9,
            "students_count": 18200,
            "thumbnail": "https://images.unsplash.com/photo-1547658719-da2b51169166?w=600",
        },
        {
            "title": "Data Structures & Algorithms",
            "description": "Crack coding interviews with deep dives into arrays, trees, graphs, DP and more.",
            "instructor": "Abdul Bari",
            "category": "Programming",
            "difficulty": "Intermediate",
            "duration_hours": 30.0,
            "rating": 4.8,
            "students_count": 7400,
            "thumbnail": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600",
        },
        {
            "title": "Deep Learning Specialization",
            "description": "Neural networks, CNNs, RNNs, and Transformers explained with practical projects.",
            "instructor": "Andrew Ng",
            "category": "Data Science",
            "difficulty": "Advanced",
            "duration_hours": 60.0,
            "rating": 5.0,
            "students_count": 22000,
            "thumbnail": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600",
        },
        {
            "title": "React - The Complete Guide",
            "description": "Build powerful single-page applications with React, Hooks, Redux and Next.js.",
            "instructor": "Maximilian Schwarzmüller",
            "category": "Web Development",
            "difficulty": "Intermediate",
            "duration_hours": 48.0,
            "rating": 4.8,
            "students_count": 15600,
            "thumbnail": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600",
        },
    ]

    for c in courses_data:
        course = Course(**c)
        db.session.add(course)
    db.session.commit()

    # --- Videos for first course ---
    py_course = Course.query.filter_by(title="Complete Python Bootcamp").first()
    video_titles = [
        "Introduction to Python",
        "Variables and Data Types",
        "Control Flow and Loops",
        "Functions and Modules",
        "Object-Oriented Programming",
        "File Handling",
        "Error Handling",
        "Python Standard Library",
    ]
    sample_urls = [
        "https://www.youtube.com/embed/r-uOLxNrNk8",
        "https://www.youtube.com/embed/kqtD5dpn9C8",
        "https://www.youtube.com/embed/6iF8Xb7Z3wQ",
        "https://www.youtube.com/embed/9Os0o3wzS_I",
        "https://www.youtube.com/embed/JeznW_7DlB0",
    ]
    for i, t in enumerate(video_titles):
        v = Video(
            course_id=py_course.id,
            title=t,
            description=f"Lesson {i+1} on {t}.",
            url=sample_urls[i % len(sample_urls)],
            duration=600 + i * 120,
            order=i + 1,
            thumbnail="https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400",
        )
        db.session.add(v)
    db.session.commit()

    # --- Subtitles ---
    first_video = Video.query.filter_by(course_id=py_course.id).first()
    sample_subs = [
        ("Welcome to the course. In this lesson, we will introduce Python.", 0, 8),
        ("Python is a high-level, interpreted programming language.", 8, 16),
        ("It emphasizes code readability and simplicity.", 16, 24),
        ("We will set up the development environment next.", 24, 32),
    ]
    for content, s, e in sample_subs:
        sub = Subtitle(video_id=first_video.id, content=content, start_time=s, end_time=e, language="en")
        db.session.add(sub)
    db.session.commit()

    # --- Assignment ---
    a1 = Assignment(
        course_id=py_course.id,
        title="Build a Calculator",
        description="Create a CLI calculator supporting +, -, *, / operations using functions.",
        due_date=datetime.utcnow() + timedelta(days=7),
        total_marks=100,
    )
    db.session.add(a1)

    # --- Quiz ---
    quiz_questions = [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "func", "define"],
            "answer": 1,
        },
        {
            "question": "What data type is the result of: 3 / 2 in Python 3?",
            "options": ["int", "float", "double", "decimal"],
            "answer": 1,
        },
        {
            "question": "Which of these is a mutable data type?",
            "options": ["tuple", "string", "list", "frozenset"],
            "answer": 2,
        },
        {
            "question": "How do you start a comment in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": 1,
        },
        {
            "question": "Which method adds an item to a list?",
            "options": ["add()", "append()", "insert()", "push()"],
            "answer": 1,
        },
    ]
    import json
    q1 = Quiz(
        course_id=py_course.id,
        title="Python Basics Quiz",
        description="Test your understanding of Python fundamentals.",
        questions=json.dumps(quiz_questions),
        time_limit=600,
    )
    db.session.add(q1)

    # --- Test ---
    test_questions = [
        {
            "question": "Write a function that returns the factorial of n.",
            "options": [],
            "answer": "",
            "type": "subjective",
            "marks": 20,
        },
        {
            "question": "Explain the difference between list and tuple.",
            "options": [],
            "answer": "",
            "type": "subjective",
            "marks": 20,
        },
    ]
    t1 = Test(
        course_id=py_course.id,
        title="Mid-Term Test",
        description="Comprehensive mid-term evaluation.",
        questions=json.dumps(test_questions),
        total_marks=100,
    )
    db.session.add(t1)
    db.session.commit()

    # --- Enrollments ---
    for c in Course.query.all():
        e = Enrollment(user_id=student.id, course_id=c.id, progress=45.0)
        db.session.add(e)
    db.session.commit()

    # --- Discussion ---
    d1 = Discussion(
        user_id=student.id,
        course_id=py_course.id,
        content="How do I install Python on Windows? Is there a recommended IDE?",
        likes=5,
    )
    db.session.add(d1)
    db.session.commit()
    d2 = Discussion(
        user_id=admin.id,
        course_id=py_course.id,
        parent_id=d1.id,
        content="Download from python.org and use VS Code. PyCharm is also great!",
        likes=3,
    )
    db.session.add(d2)
    db.session.commit()

    # --- Certificate ---
    cert = Certificate(
        user_id=student.id,
        course_id=py_course.id,
        certificate_code="CERT-DEMO12345",
    )
    db.session.add(cert)
    db.session.commit()
