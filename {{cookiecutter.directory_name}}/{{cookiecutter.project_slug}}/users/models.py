from {{ cookiecutter.project_slug }}.base.models import BaseModel
from {{ cookiecutter.project_slug }}.extensions import db, bcrypt
from {{ cookiecutter.project_slug }}.uploads import avatar_set


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(
        "email",
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )
    username = db.Column(
        "username",
        db.String(32),
        unique=True,
        nullable=False,
        index=True
    )
    password = db.Column(
        "password",
        db.String(255),
        nullable=False
    )
    avatar = db.Column(
        "avatar",
        db.String(255),
        default="default.jpg",
        required=True
    )
    is_active = db.Column(
        "is_active",
        db.Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return "<User %s>" % self.id

    @property
    def avatar_url(self):
        """
        returns an avatar URL for the user 
        instance, based on their avatar hash.
        """
        return avatar_set.url(self.avatar)


    def set_password(self, password: str):
        """
        sets a hashed version of the provided
        password on the user instance.
        """
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password: str):
        """
        returns whether the provided password
        matches the user's password hash.
        """
        return bcrypt.check_password_hash(
            password=password,
            pw_hash=self.password
        )

    def inactivate(self):
        """
        sets the `is_active` flag to false on 
        the user instance This should generally be 
        used as an alternative to hard deletes.
        """
        self.is_active = False
        self.save()
