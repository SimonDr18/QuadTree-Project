#!/usr/bin/env python3


class Arbre:
    def __init__(self, etiquette, enfants):
        self.__etiquette = etiquette
        self.__enfants = enfants

    def etiquette(self):
        return self.__etiquette

    def enfants(self):
        return self.__enfants

    @classmethod
    def Feuille(cls_arbre, etiquette):  # méthode statique
        return cls_arbre(etiquette, [])

    def add(self, nourisson):
        """
        ajoute un enfant à l'arbre
        """
        self.enfants.append(nourisson)

    def __repr__(self):
        repr_enfants = ",".join(("%r" % e) for e in self.enfants())
        return "%r<%s>" % (self.etiquette(), repr_enfants)
