import turtle
import platform
import os
from time import sleep
from tkinter import colorchooser
from rich.console import Console
from rich.prompt import Prompt
import math
from pathlib import Path
from PIL import Image, EpsImagePlugin
import sys
root_path = Path(__file__).resolve().parent.parent
gs_path = root_path / "ghostscript"
sys.path.append(str(root_path))
sys.path.append(os.path.dirname(__file__))
from myFunctions import px2ToCm2 as cm , tri_equiArea, tri_isoArea, tri_rectArea
###########Vars#############
console = Console()
screen = turtle.Screen()
screen.cv._rootwindow.withdraw()
turtle.setup(500, 500)
turtle.title("autoDraw")
turtle.hideturtle()
outline = False
filled = False
turtle.bgcolor("white")
blk = (0, 0, 0)

#############Start Function#############
try:
    def get_gs_executable():
        if platform.system() == "Windows":
            possible_paths = [
                gs_path / "gswin32c.exe"
            ]
        else:
            possible_paths = [
                gs_path / "gs"
            ]

        for path in possible_paths:
            if path.exists():
                return str(path)
        raise FileNotFoundError("Ghostscript executable not found in expected locations.")
    
    gs_dir = get_gs_executable()
    if platform.system() == "Windows":
        EpsImagePlugin.gs_windows_binary = gs_path
    else:
        EpsImagePlugin.gs_linux_binary = gs_path

    def tkickstart():
        try:
            sleep(0.75)
            print()
            console.print(f"[bold yellow]1.[/bold yellow] [cyan]Equilateral Triangle[/cyan]")
            console.print(f"[bold yellow]2.[/bold yellow] [cyan]Right Triangle[/cyan]")
            console.print(f"[bold yellow]3.[/bold yellow] [cyan]Isosceles Triangle[/cyan]")
            console.print(f"[bold yellow]4.[/bold yellow] [cyan]Return to Main Menu[/cyan]")
            global tforme
            tforme = int(Prompt.ask("[bold magenta]Choose an option [/bold magenta]"))
            match tforme:
                case 1:
                    console.print("[yellow]You chose the equilateral triangle![/yellow]")
                    cAsk()
                case 2:
                    console.print("[yellow]You chose the right triangle! [/yellow]")
                    cAsk()
                case 3:
                    console.print("[yellow]You chose the isosceles triangle![/yellow]")
                    cAsk()
                case 4:
                    import autoDraw
                    autoDraw.kickstart()
            if tforme not in [1, 2, 3]:
                console.print("[bold red]This option does not exist[/bold red]")
                sleep(0.5)
                tkickstart()
        except ValueError:
            console.print("[bold red]Please enter a valid number between 1 and 3[/bold red]")
            tkickstart()
    #geometry functions

    def tri_equi(side, fill, source):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        if source == None:
            t.color(blk)
        elif fill == True and bool(source) == True:
            fcolor = source
            t.color(fcolor)
            t.begin_fill()

        for x in range(1, 4):
            t.forward(side)
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

    def tri_rect(a, b, fill, source):
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
                    console.print(f"[cyan]Chosen outline color: {self.outColor}")
                    self.tlogicCaller()
                elif outline == False:
                    self.chosen_c = gui_chooser[1]
                    print(f"[cyan]Chosen fill color: {self.chosen_c}")
                    self.outAsk()
            elif gui_chooser[1] is None:
                console.print("[bold red]Please choose a color[/bold red]")
                if self.outColored:
                    self.cChooser(True)
                elif not self.outColored:
                    self.cChooser(False)

        def outAsk(self):
            global outline
            try:
                outline = str(Prompt.ask("[bold green]Do you want to add an outline to your shape, and optionally customize its color (1px in black by default otherwise)? (y/n) [/bold green]"))
            except ValueError:
                console.print("[bold red]Please enter a valid option")
                self.outAsk()
            if outline == "y":
                try:
                    self.outSize = float(Prompt.ask("[bold blue]Specify the size of your outline "))
                    self.outColoring = str(Prompt.ask("[bold green]Do you want to choose a color for your outline? (y/n) "))
                except ValueError:
                    console.print("[bold red]Please enter a valid number/option")
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
                console.print("[bold red]Please enter a valid option")
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
                        self.c_equi = float(Prompt.ask("[bold yellow]Insert the desired side length "))
                    except ValueError:
                        console.print("[bold red]Please enter a valid number")
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
                        self.th_rect = float(Prompt.ask("[bold green]Insert the desired height of the triangle "))
                        self.tl_rect = float(Prompt.ask("[bold magenta]Insert the desired width of the triangle "))
                    except ValueError:
                        console.print("[bold red]Please enter a valid number")
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
                        self.c_iso = float(Prompt.ask("[bold yellow]Insert the desired side for this triangle "))
                        self.b_iso = float(input("[bold blue]Insert the base length "))
                    except ValueError:
                        console.print("[bold red]Please enter a valid number")
                        self.tlogicCaller()
                    if filling:
                        self.tri_iso(self.c_iso, self.b_iso, True, self.chosen_c)
                    if outlined and self.outColored:
                        self.outDraw(self.tri_iso, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.tri_iso, self.outSize, None)
                    else:
                        self.tri_iso(self.c_iso, self.b_iso, False, None)
                    self.ending()
                    turtle.done()
        def ending(self):
            if self.tforme == 1 :
                self.fin = "equilateral triangle"
                prps = f"with side {self.c_equi} pixels"
                tsrf = f"with area {tri_equiArea(self.c_equi, self.c_equi)} pixels or {cm(tri_equiArea(self.c_equi, self.c_equi))} centimeters"
            elif self.tforme == 2:
                self.fin = "right triangle"
                prps = f"with height {self.th_rect} and width {self.tl_rect} pixels"
                tsrf = f"with area {tri_rectArea(self.tl_rect, self.th_rect)} pixels or {cm(tri_rectArea(self.tl_rect,self.th_rect))} centimeters"
            elif self.tforme == 3 :
                self.fin = "isosceles triangle"
                h_iso = math.sqrt(self.c_iso ** 2 -(self.b_iso ** 2) / 2)
                prps = f"with side {self.c_iso} and base {self.b_iso} pixels"
                tsrf = f"with area {tri_isoArea(self.b_iso, h_iso)} pixels or {cm(tri_isoArea(self.b_iso, h_iso))}"
            print()
            console.print(f"[bold cyan]Your [red]{self.fin}[/red], [red]{prps}[/red], [red]{tsrf}[/red] has been drawn[/bold cyan]!")
            self.export_canvas()
        def export_canvas(self):
            try:
                try:
                    exp_confirm = Prompt.ask(f"[yellow]Would you like to export your {self.fin} to an image format ? (y/n)[/]")
                except ValueError:
                    print("Choose a valid option")
                    self.export_canvas()
                if exp_confirm == "y":
                    canvas = screen.getcanvas()
                    canvas.postscript(file="canvas.ps", colormode='color')
                    turtle.bye()
                    try:
                        format = str(Prompt.ask(f"[bold purple]In what format you'd like to save your {self.fin} ?[/][white](jpeg/bmp/gif/png)"))
                    except ValueError:
                        print("Please choose a valid option")
                    if format not in ["jpeg","bmp","gif","png"]:
                        print("Please choose an available format")
                        self.exp_confirm()
                    img = Image.open("canvas.ps")
                    img.save(f"{self.fin}.{format}")
                    print(f"[bold blue]Your File has been saved to the current working directory (.ps and .{format}).")
                elif exp_confirm == "n":
                    pass
                else:
                    print("Please choose a valid option")
            except Exception as e:
                print(f"An error occured while exporting : {e}")
            finally:
                sys.stdout.readline()
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
            fill = Prompt.ask("[bold magenta]Do you want to fill your shape? (y/n) ")
        except ValueError:
            console.print("[bold red]Please enter a valid option")
            cAsk()
        sleep(0.25)
        if fill == "y":
            filled = True
            tlogic.cChooser(False)
        elif fill == "n":
            filled = False
            tlogic.outAsk()

        elif fill not in ["y", "n"]:
            console.print("[bold red]Please enter a valid option")
            cAsk()
        else:
            pass
except Exception as e:
    print(f"[bold red]An error occurred: [/bold red][yellow]{e}")
    restart = Prompt.ask("[bold blue]Do you want to restart the program? (y/n) [/bold blue]")
    if restart == "y":
        tkickstart()
    else:
        pass
