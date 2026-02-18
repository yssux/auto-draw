import turtle
import platform
import os
import struct
import subprocess as sb
import tempfile
import shutil
import uuid
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
pdf2svg_binpath = root_path / "bin" / "pdf2svg"
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
        raise FileNotFoundError("Ghostscript executable not found in expected locations.")
    
    gs_dir = get_gs_binpath()
    if platform.system() == "Windows":
        if arch == 64:
            EpsImagePlugin.gs_windows_binary = str(gs_path / "win" / "gswin64c.exe")
        else:
            EpsImagePlugin.gs_windows_binary = str(gs_path / "win" / "gswin32c.exe")
    else:
        if arch == 32:
            EpsImagePlugin.gs_linux_binary = str(gs_path / "linux" / "gs32")
        else:
            EpsImagePlugin.gs_linux_binary = str(gs_path / "linux" / "gs64")
    def run_cmd(args, timeout=None):
        try:
            proc = sb.run(list(map(str, args)), capture_output=True, text=True, timeout=timeout)
            return proc.returncode, proc.stdout, proc.stderr
        except Exception as e:
            return -1, "", str(e)
  
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
            # export temp paths
            self.pdf_path = None
            self.ps_path = None
            self.svg_path = None

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
            pdf_path = None
            ps_path = None
            try:
                try:
                    exp_confirm = Prompt.ask(f"[yellow]Would you like to export your {self.fin} to an image format? (y/n)[/]")
                except ValueError:
                    print("[bold red]Choose a valid option.")
                    return self.export_canvas()
                if exp_confirm.lower() == "y":
                    canvas = screen.getcanvas()
                    canvas.postscript(file="canvas.ps", colormode='color')
                    screen.cv._rootwindow.withdraw()
                    try:
                        fmt = Prompt.ask(f"[bold purple]In what format you'd like to save your {self.fin}?[/][white](jpeg/bmp/gif/png/svg) ")
                    except ValueError:
                        print("[bold red]Please choose a valid option.")
                        return self.export_canvas()
                    fmt = str(fmt).lower().strip()
                    fmt_ls = ["jpg", "jpeg", "bmp", "gif", "png", "svg"]
                    if fmt not in fmt_ls:
                        print("[bold red]Please choose an available format.")
                        return self.export_canvas()
                    if fmt == "jpg":
                        fmt = "jpeg"
                    ps_path = root_path / "canvas.ps"
                    pdf_path = root_path / f"{self.fin}.pdf"
                    if fmt != "svg":
                        img = Image.open(str(ps_path))
                        img.save(f"{self.fin}.{fmt}")
                        img.close()
                    else:
                        rc, out, err = run_cmd([gs_dir, "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite", f"-sOutputFile={str(pdf_path)}", str(ps_path)])
                        if rc != 0:
                            print(f"[bold red]Error creating PDF: returncode={rc}\n{err}[/bold red]")
                            return
                        pdf2svg_cmd = shutil.which("pdf2svg")
                        candidates = []
                        if pdf2svg_cmd:
                            candidates.append(Path(pdf2svg_cmd))
                        candidates += [pdf2svg_binpath / "win" / "pdf2svg64.exe", pdf2svg_binpath / "win" / "pdf2svg.exe", pdf2svg_binpath / "win" / "win_svg64.exe", pdf2svg_binpath / "win" / "win_svg32.exe", pdf2svg_binpath / "linux" / "pdf2svg64", pdf2svg_binpath / "linux" / "pdf2svg32"]
                        chosen = None
                        for c in candidates:
                            try:
                                if isinstance(c, Path):
                                    if not c.exists():
                                        continue
                                    cand = str(c)
                                else:
                                    cand = str(c)
                                v_rc, v_out, v_err = run_cmd([cand, "--version"])
                                if v_rc == 0 or v_out or v_err:
                                    chosen = cand
                                    break
                            except Exception:
                                continue
                        if not chosen:
                            print("[bold red]pdf2svg not found or invalid. Install it or add to PATH.[/bold red]")
                            return
                        svg_path = root_path / f"{self.fin}.svg"
                        temp_dir = Path(tempfile.gettempdir())
                        temp_pdf = temp_dir / (uuid.uuid4().hex + ".pdf")
                        temp_svg = temp_dir / (uuid.uuid4().hex + ".svg")
                        try:
                            shutil.copy2(str(pdf_path), str(temp_pdf))
                            conv_rc, conv_out, conv_err = run_cmd([chosen, str(temp_pdf), str(temp_svg)], timeout=30)
                            if conv_rc != 0 or not temp_svg.exists():
                                print(f"[bold red]Error converting to SVG (pdf2svg): rc={conv_rc}\n{conv_err}\n{conv_out}[/bold red]")
                                return
                            shutil.move(str(temp_svg), str(svg_path))
                        finally:
                            try:
                                if temp_pdf.exists():
                                    temp_pdf.unlink()
                            except Exception:
                                pass
                            try:
                                if temp_svg.exists():
                                    temp_svg.unlink()
                            except Exception:
                                pass
                    print(f"[bold blue]Your file has been saved to the current working directory (in .{fmt}).[/bold blue]")
                elif exp_confirm.lower() == "n":
                    pass
                else:
                    print("[bold red]Please choose a valid option.")
                    return self.export_canvas()
            except Exception as e:
                print(f"[bold red]An error occured while exporting : {e}")
            finally:
                try:
                    if pdf_path and pdf_path.exists():
                        pdf_path.unlink()
                except Exception:
                    pass
                try:
                    if ps_path and ps_path.exists():
                        ps_path.unlink()
                except Exception:
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
