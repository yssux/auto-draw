import turtle
import sys
import os
import struct
import subprocess as sb
import tempfile
import shutil
import uuid
sys.path.append(os.path.dirname(__file__))
try:
    from rich.console import Console
    from rich import print
    from rich.prompt import Prompt
    console = Console()
except ModuleNotFoundError:
    print("Module Rich introuvable (stdout sans couleurs)")
    rich = None
    console = None
from tkinter import colorchooser
from time import sleep
from pathlib import Path
from PIL import Image, EpsImagePlugin
import platform
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / "en-EN"))
from myFunctions import px2ToCm2, sqArea, rectArea
#########################Vars###########################
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
print(root_path)
gs_path = root_path / "bin" / "ghostscript"
pdf2svg_binpath = root_path / "bin" / "pdf2svg"
print( r'''[bold yellow]   
                     ____                _            _         _        
                    |  _ \  ___  ___ ___(_)_ __      / \  _   _| |_ ___  
                    | | | |/ _ \/ __/ __| | '_ \    / _ \| | | | __/ _ \ 
                    | |_| |  __/\__ \__ \ | | | |  / ___ \ |_| | || (_) |
                    |____/ \___||___/___/_|_| |_| /_/    \_\__,_|\__\___/  [/bold yellow]''')
#############Start Functions#############
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
        """Run a command and return (returncode, stdout, stderr)."""
        try:
            proc = sb.run(list(map(str, args)), capture_output=True, text=True, timeout=timeout)
            return proc.returncode, proc.stdout, proc.stderr
        except Exception as e:
            return -1, "", str(e)

    def kickstart():
        try:
            sleep(0.50)
            print()
            console.print("[bold yellow]1.[/bold yellow] [cyan]Carré[/cyan]")
            console.print("[bold yellow]2.[/bold yellow] [cyan]Rectangle[/cyan]")
            console.print("[bold yellow]3.[/bold yellow] [cyan]Triangles[/cyan]")
            console.print("[bold yellow]4.[/bold yellow] [cyan]Cercle[/cyan]")
            print()
            console.print("[underline][bold magenta]Les unités sont en pixels et degrés[/bold magenta][/underline]")

            # Get user choice with a prompt
            global forme
            print()
            forme = int(Prompt.ask("[bold blue]Choisissez une option (1-4) [/bold blue]"))

            match forme:
                case 1:
                    print()
                    console.print("[bold yellow]Vous avez choisi le carré ![/bold yellow]")
                    cAsk()  # Call the square function (cAsk())
                case 2:
                    print()
                    console.print("[bold yellow]Vous avez choisi le rectangle ![/bold yellow]")
                    cAsk()  # Call the rectangle function (cAsk())
                case 3:
                    print()
                    console.print("[bold yellow]Vous avez choisi le triangle ![/bold yellow]")
                    console.print()
                    console.print("[underline]Trois types sont disponibles :[/underline]")
                    import triangle_types
                    triangle_types.tkickstart()  # Call the triangle types function (tkickstart)
                case 4:
                    print()
                    console.print("[bold yellow]Vous avez choisi le cercle![/bold yellow]")
                    cAsk()


            if forme not in [1, 2, 3]:
                console.print("[bold red]Cette option est inexistante[/bold red]")
                sleep(0.5)
                kickstart()  # Retry if invalid input
        except ValueError:
            console.print("[bold red]Veuillez entrer un nombre valide entre 1 et 3[/bold red]")
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
            # paths used during export
            self.pdf_path = None
            self.ps_path = None
            self.svg_path = None

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
                outline = str(Prompt.ask("[bold green]Voulez-vous ajouter un contour à votre forme, et, au choix, customizer sa couleur (1px en noir par défaut sinon) ? (y/n)[/bold green] "))
            except ValueError:
                print("[bold red]Veuillez entrer une option valide")
                self.outAsk()
            if outline == "y":
                try:
                    self.outSize = float(Prompt.ask("[bold magenta]Précisez la taille de votre contour [/bold magenta]"))
                    self.outColoring = str(Prompt.ask("[bold green]Voulez vous choisir une couleur pour votre contour ? (y/n) [/bold green]"))
                except ValueError:
                    print("[bold red]Veuillez entrer un nombre/option valide")
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
                print("[bold red]Veuillez entrer une option valide")
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
                        self.c_carr = float(Prompt.ask("[bold yellow]Insérez la mesure du côté désiré [/bold yellow]"))
                    except ValueError:
                        print("[bold red]Veuillez entrer un nombre valide")
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
                        self.h_rect = float(Prompt.ask("[bold green]Insérez la hauteur désirée [/bold green]"))
                        self.l_rect = float(Prompt.ask("[bold yellow]Insérez la largeur désirée [/bold yellow]"))
                    except ValueError:
                        print("[bold red]Veuillez entrer un nombre valide")
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
                        self.c_rad = float(Prompt.ask("[bold green]Insérez le rayon désiré [/bold green]"))
                    except ValueError:
                        print("[bold red]Veuillez entrer un nombre valide")
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
                self.fin = "carré"
                srf = sqArea(self.c_carr)
                prps = f"de coté {self.c_carr} pixels"
            elif self.forme == 2:
                self.fin = "rectangle"
                srf = rectArea(self.h_rect, self.l_rect)
                prps = f"de hauteur {self.h_rect} et de largeur {self.l_rect} pixels"
            elif self.forme == 4:
                self.fin = "cercle"
                srf = round(3.141592653589793 * self.c_rad ** 2, 2)
                prps = f"de rayon {self.c_rad} pixels"
            print()
            print(f"[bold cyan]Votre {self.fin}, [bold red]{prps}[/bold red], d'aire [bold red]{srf}[/bold red] pixels ou [bold red]{px2ToCm2(srf)}[/bold red] centimètres a été dessiné ![/bold cyan]")
            self.export_canvas()
        def export_canvas(self):
            pdf_path = None
            ps_path = None
            try:
                try:
                    exp_confirm = Prompt.ask(f"[bold yellow]Souhaitez-vous exporter votre {self.fin} au format image ? (y/n)[/]")
                except ValueError:
                    print("[bold red]Choisissez une option valide")
                    return self.export_canvas()
                if exp_confirm.lower() == "y":
                    canvas = screen.getcanvas()
                    canvas.postscript(file="canvas.ps", colormode='color')
                    screen.cv._rootwindow.withdraw()
                    try:
                        fmt = str(Prompt.ask(f"[bold purple]Dans quel format souhaitez-vous enregistrer votre {self.fin} ?[/][white](jpeg/bmp/gif/png/svg)"))
                    except ValueError:
                        print("[bold red]Veuillez choisir une option valide")
                        return
                    fmt = fmt.lower().strip()
                    fmt_ls = ["jpeg","jpg", "bmp", "gif", "png", "svg"]
                    if fmt not in fmt_ls:
                        print("[bold red]Veuillez choisir un format disponible")
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
                        # create PDF using Ghostscript and capture output
                        rc, out, err = run_cmd([gs_dir, "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite", f"-sOutputFile={str(pdf_path)}", str(ps_path)])
                        if rc != 0:
                            print(f"[bold red]Erreur lors de la création du PDF : returncode={rc}\n{err}[/bold red]")
                            return
                        # prepare pdf2svg command candidates
                        import shutil as _shutil
                        pdf2svg_cmd = _shutil.which("pdf2svg")
                        candidates = []
                        if pdf2svg_cmd:
                            candidates.append(Path(pdf2svg_cmd))
                        # prefer architecture-specific and existing repo binaries
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
                                # quick validation: --help or --version
                                v_rc, v_out, v_err = run_cmd([cand, "--version"])
                                if v_rc == 0 or v_out or v_err:
                                    chosen = cand
                                    break
                            except Exception:
                                continue
                        if not chosen:
                            print("[bold red]pdf2svg introuvable ou invalide. Installez pdf2svg ou ajoutez-le au PATH.[/bold red]")
                            return
                        svg_path = root_path / f"{self.fin}.svg"
                        # use ASCII-only temp files for subprocess calls to avoid encoding issues
                        temp_dir = Path(tempfile.gettempdir())
                        temp_pdf = temp_dir / (uuid.uuid4().hex + ".pdf")
                        temp_svg = temp_dir / (uuid.uuid4().hex + ".svg")
                        try:
                            shutil.copy2(str(pdf_path), str(temp_pdf))
                            # try conversion, print child stderr on failure and try no more than once per candidate
                            conv_rc, conv_out, conv_err = run_cmd([chosen, str(temp_pdf), str(temp_svg)], timeout=30)
                            if conv_rc != 0 or not temp_svg.exists():
                                print(f"[bold red]Erreur lors de la conversion vers SVG (pdf2svg): rc={conv_rc}\n{conv_err}\n{conv_out}[/bold red]")
                                return
                            # move generated svg to final location
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
                    print(f"[bold blue]Votre fichier a été enregistré dans le répertoire de travail actuel (.ps et .{fmt}).")
                elif exp_confirm.lower() == "n":
                    pass
                else:
                    print("Veuillez choisir une option valide")
                    return self.export_canvas()
            except Exception as e:
                print(f"[bold red]Une erreur est survenue lors de l'exportation : {e}")
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
                Prompt.ask("[bold white]Appuyez sur Entrée pour quitter...")
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
            fill = Prompt.ask("[bold magenta]Voulez vous remplir votre forme ? (y/n) [/bold magenta]")
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
    print(f"[bold red]Une erreur est survenue : {e}[/bold red]")
    restart = Prompt.ask("[bold cyan]Voulez-vous relancer le programme ? (y/n) [/bold cyan]")
    if restart == "y":
        kickstart()
    else:
        pass
kickstart()