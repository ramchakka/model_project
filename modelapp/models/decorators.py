import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            flash('You need to be signed in for this page.', 'danger')
            return redirect(url_for('webuser.login_user'))
        return f(*args, **kwargs)

    return decorated_function

def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print(current_app.config.get('ADMIN', ''))
        if session.get('username') not in  current_app.config.get('ADMIN', '').split(','):
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('webmodels.index'))
        return f(*args, **kwargs)

    return decorated_function

