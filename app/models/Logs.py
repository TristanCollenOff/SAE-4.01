from datetime import datetime

class Logs:   
    def __init__(self, id_log=None, type_action=None, message=None, date_fichierlog=None, id_organisation=None):
        self.id_log = id_log
        self.type_action = type_action
        self.message = message
        self.date_fichierlog = date_fichierlog if date_fichierlog else datetime.now()
        self.id_organisation = id_organisation
    
    def to_dict(self):
        
        return {
            'id_log': self.id_log,
            'type_action': self.type_action,
            'message': self.message,
            'date_fichierlog': self.date_fichierlog,
            'id_organisation': self.id_organisation
        }
    
    @staticmethod
    def from_dict(data):
        return Logs(
            id_log=data.get('id_log'),
            type_action=data.get('type_action'),
            message=data.get('message'),
            date_fichierlog=data.get('date_fichierlog'),
            id_organisation=data.get('id_organisation')
        )
    
    def __repr__(self):
        return f"<Logs {self.id_log} - Org {self.id_organisation} - {self.type_action}>"