from arbre import Arbre
import pygame


class Rectangle:
    def __init__(self, hg, bd):
        self.hg = hg
        self.bd = bd

    def centre(self):
        return ((self.hg[0] + self.bd[0]) // 2,
                (self.hg[1] + self.bd[1]) // 2)

    def quart(self, direction):
        """
        Renvoie le quart du rectangle dans la direction donnée
        """
        if direction == 0:
            return Rectangle(((self.hg[0] + self.bd[0]) // 2, self.hg[1]),
                             (self.bd[0], (self.hg[1] + self.bd[1]) // 2))
        elif direction == 1:
            return Rectangle(self.centre(), self.bd)
        elif direction == 2:
            return Rectangle((self.hg[0], (self.bd[1] + self.hg[1]) // 2),
                             ((self.hg[0] + self.bd[0]) // 2, self.bd[1]))
        elif direction == 3:
            return Rectangle(self.hg, self.centre())
        else:
            raise "Direction non valide"

    def quelQuart(self, point):
        """
        Indique dans quelle direction est point par rapport au centre de 'self'
        """
        cx, cy = self.centre()
        if point[0] < cx:
            if point[1] < cy:
                return 3
            else:
                return 2
        else:
            if point[1] < cy:
                return 0
            else:
                return 1

    def contient(self, point):
        """ retourne vrai si le point est dans le rectangle
        les cotes haut et gauche sont dans le rectangle
        les cotes bas et droit ne sont pas dans le rectangle """
        return (self.hg[0] <= point[0] and point[0] < self.bd[0]) and \
            (self.hg[1] <= point[1] and point[1] < self.bd[1])

    def largeur(self):
        """ retourne la largeur du rectangle """
        return (self.bd[0] - self.hg[0])

    def hauteur(self):
        """ retourne la hauteur du rectangle """
        return (self.bd[1] - self.hg[1])

    def surface(self):
        """ retourne la surface du rectangle """
        return (self.largeur() * self.hauteur())

    def intersection(self, r):
        """ retourne vrai si les deux rectangle ont une intersection non vide
        faux sinon """
        xhg = max(self.hg[0], r.hg[0])
        yhg = max(self.hg[1], r.hg[1])
        xbd = min(self.bd[0], r.bd[0])
        ybd = min(self.bd[1], r.bd[1])
        inter = Rectangle((xhg, yhg), (xbd, ybd))
        return not inter.estVide()

    def estVide(self):
        """ retourne True si le rectangle est vide """
        return self.largeur() <= 0 or self.hauteur() <= 0


class QuadTreeNode:
    # Les étiquettes des nœuds du quadtree
    def __init__(self, region, points):
        self.region = region  # 1 Rectanle
        self.points = points  # Ensemble de points


class QuadTree(Arbre):
    def __init__(self, region, points, capacite):
        """
        Construit un QuadTree à partir d'un ensemble de points.
        """
        self.capacite = capacite
        noeud_e = []  # On initialise avant car il peut ne pas contenir d'autres nodes. Une node doit avoir 4 points max
        # Si la taille de la liste des points est plus grande que la capacité, il faut diviser en 4.
        if len(points) > self.capacite:
            nregion = []  # Nouvelle région
            pointse = []  # On fait une list qui contiendra les points qui seront dans la nouvelle région
            for e in range(4):  # On répète la méthode 4 fois (pour 4 zones)
                # On utilise la méthode Quart pour définir le quart (NO>SO>SE>NE)
                nregion.append(region.quart(e))
                pointse.append([])
            for p in points:  # On place donc les points
                pointse[region.quelQuart(p)].append(p)
            points = set()
            noeud_e = []
            for e in range(4):
                noeud_e.append(QuadTree(nregion[e], set(pointse[e]), capacite))
        super().__init__(QuadTreeNode(region, points), noeud_e)

    def contains(self, point):
        # Question 3
        # On vérifie que la région contient le point
        test1 = self.etiquette().region.contient(point)
        # On verifie aussi que point est bien dans la liste des points
        test2 = point in self.elements()
        return test1 and test2

    def elements(self):
        """
        Renvoie l'ensemble de tous les points qui sont dans le quadTree
        """
        res = set(
            self.etiquette().points)  # On récupère les points de la node actuelle
        for e in self.enfants():  # Pour chaque node enfant
            # On utilise une concaténation avec le res, et les éléments de l'enfant.
            res = res | e.elements()
        return res

    def add(self, point):
        # Si l'ajout du point entraine un dépassement de capacité
        if len(self.etiquette().points) == self.capacite:
            self.etiquette().points.add(point)
            # On initialise une nouvelle node
            self.__init__(self.etiquette().region,
                          self.etiquette().points, self.capacite)
        else:
            self.etiquette().points.add(point)

    def remove(self, point):
        pass

    def dessine(self, s):
        (x1, y1) = self.etiquette().region.hg
        (x2, y2) = self.etiquette().region.bd
        w = x2 - x1
        h = y2 - y1
        pygame.draw.rect(s, (234, 234, 217), (x1, y1, w, h), 1)
        for (x, y) in self.etiquette().points:
            pygame.draw.rect(s, (255, 255, 255), (x - 8, y - 4, 8, 8), 0)
        for e in self.enfants():
            e.dessine(s)
