"""Décorateurs et helpers d'accès basés sur les rôles."""

from functools import wraps

from flask import abort, session

from app.services.permissions import can, normalize_role


def require_permission(*permissions):
    """Exige au moins une des permissions listées."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = normalize_role(session.get("role"))
            if not any(can(role, permission) for permission in permissions):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_roles(*roles):
    """Exige un rôle exact (admin inclus tel quel)."""

    allowed = {normalize_role(role) for role in roles}

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = normalize_role(session.get("role"))
            if role not in allowed and role != "admin":
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
