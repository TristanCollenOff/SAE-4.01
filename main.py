from app import app

# Import des contrôleurs pour enregistrer les routes
from app.controllers import LoginController
from app.controllers import IndexController
from app.controllers import AdminController  # <- indispensable

from app.controllers.RegisterController import register_bp
app.register_blueprint(register_bp)
from app.controllers.ResetPasswordController import reset_bp
app.register_blueprint(reset_bp)
from app.controllers.AdminController import admin_bp
app.register_blueprint(admin_bp)
from app.controllers.LogsController import log_bp
app.register_blueprint(log_bp)
from app.controllers.MusiqueController import musique_bp
app.register_blueprint(musique_bp)
from app.controllers.PlaylistController import playlist_bp
app.register_blueprint(playlist_bp)
from app.controllers.SitesZonesController import sites_zones_bp
app.register_blueprint(sites_zones_bp)
from app.controllers.LecteursOpsController import lecteurs_ops_bp
app.register_blueprint(lecteurs_ops_bp)
from app.controllers.AlertesController import alertes_bp
app.register_blueprint(alertes_bp)
from app.controllers.ContactController import contact_bp
app.register_blueprint(contact_bp)
from app.controllers.PlanificationController import planif_bp
app.register_blueprint(planif_bp)


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=8000, debug=True)

