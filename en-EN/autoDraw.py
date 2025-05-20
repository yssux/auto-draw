import turtle
import sys
import os
sys.path.append(os.path.dirname(__file__))
from rich.console import Console
from rich import print
from rich.prompt import Prompt
from tkinter import colorchooser
from time import sleep
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / "en-EN"))
from myFunctions import px2ToCm2, sqArea, rectArea
#############Vars#######################"
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
print(r''' [bold yellow]
              _        _____                     
             | |      |  __ \                    
   __ _ _   _| |_ ___ | |  | |_ __ __ ___      __
  / _` | | | | __/ _ \| |  | | '__/ _` \ \ /\ / /
 | (_| | |_| | || (_) | |__| | | | (_| |\ V  V / 
  \__,_|\__,_|\__\___/|_____/|_|  \__,_| \_/\_/                     
                                                                            [/bold yellow] ''')
#############Start Function#############
try:
    def kickstart():
        try:
            sleep(0.50)
            print()
            console.print("[bold yellow]1.[/bold yellow] [cyan]Square[/cyan]")
            console.print("[bold yellow]2.[/bold yellow] [cyan]Rectangle[/cyan]")
            console.print("[bold yellow]3.[/bold yellow] [cyan]Triangles[/cyan]")
            console.print("[bold yellow]4.[/bold yellow] [cyan]Circle[/cyan]")
            print()
            console.print("[underline][bold magenta]The units are in pixels and degrees[/bold magenta][/underline]")

            # Get user choice with a prompt
            global forme
            print()
            forme = int(Prompt.ask("[bold blue]Choose an option (1-4) [/bold blue]"))

            match forme:
                case 1:
                    print()
                    console.print("[bold yellow]You have chosen the square![/bold yellow]")
                    cAsk()  # Call the square function (cAsk())
                case 2:
                    print()
                    console.print("[bold yellow]You have chosen the rectangle![/bold yellow]")
                    cAsk()  # Call the rectangle function (cAsk())
                case 3:
                    print()
                    console.print("[bold yellow]You have chosen the triangle![/bold yellow]")
                    console.print()
                    console.print("[underline]Three types are available:[/underline]")
                    import triangleTypes
                    triangleTypes.tkickstart()  # Call the triangle types function (tkickstart)
                case 4:
                    print()
                    console.print("[bold yellow]You have chosen the circle![/bold yellow]")
                    cAsk()


            if forme not in [1, 2, 3]:
                console.print("[bold red]This option does not exist[/bold red]")
                sleep(0.5)
                kickstart()  # Retry if invalid input
        except ValueError:
            console.print("[bold red]Please enter a valid number between 1 and 3[/bold red]")
            kickstart()  # Retry if invalid input
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

    def circle(rad, fill, source):
        screen.cv._rootwindow.deiconify()
        t = turtle.Turtle()
        if source == None:
            t.color(blk)
        elif fill == True and bool(source) == True:
            fcolor = source
            t.color(fcolor)
            t.begin_fill()
        t.circle(rad)
        if fill == True:
            t.end_fill()

    class Logic:
        def __init__(self):
            self.square = carr  # Associate square with carr function
            self.rect = rect  # Associate rect with rect function
            self.triangle = triang  # Associate triangle with triang function
            self.circ = circle #Associate circ with circle function
            self.outColored = None
            self.outSize = 1 # Default outline size

        def cChooser(self, outline):
            gui_chooser = colorchooser.askcolor()
            if gui_chooser[1] is not None:
                if outline:
                    self.outColor = gui_chooser[1]
                    print(f"Chosen outline color: {self.outColor}")
                    self.logicCaller()
                elif outline == False:
                    self.chosen_c = gui_chooser[1]
                    print(f"Chosen fill color: {self.chosen_c}")
                    self.outAsk()
            elif gui_chooser[1] is None:
                print("Please choose a color")
                if self.outColored:
                    self.cChooser(True)
                elif not self.outColored:
                    self.cChooser(False)

        def outAsk(self):
            global outline
            try:
                outline = str(Prompt.ask("[bold green]Do you want to add an outline to your shape, and optionally customize its color (1px in black by default otherwise)? (y/n)[/bold green] "))
            except ValueError:
                print("[bold red]Please enter a valid option")
                self.outAsk()
            if outline == "y":
                try:
                    self.outSize = float(Prompt.ask("[bold magenta]Specify the size of your outline [/bold magenta]"))
                    self.outColoring = str(Prompt.ask("[bold green]Do you want to choose a color for your outline? (y/n) [/bold green]"))
                except ValueError:
                    print("[bold red]Please enter a valid number/option")
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
                print("[bold red]Please enter a valid option")
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
                        self.c_carr = float(Prompt.ask("[bold yellow]Enter the side length you want [/bold yellow]"))
                    except ValueError:
                        print("[bold red]Please enter a valid number")
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
                        self.h_rect = float(Prompt.ask("[bold green]Enter the desired height [/bold green]"))
                        self.l_rect = float(Prompt.ask("[bold yellow]Enter the desired width [/bold yellow]"))
                    except ValueError:
                        print("[bold red]Please enter a valid number")
                        self.logicCaller()
                    if filling:
                        self.rect(self.h_rect, self.l_rect, True, self.chosen_c)
                    elif not filling:
                        self.rect(self.h_rect, self.l_rect, False, None)
                    if outlined and self.outColored:
                        self.outDraw(self.rect, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.rect, self.outSize, None)
                    elif not outlined and not filled and not self.outColored:
                        self.rect(self.h_rect, self.l_rect, False, None)
                    self.ending()
                    turtle.done()
                case 4:
                    print()
                    try:
                        self.c_rad = float(Prompt.ask("[bold green]Enter the desired radius [/bold green]"))
                    except ValueError:
                        print("[bold red]Please enter a valid number")
                        self.logicCaller()
                    if filling:
                        self.circ(self.c_rad,True, self.chosen_c)
                    elif not filling:
                        self.circ(self.c_rad,False, None)
                    if outlined and self.outColored:
                        self.outDraw(self.circ, self.outSize, self.outColor)
                    elif outlined and not self.outColored:
                        self.outDraw(self.circ, self.outSize, None)
                    elif not outlined and not filled and not self.outColored:
                        self.circ(self.c_rad, False, None)
                    self.ending()
                    turtle.done()

        def ending(self):
            if self.forme == 1 :
                fin = "square"
                srf = sqArea(self.c_carr)
                prps = f"side {self.c_carr} pixels"
            elif self.forme == 2:
                fin = "rectangle"
                srf = rectArea(self.h_rect, self.l_rect)
                prps = f"height {self.h_rect} and width {self.l_rect} pixels"
            elif self.forme == 4:
                fin = "circle"
                srf = round(3.141592653589793 * self.c_rad ** 2, 2)
                prps = f"radius {self.c_rad} pixels"
            print()
            print(f"[bold cyan]Your {fin}, [bold red]{prps}[/bold red], with an area of [bold red]{srf}[/bold red] pixels or [bold red]{px2ToCm2(srf)}[/bold red] centimeters has been drawn![/bold cyan]")
            sys.stdin.readline()
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
            elif shape == self.circ:
                self.outCircle(self.c_rad)

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
        def outCircle(self, rad):
            turtle.circle(rad)

    logic = Logic()


    def cAsk():
        global filled
        print()
        try:
            fill = Prompt.ask("[bold magenta]Do you want to fill your shape? (y/n) [/bold magenta]")
        except ValueError:
            print("Please enter a valid option")
            cAsk()
        sleep(0.25)
        if fill == "y":
            filled = True
            logic.cChooser(False)
        elif fill == "n":
            filled = False
            logic.outAsk()

        elif fill not in ["y", "n"]:
            print("Please enter a valid option")
            cAsk()
        else:
            pass
except Exception as e:
    print(f"[bold red]An error occurred: {e}[/bold red]")
    restart = Prompt.ask("[bold cyan]Do you want to restart the program? (y/n) [/bold cyan]")
    if restart == "y":
        kickstart()
    else:
        pass
kickstart()
