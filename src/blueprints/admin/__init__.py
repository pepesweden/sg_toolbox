from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

from . import users  # importerar users.py