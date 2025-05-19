from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_fname = db.Column(db.String(100), nullable=False)
    user_lname = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_type = db.Column(db.Enum('freelancer', 'client', name='user_type_enum'), nullable=False)
    user_pwd = db.Column(db.String(200), nullable=False)
    first_login = db.Column(db.Boolean, default=True)  # Track first login
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add this relationship
    posted_jobs = db.relationship('Jobs', backref='job_owner', lazy=True)
   
class ClientProfileTable(db.Model):
    __tablename__ = 'client_profile'
    client_profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    hiring_needs = db.Column(db.String(500), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobApplicationsTable(db.Model):
    __tablename__ = 'job_applications_table'
    job_applications_table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jobs_id = db.Column(db.Integer, db.ForeignKey('jobs.jobs_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    proposal = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FreelancerProfileTable(db.Model):
    __tablename__ = 'freelancer_profile_table'
    freelancer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    job_title = db.Column(db.String(500), nullable=False)
    skills = db.Column(db.String(500), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    about_me = db.Column(db.String(500), nullable=True)
    average_rating = db.Column(db.Float, nullable=False, default=0.0)
    reviews_count = db.Column(db.Integer, nullable=False, default=0)
    portfolio = db.Column(db.String(500), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='freelancer_profile_table', lazy=True)
class Messages(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Enum('pending', 'read', 'failed', name='message_status_enum'), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Reviews(db.Model):
    __tablename__ = 'reviews'
    reviews_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jobs_id = db.Column(db.Integer, db.ForeignKey('jobs.jobs_id'), nullable=False)
    reviewer_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    reviewee_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Jobs(db.Model):
    __tablename__ = 'jobs'
    jobs_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('pending', 'success', 'failed', name='job_status_enum'), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to the User model
    client = db.relationship('User', backref='jobs', lazy=True)


class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # One participant
    user2_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Other participant
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



class Notifications(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)  # Recipient of the notification
    content = db.Column(db.Text, nullable=False)  # Notification message
    is_read = db.Column(db.Boolean, default=False)  # Track if the notification has been read
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for the notification