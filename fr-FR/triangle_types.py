import turtle
import platform
import os
import struct
import subprocess as sb
from time import sleep
from tkinter import colorchooser
try:
    from rich.console import Console
    from rich import print
    from rich.prompt import Prompt
    console = Console()
except ModuleNotFoundError:
    rich = None
    console = None
import math
from pathlib import Path
from PIL import Image, EpsImagePlugin
import sys
###########Vars#############
screen = turtle.Screen()
screen.cv._rootwindow.withdraw()
twindow = screen.getcanvas().winfo_toplevel()
twindow.geometry("600x600")
turtle.setup(500, 500)
turtle.title("autoDraw")
turtle.hideturtle()
outline = False
filled = False
turtle.bgcolor("white")
blk = (0, 0, 0)
arch = struct.calcsize("P")*8
root_path = Path(__file__).resolve().parent.parent
gs_path = root_path / "ghostscript"
sys.path.append(str(root_path))
from myFunctions import px2ToCm2 as cm , tri_equiArea, tri_isoArea, tri_rectArea
sys.path.append(str(root_path / "en-EN"))
gs_path = root_path / "bin" / "ghostscript"
pdf2svg_binpath = str(root_path / "bin" / "pdf2svg")
#############Start Function#############
try:
    def get_gs_binpath():
        if platform.system() == "Windows":
            if arch == 64:
                possible_paths = [gs_path / "win" / "gswin64c.exe"]
            else:
                possible_paths = [gs_path / "win"/ "gswin32c.exe"]
        else:
            if arch == 64:
                possible_paths = [gs_path / "linux" / "gs64"]
            else:
                possible_paths = [gs_path / "linux" / "gs32"]
        for path in possible_paths:
            if path.exists():
                return str(path)
        raise FileNotFoundError("Les binaires Ghostscript n'ont pas été trouvées aux répertoires attendus.")
    gs_dir = get_gs_binpath()
    if platform.system() == "Windows":
        if arch == "64":
            EpsImagePlugin.gs_windows_binary = str(gs_path / "win" / "gswin64c.exe")
        else:
            EpsImagePlugin.gs_windows_binary = str(gs_path / "win" / "gswin32c.exe")
    else:
        if arch == "32":
            EpsImagePlugin.gs_linux_binary = str(gs_path / "linux" / "gs32")
        else:
            EpsImagePlugin.gs_linux_binary = str(gs_path / "linux" / "gs64")
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
                    import dessin_autom
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
            self.export_canvas()
        def export_canvas(self):
            try:
                try:
                    exp_confirm=Prompt.ask(f"[yellow]Would you like to export your {self.fin} to an image format? (y/n)[/]")
                except ValueError:
                    print("[bold red]Choose a valid option.")
                    return self.export_canvas()
                if exp_confirm.lower()=="y":
                    canvas=screen.getcanvas()
                    canvas.postscript(file="canvas.ps",colormode='color')
                    screen.cv._rootwindow.withdraw()
                    try:
                        format=Prompt.ask(f"[bold purple]In what format you'd like to save your {self.fin}?[/][white](jpeg/bmp/gif/png/svg) ").lower()
                    except ValueError:
                        print("[bold red]Please choose a valid option.")
                        return self.export_canvas()
                    fmt_ls=["jpg","jpeg","bmp","gif","png", "svg"]
                    if format not in fmt_ls:
                        print("[bold red]Please choose an available format.")
                        return self.export_canvas()
                    if format=="jpg":
                        format="jpeg"
                    if format != "svg":
                        img=Image.open("canvas.ps")
                        img.save(f"{self.fin}.{format.rstrip()}")
                        img.close()
                    elif format == "svg":
                        pdf_path = root_path / f"{self.fin}.pdf"
                        svg_path = root_path / f"{self.fin}.svg"
                        ps_path = root_path / "canvas.ps"
                        if platform.system() == "Windows":
                            gs_exec = "gswin64c.exe" if arch == "64" else "gswin32c.exe"
                            pdf2svg_exec = "win_svg64.exe" if arch == "64" else "win_svg32.exe"
                            gs_full_path = gs_path / "win" / gs_exec
                            pdf2svg_full_path = Path(pdf2svg_binpath) / "win" / pdf2svg_exec
                        elif platform.system() == "Linux":
                            gs_exec = "gs64" if arch == "64" else "gs32"
                            pdf2svg_exec = "pdf2svg64" if arch == "64" else "pdf2svg32"
                            gs_full_path = root_path / "linux" / gs_exec
                            pdf2svg_full_path = Path(pdf2svg_binpath) / "linux" / pdf2svg_exec
                        else:
                            print("[bold red]Your system isn't currently supported![/bold red]")
                            return
                        sb.run([str(gs_full_path), "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite", f"-sOutputFile={str(pdf_path)}", str(ps_path)], check=True)
                        sb.run([str(pdf2svg_full_path), str(pdf_path), str(svg_path)], check=True)
                    print(f"[bold blue]Your file has been saved to the current working directory (in .{format}).[/bold blue]")
                elif exp_confirm.lower()=="n":
                    pass
                else:
                    print("[bold red]Please choose a valid option.")
                    return self.export_canvas()
            except Exception as e:
                print("[bold red]An error occured while exporting : {e}")
            finally:
                if pdf_path != False or ps_path != False:
                    if pdf_path.exists():
                        pdf_path.unlink()
                    if ps_path.exists():
                        ps_path.unlink()
                else:
                    pass
                input("Press Enter to exit...")
                sys.exit()  
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

