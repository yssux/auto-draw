import turtle
from myFunctions import sqArea, rectArea, triArea, px2ToCm2
import math
from tkinter import colorchooser
from time import sleep

screen = turtle.Screen()
screen.cv._rootwindow.withdraw()
turtle.setup(500, 500)
turtle.title("Dessin automatique")
turtle.hideturtle()
outline = False
filled = False
turtle.bgcolor("#212121")
blk = (0, 0, 0)


print('''

                 ____                _            _         _        
                |  _ \  ___  ___ ___(_)_ __      / \  _   _| |_ ___  
                | | | |/ _ \/ __/ __| | '_ \    / _ \| | | | __/ _ \ 
                | |_| |  __/\__ \__ \ | | | |  / ___ \ |_| | || (_) |
                |____/ \___||___/___/_|_| |_| /_/    \_\__,_|\__\___/   

                                                                            ''')
#############Start Function#############
try:
    def kickstart():
        try:
            sleep(0.75)
            print(" 1. Carré")
            print(" 2. Rectangle")
            print(" 3. Triangle (équilatéral)")
            print("Les unités sont en pixels et degrés")
            global forme
            forme = int(input("Choisissez une option : "))
            match forme:
                case 1:
                    print("Vous avez choisi le carré !")
                    cAsk()
                case 2:
                    print("Vous avez choisi le rectangle")
                    cAsk()
                case 3:
                    print("Vous avez choisi le triangle !")
                    cAsk()
            if forme not in [1, 2, 3]:
                print("Cette option est inexistante")
                sleep(0.5)
                kickstart()
        except ValueError:
            print("Veuillez entrer un nombre valide entre 1 et 3")
            kickstart()
    #geometry functions


    def rect(height, length, fill, source):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        if source == None:
            t.color(blk)
        elif fill == True and bool(source) == True:
            fcolor = source
            t.color(fcolor)
            t.begin_fill()

        t.forward(length)
        t.left(90)
        t.forward(height)
        t.left(90)
        t.forward(length)
        t.left(90)
        t.forward(height)
        if fill:
            t.end_fill()


    def carr(cote, fill, source):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        if source == None:
            t.color(blk)
        elif fill == True and bool(source) == True:
            fcolor = source
            t.color(fcolor)
            t.begin_fill()

        for x in range(0, 5):
            t.forward(cote)
            t.left(90)
        if fill == True:
            t.end_fill()

    def triang(cote,fill, source):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        if source == None:
            t.color(blk)
        elif fill == True and bool(source) == True:
            fcolor = source
            t.color(fcolor)
            t.begin_fill()

        for x in range(1, 4):
            t.forward(cote)
            t.left(360/3)
        if fill == True:
            t.end_fill()



    class Logic:
        def __init__(self):
            self.square = carr  # Associate square with carr function
            self.rect = rect  # Associate rect with rect function
            self.triangle = triang  # Associate triangle with triang function
            self.outColored = None
            self.outSize = 1 # Default outline size

        def cChooser(self, outline):
            gui_chooser = colorchooser.askcolor()
            if gui_chooser[1] is not None:
                if outline:
                    self.outColor = gui_chooser[1]
                    print(f"Couleur de contour choisie : {self.outColor}")
                    self.logicCaller()
                elif outline == False:
                    self.chosen_c = gui_chooser[1]
                    print(f"Couleur de remplissage choisie : {self.chosen_c}")
                    self.outAsk()
            elif gui_chooser[1] is None:
                print("Veuillez choisir une couleur")
                if self.outColored:
                    self.cChooser(True)
                elif not self.outColored:
                    self.cChooser(False)

        def outAsk(self):
            global outline
            try:
                outline = str(input("Voulez-vous ajouter un contour à votre forme, et, au choix, customizer sa couleur (1px en noir par défaut sinon) ? (y/n) : "))
            except ValueError:
                print("Veuillez entrer une option valide")
                self.outAsk()
            if outline == "y":
                try:
                    self.outSize = float(input("Précisez la taille de votre contour : "))
                    self.outColoring = str(input("Voulez vous choisir une couleur pour votre contour ? (y/n) : "))
                except ValueError:
                    print("Veuillez entrer un nombre/option valide")
                    self.outAsk()
                if self.outColoring == "y":
                    self.outColored = True
                    self.cChooser(True)
                else:
                    self.outColored = False
                outline = True
                self.logicCaller()
            elif outline == "n":
                outline = False
                self.logicCaller()
            else:
                print("Veuillez entrer une option valide")
                self.outAsk()

        def logicCaller(self):
            if outline and filled:
                self.logic(True, True)
            elif outline and not filled:
                self.logic(False, True)
            elif not outline and filled:
                self.logic(True, False)
            elif not outline and not filled:
                self.logic(False, False)

        def logic(self, filling, outlined):
            global c_carr, c_tri, h_rect, l_rect
            self.forme = forme
            match self.forme:
                case 1:
                    print()
                    try:
                        self.c_carr = float(input("Insérez la mesure du côté désiré : "))
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                        self.logicCaller()
                    if filling:
                        self.square(self.c_carr, True, self.chosen_c)
                    if outlined and self.outColored:
                        self.outDraw(self.square, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.square, self.outSize, None)
                    elif not outlined and not filled and not self.outColored:
                        self.square(self.c_carr, False, None)
                    self.ending()
                    turtle.done()

                case 2:
                    print()
                    try:
                        self.h_rect = float(input("Insérez la hauteur désirée : "))
                        self.l_rect = float(input("Insérez la largeur désirée : "))
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                        self.logicCaller()
                    if filling:
                        self.rect(self.h_rect, self.l_rect, True, self.chosen_c)
                    if outlined and self.outColored:
                        self.outDraw(self.rect, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.rect, self.outSize, None)
                    elif not outlined and not filled and not self.outColored:
                        self.rect(self.h_rect, self.l_rect, False, None)
                    self.ending()
                    turtle.done()


                case 3:
                    print()
                    try:
                        self.c_tri = float(input("Insérez le côté désiré pour ce triangle : "))
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                        self.logicCaller()
                    if filling:
                        self.triangle(self.c_tri, True, self.chosen_c)
                    if outlined and self.outColored:
                        self.outDraw(self.triangle, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.triangle, self.outSize, None)
                    else:
                        self.triangle(self.c_tri, False, None)
                    self.ending()
                    turtle.done()
        def ending(self):
            if self.forme == 1 :
                fin = "carré"
                srf = sqArea(self.c_carr)
                prps = f"de coté {self.c_carr} pixels"
            elif self.forme == 2:
                fin = "rectangle"
                srf = rectArea(self.h_rect, self.l_rect)
                prps = f"de hauteur {self.h_rect} et de largeur {self.l_rect} pixels"
            elif self.forme == 3 :
                fin = "triangle"
                htr = round(math.sqrt(3)/2 * self.c_tri, 2)
                srf = triArea(self.c_tri, htr)
                prps = f"de coté {self.c_tri} et d'hauteur {htr} pixels"
            print()
            print(f"Votre {fin}, {prps}, d'aire {srf} pixels ou {px2ToCm2(srf)} centimètres a été dessiné")

        def outDraw(self, shape, size, src):
            turtle.pensize(size)
            turtle.penup()
            turtle.setheading(0)
            turtle.pendown()
            if bool(src) == True:
                turtle.color(src)
            else:
                turtle.color(blk)

            if shape == self.square:
                self.outSq(self.c_carr)
            elif shape == self.triangle:
                self.outTri(self.c_tri)
            elif shape == self.rect:
                self.outRect(self.h_rect, self.l_rect)

            turtle.penup()
            turtle.home()

        def outSq(self, size):
            for _ in range(4):
                turtle.forward(size)
                turtle.left(90)

        def outRect(self, height, width):
            for _ in range(2):
                turtle.forward(width)
                turtle.left(90)
                turtle.forward(height)
                turtle.left(90)

        def outTri(self, side):
            for _ in range(3):
                turtle.forward(side)
                turtle.left(120)

    logic = Logic()


    def cAsk():
        global filled
        print()
        try:
            fill = input("Voulez vous remplir votre forme ? (y/n) : ")
        except ValueError:
            print("Veuillez entrer une option valide")
            cAsk()
        sleep(0.25)
        if fill == "y":
            filled = True
            logic.cChooser(False)
        elif fill == "n":
            filled = False
            logic.outAsk()

        elif fill not in ["y", "n"]:
            print("Veuillez entrer une option valide")
            cAsk()
        else:
            pass
except Exception as e:
    print(f"Une erreur est survenue : {e}")
    restart = input("Voulez-vous relancer le programme ? (y/n) : ")
    if restart == "y":
        kickstart()
    else:
        pass
if __name__ == "__main__":
    kickstart()