"""Définition centralisée des rôles et permissions RYTHMO."""

ROLE_ADMIN = "admin"
ROLE_MARKETING = "marketing"
ROLE_COMMERCIAL = "commercial"

LEGACY_ROLE_MAP = {
    "superviseur": ROLE_MARKETING,
    "utilisateur": ROLE_COMMERCIAL,
    "Administrateur": ROLE_ADMIN,
}

ROLE_LABELS = {
    ROLE_ADMIN: "Administrateur",
    ROLE_MARKETING: "Marketing",
    ROLE_COMMERCIAL: "Commercial",
}

# Permissions par rôle (admin = tout)
ROLE_PERMISSIONS = {
    ROLE_ADMIN: {
        "view_playlists": True,
        "create_playlist": True,
        "edit_playlist": True,
        "plan_playlist": True,
        "manage_audio_files": True,
        "sync_playlists": True,
        "view_history": True,
        "choose_mood": True,
        "view_playlists_readonly": True,
        "add_ad": True,
        "add_announcement": True,
        "plan_ad": True,
        "choose_slot": True,
        "urgent_announcement": True,
        "view_lecteur_status": True,
        "manage_users": True,
        "manage_lecteurs": True,
        "manage_sites_zones": True,
        "manage_alertes": True,
        "export_history": True,
        "control_music": True,
    },
    ROLE_MARKETING: {
        "view_playlists": True,
        "create_playlist": True,
        "edit_playlist": True,
        "plan_playlist": True,
        "manage_audio_files": True,
        "sync_playlists": True,
        "view_history": True,
        "choose_mood": True,
        "view_playlists_readonly": False,
        "add_ad": False,
        "add_announcement": False,
        "plan_ad": False,
        "choose_slot": False,
        "urgent_announcement": False,
        "view_lecteur_status": False,
        "manage_users": False,
        "manage_lecteurs": False,
        "manage_sites_zones": False,
        "manage_alertes": False,
        "export_history": False,
        "control_music": True,
    },
    ROLE_COMMERCIAL: {
        "view_playlists": False,
        "create_playlist": False,
        "edit_playlist": False,
        "plan_playlist": False,
        "manage_audio_files": False,
        "sync_playlists": False,
        "view_history": True,
        "choose_mood": True,
        "view_playlists_readonly": True,
        "add_ad": True,
        "add_announcement": True,
        "plan_ad": True,
        "choose_slot": True,
        "urgent_announcement": True,
        "view_lecteur_status": True,
        "manage_users": False,
        "manage_lecteurs": False,
        "manage_sites_zones": False,
        "manage_alertes": False,
        "export_history": False,
        "control_music": False,
    },
}


def normalize_role(role):
    if not role:
        return ROLE_COMMERCIAL
    return LEGACY_ROLE_MAP.get(role, role)


def role_label(role):
    return ROLE_LABELS.get(normalize_role(role), str(role).title())


def get_role_permissions(role):
    role = normalize_role(role)
    if role == ROLE_ADMIN:
        return ROLE_PERMISSIONS[ROLE_ADMIN]
    return ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS[ROLE_COMMERCIAL])


def can(role, permission):
    if normalize_role(role) == ROLE_ADMIN:
        return True
    return get_role_permissions(role).get(permission, False)


def can_any(role, *permissions):
    return any(can(role, p) for p in permissions)


def can_view_playlists(role):
    return can_any(role, "view_playlists", "view_playlists_readonly")


def is_playlist_readonly(role):
    return can(role, "view_playlists_readonly") and not can(role, "edit_playlist")
