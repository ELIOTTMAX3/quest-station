#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys, unicodedata, re
sys.stdout.reconfigure(encoding='utf-8')

def slugify(name):
    n = unicodedata.normalize('NFD', name.lower())
    n = ''.join(c for c in n if unicodedata.category(c) != 'Mn')
    n = re.sub(r'[^a-z0-9]+', '-', n)
    return n.strip('-')

SORTS_JS = r"E:\12_LOGICIEL_DnD\quest-station\sorts.js"

with open(SORTS_JS, 'r', encoding='utf-8') as f:
    content = f.read()
sorts = json.loads(content[len('window.SORTS = '):].rstrip().rstrip(';'))

# Rôdeur est stocké comme 'Ranger' dans sorts.js
CLASSE = 'Ranger'

AJOUTER = {
    'Communion avec la nature', "Invocation d'êtres sylvestres", 'Mur de vent',
    'Nappe de brouillard', 'Passage par les arbres', 'Peau de pierre', 'Sens des pièges'
}
RETIRER = {
    'Arme élémentaire', 'Arme magique', 'Communication à distance',
    'Compréhension des langues', 'Contresort', 'Dissipation de la magie',
    'Enchevêtrement', 'Feuille morte', 'Fusion dans la pierre',
    "Modification d'apparence", 'Mort simulée', 'Repli expéditif',
    'Retour à la vie', "Sens de l'orientation", 'Tempête de neige', 'Vol',
    'Zone de vérité'
}

ajoutes, retires = [], []
for s in sorts:
    nom = s.get('n', '')
    cl = s.get('cl', [])
    if nom in AJOUTER and CLASSE not in cl:
        cl.append(CLASSE)
        s['cl'] = cl
        ajoutes.append(nom)
    if nom in RETIRER and CLASSE in cl:
        cl.remove(CLASSE)
        s['cl'] = cl
        retires.append(nom)

print(f'Ajoutés ({len(ajoutes)}) :', sorted(ajoutes))
print(f'Retirés ({len(retires)}) :', sorted(retires))

new_json = json.dumps(sorts, ensure_ascii=False, separators=(',', ':'))
with open(SORTS_JS, 'w', encoding='utf-8') as f:
    f.write('window.SORTS = ' + new_json + ';\n')

# Vérification finale
xml_set = {
    'alarme','amitie-avec-les-animaux','baies-nourricieres','communication-avec-les-animaux',
    'detection-de-la-magie','detection-du-poison-et-des-maladies','frappe-piegeuse',
    'grande-foulee','grele-d-epines','marque-du-chasseur','nappe-de-brouillard','saut','soins',
    'cordon-de-fleches','croissance-d-epines','localisation-d-animaux-ou-de-plantes',
    'localisation-d-objet','messager-animal','passage-sans-trace','peau-d-ecorce',
    'protection-contre-le-poison','restauration-partielle','sens-animal','sens-des-pieges',
    'silence','vision-dans-le-noir','antidetection','communication-avec-les-plantes',
    'croissance-vegetale','fleche-de-foudre','invocation-d-animaux','invocation-de-projectiles',
    'lumiere-du-jour','marche-sur-l-eau','mur-de-vent','protection-contre-une-energie',
    'respiration-aquatique','invocation-d-etres-sylvestres','liane-avide','liberte-de-mouvement',
    'localisation-de-creature','peau-de-pierre','carquois-magique','communion-avec-la-nature',
    'invocation-de-volee','passage-par-les-arbres'
}
rod_final = {slugify(s['n']) for s in sorts if CLASSE in s.get('cl', [])}
manquants = xml_set - rod_final
en_trop = rod_final - xml_set
print(f'\nVérification : manquants={len(manquants)}, en trop={len(en_trop)}')
if manquants:
    print('MANQUANTS:', sorted(manquants))
if en_trop:
    print('EN TROP:', sorted(en_trop))
