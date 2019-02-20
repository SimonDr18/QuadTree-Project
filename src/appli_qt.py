import pygame
import sys
import random
from quadtree import QuadTree, Rectangle

global FPSCLOCK
FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 512
ARRIERE_PLAN = (42, 17, 51)

red = (200,0,0)
green = (0,200,0)

class Quitte(BaseException):
    pass


def isQuitEvent(event):
    return (event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE))


def isClick(event):
    return (event.type == pygame.MOUSEBUTTONUP)


def handleClick(quadTree, event):
    x, y = pygame.mouse.get_pos()
    trouve = False
    if x<512 :
        for realx in range(x - 5, x + 5):
            for realy in range(y - 5, y + 5):
                if quadTree.contains((realx, realy)):
                    print("Le point", realx, realy, "est dans le quadTree")
                    pygame.mixer.Sound("../lib/sounds/bow.wav").play()
                    trouve = True
                    quadTree.remove((realx,realy)) #On retire le point qui est à nos coordonnées
        if not trouve:  # Non trouvé donc on ajout un point
            print("Ce point n'est pas dans le quadTree")
            quadTree.add((x, y))
            pygame.mixer.Sound("../lib/sounds/pew.wav").play()
    else :
        print("Menu")

def handleEvents(quadTree):
    for event in pygame.event.get():  # event handling loop
        if isQuitEvent(event):
            raise Quitte
        elif isClick(event):
            handleClick(quadTree, event)


def refresh(s):
    s.fill(ARRIERE_PLAN)


def drawApp(s, quadTree):
    refresh(s)
    quadTree.dessine(s)


def ensemble_points(nb_points, w, h):
    s = set()
    for i in range(nb_points):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s.add((x, y))
    return s


def main():
    capacite = input(
        "Veuillez entrer la capacitée maximale que QuadTree peut contenir ")
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('QuadTree Project')
    ecran = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    refresh(ecran)

    e = ensemble_points(0, 512, 512)  # création de 8 points aléatoires
    # dans un univers de taille
    # 512x512
    region = Rectangle((0, 0), (512, 512))
    quadTree = QuadTree(region, e, int(capacite))

    while True:  # boucle principale
        try:
            handleEvents(quadTree)
            drawApp(ecran, quadTree)
            pygame.display.update()

        except Quitte:
            break

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
