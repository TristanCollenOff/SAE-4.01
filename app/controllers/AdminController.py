from flask import Blueprint, render_template, redirect, url_for, session, abort
from app.services.user_service import UserService
from app.services.log_service import log_action

admin_bp = Blueprint("admin", __name__, url_prefix="/admin/users")
user_service = UserService()

def admin_required():
    if session.get("role") not in ["admin", "Administrateur"]:
        abort(403)


@admin_bp.route("/", endpoint="admin")
def list_users():
    admin_required()
    users = user_service.getUsers()
    metadata = {"title": "Admin - Gestion Utilisateurs", "pagename": "admin"}
    return render_template("admin.html", users=users, metadata=metadata)


@admin_bp.route("/block/<int:user_id>")
def block_user(user_id):
    admin_required()

    # Récupère l'utilisateur cible
    target_user = user_service.getUserById(user_id)
    if not target_user:
        abort(404)  # Si l'utilisateur n'existe pas

    # Bloquer l'utilisateur
    user_service.block_user(user_id, minutes=60)

    # Log de l'action admin
    admin_user = session.get("nom_utilisateur")  # admin connecté
    log_action(admin_user, f"A bloqué l'utilisateur {target_user.username}")

    return redirect(url_for("admin.admin"))


@admin_bp.route("/unblock/<int:user_id>")
def unblock_user(user_id):
    admin_required()
    # Récupérer l'utilisateur cible
    target_user = user_service.getUserById(user_id)
    if not target_user:
        abort(404)

    # Débloquer l'utilisateur
    user_service.unblock_user(user_id)

    # Log de l'action admin
    admin_user = session.get("nom_utilisateur", "admin inconnu")
    log_action(admin_user, f"A débloqué l'utilisateur {target_user.username}")

    return redirect(url_for("admin.admin"))










