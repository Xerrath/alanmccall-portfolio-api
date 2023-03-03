import psycopg2
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from flask_cors import CORS
from config import Config
from datetime import datetime, timedelta
from sqlalchemy import Sequence, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from functools import wraps
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from dotenv import load_dotenv
import base64
import bleach
import jwt
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qcbcnrbhulehyi:c355f1b32340ef3d79a76e5d3e762aed70541c7ef57b8c6a0e045533f7e95106@ec2-3-230-122-20.compute-1.amazonaws.com:5432/dgo054b79rigd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# directory = 'https://127.0.0.1:5000'


# Classes
class AdminUser(db.Model):
    admin_id = db.Column(db.Integer, Sequence(
        'admin_id_seq'), primary_key=True)
    admin_name = db.Column(db.String(180), nullable=False)
    admin_email = db.Column(db.String(240), unique=True, nullable=False)
    admin_pw = db.Column(db.String, nullable=False)
    project = db.relationship('Project', backref=db.backref(
        'admin_user', lazy=True), cascade='all, delete, delete-orphan')
    blog = db.relationship('Blog', backref=db.backref(
        'admin_user', lazy=True), cascade='all, delete, delete-orphan')
    users = db.relationship('Users', backref=db.backref(
        'admin_user', lazy=True), cascade='all, delete, delete-orphan')
    testimonial = db.relationship('Testimonial', backref=db.backref(
        'admin_user', lazy=True), cascade='all, delete, delete-orphan')

    def __init__(self, admin_name, admin_email, admin_pw):
        self.admin_name = admin_name
        self.admin_email = admin_email
        self.admin_pw = admin_pw


class Project(db.Model):
    project_id = db.Column(db.Integer, Sequence(
        'project_id_seq'), primary_key=True)
    project_thumb_img = db.Column(db.LargeBinary, nullable=True)
    project_logo_img = db.Column(db.LargeBinary, nullable=True)
    project_hero_img = db.Column(db.LargeBinary, nullable=True)
    project_title = db.Column(db.String(80), nullable=False)
    project_language = db.Column(db.String(120), nullable=True)
    project_development_type = db.Column(db.String(60), nullable=True)
    project_description = db.Column(db.Text, nullable=False)
    project_url = db.Column(db.String(240), nullable=True)
    project_admin_id = db.Column(db.Integer, ForeignKey(
        'admin_user.admin_id'), nullable=False)

    def __init__(self, project_thumb_img, project_logo_img, project_hero_img, project_title, project_language, project_development_type, project_description, project_url, project_admin_id):
        self.project_thumb_img = project_thumb_img
        self.project_logo_img = project_logo_img
        self.project_hero_img = project_hero_img
        self.project_title = project_title
        self.project_language = project_language
        self.project_development_type = project_development_type
        self.project_description = project_description
        self.project_url = project_url
        self.project_admin_id = project_admin_id


class Blog(db.Model):
    blog_id = db.Column(db.Integer, Sequence('blog_id_seq'), primary_key=True)
    blog_thumb_img = db.Column(db.LargeBinary, nullable=True)
    blog_hero_img = db.Column(db.LargeBinary, nullable=True)
    blog_title = db.Column(db.String(240), nullable=False)
    blog_contents = db.Column(db.Text, nullable=False)
    blog_date = db.Column(db.Date, nullable=False)
    blog_admin_id = db.Column(db.Integer, ForeignKey(
        'admin_user.admin_id'), nullable=False)

    def __init__(self, blog_thumb_img, blog_hero_img, blog_title, blog_contents, blog_date, blog_admin_id):
        self.blog_thumb_img = blog_thumb_img
        self.blog_hero_img = blog_hero_img
        self.blog_title = blog_title
        self.blog_contents = blog_contents
        self.blog_date = blog_date
        self.blog_admin_id = blog_admin_id


class Users(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    user_email = db.Column(db.String(240), unique=True, nullable=False)
    user_pw = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String(180), nullable=False)
    user_url = db.Column(db.String(240), nullable=True, default='N/A')
    user_admin_id = db.Column(db.Integer, ForeignKey(
        'admin_user.admin_id'), nullable=False)
    testimonial = db.relationship('Testimonial', backref=db.backref(
        'users', lazy=True), cascade='all, delete, delete-orphan')

    def __init__(self, user_email, user_pw, user_name, user_url, user_admin_id):
        self.user_email = user_email
        self.user_pw = user_pw
        self.user_name = user_name
        self.user_url = user_url
        self.user_admin_id = user_admin_id


class Testimonial(db.Model):
    testimonial_id = db.Column(db.Integer, Sequence(
        'testimonial_id_seq'), primary_key=True)
    testimonial_review = db.Column(db.Text, nullable=False)
    testimonial_published = db.Column(
        db.Boolean, nullable=False, default=False)
    testimonial_id_users = db.Column(db.Integer, ForeignKey('users.user_id'))
    testimonial_admin_id = db.Column(
        db.Integer, ForeignKey('admin_user.admin_id'))

    def __init__(self, testimonial_review, testimonial_published, testimonial_id_users, testimonial_admin_id):
        self.testimonial_review = testimonial_review
        self.testimonial_published = testimonial_published
        self.testimonial_id_users = testimonial_id_users
        self.testimonial_admin_id = testimonial_admin_id


# Schemas
class AdminUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AdminUser

    admin_id = fields.Integer(dump_only=True)
    admin_name = fields.String(required=True)
    admin_email = fields.String(required=True)
    admin_pw = fields.String(required=True, load_only=True)


admin_user_schema = AdminUserSchema()
multiple_admin_user_schema = AdminUserSchema(many=True)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    admin_relation = ma.Nested(admin_user_schema)
    project_admin_id = ma.auto_field()

    class Meta:
        model = Project


project_schema = ProjectSchema()
multiple_project_schema = ProjectSchema(many=True)


class BlogSchema(ma.SQLAlchemyAutoSchema):
    admin_relation = ma.Nested(admin_user_schema)
    blog_admin_id = ma.auto_field()

    class Meta:
        model = Blog


blog_schema = BlogSchema()
multiple_blog_schema = BlogSchema(many=True)


class UsersSchema(ma.SQLAlchemySchema):
    admin_relation = ma.Nested(admin_user_schema)
    user_admin_id = ma.auto_field()

    class Meta:
        model = Users

    user_id = fields.Integer(dump_only=True)
    user_email = fields.String(required=True)
    user_pw = fields.String(required=True, load_only=True)
    user_name = fields.String(required=True)
    user_url = fields.String(required=True)
    user_admin_id = fields.Integer(required=True)


users_schema = UsersSchema()
multiple_users_schema = UsersSchema(many=True)


class TestimonialSchema(ma.SQLAlchemyAutoSchema):
    user_relation = ma.Nested(users_schema)
    admin_relation = ma.Nested(admin_user_schema)
    testimonial_id_users = ma.auto_field()
    testimonial_admin_id = ma.auto_field()

    class Meta:
        model = Testimonial


testimonial_schema = TestimonialSchema()
multiple_testimonial_schema = TestimonialSchema(many=True)


def create_tables():
    with app.app_context():
        db.create_all()

# --------------------------------
# Settings (headers, or middleware)
# --------------------------------


def set_headers_post(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Admin_Authorization')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, User_Authorization')

    return response


def set_headers_get(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Admin_Authorization')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, User_Authorization')
    return response


def set_headers_delete(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'DELETE')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Admin_Authorization')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, User_Authorization')
    return response


# Endpoints

# --------------------------------------
# Admin Routes
# --------------------------------------

@app.route('/admin', methods=['GET'])
def get_all_admin_users():
    all_admin_users = db.session.query(AdminUser).all()

    response = jsonify(multiple_admin_user_schema(all_admin_users))

    return set_headers_get(response)


@app.route('/admin/add', methods=['POST'])
def add_admin_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    admin_name = post_data.get('username')
    admin_email = post_data.get('email')
    admin_pw = post_data.get('pw')

    admin_user_email_duplicate = db.session.query(AdminUser).filter(
        AdminUser.admin_email == admin_email).first()

    if admin_user_email_duplicate is not None:
        return jsonify("Error: The user is already registered.")

    encrypted_password = bcrypt.generate_password_hash(
        admin_pw).decode('utf-8')
    new_admin_user = AdminUser(admin_name, admin_email, encrypted_password)

    db.session.add(new_admin_user)
    db.session.commit()

    response = jsonify(admin_user_schema.dump(new_admin_user))
    return set_headers_post(response)


@app.route('/admin/delete/<admin_id>', methods=['DELETE'])
def delete_admin_user(id):
    admin_user = db.session.query(AdminUser).filter(
        AdminUser.admin_id == id).first()
    db.session.delete(AdminUser)
    db.session.commit()

    response = jsonify('The slected Admin has been deleted')

    return set_headers_delete(response)

# --------------------------------------
# Blog Routes
# --------------------------------------


@app.route('/get/blogs', methods=['GET'])
def get_all_blgos():
    all_blogs = db.session.query(Blog).all()

    response = jsonify(multiple_blog_schema.dump(all_blogs))

    return set_headers_get(response)


@app.route('/get/blogs/by/<int:blog_admin_id>',  methods=['GET'])
def get_all_blogs_by_relation(blog_admin_id):
    all_blogs = Blog.query.filter_by(blog_admin_id=blog_admin_id).all()
    blogs_filter = multiple_blog_schema.dump(all_blogs)

    response = jsonify(blogs_filter)

    return set_headers_get(response)


@app.route('/blog/add', methods=['POST'])
def add_blog():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    blog_thumb_img = post_data.get('thumb_img')
    blog_hero_img = post_data.get('hero_img')
    blog_title = post_data.get('title')
    blog_contents = post_data.get('contents')
    blog_date = post_data.get('date')
    blog_admin_id = post_data.get('admin_auth')
    
    if blog_thumb_img is not None:
        thumb_image_data = bytes(blog_thumb_img)
        thumb_image_str = base64.b64encode(thumb_image_data).decode('utf-8')
        thumb_image_bytes = thumb_image_str.encode('utf-8')
    else:
        blog_thumb_img = None
        thumb_image_str = None
        thumb_image_bytes = None

    if blog_hero_img is not None:
        hero_image_data = bytes(blog_hero_img)
        hero_image_str = base64.b64encode(hero_image_data).decode('utf-8')
        hero_image_bytes = hero_image_str.encode('utf-8')
    else:
        blog_hero_img = None
        hero_image_str = None
        hero_image_bytes = None

    new_blog = Blog(blog_thumb_img=thumb_image_bytes, blog_hero_img=hero_image_bytes,
                    blog_title=blog_title, blog_contents=blog_contents, blog_date=blog_date, blog_admin_id=blog_admin_id)

    db.session.add(new_blog)
    db.session.commit()

    response = jsonify(blog_schema.dump(add_blog))

    return set_headers_post(response)


@app.route('/blog/edit/<int:id>', methods=['POST'])
def edit_blog_by_id(id):

    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    blog = Blog.query.get(id)

    post_data = request.get_json()
    blog_thumb_img = post_data.get('updated_thumb_img')
    blog_hero_img = post_data.get('updated_hero_img')
    blog_title = post_data.get('updated_title')
    blog_contents = post_data.get('updated_content')
    blog_date = post_data.get('updated_blog_date')
    blog_admin_id = post_data.get('admin_auth')

    if blog_thumb_img is not None:
        thumb_image_data = bytes(blog_thumb_img)
        thumb_image_str = base64.b64encode(thumb_image_data).decode('utf-8')
        thumb_image_bytes = thumb_image_str.encode('utf-8')
    else:
        blog_thumb_img = None
        thumb_image_str = None
        thumb_image_bytes = None

    if blog_hero_img is not None:
        hero_image_data = bytes(blog_hero_img)
        hero_image_str = base64.b64encode(hero_image_data).decode('utf-8')
        hero_image_bytes = hero_image_str.encode('utf-8')
    else:
        blog_hero_img = None
        hero_image_str = None
        hero_image_bytes = None

    if blog:
        blog.blog_thumb_img = thumb_image_bytes
        blog.blog_hero_img = hero_image_bytes
        blog.blog_title = blog_title
        blog.blog_date = blog_date
        blog.blog_contents = blog_contents
        blog.blog_admin_id = blog_admin_id

        db.session.commit()
        response = jsonify(blog_schema.dump(blog))
        return set_headers_post(response)

    else:
        response = jsonify('Blog was not found.')
        return set_headers_post(response)


@app.route('/blog/<int:id>',  methods=['GET'])
def get_blog__by_id(id):
    blog = db.session.query(Blog).filter(Blog.blog_id == id).first()

    response = jsonify(blog_schema.dump(blog))

    return set_headers_get(response)


@app.route('/blog/delete/<id>', methods=['DELETE'])
def delete_blog_by_id(id):
    blog = db.session.query(Blog).filter(Blog.blog_id == id).first()
    db.session.delete(blog)
    db.session.commit()

    response = jsonify("The selected blog has been deleted")

    return set_headers_delete(response)
# --------------------------------------
# Project Routes
# --------------------------------------


@app.route('/get/projects', methods=['GET'])
def get_all_projects():
    all_projects = db.session.query(Project).all()

    response = jsonify(multiple_project_schema.dump(all_projects))

    return set_headers_get(response)


@app.route('/get/projects/by/<int:project_admin_id>',  methods=['GET'])
def get_all_projects_by_relation(project_admin_id):
    all_projects = Project.query.filter_by(
        project_admin_id=project_admin_id).all()

    response = jsonify(multiple_project_schema.dump(all_projects))

    return set_headers_get(response)


@app.route('/project/edit/<int:project_id>', methods=['POST'])
def edit_project_by_id(project_id):

    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    project = Project.query.get(project_id)

    post_data = request.get_json()
    project_thumb_img = post_data.get('updated_thumb_img')
    project_logo_img = post_data.get('updated_logo_img')
    project_hero_img = post_data.get('updated_hero_img')
    project_title = post_data.get('updated_title')
    project_language = post_data.get('updated_language')
    project_development_type = post_data.get('updated_development_type')
    project_description = post_data.get('updated_description')
    project_url = post_data.get('updated_url')

    if project_thumb_img is not None:
        thumb_image_data = bytes(project_thumb_img)
        thumb_image_str = base64.b64encode(thumb_image_data).decode('utf-8')
        thumb_image_bytes = thumb_image_str.encode('utf-8')
    else:
        project_thumb_img = None
        thumb_image_str = None
        thumb_image_bytes = None

    if project_logo_img is not None:
        logo_image_data = bytes(project_logo_img)
        logo_image_str = base64.b64encode(logo_image_data).decode('utf-8')
        logo_image_bytes = logo_image_str.encode('utf-8')
    else:
        project_logo_img = None
        logo_image_str = None
        logo_image_bytes = None

    if project_hero_img is not None:
        hero_image_data = bytes(project_hero_img)
        hero_image_str = base64.b64encode(hero_image_data).decode('utf-8')
        hero_image_bytes = hero_image_str.encode('utf-8')
    else:
        project_hero_img = None
        hero_image_str = None
        hero_image_bytes = None

    if project:
        project.project_thumb_img = thumb_image_bytes
        project.project_logo_img = logo_image_bytes
        project.project_hero_img = hero_image_bytes
        project.project_title = project_title
        project.project_language = project_language
        project.project_development_type = project_development_type
        project.project_description = project_description
        project.project_url = project_url

        db.session.commit()
        response = jsonify(project_schema.dump(project))
        return set_headers_post(response)

    else:
        response = jsonify('Project was not found.')
        return set_headers_post(response)


@app.route('/project/<id>', methods=['GET'])
def get_project_by_id(id):
    project = db.session.query(Project).filter(
        Project.project_id == id).first()

    response = jsonify(project_schema.dump(project))

    return set_headers_get(response)


@app.route('/project/delete/<project_id>', methods=['DELETE'])
def delete_project_by_id(project_id):
    project = db.session.query(Project).filter(
        Project.project_id == project_id).first()
    db.session.delete(project)
    db.session.commit()

    response = jsonify("The selected project has been deleted")

    return set_headers_delete(response)


@app.route('/project/add', methods=['POST'])
def add_project():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    project_thumb_img = post_data.get('thumb_img')
    project_logo_img = post_data.get('logo_img')
    project_hero_img = post_data.get('hero_img')
    project_title = post_data.get('title')
    project_language = post_data.get('language')
    project_development_type = post_data.get('development_type')
    project_description = post_data.get('description')
    project_url = post_data.get('url')
    project_admin_id = post_data.get('admin_auth')

    if project_thumb_img is not None:
        thumb_image_data = bytes(project_thumb_img)
        thumb_image_str = base64.b64encode(thumb_image_data).decode('utf-8')
        thumb_image_bytes = thumb_image_str.encode('utf-8')
    else:
        project_thumb_img = None
        thumb_image_str = None
        thumb_image_bytes = None

    if project_logo_img is not None:
        logo_image_data = bytes(project_logo_img)
        logo_image_str = base64.b64encode(logo_image_data).decode('utf-8')
        logo_image_bytes = logo_image_str.encode('utf-8')
    else:
        project_logo_img = None
        logo_image_str = None
        logo_image_bytes = None

    if project_hero_img is not None:
        hero_image_data = bytes(project_hero_img)
        hero_image_str = base64.b64encode(hero_image_data).decode('utf-8')
        hero_image_bytes = hero_image_str.encode('utf-8')
    else:
        project_hero_img = None
        hero_image_str = None
        hero_image_bytes = None

    new_project = Project(thumb_image_bytes, logo_image_bytes, hero_image_bytes, project_title,
                          project_language, project_development_type, project_description, project_url, project_admin_id)

    db.session.add(new_project)
    db.session.commit()

    response = jsonify(project_schema.dump(new_project))

    return set_headers_post(response)

# --------------------------------------
# Users Routes
# --------------------------------------


@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = db.session.query(Users).all()

    response = jsonify(multiple_users_schema.dump(all_users))

    return set_headers_get(response)


@app.route('/get/all/users/<int:user_admin_id>', methods=['GET'])
def get_all_users_by_admin_relation(user_admin_id):
    all_users = Users.query.filter_by(user_admin_id=user_admin_id).all()

    response = jsonify(multiple_users_schema.dump(all_users))

    return set_headers_get(response)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = Users.query.get(user_id)

    response = jsonify(users_schema.dump(user))

    return set_headers_get(response)


@app.route('/users/edit/<int:user_id>', methods=['POST'])
def edit_user_by_id(user_id):

    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    user = Users.query.get(user_id)

    post_data = request.get_json()
    user_email = post_data.get('updated_email')
    user_pw = post_data.get('updated_pw')
    user_name = post_data.get('updated_username')
    user_url = post_data.get('updated_url')

    if ((db.session.query(Users).filter(Users.user_email == user_email).count()) > 1):
        return jsonify("Error: The user email is already in use.")

    encrypted_password = bcrypt.generate_password_hash(user_pw).decode('utf-8')

    if user:
        user.user_email = user_email
        user.user_pw = encrypted_password
        user.user_name = user_name
        user.user_url = user_url

        db.session.commit()
        response = jsonify(users_schema.dump(user))
        return set_headers_post(response)
    else:
        response = jsonify('User was not found.')
        return set_headers_post(response)


@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    response = ('The selected user has been deleted')

    return response


@app.route('/user/add', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    user_email = post_data.get('email')
    user_pw = post_data.get('pw')
    user_name = post_data.get('username')
    user_url = post_data.get('url')
    user_admin_id = post_data.get('adminAuth')

    user_email_duplicate = db.session.query(Users).filter(
        Users.user_email == user_email).first()

    if user_email_duplicate is not None:
        return jsonify("Error: The user already registered.")

    encrypted_password = bcrypt.generate_password_hash(user_pw).decode('utf-8')
    new_user = Users(user_email, encrypted_password,
                     user_name, user_url, user_admin_id)

    db.session.add(new_user)
    db.session.commit()

    response = jsonify(users_schema.dump(new_user))

    return set_headers_post(response)

# --------------------------------------
# Testimonial Routes
# --------------------------------------


@app.route('/get/testimonials/by/admin/relation/<int:id>', methods=['GET'])
def get_all_testimonials_related_to_admin(id):
    all_testimonials = Testimonial.query.filter(
        Testimonial.testimonial_admin_id == id).all()

    response = jsonify(multiple_testimonial_schema.dump(all_testimonials))

    return set_headers_get(response)


@app.route('/testimonial/publish/<int:id>', methods=['POST'])
def edit_testimonial_by_id(id):

    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    testimonial = Testimonial.query.get(id)

    post_data = request.get_json()
    testimonial_review = post_data.get('review')
    testimonial_published = post_data.get('publish')
    testimonial_id_users = post_data.get('user_id')
    testimonial_admin_id = post_data.get('admin_id')

    if testimonial:
        testimonial.testimonial_review = testimonial_review
        testimonial.testimonial_published = testimonial_published
        testimonial.testimonial_id_users = testimonial_id_users
        testimonial.testimonial_admin_id = testimonial_admin_id

        db.session.commit()
        response = jsonify(testimonial_schema.dump(testimonial))
        return set_headers_post(response)
    else:
        response = jsonify('Testimonial was not found.')
        return set_headers_post(response)


@app.route('/get/testimonials/by/user/relation/<int:testimonial_id_users>', methods=['GET'])
def get_all_testimonials_by_user(testimonial_id_users):
    all_testimonials = Testimonial.query.filter_by(
        testimonial_id_users=testimonial_id_users).all()

    response = jsonify(multiple_testimonial_schema(all_testimonials))

    return set_headers_get(response)


@app.route('/testimonial/<int:id>', methods=['GET'])
def get_testimonial_by_id(id):
    testimonial = db.session.query(Testimonial).filter(
        Testimonial.testimonial_id == id).first()

    response = jsonify(testimonial_schema.dump(testimonial))

    return set_headers_get(response)


@app.route('/testimonial/delete/<id>', methods=['DELETE'])
def delete_testimony_by_id(id):
    testimonial = db.session.query(Testimonial).filter(
        Testimonial.testimonial_id == id).first()
    db.session.delete(testimonial)
    db.session.commit()

    response = ('The selected Testimony has been deleted')

    return response


@app.route('/testimonial/add', methods=['POST'])
def add_testimonial():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    testimonial_review = post_data.get('review')
    testimonial_published = post_data.get('publish')
    testimonial_id_users = post_data.get('user_id')
    testimonial_admin_id = post_data.get('admin_id')

    new_testimonial = Testimonial(testimonial_review=testimonial_review, testimonial_published=testimonial_published,
                                  testimonial_id_users=testimonial_id_users, testimonial_admin_id=testimonial_admin_id)

    db.session.add(new_testimonial)
    db.session.commit()

    response = jsonify(testimonial_schema.dump(new_testimonial))

    return set_headers_post(response)


# --------------------------------------
# Login Routes
# --------------------------------------

@app.route('/log/verify/user', methods=["POST"])
def verifyUser():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    email = post_data.get('email')
    pw = post_data.get('pw')

    user = db.session.query(Users).filter(Users.user_email == email).first()

    if request.headers.get("User_Authorization") != "Bearer null":
        try:
            user_token = request.headers.get(
                "User_Authorization").split(" ")[1]
            secret = app.config["SECRET_KEY"]
            payload = jwt.decode(user_token, secret, algorithms=["HS256"])
            email = payload["email"]
            user = db.session.query(Users).filter(
                Users.user_email == email).first()

            if user:
                user_logged_in = "USER"
                user_id = user.user_id
                response = jsonify({"message": "USER is Logged in", 'data': payload,
                                   "user_logged_in": user_logged_in, "user_id": user_id})
                return set_headers_post(response)

            else:
                response = jsonify({"error": "Problem with the user_token."})
                return set_headers_post(response)

        except jwt.ExpiredSignatureError:
            response = jsonify({"error": "user_token has expired!"})
            return set_headers_post(response)

        except jwt.InvalidTokenError:
            if user is None:
                response = jsonify({"error": "Not logged in!"})
                return set_headers_post(response)

            elif not bcrypt.check_password_hash(admin_user.admin_pw, pw):
                response = jsonify({"error": "Password does not match!"})
                return set_headers_post(response)

            else:
                payload = {"email": email}
                secret = app.config["SECRET_KEY"]
                user_token = jwt.encode(payload, secret, algorithm="HS256")
                response = jsonify(
                    {'user_token': user_token, 'data': users_schema.dump(user)})
                return set_headers_post(response)

    elif request.headers.get("User_Authorization") == "Bearer null":
        if user is None:
            response = jsonify("User is NOT verified")
            return set_headers_post(response)

        elif not bcrypt.check_password_hash(user.user_pw, pw):
            response = jsonify({"error": "Password does not match!"})
            return set_headers_post(response)

        else:
            user_logged_in = "USER"
            user_id = user.user_id
            payload = {"email": email}
            secret = app.config["SECRET_KEY"]
            user_token = jwt.encode(payload, secret, algorithm="HS256")
            response = jsonify({'user_token': user_token, 'data': users_schema.dump(
                user), 'user_logged_in': user_logged_in, 'user_id': user_id})
            return set_headers_post(response)

    response = jsonify(users_schema.dump(user))
    return set_headers_post(response)


@app.route('/log/verify/admin', methods=["POST"])
def verifyAdmin():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    email = post_data.get('email')
    pw = post_data.get('pw')

    admin_user = db.session.query(AdminUser).filter(
        AdminUser.admin_email == email).first()

    if request.headers.get("Admin_Authorization") != "Bearer null":
        try:
            admin_token = request.headers.get(
                "Admin_Authorization").split(" ")[1]
            secret = app.config["SECRET_KEY"]
            payload = jwt.decode(admin_token, secret, algorithms=["HS256"])
            email = payload["email"]
            admin_user = db.session.query(AdminUser).filter(
                AdminUser.admin_email == email).first()

            if admin_user:
                admin_logged_in = "ADMIN"
                admin_auth_id = admin_user.admin_id
                response = jsonify({"message": "Admin is Logged in", 'data': payload,
                                   "admin_logged_in": admin_logged_in, "admin_auth_id": admin_auth_id})
                return set_headers_post(response)

            else:
                response = jsonify({"error": "Problem with the admin_token."})
                return set_headers_post(response)

        except jwt.ExpiredSignatureError:
            response = jsonify({"error": "admin_token has expired!"})
            return set_headers_post(response)

        except jwt.InvalidTokenError:
            if admin_user is None:
                response = jsonify({"error": "Not logged in!"})
                return set_headers_post(response)

            elif not bcrypt.check_password_hash(admin_user.admin_pw, pw):
                response = jsonify({"error": "Password does not match!"})
                return set_headers_post(response)

            else:
                payload = {"email": email}
                secret = app.config["SECRET_KEY"]
                admin_token = jwt.encode(payload, secret, algorithm="HS256")
                response = jsonify(
                    {'admin_token': admin_token, 'data': admin_user_schema.dump(admin_user)})
                return set_headers_post(response)

    elif request.headers.get("Admin_Authorization") == "Bearer null":
        if admin_user is None:
            response = jsonify('Admin is NOT verified')
            return set_headers_post(response)

        elif not bcrypt.check_password_hash(admin_user.admin_pw, pw):
            response = jsonify({"error": "Password does not match!"})
            return set_headers_post(response)

        else:
            admin_logged_in = "ADMIN"
            admin_auth_id = admin_user.admin_id
            payload = {"email": email}
            secret = app.config["SECRET_KEY"]
            admin_token = jwt.encode(payload, secret, algorithm="HS256")
            response = jsonify({'admin_token': admin_token, 'data': admin_user_schema.dump(
                admin_user), 'admin_logged_in': admin_logged_in, 'admin_auth_id': admin_auth_id})
            return set_headers_post(response)

    response = jsonify(users_schema.dump(admin_user))
    return set_headers_post(response)


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
