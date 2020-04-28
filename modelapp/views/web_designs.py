from flask import Blueprint, request, session, url_for, render_template, redirect,flash,current_app,send_from_directory
#from resources.user import  User, UserModel
#from schemas.user import UserSchema
from schemas.design import DesignSchema
from models import requires_login, DesignModel
from werkzeug.security import safe_str_cmp
from flask_uploads import UploadNotAllowed
from libs import image_helper
import os
import datetime
import logging
import traceback

logger = logging.getLogger()
webmodel_blueprint = Blueprint('webmodels', __name__)
design_schema = DesignSchema()
design_list_schema = DesignSchema(many=True)



@webmodel_blueprint.route("/new", methods=["GET", "POST"])
@requires_login
def create_model():
    if request.method == "POST":

        if 'file1' not in request.files:
            return "Missing file part"

        file1 = request.files['file1']
        name = file1.filename
        if DesignModel.find_by_name(name):
            return "Model already exists with name. Try another name"

        try:
            username = session['username']
            folder = f"user_{username}"
            image_path = image_helper.save_image(file1, folder=os.path.join(folder))
            logger.info(image_path)
            basename = image_helper.get_basename(image_path)
            logger.info(basename)
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(file1)
            return  f"Unable to upload the extension {extension}"

        design = DesignModel(name=name,username=session['username'],objname=image_path)
        try:
            design.save_to_db()
        except:
            return "Error creating model"

        return redirect(url_for(".index"))

    return render_template("models/new_model.html")

@webmodel_blueprint.route("/")
@requires_login
def index():
    models = DesignModel.find_by_username(session["username"])
    #print(design_list_schema.dump(models))
    return render_template("models/index.html", models=design_list_schema.dump(models))

@webmodel_blueprint.route("/edit/<string:model_id>", methods=["GET", "POST"])
@requires_login
def edit_model(model_id):
    if request.method == "POST":
        name = request.form['name']
        model = DesignModel.find_by_id(model_id)
        model.name = name
        try:
            model.save_to_db()
        
        except:
            flash('Error renaming model', 'danger')
            #return "Error renaming model"

        return redirect(url_for(".index"))
        
    # What happens if it's a GET request
    return render_template("models/edit_model.html", model=DesignModel.find_by_id(model_id))

@webmodel_blueprint.route("/delete/<string:model_id>")
@requires_login
def delete_model(model_id):
    model = DesignModel.find_by_id(model_id)
    if model.username == session["username"]:
        model.delete_from_db()
    try:
        uploads = os.path.join( current_app.config['UPLOADED_FILES_DEST'])
        os.remove(os.path.join(uploads,model.objname))
    except:
        traceback.print_exc()
        return "File deletion failed"

    return redirect(url_for(".index"))


@webmodel_blueprint.route("/download/<string:model_id>")
@requires_login
def download_file(model_id):

    model = DesignModel.find_by_id(model_id)
    try:
        uploads = os.path.join( current_app.config['UPLOADED_FILES_DEST'], os.path.dirname(model.objname))
        return send_from_directory(directory=uploads, filename=os.path.basename(model.objname),attachment_filename=model.name,as_attachment=True)
    except:
        traceback.print_exc()
        return "File not found!"

    return redirect(url_for(".index",model_id=model_id))