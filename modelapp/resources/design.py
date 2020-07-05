from flask_restful import Resource
from models.user import UserModel
from models.design import DesignModel
from schemas.design import DesignSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


NAME_ALREADY_EXISTS = "A model with name '{}' already exists."
ERROR_INSERTING = "An model occurred while inserting the model."
DESIGN_NOT_FOUND = "Model not found."
DESIGN_DELETED = "Model deleted."

design_schema = DesignSchema()
design_list_schema = DesignSchema(many=True)


class Design(Resource):
    @classmethod
    def get(cls, name: str):
        design = DesignModel.find_by_name(name)
        if design:
            return design_schema.dump(design), 200

        return {"message": DESIGN_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if DesignModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        design = DesignModel(name=name)
        try:
            design.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return design_schema.dump(design), 201

    @classmethod
    def delete(cls, name: str):
        design = DesignModel.find_by_name(name)
        if design:
            design.delete_from_db()
            return {"message": DESIGN_DELETED}, 200

        return {"message": DESIGN_NOT_FOUND}, 404


class DesignList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        #return {"models": design_list_schema.dump(DesignModel.find_all())}, 200
        username = UserModel.find_by_id(get_jwt_identity()).username
        return {"models": design_list_schema.dump(DesignModel.find_all_by_username(username))}, 200
        