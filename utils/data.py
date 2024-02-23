import json
from random import randint
import statistics

from utils.enums import Categories
from utils.formatter import Formatter, console



class Data:
    def __init__(self):
        try:
            with open('pokeinfo.json') as json_file:
                pokes = json.load(json_file)
                self.pokes = pokes

        except:
            Formatter.error("Dataset not found! Please save pokeinfo.json in the same directory")

    def delete_entries_with(self, category: Categories, value: str):
        filtered_list = [poke for poke in self.pokes if not value in poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "includes (or is equal to)", value)

        self.pokes = filtered_list

    def delete_entries_with_exact(self, category: Categories, values):
        filtered_list = [poke for poke in self.pokes if not values == poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "is equal to", values if isinstance(values, str) else ", ".join(values))

        self.pokes = filtered_list

    def delete_entries_above(self, category: Categories, values):
        filtered_list = [poke for poke in self.pokes if  values > poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "is greater than", values)

        self.pokes = filtered_list

    def delete_entries_below(self, category: Categories, values):
        filtered_list = [poke for poke in self.pokes if  values < poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "is lower than", values)

        self.pokes = filtered_list
    
    def delete_entries_not_equal(self, category: Categories, values):
        filtered_list = [poke for poke in self.pokes if  values == poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "is not equal than", values)

        self.pokes = filtered_list
    

    def delete_entries_without(self, category: Categories, value: str):
        filtered_list = [poke for poke in self.pokes if value in poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "does not include", value)

        self.pokes = filtered_list

    

    def delete_entries_without_exact(self, category: Categories, values):
        filtered_list = [poke for poke in self.pokes if values == poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "is not equal to", values if isinstance(values, str) else ", ".join(values))

        self.pokes = filtered_list


    def delete_entries_without_all(self, category: Categories, value1: str, value2: str, value3: str = "", value4: str = "", value5: str = ""):
        filtered_list = [poke for poke in self.pokes if value1 in poke[category.value] or value2 in poke[category.value] or value3 in poke[category.value] or value4 in poke[category.value] or value5 in poke[category.value]]

        Formatter.print_deletion_text(len(self.pokes) - len(filtered_list), category.value, "does not include", value1 + " or " + value2)

        self.pokes = filtered_list


    def get_random_poke(self):
        return self.pokes[randint(0, len(self.pokes) - 1)]

    def get_poke(self, name: str):
        try:
            return [c for c in self.pokes if name.lower() == c["pokemonName"].lower()][0]
        except:
            return None


    def get_next_poke(self, mode: str):
        if mode == "random":
            return self.get_random_poke()


        scores = {}

        median_evolution = statistics.median([int(c[Categories.EVOLUTION_STAGE.value]) for c in self.pokes])
        median_height = statistics.median([int(c[Categories.HEIGHT.value]) for c in self.pokes])
        median_weight = statistics.median([int(c[Categories.WEIGHT.value]) for c in self.pokes])

        for poke in self.pokes:
            score = 0

            # year 
            score -= abs(median_evolution - int(poke[Categories.EVOLUTION_STAGE.value]))
            score -= abs(median_height - int(poke[Categories.HEIGHT.value]))
            score -= abs(median_weight - int(poke[Categories.WEIGHT.value]))
            


            for c in [Categories.TYPE1, Categories.TYPE2, Categories.HABITAT, Categories.COLOR]:
                if isinstance(poke[c.value], str):
                    score += self._get_number_of_occurences_for(c, poke[c.value])
                else:
                    for v in poke[c.value]:
                        score += self._get_number_of_occurences_for(c, v)

            
            scores[poke["pokemonName"]] = score


        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=False if mode == "worst" else True))


        Formatter.print_top_picks(list(scores)[:3], list(scores.values())[:3])


        return [c for c in self.pokes if c["pokemonName"] == list(scores)[0]][0]


        
    def _get_number_of_occurences_for(self, category: Categories, value: str):
        return sum(1 for c in self.pokes if value in c[category.value]) - 1



    def get_poke_table(self):
        self.poke_table = Formatter.init_poke_table("pokes in pool")

        pokes = self.pokes

        for poke in pokes:
            self.poke_table = Formatter.add_to_poke_table(self.poke_table, poke)

        return self.poke_table
