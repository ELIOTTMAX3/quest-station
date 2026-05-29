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

# Dans sorts.js, l'Occultiste est la classe "Sorcier"
CLASSE = 'Sorcier'

AJOUTER = {
    'Bagou', 'Cercle de mort', 'Compréhension des langues', 'Coup au but',
    'Couronne du dément', 'Discours captivant', 'Emprisonnement', 'Flétrissement',
    'Fracassement', 'Immobilisation de personne', 'Invisibilité', 'Motif hypnotique',
    'Peur', 'Portail magique', 'Porte dimensionnelle', 'Prémonition',
    'Suggestion de groupe', 'Terrain hallucinatoire', 'Texte illusoire', 'Trait ensorcelé'
}
RETIRER = {
    'Amélioration de caractéristique', 'Bouche magique', 'Brume mortelle', 'Carquois magique',
    'Cécité/Surdité', "Chaîne d'éclairs", 'Clairvoyance', 'Communication à distance',
    'Confusion', "Contrôle de l'eau", 'Dédale', 'Déguisement', 'Domination de bête',
    'Domination de personne', 'Double illusoire', 'Enchevêtrement', 'Ennemi subconscient',
    'Esprit impénétrable', 'Flèche acide de Melf', 'Flou', 'Force fantasmagorique', 'Glas',
    'Inversion de la gravité', 'Lenteur', 'Lévitation', 'Lueurs féeriques', 'Malédiction',
    'Message', 'Mirage', 'Moquerie cruelle', 'Mort simulée', 'Nuage nauséabond',
    'Peau de pierre', 'Poigne électrique', 'Portail', "Protection contre une énergie",
    'Quête', 'Rayon empoisonné', 'Rayons prismatiques', 'Simulacre', 'Soins',
    'Soins de groupe', 'Sommeil', 'Sphère de feu', "Sphère glaciale d'Otiluke",
    "Sphère résiliente d'Otiluke", 'Symbole', 'Télékinésie', 'Téléportation',
    'Tempête de neige', "Tentacules noirs d'Evard", 'Terraformage', "Toile d'araignée",
    'Tremblement de terre', 'Urne magique', 'Verrou magique', 'Vision dans le noir',
    'Voile spirituel', "Voir l'invisible", 'Zone de vérité'
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
    'amis','bouffee-de-poison','contact-glacial','coup-au-but','decharge-occulte',
    'illusion-mineure','main-de-mage','prestidigitation','protection-contre-les-armes',
    'armure-d-agathys','charme-personne','comprehension-des-langues','malefice',
    'protection-contre-le-mal-et-le-bien','repli-expeditif','represailles-infernales',
    'serviteur-invisible','tentacules-de-hadar','texte-illusoire','trait-ensorcele',
    'couronne-du-dement','discours-captivant','foulee-brumeuse','fracassement','image-miroir',
    'immobilisation-de-personne','invisibilite','nuee-de-dagues','pattes-d-araignee',
    'rayon-affaiblissant','suggestion','tenebres','cercle-magique','contresort',
    'delivrance-des-maledictions','dissipation-de-la-magie','don-des-langues','forme-gazeuse',
    'image-majeure','motif-hypnotique','peur','toucher-du-vampire','vol','voracite-de-hadar',
    'bannissement','fletrissement','porte-dimensionnelle','terrain-hallucinatoire',
    'contact-avec-un-autre-plan','immobilisation-de-monstre','scrutation','songe',
    'cercle-de-mort','creation-de-mort-vivant','invocation-de-fee','mauvais-oeil',
    'petrification','portail-magique','suggestion-de-groupe','vision-supreme','cage-de-force',
    'changement-de-plan','doigt-de-mort','forme-etheree','bagou','demi-plan',
    'domination-de-monstre','esprit-faible','mot-de-pouvoir-etourdissant','emprisonnement',
    'metamorphose-supreme','mot-de-pouvoir-mortel','premonition','projection-astrale'
}
occ_final = {slugify(s['n']) for s in sorts if CLASSE in s.get('cl', [])}
manquants = xml_set - occ_final
en_trop = occ_final - xml_set
print(f'\nVérification : manquants={len(manquants)}, en trop={len(en_trop)}')
if manquants:
    print('MANQUANTS:', sorted(manquants))
if en_trop:
    print('EN TROP:', sorted(en_trop))
