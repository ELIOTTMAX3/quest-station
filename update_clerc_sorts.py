#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_clerc_sorts.py
Met à jour la liste des sorts de Clerc dans sorts.js.
- Retire "Clerc" des sorts spécifiés
- Ajoute "Clerc" à "Sens des pièges"
Ne modifie que les tableaux cl[] des sorts concernés.
"""

import json
import re
import sys

SORTS_JS = r"E:\12_LOGICIEL_DnD\quest-station\sorts.js"

# Sorts dont il faut RETIRER "Clerc"
RETIRER_CLERC = {
    "Aura de pureté",
    "Aura de vie",
    "Contresort",
    "Détection des pensées",
    "Domination de bête",
    "Double illusoire",
    "Éclat du soleil",
    "Esprit impénétrable",
    "Éveil",
    "Flétrissement",
    "Héroïsme",
    "Image miroir",
    "Identification",
    "Immobilisation de monstre",
    "Invisibilité",
    "Lame de feu",
    "Lien télépathique de Rary",
    "Lumières dansantes",
    "Métal brûlant",
    "Mot de pouvoir étourdissant",
    "Mot de pouvoir guérisseur",
    "Mot de pouvoir mortel",
    "Oeil magique",
    "Passage sans trace",
    "Peur",
    "Protection contre les armes",
    "Protections et sceaux",
    "Rayon de lune",
    "Rayon empoisonné",
    "Rayon de soleil",
    "Respiration aquatique",
    "Simulacre",
    "Sommeil",
    "Télékinésie",
    "Téléportation",
    "Tempête vengeresse",
}

# Sorts auxquels il faut AJOUTER "Clerc"
AJOUTER_CLERC = {
    "Sens des pièges",
}

def main():
    with open(SORTS_JS, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Extraire le tableau JSON : window.SORTS = [...]
    prefix = "window.SORTS = "
    if not content.startswith(prefix):
        print("ERREUR: format inattendu (pas de 'window.SORTS = ')")
        sys.exit(1)

    json_str = content[len(prefix):]
    # Retirer le point-virgule final si présent
    json_str = json_str.rstrip().rstrip(";")

    sorts = json.loads(json_str)
    print(f"Total sorts chargés : {len(sorts)}")

    retires = []
    ajoutes = []
    non_trouves_retirer = list(RETIRER_CLERC)
    non_trouves_ajouter = list(AJOUTER_CLERC)

    for sort in sorts:
        nom = sort.get("n", "")
        cl = sort.get("cl", [])

        if nom in RETIRER_CLERC:
            non_trouves_retirer = [x for x in non_trouves_retirer if x != nom]
            if "Clerc" in cl:
                cl.remove("Clerc")
                sort["cl"] = cl
                retires.append(nom)
            else:
                print(f"INFO: '{nom}' n'avait pas 'Clerc' dans cl[]")

        if nom in AJOUTER_CLERC:
            non_trouves_ajouter = [x for x in non_trouves_ajouter if x != nom]
            if "Clerc" not in cl:
                cl.append("Clerc")
                sort["cl"] = cl
                ajoutes.append(nom)
            else:
                print(f"INFO: '{nom}' avait déjà 'Clerc' dans cl[]")

    print(f"\nRetraits effectués ({len(retires)}) :")
    for n in sorted(retires):
        print(f"  - {n}")

    print(f"\nAjouts effectués ({len(ajoutes)}) :")
    for n in sorted(ajoutes):
        print(f"  + {n}")

    if non_trouves_retirer:
        print(f"\nATTENTION - sorts à retirer NON TROUVÉS dans sorts.js :")
        for n in non_trouves_retirer:
            print(f"  ? {n}")

    if non_trouves_ajouter:
        print(f"\nATTENTION - sorts à ajouter NON TROUVÉS dans sorts.js :")
        for n in non_trouves_ajouter:
            print(f"  ? {n}")

    # Réécrire le fichier
    new_json = json.dumps(sorts, ensure_ascii=False, separators=(',', ':'))
    new_content = prefix + new_json + ";\n"

    with open(SORTS_JS, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"\nFichier mis à jour : {SORTS_JS}")

if __name__ == "__main__":
    main()
