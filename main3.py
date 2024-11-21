import pygame
import math
from pygame.locals import *

# Clasa Buton
class Buton():
    def __init__(self, pozitie, latime, inaltime, valoare):
        self.poz_x, self.poz_y = pozitie
        self.inaltime = inaltime
        self.latime = latime
        self.valoare = valoare
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.over_time = 0

    def este_interior(self, poz):
        tempx, tempy = poz
        if tempx < self.poz_x:
            return False
        if tempx > self.poz_x + self.latime:
            return False
        if tempy < self.poz_y:
            return False
        if tempy >= self.poz_y + self.inaltime:
            return False
        return True

    def afiseaza(self, ecran, poz_mouse, apasat):

        if not apasat:
            culoare = (50, 50, 50)
            if self.este_interior(poz_mouse):
                self.over_time = min(155, self.over_time + 20)
                culoare = (70, 70, 70)
            else:
                self.over_time = max(0, self.over_time - 20)
        else:
            culoare = (30, 30, 30)

        pygame.draw.rect(ecran, culoare, pygame.Rect(self.poz_x, self.poz_y, self.latime, self.inaltime), 0, 4)

        cx = self.poz_x + int(self.latime / 2)
        cy = self.poz_y + int(self.inaltime / 2)

        text = self.font.render(str(self.valoare), True, (255, 255, 255))

        offset_x = int(text.get_rect().width / 2)
        offset_y = int(text.get_rect().height / 2)
        ecran.blit(text, (cx - offset_x, cy - offset_y))

# Clasa Popup
class Popup:
    def __init__(self, mesaj, caseta, timp_afisare=None):
        self.mesaj = mesaj
        self.timp_afisare = timp_afisare
        self.de_afisat = 0

        self.caseta = caseta
        self.font = pygame.font.SysFont('Arial', 24)

    def arata(self):
        if self.timp_afisare is None:
            self.de_afisat = -1
        else:
            self.de_afisat = self.timp_afisare

    def ascunde(self):
        self.de_afisat = 0

    def actualizeaza(self):
        if self.de_afisat > 0:
            self.de_afisat -= 1

    def afiseaza(self, ecran):
        if self.de_afisat != 0:
            pygame.draw.rect(ecran, (50, 50, 50), self.caseta, 0, 5)

            cx = self.caseta.x + int(self.caseta.w / 2)
            cy = self.caseta.y + int(self.caseta.h / 2)

            text = self.font.render(str(self.mesaj), True, (255, 255, 255))

            offset_x = int(text.get_rect().width / 2)
            offset_y = int(text.get_rect().height / 2)
            ecran.blit(text, (cx - offset_x, cy - offset_y))

# Clasa Nod
class Nod():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.r_arc = 15
        self.arce = []
        self.hl_arce = []

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)
        self.selectat = False

        self.number = 0  # Will be set when nodes are renumbered

    def adauga_arc(self, dest, greutate, afisat):
        self.arce.append([dest, greutate, afisat])

    def selecteaza(self, sel):
        self.selectat = sel

    def get_dest_arc_selectat(self, x, y):
        for a in self.arce:
            if a[2]:
                x1, y1 = self.get_pozitie()
                x2, y2 = a[0].get_pozitie()

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                d = math.sqrt((cx - x) ** 2 + (cy - y) ** 2)

                if d < self.r_arc:
                    return a[0]

        return None

    def sterge_arc(self, dest, afisat):
        if afisat:
            dest.sterge_arc(self, False)
        for a in self.arce:
            if a[0] == dest:
                self.arce.remove(a)
                break

    def editeaza_arc(self, dest, greutate, afisat):
        if afisat:
            dest.editeaza_arc(self, greutate, False)

        gasit = False
        for a in self.arce:
            if a[0] == dest:
                gasit = True
                a[1] = greutate
                a[2] = afisat
                break
        if not gasit:
            self.adauga_arc(dest, greutate, afisat)

    def get_greutate_arc(self, dest):
        for a in self.arce:
            if a[0] == dest:
                return a[1]
        return None

    def translateaza(self, dx, dy):
        self.x += dx
        self.y += dy

    def este_interior(self, px, py):
        d = math.sqrt((px - self.x) ** 2 + (py - self.y) ** 2)

        if d > self.r:
            return False

        return True

    def get_pozitie(self):
        return (self.x, self.y)

    def evidentiaza_arc(self, dest=None, callback=True):
        if dest is None:
            self.hl_arce = []
        else:
            if callback:
                dest.evidentiaza_arc(self, False)

            for a in self.arce:
                if a[0] == dest:
                    self.hl_arce.append(a)

    def deseneaza_arce(self, ecran, poz_mouse):
        for a in self.arce:
            if a[2]:
                x1, y1 = self.get_pozitie()
                x2, y2 = a[0].get_pozitie()

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                d = math.sqrt((cx - poz_mouse[0]) ** 2 + (cy - poz_mouse[1]) ** 2)

                if a in self.hl_arce:
                    culoare = (255, 100, 100)
                else:
                    culoare = (200, 200, 200)

                pygame.draw.line(ecran, culoare, (x1, y1), (x2, y2), 2)

                if d < self.r_arc:
                    pygame.draw.circle(ecran, (100, 100, 100), (cx, cy), self.r_arc, 0)
                    text = self.font.render(str(a[1]), True, (255, 255, 255))
                else:
                    pygame.draw.circle(ecran, (200, 200, 200), (cx, cy), self.r_arc, 0)
                    text = self.font.render(str(a[1]), True, (50, 50, 50))

                offset_x = int(text.get_rect().width / 2)
                offset_y = int(text.get_rect().height / 2)
                ecran.blit(text, (cx - offset_x, cy - offset_y))

    def deseneaza(self, ecran):
        if self.selectat:
            culoare = (255, 100, 100)
        else:
            culoare = (200, 200, 200)
        pygame.draw.circle(ecran, culoare, self.get_pozitie(), self.r, 0)
        self.deseneaza_text(ecran, self.number)  # Display the node number

    def deseneaza_text(self, ecran, mesaj):
        text = self.font.render(str(mesaj), True, (50, 50, 50))
        offset_x = int(text.get_rect().width / 2)
        offset_y = int(text.get_rect().height / 2)
        ecran.blit(text, (self.x - offset_x, self.y - offset_y))

# Funcție pentru renumerotarea nodurilor
def renumber_nodes():
    for i, node in enumerate(lista_noduri):
        node.number = i + 1

# Funcție pentru salvarea grafului într-un fișier text
def save_graph():
    with open('graph.txt', 'w') as f:
        # Scrie nodurile
        f.write('Noduri:\n')
        for node in lista_noduri:
            f.write(f'{node.number} {node.x} {node.y}\n')  # Salvăm și poziția nodurilor
        # Scrie muchiile
        f.write('Muchii:\n')
        edges_set = set()
        for node in lista_noduri:
            for arc in node.arce:
                dest = arc[0]
                weight = arc[1]
                # Pentru a evita duplicatele în grafuri neorientate
                edge = tuple(sorted((node.number, dest.number)))
                if edge not in edges_set:
                    edges_set.add(edge)
                    f.write(f'{node.number} {dest.number} {weight}\n')
    print('Graful a fost incarcat din fisierul graph.txt')

# Funcție pentru încărcarea grafului dintr-un fișier text
def load_graph():
    try:
        with open('graph.txt', 'r') as f:
            lines = f.readlines()
        noduri_section = False
        muchii_section = False
        noduri_data = []
        muchii_data = []

        for line in lines:
            line = line.strip()
            if line == 'Noduri:':
                noduri_section = True
                muchii_section = False
                continue
            elif line == 'Muchii:':
                noduri_section = False
                muchii_section = True
                continue
            elif line == '':
                continue

            if noduri_section:
                parts = line.split()
                if len(parts) == 3:
                    numar, x, y = parts
                    noduri_data.append((int(numar), float(x), float(y)))
            elif muchii_section:
                parts = line.split()
                if len(parts) == 3:
                    n1, n2, weight = parts
                    muchii_data.append((int(n1), int(n2), int(weight)))

        # Clear the current graph
        lista_noduri.clear()

        # Create nodes
        node_dict = {}
        for numar, x, y in noduri_data:
            node = Nod(x, y, R_CERC)
            node.number = numar
            lista_noduri.append(node)
            node_dict[numar] = node

        # Create edges
        for n1, n2, weight in muchii_data:
            node1 = node_dict.get(n1)
            node2 = node_dict.get(n2)
            if node1 and node2:
                node1.editeaza_arc(node2, weight, True)

        renumber_nodes()
        print('Graful a fost incarcat din fisierul graph.txt')

    except FileNotFoundError:
        print('Fisierul graph.txt nu a fost gasit.')
    except Exception as e:
        print('Eroare la incarcarea grafului:', e)

# Inițializare Pygame
pygame.init()

R_CERC = 25  # Increased the node radius for better visibility

# Fullscreen settings
infoObject = pygame.display.Info()
latime, inaltime = infoObject.current_w, infoObject.current_h  # Get the screen resolution
dimensiune = latime, inaltime

negru = 30, 30, 30  # Darker background for a modern look
alb = 255, 255, 255

ecran = pygame.display.set_mode(dimensiune, pygame.FULLSCREEN)

pygame.display.set_caption('Editor de Grafuri')

ceas = pygame.time.Clock()

lista_noduri = []

# Butoane - Adjusted positions for full screen
button_width = 200
button_height = 50
button_gap = 20
total_button_width = 3 * button_width + 2 * button_gap
start_x = (latime - total_button_width) // 2
button_y = inaltime - button_height - 30

b_salveaza = Buton((start_x, button_y), button_width, button_height, "Salvează Graf")
b_sterge = Buton((start_x + button_width + button_gap, button_y), button_width, button_height, "Șterge Nod")
b_importa = Buton((start_x + 2 * (button_width + button_gap), button_y), button_width, button_height, "Importă Graf")

selectare = False
poz_selectare = None
selectate = []

desenare = False
trage = False
mutat = False
conectare = False
ind_trage = 0

editare = False
info_editare = (0, 0)
valoare_curenta = ""

# Popup
rect_popup = pygame.Rect(100, 10, latime - 200, 60)

popup_editare = Popup("Apasă Enter pentru a confirma", rect_popup)

while True:
    ecran.fill(negru)

    if not editare:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    mx, my = ev.pos

                    if b_salveaza.este_interior(ev.pos):
                        # Salvează graful
                        save_graph()
                    elif b_importa.este_interior(ev.pos):
                        # Încarcă graful
                        load_graph()
                    elif b_sterge.este_interior(ev.pos):
                        # Șterge ultimul nod
                        if lista_noduri:
                            lista_noduri.pop()
                            renumber_nodes()
                    else:
                        i = 0
                        if conectare:
                            ind_start = ind_trage
                        ind_trage = None
                        gasit = False
                        for ob in lista_noduri:
                            if ob.este_interior(mx, my):
                                if not conectare:
                                    trage = True
                                    mutat = False
                                    ind_trage = i
                                    x_start = mx
                                    y_start = my
                                else:
                                    ind_trage = i

                                gasit = True
                                break
                            i += 1

                        if not gasit:
                            for ob in lista_noduri:
                                x = ob.get_dest_arc_selectat(mx, my)
                                if x is not None:
                                    selectate = []
                                    editare = True
                                    popup_editare.arata()

                                    info_editare = (ob, x)
                                    valoare_curenta = str(ob.get_greutate_arc(x))
                                    break

                            if not editare:
                                selectare = True
                                poz_selectare = ev.pos

                        if conectare:
                            if ind_trage is not None:
                                lista_noduri[ind_start].editeaza_arc(lista_noduri[ind_trage], 1, True)
                            conectare = False

                elif ev.button == 2:
                    selectate = []

                    mx, my = ev.pos
                    nod_sters = None
                    for ob in lista_noduri:
                        if ob.este_interior(mx, my):
                            nod_sters = ob
                            break

                    if nod_sters is not None:
                        lista_noduri.remove(nod_sters)
                        renumber_nodes()
                    else:
                        for ob in lista_noduri:
                            x = ob.get_dest_arc_selectat(mx, my)
                            if x is not None:
                                ob.sterge_arc(x, True)
                                break

                elif ev.button == 3:
                    selectate = []

                    mx, my = ev.pos
                    x = Nod(mx, my, R_CERC)
                    lista_noduri.append(x)
                    renumber_nodes()

            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:

                    if trage and not mutat:
                        conectare = True
                        selectate = []

                    trage = False
                    selectare = False

            elif ev.type == pygame.MOUSEMOTION:
                if desenare:
                    mx, my = ev.pos
                    desenare_w = mx - x_start
                    desenare_h = my - y_start
                if trage:
                    mutat = True
                    mx, my = ev.pos
                    dx = mx - x_start
                    dy = my - y_start

                    lista_noduri[ind_trage].translateaza(dx, dy)

                    x_start = mx
                    y_start = my

    else:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    editare = False
                    popup_editare.ascunde()
                if ev.key == pygame.K_RETURN:
                    editare = False
                    popup_editare.ascunde()
                if ev.key == K_BACKSPACE:
                    valoare_curenta = valoare_curenta[0:-1]
                if ev.unicode.isdigit():
                    valoare_curenta += ev.unicode

        if valoare_curenta == "":
            valoare_curenta = "0"
        info_editare[0].editeaza_arc(info_editare[1], max(1, int(valoare_curenta)), True)

    for ob in lista_noduri:
        ob.evidentiaza_arc()

    if selectare:
        mx, my = pygame.mouse.get_pos()
        x_rect = min(poz_selectare[0], mx)
        y_rect = min(poz_selectare[1], my)
        w_rect = abs(mx - poz_selectare[0])
        h_rect = abs(my - poz_selectare[1])
        pygame.draw.rect(ecran, (200, 200, 200), pygame.Rect(x_rect, y_rect, w_rect, h_rect), 1)

    for ob in lista_noduri:
        ob.deseneaza_arce(ecran, pygame.mouse.get_pos())

    for ob in lista_noduri:
        ob.deseneaza(ecran)

    # Afișare Butoane
    b_salveaza.afiseaza(ecran, pygame.mouse.get_pos(), False)
    b_sterge.afiseaza(ecran, pygame.mouse.get_pos(), False)
    b_importa.afiseaza(ecran, pygame.mouse.get_pos(), False)

    if conectare:
        pygame.draw.line(ecran, alb, (x_start, y_start), pygame.mouse.get_pos(), 2)

    # Actualizare Popup
    popup_editare.actualizeaza()

    # Afișare Popup
    popup_editare.afiseaza(ecran)

    pygame.display.update()

    ceas.tick(60)
