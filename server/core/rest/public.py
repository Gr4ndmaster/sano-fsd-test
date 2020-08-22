# API for public endpoints
# Note: think carefully before putting anything in here...
# ...anyone will have access to data exposed from these endpoints

import json
import logging
import zlib
from time import sleep, time

import peewee
import stripe
from dateutil.parser import parse
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request

from core.auth.store import auth_store
from core.models import Studies
from core.config import config
from playhouse.shortcuts import model_to_dict

logger = logging.getLogger(__name__)
public_api = Blueprint("public_api", __name__)


# -------
# Write you endpoint to retrieve all available studies here.
# -------

@public_api.route('/studies', methods=["GET"])
def studies():
    studies = Studies.select()
    items = [model_to_dict(study) for study in studies]
    return jsonify(items)