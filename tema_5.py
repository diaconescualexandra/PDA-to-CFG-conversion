import sys

def citire_date(fisier):
    with open(fisier, 'r') as f:
        pda1 = {}
        alfabet_pda = f.readline().strip().split(',')
        alfabet_stiva = f.readline().strip().split(',')
        initial_stiva_pda = f.readline().strip()
        stari_pda = f.readline().strip().split(',')
        stare_initiala_pda = f.readline().strip().split(',')
        tranzitii = {}

        for line in f:
            tranzitii_values = line.strip().split(',')
            key = (tranzitii_values[0], tranzitii_values[1], tranzitii_values[2])
            value = (tranzitii_values[3], tranzitii_values[4])
            tranzitii.setdefault(key, []).append(value)

        pda1['alfabet_pda'] = alfabet_pda
        pda1['alfabet_stiva'] = alfabet_stiva
        pda1['initial_stiva_pda'] = initial_stiva_pda
        pda1['stari_pda'] = stari_pda
        pda1['stare_initiala_pda'] = stare_initiala_pda
        pda1['tranzitii'] = tranzitii

        return pda1

def pda_2_cfg(pda):
  
    # variabile
    # pt fiecare pereche de stari (p,q) e creata o variabila de forma A{}{}'.format(p, q)
    variables = set(['A{}{}'.format(p, q)for p in pda['stari_pda'] for q in pda['stari_pda']])
    #terminalele sunt create concatenand alfabetul pda ului cu alfabetul stivei
    terminals = set(pda['alfabet_pda'] + pda['alfabet_stiva'])
    productions = []

    # varibila de start
    # formatul este de tipul 'Aq0qaccept' , unde q0 e starea initiala a pda ului
    start = 'A{}{}'.format(pda['stare_initiala_pda'][0], 'qaccept')

    # reguli vizitate
    reguli_vizitate = set()

    # regula 1: Apq → aArsb, p,q,r,s apartin starilor;    a,b apartin alfabetului pda ului;      u apartine stivei
    for p in pda['stari_pda']:
        for q in pda['stari_pda']:
            for r in pda['stari_pda']:
                for s in pda['stari_pda']:
                    for a in pda['alfabet_pda']:
                        for b in pda['alfabet_pda']:
                            for u in pda['alfabet_stiva']:
                                if (r, u) in pda['tranzitii'].get((p, a, ''), []) and (q, '') in pda['tranzitii'].get((s, b, u), []):
                                    prod = ('A{}{}'.format(p, q), '{}A{}{}{}{}'.format(
                                        a, 'A{}{}'.format(r, s), b, r, s))
                                    if prod not in reguli_vizitate:
                                        reguli_vizitate.add(prod)
                                        productions.append(prod)

    # regula 2: Apq → AprArq
    for p in pda['stari_pda']:
        for q in pda['stari_pda']:
            for r in pda['stari_pda']:
                prod = ('A{}{}'.format(p, q), 'A{}{}A{}{}'.format(p, r, r, q))
                if prod not in reguli_vizitate:
                    reguli_vizitate.add(prod)
                    productions.append(prod)

    # regula 3: App → epsilon
    for p in pda['stari_pda']:
        prod = ('A{}{}'.format(p, p), '')
        if prod not in reguli_vizitate:
            reguli_vizitate.add(prod)
            productions.append(prod)

    # CFG
    cfg = {'variabile': variables, 'terminale': terminals,
           'productii': productions, 'start': start}
    return cfg


if len(sys.argv) != 3:
    print("nr incorect de arg")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

pda_data = citire_date(input_file)
cfg_data = pda_2_cfg(pda_data)

with open(output_file, "w") as file:
    file.write(str(cfg_data))
