import turtle
from time import sleep
from tkinter import colorchooser
import dessin_autom
import math
from myFunctions import px2ToCm2, triArea
###########Logic#############

screen = turtle.Screen()
screen.cv._rootwindow.withdraw()
turtle.setup(500, 500)
turtle.title("Dessin automatique")
turtle.hideturtle()
outline = False
filled = False
turtle.bgcolor("#212121")
blk = (0, 0, 0)

#############Start Function#############
try:
    def tkickstart():
        try:
            sleep(0.75)
            print()
            print(" 1. Triangle équilatéral")
            print(" 2. Triangle rectangle")
            print(" 3. Triangle isocèle")
            print(" 4. Revenir au menu principal")
            global tforme
            tforme = int(input("Choisissez une option : "))
            match tforme:
                case 1:
                    print("Vous avez choisi le triangle équilatéral !")
                    cAsk()
                case 2:
                    print("Vous avez choisi le triangle rectangle ! ")
                    cAsk()
                case 3:
                    print("Vous avez choisi le triangle isocèle !")
                    cAsk()
                case 4:
                    dessin_autom.kickstart()
            if tforme not in [1, 2, 3]:
                print("Cette option est inexistante")
                sleep(0.5)
                tkickstart()
        except ValueError:
            print("Veuillez entrer un nombre valide entre 1 et 3")
            tkickstart()
    #geometry functions

    def tri_equi(cote,fill, source):
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
            t.left(360 / 3)
        if fill == True:
            t.end_fill()


    def tri_iso(side, base):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        angle = math.acos((2 * side ** 2 - base ** 2) / (2 * side ** 2))
        angle_deg = math.degrees(angle)

        t.forward(side)
        t.left(180 - angle_deg)

        t.forward(side)
        t.left(180 - (2 * angle_deg))


    def tri_rect(a, b,fill, source):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        if source == None:
            t.color(blk)
        elif fill == True and bool(source) == True:
            fcolor = source
            t.color(fcolor)
            t.begin_fill()
        t = turtle.Turtle()
        # Calculate hypotenuse
        c = math.sqrt(a ** 2 + b ** 2)
        angle = math.degrees(math.atan2(b, a))
        # Move to starting position (optional)
        t.penup()
        t.goto(-a // 2, -b // 2)  # Centering the triangle
        t.pendown()
        # Draw the triangle correctly
        t.forward(a)  # Base
        t.left(90)
        t.forward(b)  # Height
        t.left(90 + angle)
        t.forward(c)  # Hypotenuse


    class TLogic:
        def __init__(self):
            self.tri_iso  = tri_iso  # Associate square with carr function
            self.tri_rect = tri_rect  # Associate rect with rect function
            self.tri_equi = tri_equi  # Associate triangle with triang function
            self.outColored = None
            self.outSize = 1 # Default outline size

        def cChooser(self, outline):
            gui_chooser = colorchooser.askcolor()
            if gui_chooser[1] is not None:
                if outline:
                    self.outColor = gui_chooser[1]
                    print(f"Couleur de contour choisie : {self.outColor}")
                    self.tlogicCaller()
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
                self.tlogicCaller()
            elif outline == "n":
                outline = False
                self.tlogicCaller()
            else:
                print("Veuillez entrer une option valide")
                self.outAsk()

        def tlogicCaller(self):
            if outline and filled:
                self.tlogic(True, True)
            elif outline and not filled:
                self.tlogic(False, True)
            elif not outline and filled:
                self.tlogic(True, False)
            elif not outline and not filled:
                self.tlogic(False, False)

        def tlogic(self, filling, outlined):
            global c_equi, c_iso, b_iso, th_rect, tl_rect
            self.tforme = tforme
            match self.tforme:
                case 1:
                    print()
                    try:
                        self.c_equi = float(input("Insérez la mesure du côté désiré : "))
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                        self.tlogicCaller()
                    if filling:
                        self.tri_equi(self.c_equi, True, self.chosen_c)
                    elif not filling and not outlined:
                        self.tri_equi(self.c_equi, False, None)

                    if outlined and self.outColored:
                        self.outDraw(self.tri_equi, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.tri_equi, self.outSize, None)
                    self.ending()
                    turtle.done()

                case 2:
                    print()
                    try:
                        self.th_rect = float(input("Insérez la hauteur désirée du triangle : "))
                        self.tl_rect = float(input("Insérez la largeur désirée du triangle: "))
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                        self.tlogicCaller()
                    if filling:
                        self.tri_rect(self.th_rect, self.tl_rect, True, self.chosen_c)
                    if outlined and self.outColored:
                        self.outDraw(self.tri_rect, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.tri_rect, self.outSize, None)
                    else:
                        self.tri_rect(self.th_rect, self.tl_rect, False, None)
                    self.ending()
                    turtle.done()


                case 3:
                    print()
                    try:
                        self.c_iso = float(input("Insérez le côté désiré pour ce triangle : "))
                        self.b_iso = float(input("Insérez la mesure de la base :"))
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                        self.tlogicCaller()
                    if filling:
                        self.tri_iso(self.c_tri,self.b_tri, True, self.chosen_c)
                    if outlined and self.outColored:
                        self.outDraw(self.tri_iso, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.tri_iso, self.outSize, None)
                    else:
                        self.triangle(self.c_tri,self.b_tri, False, None)
                    self.ending()
                    turtle.done()
        def ending(self):
            if self.tforme == 1 :
                fin = "triangle équilatéral"
                prps = f"de coté {self.c_equi} pixels"
            elif self.tforme == 2:
                fin = "triangle rectangle"
                prps = f"de hauteur {self.th_rect} et de largeur {self.tl_rect} pixels"
            elif self.tforme == 3 :
                fin = "triangle isocèle"
                prps = f"de coté {self.c_iso} et de base {self.b_iso} pixels"
            print()
            print(f"Votre {fin}, {prps}, a été dessiné")

        def outDraw(self, shape, size, src):
            turtle.pensize(size)
            turtle.penup()
            turtle.setheading(0)
            turtle.pendown()
            if bool(src) == True:
                turtle.color(src)
            else:
                turtle.color(blk)

            if shape == self.tri_equi:
                self.outTriEqui(self.c_equi)
            elif shape == self.tri_rect:
                self.outTriRect(self.th_rect, self.tl_rect)
            elif shape == self.tri_iso:
                self.outTriIso(self.c_iso, self.b_iso)

            turtle.penup()
            turtle.home()

        def outTriEqui(self,side):
            for _ in range(3):
                turtle.forward(side)
                turtle.left(120)

        def outTriIso(self,equal_side, base):
            angle = math.acos((2 * equal_side ** 2 - base ** 2) / (2 * equal_side ** 2))
            angle_deg = math.degrees(angle)

            turtle.forward(equal_side)
            turtle.left(180 - angle_deg)

            turtle.forward(equal_side)
            turtle.left(180 - (2 * angle_deg))

        def outTriRect(self,a, b):
            c = math.sqrt(a ** 2 + b ** 2)
            angle = math.degrees(math.atan2(b, a))
            # Move to starting position (optional)
            turtle.penup()
            turtle.goto(-a // 2, -b // 2)  # Centering the triangle
            turtle.pendown()
            # Draw the triangle correctly
            turtle.forward(a)  # Base
            turtle.left(90)
            turtle.forward(b)  # Height
            turtle.left(90 + angle)
            turtle.forward(c)  # Hypotenuse

    tlogic = TLogic()


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
            tlogic.cChooser(False)
        elif fill == "n":
            filled = False
            tlogic.outAsk()

        elif fill not in ["y", "n"]:
            print("Veuillez entrer une option valide")
            cAsk()
        else:
            pass
except Exception as e:
    print(f"Une erreur est survenue : {e}")
    restart = input("Voulez-vous relancer le programme ? (y/n) : ")
    if restart == "y":
        tkickstart()
    else:
        pass
if __name__ == "__main__":
    tkickstart()

