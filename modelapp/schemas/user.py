from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:  
        #load_instance = True
        #include_relationships = True
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

