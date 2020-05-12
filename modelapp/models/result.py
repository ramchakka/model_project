from typing import List

from db import db
from sqlalchemy.sql import func



class ResultModel(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False, unique=False)
    objname = db.Column(db.String(2048), nullable=False, unique=False,default=None)

    model_id = db.Column(db.Integer, db.ForeignKey("models.id"), nullable=False)
    model = db.relationship("DesignModel")

    time_created = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    saved_by = db.Column(db.String, db.ForeignKey("users.username"), nullable=True)
    saved_user = db.relationship("UserModel",back_populates="result")

    @classmethod
    def find_by_name(cls, name: str) -> "ResultModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id: int) -> "ResultModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List["ResultModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
