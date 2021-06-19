import time
import pygame
import sys
from copy import deepcopy as dc

ADANCIME_MAX = 4


def mutare_valida(i, j):
    if i < 0 or i > 7:
        return False
    if j < 0 or j > 7:
        return False
    return True


class Joc:
    """
    Clasa care defineste jocul.
    """

    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    GOL = "#"

    @classmethod
    def initializeaza(cls, display, NR_COLOANE=8, dim_celula=100):
        # TODO: initializat tabla de sah cu damele albe si negre pe pozitiile corespunzatoare
        cls.display = display
        cls.dim_celula = dim_celula
        cls.alb_img = pygame.image.load("white.png")
        cls.alb_img = pygame.transform.scale(cls.alb_img, (dim_celula, dim_celula))
        cls.alb_r_img = pygame.image.load("white_R.png")
        cls.alb_r_img = pygame.transform.scale(cls.alb_r_img, (dim_celula, dim_celula))
        cls.negru_img = pygame.image.load("black.png")
        cls.negru_img = pygame.transform.scale(cls.negru_img, (dim_celula, dim_celula))
        cls.negru_r_img = pygame.image.load("black_R.png")
        cls.negru_r_img = pygame.transform.scale(cls.negru_r_img, (dim_celula, dim_celula))
        cls.celuleGrid = [[] for i in range(NR_COLOANE)]  # este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(
                    coloana * (dim_celula + 1),
                    linie * (dim_celula + 1),
                    dim_celula,
                    dim_celula,
                )
                cls.celuleGrid[linie].append(patr)

    def deseneaza_grid(self):
        # TODO: Desenat grid-ul la fiecare pas al jocului
        # tabla este o lista de 8 liste cu cate 8 caractere fiecare
        culoare_alb = (252, 204, 106)
        culoare_negru = (87, 58, 46)
        for i in range(len(self.matr)):
            for j in range(len(self.matr)):
                # pe liniile pare
                if i % 2 == 0:
                    if j % 2 == 1:
                        pygame.draw.rect(self.__class__.display, culoare_negru, self.__class__.celuleGrid[i][j])
                    else:
                        pygame.draw.rect(self.__class__.display, culoare_alb, self.__class__.celuleGrid[i][j])
                else:
                    if j % 2 == 1:
                        pygame.draw.rect(self.__class__.display, culoare_alb, self.__class__.celuleGrid[i][j])
                    else:
                        pygame.draw.rect(self.__class__.display, culoare_negru, self.__class__.celuleGrid[i][j])

                if self.matr[i][j] == "a":
                    self.__class__.display.blit(
                        self.__class__.alb_img,
                        (
                            j * (self.__class__.dim_celula + 1),
                            i * (self.__class__.dim_celula + 1),
                        ),
                    )
                elif self.matr[i][j] == "A":
                    self.__class__.display.blit(
                        self.__class__.alb_r_img,
                        (
                            j * (self.__class__.dim_celula + 1),
                            i * (self.__class__.dim_celula + 1),
                        ),
                    )
                elif self.matr[i][j] == "n":
                    self.__class__.display.blit(
                        self.__class__.negru_img,
                        (
                            j * (self.__class__.dim_celula + 1),
                            i * (self.__class__.dim_celula + 1),
                        ),
                    )
                elif self.matr[i][j] == "N":
                    self.__class__.display.blit(
                        self.__class__.negru_r_img,
                        (
                            j * (self.__class__.dim_celula + 1),
                            i * (self.__class__.dim_celula + 1),
                        ),
                    )
        pygame.display.flip()

    def __init__(self, tabla=None):
        # TODO: implement
        self.matr = tabla

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        # TODO: functie care verifica daca s-a terminat jocul, adica daca un jucator a ramas fara piese \
        #  sau daca nu mai are posibilitatea sa faca nici macar o mutare
        nr_piese_jmin = 0
        nr_piese_jmax = 0
        nr_mutari_jmin = self.mutari(self.JMIN)
        nr_mutari_jmax = self.mutari(self.JMAX)

        breakfor = False
        for i in range(len(self.matr)):
            for j in range(len(self.matr)):
                if self.matr[i][j].lower() == Joc.JMIN:
                    nr_piese_jmin += 1
                if self.matr[i][j].lower() == Joc.JMAX:
                    nr_piese_jmax += 1
                if nr_piese_jmax != 0 and nr_piese_jmin != 0:
                    breakfor = True
                    break
            if breakfor:
                break

        if not nr_mutari_jmax or nr_piese_jmax == 0:
            return Joc.JMIN
        if not nr_mutari_jmin or nr_piese_jmin == 0:
            return Joc.JMAX
        return False

    def mutari(self, jucator):
        # TODO: functie care face toate mutarile posibile ale jucatorului respectiv
        """
        Functia mutari verifica mai intai daca exista vreo mutare de capturare a piesei adversarului. Daca da,
        returneaza direct lista de mutari cu mutarea aceasta.

        """

        mutari = []
        indici = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        # stanga-sus, dreapta-sus, stanga-jos, dreapta-jos, din punctul de vedere al jucatorului

        for i in range(len(self.matr)):
            for j in range(len(self.matr)):

                # cand gasesc o piesa de a jucatorului respectiv si acesta este JMIN
                if self.matr[i][j].lower() == jucator and jucator == Joc.JMIN:
                    # voi verifica mai intai daca exista vreo mutare cu care capturez o piesa, caz in care returnez direct
                    # mutari cu mutarea aceea

                    # mutari in 2 directii trebuie 100% sa le verific, iar daca e piesa Rege, verific in 4 directii
                    for ind in range(2):
                        # daca pot face mutare 2 pasi peste piesa adversarului si sa o capturez
                        if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                            if self.matr[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                                    self.matr[i + indici[ind][0]][j + indici[ind][1]].lower() == Joc.JMAX:
                                matrice_noua = dc(self.matr)
                                matrice_noua[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] = matrice_noua[i][j]
                                matrice_noua[i][j] = Joc.GOL
                                matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = Joc.GOL

                                if i + 2 * indici[ind][0] == 0:
                                    matrice_noua[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] = jucator.upper()

                                mutari.append(Joc(matrice_noua))
                                return mutari

                    # verific daca piesa e Rege, atunci inseamna ca poate sa mute si in celelalte 2 directii
                    if self.matr[i][j] == Joc.JMIN.upper():
                        for ind in range(2, 4):
                            if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                                if self.matr[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                                        self.matr[i + indici[ind][0]][j + indici[ind][1]].lower() == Joc.JMAX:
                                    matrice_noua = dc(self.matr)
                                    matrice_noua[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] = matrice_noua[i][j]
                                    matrice_noua[i][j] = Joc.GOL
                                    matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = Joc.GOL

                                    mutari.append(Joc(matrice_noua))
                                    return mutari

                # la fel ca bucata de 33 randuri de mai sus, doar ca verifica pentru cazul in care jucatorul curent e JMAX
                elif self.matr[i][j].lower() == jucator and jucator == Joc.JMAX:
                    for ind in range(2, 4):
                        # daca pot face mutare 2 pasi peste piesa adversarului si sa o capturez
                        if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                            if self.matr[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                                    self.matr[i + indici[ind][0]][j + indici[ind][1]].lower() == Joc.JMIN:
                                matrice_noua = dc(self.matr)
                                matrice_noua[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] = matrice_noua[i][j]
                                matrice_noua[i][j] = Joc.GOL
                                matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = Joc.GOL

                                if i + 2 * indici[ind][0] == 7:
                                    matrice_noua[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] = jucator.upper()

                                mutari.append(Joc(matrice_noua))
                                return mutari

                    # verific daca piesa e Rege, atunci inseamna ca poate sa mute si in celelalte 2 directii
                    if self.matr[i][j] == Joc.JMAX.upper():
                        for ind in range(2):
                            # daca pot face mutare 2 pasi peste piesa adversarului si sa o capturez
                            if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                                if self.matr[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                                        self.matr[i + indici[ind][0]][j + indici[ind][1]].lower() == Joc.JMIN:
                                    matrice_noua = dc(self.matr)
                                    matrice_noua[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] = matrice_noua[i][j]
                                    matrice_noua[i][j] = Joc.GOL
                                    matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = Joc.GOL

                                    mutari.append(Joc(matrice_noua))
                                    return mutari

        """ 
        daca ajunge programul in punctul asta al functiei, inseamna ca nu a gasit nicio mutare prin care ar captura o piesa
        deci mai departe doar calculez toate mutarile posibile pe care le poate face, iar la final returnez lista de mutari
        """

        for i in range(len(self.matr)):
            for j in range(len(self.matr)):

                # cand gasesc o piesa de a jucatorului respectiv
                if self.matr[i][j].lower() == jucator and jucator == Joc.JMIN:
                    # mutari in 2 directii trebuie 100% sa le verific, iar daca e piesa Rege, verific in 4 directii
                    for ind in range(2):
                        # daca pot face mutarea un pas in stanga/dreapta sus
                        if mutare_valida(i + indici[ind][0], j + indici[ind][1]):
                            if self.matr[i + indici[ind][0]][j + indici[ind][1]] == Joc.GOL:
                                matrice_noua = dc(self.matr)
                                matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = matrice_noua[i][j]
                                matrice_noua[i][j] = Joc.GOL

                                if i + indici[ind][0] == 0:
                                    matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = jucator.upper()

                                mutari.append(Joc(matrice_noua))

                    # verific daca piesa e Rege, atunci inseamna ca poate sa mute si in celelalte 2 directii
                    if self.matr[i][j] == Joc.JMIN.upper():
                        for ind in range(2, 4):
                            # daca pot face mutarea un pas in stanga/dreapta jos
                            if mutare_valida(i + indici[ind][0], j + indici[ind][1]):
                                if self.matr[i + indici[ind][0]][j + indici[ind][1]] == Joc.GOL:
                                    matrice_noua = dc(self.matr)
                                    matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = matrice_noua[i][j]
                                    matrice_noua[i][j] = Joc.GOL

                                    mutari.append(Joc(matrice_noua))

                elif self.matr[i][j].lower() == jucator and jucator == Joc.JMAX:
                    for ind in range(2, 4):
                        # daca pot face mutarea un pas in stanga/dreapta jos
                        if mutare_valida(i + indici[ind][0], j + indici[ind][1]):
                            if self.matr[i + indici[ind][0]][j + indici[ind][1]] == Joc.GOL:
                                matrice_noua = dc(self.matr)
                                matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = matrice_noua[i][j]
                                matrice_noua[i][j] = Joc.GOL

                                if i + indici[ind][0] == 7:
                                    matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = jucator.upper()

                                mutari.append(Joc(matrice_noua))

                    # verific daca piesa e Rege, atunci inseamna ca poate sa mute si in celelalte 2 directii
                    if self.matr[i][j] == Joc.JMAX.upper():
                        for ind in range(2):
                            # daca pot face mutarea un pas in stanga/dreapta sus
                            if mutare_valida(i + indici[ind][0], j + indici[ind][1]):
                                if self.matr[i + indici[ind][0]][j + indici[ind][1]] == Joc.GOL:
                                    matrice_noua = dc(self.matr)
                                    matrice_noua[i + indici[ind][0]][j + indici[ind][1]] = matrice_noua[i][j]
                                    matrice_noua[i][j] = Joc.GOL

                                    mutari.append(Joc(matrice_noua))
        return mutari

    def estimeaza_scor(self, adancime):
        # TODO: implement
        """
        Calculez diferanta dintre numarul de piese ale fiecarui jucator, unde piesele Rege valoreaza mai mult decat alea simple
        """
        t_final = self.final()
        nr_piese_jmin = 0
        nr_piese_jmax = 0
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        else:
            for i in range(len(self.matr)):
                for j in range(len(self.matr)):
                    if self.matr[i][j] == Joc.JMIN:
                        nr_piese_jmin += 1
                    if self.matr[i][j] == Joc.JMAX:
                        nr_piese_jmax += 1
                    if self.matr[i][j] == Joc.JMIN.upper():
                        nr_piese_jmin += 3
                    if self.matr[i][j] == Joc.JMAX.upper():
                        nr_piese_jmax += 3
            return nr_piese_jmax - nr_piese_jmin


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile
    posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime - 1, parinte=self)
            for mutare in l_mutari
        ]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float("-inf")

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float("inf")

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()

    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


class Buton:
    def __init__(
            self,
            display=None,
            left=0,
            top=0,
            w=0,
            h=0,
            culoareFundal=(92, 92, 92),
            culoareFundalSel=(252, 204, 106),
            text="",
            font="arial",
            fontDimensiune=24,
            culoareText=(0, 0, 0),
            valoare="",
    ):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(
            self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0
    ):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += spatiuButoane + b.w

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


# --------------- ecran initial -----------------#

def deseneaza_alegeri(display):
    btn_alg = GrupButoane(
        top=200,
        left=260,
        listaButoane=[
            Buton(display=display, w=130, h=50, text="minimax", valoare="minimax"),
            Buton(display=display, w=130, h=50, text="alphabeta", valoare="alphabeta"),
        ],
        indiceSelectat=1,
    )
    btn_juc = GrupButoane(
        top=280,
        left=290,
        listaButoane=[
            Buton(display=display, w=100, h=50, text="alb", valoare="a"),
            Buton(display=display, w=100, h=50, text="negru", valoare="n"),
        ],
        indiceSelectat=0,
    )
    btn_dificultate = GrupButoane(
        top=360,
        left=235,
        listaButoane=[
            Buton(display=display, w=100, h=50, text="usor", valoare="3"),
            Buton(display=display, w=100, h=50, text="mediu", valoare="5"),
            Buton(display=display, w=100, h=50, text="greu", valoare="7")
        ],
        indiceSelectat=1
    )
    btn_mod = GrupButoane(
        top=440,
        left=290,
        listaButoane=[
            Buton(display=display, w=100, h=50, text="P vs AI", valoare="c"),
            Buton(display=display, w=100, h=50, text="P vs P", valoare="p"),
        ],
        indiceSelectat=0,
    )
    ok = Buton(
        display=display,
        top=600,
        left=360,
        w=80,
        h=60,
        text="OK",
        culoareFundal=(46, 136, 32),
    )
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dificultate.deseneaza()
    btn_mod.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dificultate.selecteazaDupacoord(pos):
                            if not btn_mod.selecteazaDupacoord(pos):
                                if ok.selecteazaDupacoord(pos):
                                    return btn_juc.getValoare(), btn_alg.getValoare(), btn_dificultate.getValoare(), btn_mod.getValoare()
        pygame.display.update()


def verifica(jucator, tabla_joc, i, j):
    """
    Functia asta verifica daca un jucator anume mai poate sa ia o piesa a adversarului, cu o anume piesa a lui.

    Initial o facusem sa returneze True/False daca se mai poate lua o piesa dupa o mutare. Dar am decis sa
    returnez indicii piesei care mai poate fi luata pentru a putea folosi functia si atunci cand muta calculatorul.

    Am pus comentarii mai detaliate la fiecare pas al functiei.
    """
    indici = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
    jucator_opus = Joc.jucator_opus(jucator=jucator)

    # verific pentru fiecare jucator in parte pentru ca directiile de mutare sunt opuse pentru piesele simple
    # JMIN poate sa mute in sus cu piesele simple, iar JMAX doar in jos
    if jucator == Joc.JMIN:
        # verific primele doua directii, adica sus-stanga si sus-dreapta
        for ind in range(2):
            # daca este mutare valida peste 2 pozitii in directia respectiva
            if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                # trebuie sa verific daca ajung intr-o casuta goala si daca sar peste o piesa a jucatorului opus
                if tabla_joc[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                        tabla_joc[i + indici[ind][0]][j + indici[ind][1]].lower() == jucator_opus:
                    # returnez direct indicii directiei in care va fi luata piesa
                    # pentru ca inseamna ca exista cel putin o mutare posibila
                    return indici[ind]
        # pentru a verifica si celelalte 2 directii, trebuie sa vad daca piesa este piesa rege mai intai
        if tabla_joc[i][j] == jucator.upper():
            for ind in range(2, 4):
                if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                    if tabla_joc[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                            tabla_joc[i + indici[ind][0]][j + indici[ind][1]].lower() == jucator_opus:
                        return indici[ind]
    elif jucator == Joc.JMAX:
        # daca jucatorul e JMAX, verific mai intai directiile 2 si 3, adica in jos, iar daca e piesa rege verific si in sus
        for ind in range(2, 4):
            if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                if tabla_joc[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                        tabla_joc[i + indici[ind][0]][j + indici[ind][1]].lower() == jucator_opus:
                    return indici[ind]
        if tabla_joc[i][j] == jucator.upper():
            for ind in range(2):
                if mutare_valida(i + 2 * indici[ind][0], j + 2 * indici[ind][1]):
                    if tabla_joc[i + 2 * indici[ind][0]][j + 2 * indici[ind][1]] == Joc.GOL and \
                            tabla_joc[i + indici[ind][0]][j + indici[ind][1]].lower() == jucator_opus:
                        return indici[ind]
    # daca nu gasesc nicio mutare cu care iau o piesa, returnez lista goala.
    return []


def mutare(stare_curenta, pozitie_mouse, piesa_selectata):
    """
    Functia asta este cea care face mutarea unui jucator, nu a calculatorului.

    Ce face functia depinde de piesa_selectata. Aceasta e None initial, iar cand va fi selectata o piesa,
    piesa_selectata devine acea piesa. Apoi, cand are o piesa selectata deja, asteapta un click pe o casuta goala,
    iar daca aceasta este o casuta corespunzatoare unei mutari (in functie de piesa), va face mutarea in casuta aceea.

    Daca mutarea este una de capturare a unei piese a adversarului, ma folosesc si de functia verifica de mai sus, dar
    o folosesc doar sa returneze ceva , ca si cum ar returna True/False, adica atunci cand returneaza o lista cu cei
    doi indici, inseamna ca mai pot face o mutare in continuare. Daca returneaza o lista goala, e practic False, deci
    schimb jucatorul si piesa_selectata devine None din nou.

    Update: nu imi place in mod special cum arata functia, dar merge bine. Am adaugat verificarea jucatorului la linia
    685 si s-a cam dublat numarul de linii al functiei.
    """

    break_for = False
    jucator_opus = Joc.jucator_opus(stare_curenta.j_curent)
    for i in range(len(Joc.celuleGrid)):
        for j in range(len(Joc.celuleGrid)):

            if Joc.celuleGrid[i][j].collidepoint(pozitie_mouse):

                # daca dau click in celula cu o piesa de a mea
                if stare_curenta.tabla_joc.matr[i][j].lower() == stare_curenta.j_curent:
                    if piesa_selectata is None:
                        # daca nu era selectata nicio piesa, doar selectez piesa si astept click-ul urmator
                        piesa_selectata = [i, j]
                        break_for = True
                        break

                    # daca deja selectasem o piesa si dau click pe alta piesa de a mea, schimb piesa selectata
                    if piesa_selectata is not None:
                        piesa_selectata = [i, j]

                # daca dau click pe o casuta goala
                if stare_curenta.tabla_joc.matr[i][j] == Joc.GOL:
                    print(piesa_selectata)
                    if piesa_selectata is not None:
                        # se va intampla ceva doar in cazul in care deja selectasem o piesa.
                        # pana nu am o piesa selectata, pot da click oriunde fara niciun efect

                        indici = [[-1, -1], [-1, 1], [1, -1], [1, 1]]

                        if stare_curenta.j_curent == Joc.JMIN:
                            for ind in range(2):
                                if i == piesa_selectata[0] + indici[ind][0] and j == piesa_selectata[1] + indici[ind][1]:
                                    stare_curenta.tabla_joc.matr[i][j] = \
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                            piesa_selectata[1]]
                                    if i == 0:
                                        stare_curenta.tabla_joc.matr[i][j] = stare_curenta.tabla_joc.matr[i][j].upper()
                                    stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]] = Joc.GOL
                                    stare_curenta.tabla_joc.deseneaza_grid()
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                                    piesa_selectata = None
                                    break_for = True
                                    break

                                if i == piesa_selectata[0] + 2 * indici[ind][0] and j == piesa_selectata[1] + 2 * \
                                        indici[ind][1] and \
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                            piesa_selectata[1] + indici[ind][1]].lower() == jucator_opus:
                                    stare_curenta.tabla_joc.matr[i][j] = \
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                            piesa_selectata[1]]
                                    if i == 0:
                                        stare_curenta.tabla_joc.matr[i][j] = stare_curenta.tabla_joc.matr[i][j].upper()
                                    stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]] = Joc.GOL
                                    stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                        piesa_selectata[1] + indici[ind][1]] = Joc.GOL
                                    stare_curenta.tabla_joc.deseneaza_grid()

                                    # daca nu mai pot face o alta mutare dupa ce iau o piesa, schimb jucatorul, altfel, sunt lasat sa fac o alta mutare
                                    if not verifica(stare_curenta.j_curent, stare_curenta.tabla_joc.matr, i, j):
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        piesa_selectata = None
                                    else:
                                        piesa_selectata = [i, j]

                                    break_for = True
                                    break
                            if piesa_selectata:
                                if stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]] == stare_curenta.j_curent.upper():
                                    for ind in range(2, 4):
                                        if i == piesa_selectata[0] + indici[ind][0] and j == piesa_selectata[1] + \
                                                indici[ind][1] and \
                                                stare_curenta.tabla_joc.matr[i][j] == Joc.GOL:
                                            stare_curenta.tabla_joc.matr[i][j] = \
                                                stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]]
                                            stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                                piesa_selectata[1]] = Joc.GOL
                                            stare_curenta.tabla_joc.deseneaza_grid()
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                            piesa_selectata = None
                                            break_for = True
                                            break

                                        if i == piesa_selectata[0] + 2 * indici[ind][0] and j == piesa_selectata[
                                            1] + 2 * \
                                                indici[ind][1] and \
                                                stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                                    piesa_selectata[1] + indici[ind][1]].lower() == jucator_opus:
                                            stare_curenta.tabla_joc.matr[i][j] = \
                                                stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]]
                                            stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                                piesa_selectata[1]] = Joc.GOL
                                            stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                                piesa_selectata[1] + indici[ind][1]] = Joc.GOL
                                            stare_curenta.tabla_joc.deseneaza_grid()

                                            if not verifica(stare_curenta.j_curent, stare_curenta.tabla_joc.matr, i, j):
                                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                                piesa_selectata = None
                                            else:
                                                piesa_selectata = [i, j]

                                            break_for = True
                                            break

                        elif stare_curenta.j_curent == Joc.JMAX:
                            for ind in range(2, 4):
                                if i == piesa_selectata[0] + indici[ind][0] and j == piesa_selectata[1] + indici[ind][1]:
                                    stare_curenta.tabla_joc.matr[i][j] = \
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                        piesa_selectata[1]]
                                    if i == 7:
                                        stare_curenta.tabla_joc.matr[i][j] = stare_curenta.tabla_joc.matr[i][j].upper()
                                    stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]] = Joc.GOL
                                    stare_curenta.tabla_joc.deseneaza_grid()
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                                    piesa_selectata = None
                                    break_for = True
                                    break

                                if i == piesa_selectata[0] + 2 * indici[ind][0] and j == piesa_selectata[1] + 2 * \
                                        indici[ind][1] and \
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                            piesa_selectata[1] + indici[ind][1]].lower() == jucator_opus:
                                    stare_curenta.tabla_joc.matr[i][j] = \
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                        piesa_selectata[1]]
                                    if i == 7:
                                        stare_curenta.tabla_joc.matr[i][j] = stare_curenta.tabla_joc.matr[i][j].upper()
                                    stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]] = Joc.GOL
                                    stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                        piesa_selectata[1] + indici[ind][1]] = Joc.GOL
                                    stare_curenta.tabla_joc.deseneaza_grid()

                                    # daca nu mai pot face o alta mutare dupa ce iau o piesa, schimb jucatorul, altfel, sunt lasat sa fac o alta mutare
                                    if not verifica(stare_curenta.j_curent, stare_curenta.tabla_joc.matr, i, j):
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        piesa_selectata = None
                                    else:
                                        piesa_selectata = [i, j]

                                    break_for = True
                                    break
                            if piesa_selectata and stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]] == stare_curenta.j_curent.upper():
                                for ind in range(2):
                                    if i == piesa_selectata[0] + indici[ind][0] and j == piesa_selectata[1] + \
                                            indici[ind][1] and \
                                            stare_curenta.tabla_joc.matr[i][j] == Joc.GOL:
                                        stare_curenta.tabla_joc.matr[i][j] = \
                                            stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]]
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                            piesa_selectata[1]] = Joc.GOL
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        piesa_selectata = None
                                        break_for = True
                                        break

                                    if i == piesa_selectata[0] + 2 * indici[ind][0] and j == piesa_selectata[
                                        1] + 2 * \
                                            indici[ind][1] and \
                                            stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                                piesa_selectata[1] + indici[ind][1]].lower() == jucator_opus:
                                        stare_curenta.tabla_joc.matr[i][j] = \
                                            stare_curenta.tabla_joc.matr[piesa_selectata[0]][piesa_selectata[1]]
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0]][
                                            piesa_selectata[1]] = Joc.GOL
                                        stare_curenta.tabla_joc.matr[piesa_selectata[0] + indici[ind][0]][
                                            piesa_selectata[1] + indici[ind][1]] = Joc.GOL
                                        stare_curenta.tabla_joc.deseneaza_grid()

                                        if not verifica(stare_curenta.j_curent, stare_curenta.tabla_joc.matr, i, j):
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                            piesa_selectata = None
                                        else:
                                            piesa_selectata = [i, j]

                                        break_for = True
                                        break

        if break_for:
            break
    return stare_curenta, piesa_selectata


def main():
    global ADANCIME_MAX

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption("Staicu Bogdan - Dame")
    # dimensiunea ferestrei in pixeli
    ecran = pygame.display.set_mode(size=(807, 807))  # N *100+ N-1

    background_color = (71, 16, 16)
    ecran.fill(background_color)
    pygame.display.update()

    Joc.JMIN, tip_algoritm, dificultate, mod_joc = deseneaza_alegeri(ecran)
    ADANCIME_MAX = int(dificultate)
    Joc.initializeaza(ecran)
    Joc.JMAX = "a" if Joc.JMIN == "n" else "n"

    tabla_dame = [
        ["#", "a", "#", "a", "#", "a", "#", "a"],
        ["a", "#", "a", "#", "a", "#", "a", "#"],
        ["#", "a", "#", "a", "#", "a", "#", "a"],
        ["#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#"],
        ["n", "#", "n", "#", "n", "#", "n", "#"],
        ["#", "n", "#", "n", "#", "n", "#", "n"],
        ["n", "#", "n", "#", "n", "#", "n", "#"]
    ]
    if Joc.JMIN == "a":
        tabla_dame = [
            ["#", "n", "#", "n", "#", "n", "#", "n"],
            ["n", "#", "n", "#", "n", "#", "n", "#"],
            ["#", "n", "#", "n", "#", "n", "#", "n"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["a", "#", "a", "#", "a", "#", "a", "#"],
            ["#", "a", "#", "a", "#", "a", "#", "a"],
            ["a", "#", "a", "#", "a", "#", "a", "#"]
        ]

    tabla_curenta = Joc(tabla_dame)
    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, "n", ADANCIME_MAX)
    tabla_curenta.deseneaza_grid()

    if mod_joc == "c":
        piesa_selectata = None
        while True:

            if stare_curenta.j_curent == Joc.JMIN:
                # muta jucatorul

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()  # coordonatele clickului

                        # am observat ca aveam o bucata mare de cod aici, iar tot ce se modifica erau starea curenta si piesa_selectata
                        # asa ca am facut o functie separata pentru a nu copia acelasi cod de mai multe ori
                        stare_curenta, piesa_selectata = mutare(stare_curenta, pos, piesa_selectata)

                    if stare_curenta.j_curent == Joc.JMAX:
                        # JMIN si-a facut deja mutarea
                        break

            # --------------------------------
            else:  # jucatorul e JMAX (calculatorul)
                # Mutare calculator

                # cand e randul calculatorului, ma uit cate piese aveam eu inainte sa mute el si dupa ce muta el.
                # Daca dupa mutarea lui eu am mai putine piese, verific ce piesa a mutat el, adica piesa cu care mi-a luat mie o piesa
                # iar apoi daca dupa ce aplic functia "verifica" pe piesa lui si vad ca nu mai poate lua alta piesa, schimb jucatorul
                copie_matr = dc(stare_curenta.tabla_joc.matr)
                nr_piese_jmin_inainte = 0
                for i in range(8):
                    for j in range(8):
                        if stare_curenta.tabla_joc.matr[i][j] == Joc.JMIN:
                            nr_piese_jmin_inainte += 1

                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))
                if tip_algoritm == "1":
                    stare_actualizata = min_max(stare_curenta)
                else:  # tip_algoritm==2
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                # print("Tabla dupa mutarea calculatorului")
                # print(str(stare_curenta))

                stare_curenta.tabla_joc.deseneaza_grid()
                # preiau timpul in milisecunde de dupa mutare
                t_dupa = int(round(time.time() * 1000))
                print(
                    'Calculatorul a "gandit" timp de '
                    + str(t_dupa - t_inainte)
                    + " milisecunde."
                )

                if afis_daca_final(stare_curenta):
                    break

                nr_piese_jmin_dupa = 0
                for i in range(8):
                    for j in range(8):
                        if stare_curenta.tabla_joc.matr[i][j] == Joc.JMIN:
                            nr_piese_jmin_dupa += 1

                break_for = False
                if nr_piese_jmin_inainte != nr_piese_jmin_dupa:
                    # inseamna ca mi-a luat o piesa calculatorul
                    # trebuie sa vad ce piesa a luat
                    for i in range(8):
                        for j in range(8):
                            if copie_matr[i][j] == Joc.GOL and stare_curenta.tabla_joc.matr[i][j] == Joc.JMAX:
                                # daca am gasit o casuta unde nu era piesa de a lui si acum e, inseamna ca aia e ultima mutare
                                # indicii piesei cu care trebuie sa mai ia alta piesa sunt i si j

                                ii = dc(i)
                                jj = dc(j)

                                # directie_mutare e lista cu cei 2 indici ai directiei in care mai poate lua piesa
                                directie_mutare = verifica(Joc.JMAX, stare_curenta.tabla_joc.matr, ii, jj)
                                while directie_mutare:
                                    # cat timp poate lua o piesa, iau piesa, modific in matrice si updatez iar piesa
                                    stare_curenta.tabla_joc.matr[ii + 2 * directie_mutare[0]][
                                        jj + 2 * directie_mutare[1]] = stare_curenta.tabla_joc.matr[ii][jj]
                                    stare_curenta.tabla_joc.matr[ii][jj] = Joc.GOL
                                    stare_curenta.tabla_joc.matr[ii + directie_mutare[0]][
                                        jj + directie_mutare[1]] = Joc.GOL

                                    # daca se intampla sa ajunga pe ultima linie devine si piesa Rege
                                    if ii + 2 * directie_mutare[0] == 7:
                                        stare_curenta.tabla_joc.matr[ii + 2 * directie_mutare[0]][
                                            jj + 2 * directie_mutare[1]] = Joc.JMAX.upper()

                                    stare_curenta.tabla_joc.deseneaza_grid()

                                    # updatez indicii piesei curente dupa ce a luat piesa adversarului
                                    ii = ii + 2 * directie_mutare[0]
                                    jj = jj + 2 * directie_mutare[1]
                                    # si verific iar daca mai poate lua o piesa din pozitia noua in care a ajuns
                                    directie_mutare = verifica(Joc.JMAX, stare_curenta.tabla_joc.matr, ii, jj)
                                # cand iese din while, inseamna ca nu mai poate face mutari in continuare, deci schimb si jucatorul
                                stare_curenta.j_curent = Joc.JMIN
                                break_for = True
                                break
                        if break_for:
                            break
                # inseamna ca nu mi-a luat o piesa, doar a facut mutare simpla, caz in care doar schimb jucatorul direct
                stare_curenta.j_curent = Joc.JMIN
    else:
        piesa_selectata = None
        while True:

            if stare_curenta.j_curent == Joc.JMIN:
                # muta jucatorul 1

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()  # coordonatele clickului

                        # am observat ca aveam o bucata mare de cod aici, iar tot ce se modifica erau starea curenta si piesa_selectata
                        # asa ca am facut o functie separata pentru a nu copia acelasi cod de mai multe ori
                        stare_curenta, piesa_selectata = mutare(stare_curenta, pos, piesa_selectata)

                    if stare_curenta.j_curent == Joc.JMAX:
                        # JMIN si-a facut deja mutarea
                        break

            # --------------------------------

            else:  # jucatorul e JMAX (celalalt jucator)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()  # coordonatele clickului

                        stare_curenta, piesa_selectata = mutare(stare_curenta, pos, piesa_selectata)

                    if stare_curenta.j_curent == Joc.JMIN:
                        # JMAX si-a facut deja mutarea
                        break


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
