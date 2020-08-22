# API for user authenticated endpoints
# Note: none of these endpoints should have a user_id or user_email parameter passed in via the request.
# the user_id and user_email is obtained from the JWT, if valid
import io
import json
import logging
from datetime import datetime as dt

import numpy as np
import pytz
import shortuuid
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from core.auth.decorators import user_only
from core.models import Users, StudiesUsers, Studies

tz = pytz.timezone("Europe/London")
user_api = Blueprint("user_api", __name__)
logger = logging.getLogger(__name__)


# An example user authenticated endpoint.
@user_api.route("/user", methods=["GET"])
@user_only
def get_user(user_id, user_email):
    return jsonify(user_id)

@user_api.route('/user/studies')
@user_only
def get_user_studies(user_id, user_email):
    # user = Users.get(id=user_id)

    query = (Studies.select()
        .join(StudiesUsers)
        .join(Users)
        .where(Users.id == user_id))

    print(query)

    items = [model_to_dict(study) for study in query]
    return jsonify(items)

@user_api.route("/enroll", methods=["POST"])
@user_only
def enroll(user_id, user_email):
    study_id = request.json["study_id"]

    if StudiesUsers.select().where(StudiesUsers.user_id == user_id).where(StudiesUsers.study_id == study_id):
        return 'match'
    else:
        StudiesUsers.create(user_id=user_id, study_id=study_id)

        return jsonify({"study added successfully!"})
    # return jsonify(model_to_dict(user))
    return jsonify(study_id)


@user_api.route("/enroll/remove", methods=["POST"])
@user_only
def unenroll(user_id, user_email):
    study_id = request.json["study_id"]

    studies_users = StudiesUsers.select().where(StudiesUsers.user_id == user_id).where(StudiesUsers.study_id == study_id).first()
    studies_users.delete_instance()

    return jsonify('successfully removed study'), 200