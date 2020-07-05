from typing import List

from db import db
from sqlalchemy.sql import func



class DesignModel(db.Model):
    __tablename__ = "models"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False, unique=False)
    objname = db.Column(db.String(2048), nullable=False, unique=False,default=None)

    username = db.Column(db.String, db.ForeignKey("users.username"), nullable=True)
    user = db.relationship("UserModel",back_populates="design")
    
    time_created = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    results = db.relationship("ResultModel", lazy="dynamic")

    @classmethod
    def find_by_name(cls, name: str) -> "DesignModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_username(cls, username: str) -> "DesignModel":
        return cls.query.filter_by(username=username)
    
    @classmethod
    def find_by_designname_and_username(cls, dname: str, uname: str) -> "DesignModel":
        return cls.query.filter_by(name=dname,username=uname).first()


    @classmethod
    def find_by_id(cls, id: int) -> "DesignModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List["DesignModel"]:
        return cls.query.all()
    
    @classmethod
    def find_all_by_username(cls,uname: str) -> List["DesignModel"]:
        return cls.query.filter_by(username=uname)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
