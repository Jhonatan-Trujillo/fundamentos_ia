# motor_inferencia.py
# Motor de inferencia: encadenamiento hacia adelante
# Reglas y hechos iniciales
rules = [(['raining'], 'wet'),
         (['wet','have_umbrella'], 'use_umbrella'),
         (['use_umbrella'], 'stay_dry')]

facts = {'raining', 'have_umbrella'}

# Encadenamiento hacia adelante (una pasada)
for conds, concl in rules:
    if all(c in facts for c in conds):
        facts.add(concl)

print(facts)