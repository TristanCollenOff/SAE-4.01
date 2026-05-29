from datetime import datetime

class Logs:   
    def __init__(self, id_fichierlog=None, user_id=None, username=None, type_log=None, message=None, date_fichierlog=None):
        self.id_fichierlog = id_fichierlog
        self.user_id = user_id
        self.username = username
        self.type_log = type_log
        self.message = message
        self.date_fichierlog = date_fichierlog if date_fichierlog else datetime.now()
    
    def to_dict(self):
        return {
            'id_fichierlog': self.id_fichierlog,
            'user_id': self.user_id,
            'username': self.username,
            'type_log': self.type_log,
            'message': self.message,
            'date_fichierlog': self.date_fichierlog
        }
    
    @staticmethod
    def from_dict(data):
        return Logs(
            id_fichierlog=data.get('id_fichierlog'),
            user_id=data.get('user_id'),
            username=data.get('username'),
            type_log=data.get('type_log'),
            message=data.get('message'),
            date_fichierlog=data.get('date_fichierlog')
        )
    
    def __repr__(self):
        return f"<Logs {self.id_fichierlog} - {self.username} - {self.type_log}>"