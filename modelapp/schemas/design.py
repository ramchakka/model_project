from ma import ma
from models.design import DesignModel

class DesignSchema(ma.ModelSchema):
    class Meta:
        model = DesignModel
        dump_only = ("id",)
        load_only = ("objname","user")
        include_fk = True
