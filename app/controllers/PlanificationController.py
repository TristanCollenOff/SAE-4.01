from flask import Blueprint, render_template, session, abort, request, redirect, url_for, flash
from app.models.PlanificationDAO import PlanificationDAO
from app.models.LecteurDAO import LecteurDAO
from app.models.PlaylistDAO import PlaylistDAO
from app.controllers.LoginController import reqlogged
from app.models.Planification import Planification
from app.services.PlanificationService import PlanificationService
from app.services.access_control import require_permission
from app.services.permissions import normalize_role

planif_bp = Blueprint('planification', __name__, url_prefix="/planification")
planif_service = PlanificationService()


@planif_bp.route('/lecteur/<int:id_lecteur>')
@reqlogged
@require_permission("plan_playlist", "plan_ad", "choose_slot")
def planifier_lecteur(id_lecteur):
    role = normalize_role(session.get("role", "commercial"))
    dao_planif = PlanificationDAO()
    dao_lecteur = LecteurDAO()
    dao_playlist = PlaylistDAO()

    lecteurs = dao_lecteur.find_all()
    lecteur = dao_lecteur.find_one(id_lecteur)

    if not lecteur:
        abort(404)

    playlists = dao_playlist.find_all()
    planifications = dao_planif.get_by_lecteur(id_lecteur)
    playlist_preselect = request.args.get('playlist', type=int)

    return render_template(
        "planification.html",
        lecteur=lecteur,
        lecteurs=lecteurs,
        playlists=playlists,
        planifications=planifications,
        playlist_preselect=playlist_preselect,
        role=role,
        can_plan_playlist=role in ("admin", "marketing"),
        can_plan_ad=role in ("admin", "commercial"),
    )


@planif_bp.route('/ajouter/<int:id_lecteur>', methods=['POST'])
@reqlogged
@require_permission("plan_playlist", "plan_ad")
def ajouter_planif(id_lecteur):
    role = normalize_role(session.get("role", "commercial"))
    contenu_type = request.form.get('contenu_type', 'playlist')

    if role == "commercial" and contenu_type != 'annonce':
        flash("Seules les publicités et annonces peuvent être planifiées.", "error")
        return redirect(url_for('planification.planifier_lecteur', id_lecteur=id_lecteur))

    if role == "marketing" and contenu_type == 'annonce':
        flash("Le rôle Marketing planifie uniquement des playlists.", "error")
        return redirect(url_for('planification.planifier_lecteur', id_lecteur=id_lecteur))

    id_playlist = request.form.get('id_playlist')

    if not id_playlist:
        flash("Veuillez sélectionner une playlist", "error")
        return redirect(url_for('planification.planifier_lecteur', id_lecteur=id_lecteur))

    new_planif = Planification(
        id_lecteur=id_lecteur,
        id_playlist=int(id_playlist),
        jour_semaine=request.form.get('jour'),
        heure_debut=request.form.get('debut'),
        heure_fin=request.form.get('fin')
    )

    planif_service.planifier(new_planif, session.get('username'))
    flash("Planification ajoutée avec succès", "success")

    return redirect(url_for('planification.planifier_lecteur', id_lecteur=id_lecteur))


@planif_bp.route('/supprimer/<int:id_planif>', methods=['POST'])
@reqlogged
@require_permission("plan_playlist", "plan_ad")
def supprimer_planif(id_planif):
    dao_planif = PlanificationDAO()

    try:
        planif = dao_planif.find_one(id_planif)

        if not planif:
            flash("Planification introuvable", "error")
            return redirect(url_for('index'))

        id_lecteur = planif.id_lecteur
        dao_planif.delete(id_planif)

        flash("Planification supprimée avec succès", "success")
        return redirect(url_for('planification.planifier_lecteur', id_lecteur=id_lecteur))

    except Exception as e:
        print(f"Erreur lors de la suppression: {e}")
        flash("Erreur lors de la suppression de la planification", "error")
        return redirect(url_for('index'))
