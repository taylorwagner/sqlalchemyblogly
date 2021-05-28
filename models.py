import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect db to Flask app"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    """Site user"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.Text,
                     nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of the user"""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first={u.first_name} last={u.last_name} image={u.image_url}>"


class Post(db.Model):
    """Blog posts by users"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text,
                     nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>"


class Tag(db.Model):
    """"""
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text, unique=True,
                     nullable=False)

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"


class PostTag(db.Model):
    """"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)   

    def __repr__(self):
        pt = self
        return f"<PostTag post_id={pt.post_id} tag_id={pt.tag_id}>"