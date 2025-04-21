import random

# Facciones para las cartas
CARTAS_FACCION = {
    "Reinos del Norte": ["Siegfried","Síle de Tansarville","Soldier","Keira Metz","Catapult"],
    "Monstruos": ["Ghoul","Nekker","Vampire","Wyvern","Ice Gigant"]
}

def generar_carta_aleatoria(faccion):
    nombres = CARTAS_FACCION[faccion]
    nombre = random.choice(nombres)
    valor = random.randint(1,10)
    return nombre, valor   