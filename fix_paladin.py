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

AJOUTER = {'Arme élémentaire', 'Aura de vitalité', 'Aura du croisé'}
RETIRER = {
    'Apparence trompeuse', 'Arme sacrée', 'Arme spirituelle', 'Cécité/Surdité',
    'Cérémonie', 'Colonne de flamme', 'Contresort', 'Convocation de céleste', 'Éveil',
    'Festin des héros', 'Flamme éternelle', 'Gardien de la foi', 'Glyphe de protection',
    'Grande foulée', 'Guérison', 'Interdiction', 'Invocation de céleste',
    'Liberté de mouvement', 'Lien de protection', 'Lien télépathique de Rary',
    "Lueur d'espoir", 'Malédiction', "Marche sur l'eau", 'Mot de guérison',
    'Mythes et légendes', 'Passage sans trace', 'Protection contre une énergie',
    'Rayon de lune', 'Régénération', 'Réparation', 'Restauration supérieure',
    'Sanctification', 'Sanctuaire', 'Scrutation', 'Soins de groupe', 'Symbole',
    'Téléportation', 'Voile spirituel'
}

ajoutes, retires = [], []
for s in sorts:
    nom = s.get('n', '')
    cl = s.get('cl', [])
    if nom in AJOUTER and 'Paladin' not in cl:
        cl.append('Paladin')
        s['cl'] = cl
        ajoutes.append(nom)
    if nom in RETIRER and 'Paladin' in cl:
        cl.remove('Paladin')
        s['cl'] = cl
        retires.append(nom)

print(f'Ajoutés ({len(ajoutes)}) :', sorted(ajoutes))
print(f'Retirés ({len(retires)}) :', sorted(retires))

new_json = json.dumps(sorts, ensure_ascii=False, separators=(',', ':'))
with open(SORTS_JS, 'w', encoding='utf-8') as f:
    f.write('window.SORTS = ' + new_json + ';\n')

# Vérification finale
xml_set = {
    'benediction','bouclier-de-la-foi','chatiment-calcinant','chatiment-courrouce',
    'chatiment-tonitruant','detection-de-la-magie','detection-du-mal-et-du-bien',
    'detection-du-poison-et-des-maladies','duel-force','faveur-divine','heroisme',
    'injonction','protection-contre-le-mal-et-le-bien','purification-de-nourriture-et-d-eau',
    'soins','aide','appel-de-destrier','arme-magique','chatiment-revelateur',
    'localisation-d-objet','protection-contre-le-poison','restauration-partielle',
    'zone-de-verite','arme-elementaire','aura-de-vitalite','aura-du-croise','cercle-magique',
    'chatiment-aveuglant','creation-de-nourriture-et-d-eau','delivrance-des-maledictions',
    'dissipation-de-la-magie','lumiere-du-jour','retour-a-la-vie','aura-de-purete',
    'aura-de-vie','bannissement','chatiment-debilitant','localisation-de-creature',
    'protection-contre-la-mort','cercle-de-pouvoir','chatiment-du-ban',
    'dissipation-du-mal-et-du-bien','quete','rappel-a-la-vie','vague-destructrice'
}
pal_final = {slugify(s['n']) for s in sorts if 'Paladin' in s.get('cl', [])}
manquants = xml_set - pal_final
en_trop = pal_final - xml_set
print(f'\nVérification : manquants={len(manquants)}, en trop={len(en_trop)}')
if manquants:
    print('MANQUANTS:', sorted(manquants))
if en_trop:
    print('EN TROP:', sorted(en_trop))
