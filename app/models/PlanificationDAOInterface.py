from abc import ABC, abstractmethod

class PlanificationDAOInterface(ABC):
    @abstractmethod
    def add(self, planif): pass
    @abstractmethod
    def get_by_lecteur(self, id_lecteur): pass
    @abstractmethod
    def delete(self, id_planification): pass