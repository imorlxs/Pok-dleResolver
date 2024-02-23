from datetime import datetime
import sys

from utils.driver import Driver
from utils.data import Data
from utils.enums import Categories, Results
from utils.formatter import Formatter, console


console.clear()


with console.status("Loading Dataset..."):
    data = Data()

mode = Formatter.prompt_mode()

with console.status("Preparing Browser..."):
    driver = Driver()



won = False
steps = 0

result = None


while won is False:

    if mode == "custom" and steps == 0:
        poke = None
        while poke is None:
            poke = data.get_poke(Formatter.prompt_poke())
    else:
        poke = data.get_next_poke(mode)


    Formatter.print_new_poke(poke["pokemonName"])

    
    with console.status("Waiting for result..."):
        result = driver.input_poke(poke["pokemonName"])
        
        if len([r for r in result.values() if r == Results.GOOD]) >= 6:
            won = True

    if result is None and steps > 0: break

    steps += 1

    with console.status("Optimizing dataset..."):
        for category in Categories:
            if result[category.value] == Results.BAD:
                # poke has A and is bad
                if isinstance(poke[category.value], str): # Dont ask
                    data.delete_entries_with(category, poke[category.value]) # keep pokes without A
                else:
                    for value in poke[category.value]: # Nevermind
                        data.delete_entries_with(category, value) # keep pokes without A
                    
            
            elif result[category.value] == Results.GOOD:
                # poke has A and is good

                if category.value == Categories.EVOLUTION_STAGE or category.value == Categories.HEIGHT or category.value == Categories.WEIGHT:
                    data.delete_entries_not_equal(category, poke[category.value])
                else:
                    data.delete_entries_without_exact(category, poke[category.value]) # keep pokes with A and only A

                #data.delete_entries_without_exact(category, poke[category.value]) # keep pokes with A and only A


            elif result[category.value] == Results.PARTIAL:
                if len(poke[category.value]) == 1: # poke has A and only A and is partially correct -> desired poke has A + unknown
                    data.delete_entries_without(category, poke[category.value][0]) # delete pokes without A
                    data.delete_entries_with_exact(category, poke[category.value]) # delete pokes with A and only A

                else: # poke has A + B and is partially correct -> desired poke has A or B, but not A and B
                    data.delete_entries_with_exact(category, poke[category.value]) # delete pokes that have exactly A + B
                    data.delete_entries_without_all(category, *poke[category.value]) # keep pokes with either A or B
                
                
            elif result[category.value] == Results.SUPERIOR:            
                # Evolution stage, height or weight higher than A
                    data.delete_entries_below(category, poke[category.value]) # Delete pokes with lower category than A
                
            elif result[category.value] == Results.INFERIOR:
                # Evolution stage, height or weight lower than A
                for i in range(int(poke[category.value]), datetime.now().year + 1):    
                    data.delete_entries_above(category, poke[category.value]) # Delete pokes with higher category than A 


    if won:
        if Formatter.winning_screen(poke["pokemonName"], steps):
            driver.driver.quit()
            sys.exit()

    else:
        console.print("\n[bold red]" + str(len(data.pokes)) + "[/bold red] {} remaining\n".format("pokes" if len(data.pokes) > 1 else "poke"))   
        console.print(data.get_poke_table())
