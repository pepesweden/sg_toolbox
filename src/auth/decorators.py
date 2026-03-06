from flask_login import current_user
from functools import wraps 
from flask import redirect, url_for, flash 

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #hämtar current_user och is_authenticade från Flask Login och jämför mot argument.
        if not current_user.is_authenticated:
           flash('Du behöver vara inoggad för att se denna sida')
           return redirect('/')
        if not current_user.is_admin:
           # Kontrollerar is_admin i Users schema.
           return redirect(url_for('welcome_page'))
        return func(*args, **kwargs)
    return wrapper