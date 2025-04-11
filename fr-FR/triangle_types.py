import turtle
import sys
import os
from rich.console import Console
from rich import print
from rich.prompt import Prompt
from tkinter import colorchooser
from time import sleep
from pathlib import Path
import math
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
sys.path.append(os.path.dirname(__file__))
sys.path.append(str(root_path / "fr-FR"))
import dessin_autom
from myFunctions import px2ToCm2 as cm, tri_equiArea, tri_isoArea, tri_rectArea
###########Logic#############
console = Console()
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
            console.print(f"[bold yellow]1.[/bold yellow] [cyan]Triangle équilatéral[/cyan]")
            console.print(f"[bold yellow]2.[/bold yellow] [cyan]Triangle rectangle[/cyan]")
            console.print(f"[bold yellow]3.[/bold yellow] [cyan]Triangle isocèle[/cyan]")
            console.print(f"[bold yellow]4.[/bold yellow] [cyan]Revenir au menu principal[/cyan]")
            global tforme
            tforme = int(Prompt.ask("[bold magenta]Choisissez une option [/bold magenta]"))
            match tforme:
                case 1:
                    console.print("[yellow]Vous avez choisi le triangle équilatéral ![/yellow]")
                    cAsk()
                case 2:
                    console.print("[yellow]Vous avez choisi le triangle rectangle ! [/yellow]")
                    cAsk()
                case 3:
                    console.print("[yellow )Vous avez choisi le triangle isocèle ![/yellow]")
                    cAsk()
                case 4:
                    dessin_autom.kickstart()
            if tforme not in [1, 2, 3]:
                console.print("[bold red]Cette option est inexistante[/bold red]")
                sleep(0.5)
                tkickstart()
        except ValueError:
            console.print("[bold red]Veuillez entrer un nombre valide entre 1 et 3[/bold red]")
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


    def tri_iso(side, base, fill, source):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        if source == None:
            t.color(blk)
        elif fill == True and bool(source) == True:
            fcolor = source
            t.color(fcolor)
            t.begin_fill()

        height = (side ** 2 - (base / 2) ** 2) ** 0.5
        # Draw the isosceles triangle
        angle = math.degrees(math.atan(height / (base / 2)))

        # Draw the isosceles triangle
        t.forward(base)  # Draw the base
        t.left(180 - angle)  # Turn to draw the first equal side
        t.forward(side)  # Draw the first equal side
        t.left(2 * angle)  # Turn to draw the second equal side
        t.forward(side)
        if fill == True:
            t.end_fill()

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
                    console.print(f"[cyan]Couleur de contour choisie : {self.outColor}")
                    self.tlogicCaller()
                elif outline == False:
                    self.chosen_c = gui_chooser[1]
                    print(f"[cyan]Couleur de remplissage choisie : {self.chosen_c}")
                    self.outAsk()
            elif gui_chooser[1] is None:
                console.print("[bold red]Veuillez choisir une couleur[/bold red]")
                if self.outColored:
                    self.cChooser(True)
                elif not self.outColored:
                    self.cChooser(False)

        def outAsk(self):
            global outline
            try:
                outline = str(Prompt.ask("[bold green]Voulez-vous ajouter un contour à votre forme, et, au choix, customizer sa couleur (1px en noir par défaut sinon) ? (y/n) [/bold green]"))
            except ValueError:
                console.print("[bold red]Veuillez entrer une option valide")
                self.outAsk()
            if outline == "y":
                try:
                    self.outSize = float(Prompt.ask("[bold blue]Précisez la taille de votre contour "))
                    self.outColoring = str(Prompt.ask("[bold green]Voulez vous choisir une couleur pour votre contour ? (y/n) "))
                except ValueError:
                    console.print("[bold red]Veuillez entrer un nombre/option valide")
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
                console.print("[bold red]Veuillez entrer une option valide")
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
                        self.c_equi = float(Prompt.ask("[bold yellow]Insérez la mesure du côté désiré "))
                    except ValueError:
                        console.print("[bold red]Veuillez entrer un nombre valide")
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
                        self.th_rect = float(Prompt.ask("[bold green]Insérez la hauteur désirée du triangle "))
                        self.tl_rect = float(Prompt.ask("[bold magenta]Insérez la largeur désirée du triangle "))
                    except ValueError:
                        console.print("[bold red]Veuillez entrer un nombre valide")
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
                        self.c_iso = float(Prompt.ask("[bold yellow]Insérez le côté désiré pour ce triangle "))
                        self.b_iso = float(input("[bold blue]Insérez la mesure de la base "))
                    except ValueError:
                        console.print("[bold red]Veuillez entrer un nombre valide")
                        self.tlogicCaller()
                    if filling:
                        self.tri_iso(self.c_iso,self.b_iso, True, self.chosen_c)
                    if outlined and self.outColored:
                        self.outDraw(self.tri_iso, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.tri_iso, self.outSize, None)
                    else:
                        self.tri_iso(self.c_iso,self.b_iso, False, None)
                    self.ending()
                    turtle.done()
        def ending(self):
            if self.tforme == 1 :
                fin = "triangle équilatéral"
                prps = f"de coté {self.c_equi} pixels"
                tsrf = f"de surface {tri_equiArea(self.c_equi, self.c_equi)} pixels ou {cm(tri_equiArea(self.c_equi, self.c_equi))} centimètres"
            elif self.tforme == 2:
                fin = "triangle rectangle"
                prps = f"de hauteur {self.th_rect} et de largeur {self.tl_rect} pixels"
                tsrf = f"de surface {tri_rectArea(self.tl_rect, self.th_rect)} pixels ou {cm(tri_rectArea(self.tl_rect,self.th_rect))} centimètres"
            elif self.tforme == 3 :
                fin = "triangle isocèle"
                h_iso = math.sqrt(self.c_iso ** 2 -(self.b_iso ** 2) / 2)
                prps = f"de coté {self.c_iso} et de base {self.b_iso} pixels"
                tsrf = f"de surface {tri_isoArea(self.b_iso, h_iso)} pixels ou {cm(tri_isoArea(self.b_iso, h_iso))}"
            print()
            console.print(f"[bold cyan]Votre [red]{fin}[/red], [red]{prps}[/red], [red]{tsrf}[/red] a été dessiné[/bold cyan] !")

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
            fill = Prompt.ask("[bold magenta]Voulez vous remplir votre forme ? (y/n) ")
        except ValueError:
            console.print("[bold red]Veuillez entrer une option valide")
            cAsk()
        sleep(0.25)
        if fill == "y":
            filled = True
            tlogic.cChooser(False)
        elif fill == "n":
            filled = False
            tlogic.outAsk()

        elif fill not in ["y", "n"]:
            console.print("[bold red]Veuillez entrer une option valide")
            cAsk()
        else:
            pass
except Exception as e:
    print(f"[bold red]Une erreur est survenue : [/bold red][yellow]{e}")
    restart = Prompt.ask("[bold blue]Voulez-vous relancer le programme ? (y/n) [/bold blue]")
    if restart == "y":
        tkickstart()
    else:
        pass

