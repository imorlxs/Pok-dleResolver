import sys
import time
from rich import panel, console, table, box, prompt

from utils.enums import Categories


console = console.Console()

class Formatter:
    def prompt_mode():
        mode = prompt.Prompt.ask("Select mode", choices=["best", "worst", "random", "custom"], default="best")
        console.clear()
        return mode

    def prompt_poke():
        poke = prompt.Prompt.ask("Select starting pokemon")
        console.clear()
        return poke
    

    def print_new_poke(poke: str):
        console.print("\n")
        console.rule("Now guessing: [bold cyan]" + poke)


    def winning_screen(poke: str, steps: int) -> bool:
        console.print("\n")
        console.rule("[bold green]YOU WON")
        #console.print(panel.Panel("[green bold]YOU WON!!![/green bold]\n\nGuesses: [red bold]" + str(steps) + "[/red bold]\n\nThe winning pokemon was:\n[bold cyan]" + poke, padding=(2, 20)), justify="center")
        console.print(panel.Panel("The winning pokemon was:\n[bold cyan]" + poke + "[/bold cyan]\n\nGuesses: [red bold]" + str(steps), padding=(2, 20)), justify="center")
        console.print("\n")

        close = prompt.Prompt.ask("Do you want to close now?", choices=["y", "n"], default="y")
        
        if close:
            console.print("Goodbye!")
            return True

        return False

    
    def print_deletion_text(count: int, category: str, verb: str, value: str):
        if count > 0:
            console.print("Deleted [bold red]{}[/] entries, because their [italic bright_black]{}[/] {} [bold magenta]{}[/]".format(str(count), category, verb, value))


    def print_top_picks(names, scores):
        for name, score, index in zip(names, scores, range(len(names))):
            console.print("Top {} pick: [bold cyan]{}[/] with score [bold magenta]{}[/]".format(str(index + 1), name, str(score)))




    def init_poke_table(title: str):
        t =  table.Table(title=title, box=box.ROUNDED)

        t.add_column("Name", style="cyan bold")
        t.add_column("Type 1")
        t.add_column("Type 2")
        t.add_column("Habitat")
        t.add_column("Color")
        t.add_column("Evolution Stage")
        t.add_column("Height")
        t.add_column("Weight")

        return t

    def add_to_poke_table(t: table.Table, poke):
        t.add_row(
        poke["pokemonName"],
        poke[Categories.TYPE2.value],
        poke[Categories.TYPE1.value],
        poke[Categories.HABITAT.value],
        ", ".join(poke[Categories.COLOR.value]),
        str(poke[Categories.EVOLUTION_STAGE.value]),
        str(poke[Categories.HEIGHT.value]),
        str(poke[Categories.WEIGHT.value])
)

        return t

    def error(text):
        console.log(text, style="red bold")
        time.sleep(5)
        sys.exit()
