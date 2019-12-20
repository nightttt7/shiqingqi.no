from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from . import db, login_manager
from markdown import markdown
from datetime import datetime
import bleach



class URL(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    urlname = db.Column(db.String(64), unique=True, index=True)
    url = db.Column(db.String(256))

    def __repr__(self):
        return '<urlname: %r url: %r>' % (self.urlname, self.url)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @staticmethod
    def giveblog(email):
        User.query.filter_by(email=email).first().role = Role.query.filter_by(name='Bloger').first()
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('no password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # return True if has this permission
    # parameter see class Permission
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    # return True if is administrator
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return '<User email: %r username: %r>' % (self.email, self.username)


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Permission:
    # blog access: 1
    # timesheet and keep access: 2
    # administration access: 4
    BLOG = 1
    KEEP = 2
    ADMIN = 4


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    # not need self argument
    # use it when adding new role
    @staticmethod
    def insert_roles():
        roles = {
            'Keeper': [Permission.KEEP],
            'Bloger': [Permission.KEEP, Permission.BLOG],
            'Administrator': [Permission.KEEP, Permission.BLOG, Permission.ADMIN],
        }
        default_role = 'Keeper'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions = self.permissions + perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions = self.permissions - perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        # bitwise and operator: &
        # no worry anyway, it works
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Post.body, 'set', Post.on_changed_body)
