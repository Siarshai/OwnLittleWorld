from plants.plant import *
from plants.plantdnalibrary import PlantDNALibrary

if __name__ == "__main__":
    plant = Plant()
    print(PlantDNALibrary.basic["dna_white"])
    print(plant.dna["dna_white"])
    print(plant.reproduction_turns)

