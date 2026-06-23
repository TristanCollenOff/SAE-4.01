from flask import Blueprint, render_template, redirect, url_for, session, abort
from app.services.user_service import UserService
from app.services.log_service import log_action
from datetime import datetime, timedelta

admin_bp = Blueprint("admin", __name__, url_prefix="/admin/users")

user_service = UserService()


# -----------------------------
# CHECK ADMIN
# -----------------------------
from app.services.permissions import normalize_role


def admin_required():
    if normalize_role(session.get("role")) != "admin":
        abort(403)


# -----------------------------
# LIST USERS
# -----------------------------
@admin_bp.route("/", endpoint="admin")
def list_users():
    admin_required()
    users = user_service.getUsers()
    metadata = {"title": "Admin - Gestion Utilisateurs", "pagename": "admin"}
    return render_template("admin.html", users=users, metadata=metadata)


# -----------------------------
# BLOCK USER
# -----------------------------
@admin_bp.route("/block/<int:user_id>")
def block_user(user_id):
    admin_required()

    target_user = user_service.getUserById(user_id)
    if not target_user:
        abort(404)

    # 🔥 BLOQUAGE PROPRE VIA DAO
    user_service.block_user(user_id, minutes=60)

    admin_user = session.get("username", "admin")

    log_action(
        admin_user,
        f"A bloqué l'utilisateur {getattr(target_user, 'username', 'inconnu')}"
    )

    return redirect(url_for("admin.admin"))


# -----------------------------
# UNBLOCK USER
# -----------------------------
@admin_bp.route("/unblock/<int:user_id>")
def unblock_user(user_id):
    admin_required()

    target_user = user_service.getUserById(user_id)
    if not target_user:
        abort(404)

    # 🔥 UNBLOCK PROPRE VIA DAO
    user_service.unblock_user(user_id)

    admin_user = session.get("username", "admin")

    log_action(
        admin_user,
        f"A débloqué l'utilisateur {getattr(target_user, 'username', 'inconnu')}"
    )

    return redirect(url_for("admin.admin"))