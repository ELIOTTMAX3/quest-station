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

AJOUTER = {
    'Amis', 'Aversion/Attirance', 'Bouffée de poison', 'Champ antimagie', 'Contrat',
    'Contrôle du climat', 'Dédale', 'Éclat du soleil', 'Flétrissement',
    'Localisation de créature', 'Mauvais oeil', 'Mot de pouvoir étourdissant',
    'Mot de pouvoir mortel', 'Mur de feu', 'Nuage incendiaire', 'Peur',
    'Préservation des morts', 'Rayon de soleil', 'Rayon empoisonné', 'Saut',
    'Tempête de neige', "Tentacules noirs d'Evard", 'Terraformage', 'Urne magique'
}
RETIRER = {
    'Aube', 'Augure', 'Carquois magique', 'Décharge occulte', 'Discours captivant',
    'Domination de bête', 'Enchevêtrement', 'Éveil', 'Fusion dans la pierre', 'Glas',
    'Injonction', 'Mur de vent', 'Régénération', 'Représailles infernales',
    'Retour à la vie', 'Sens des pièges', 'Silence', 'Soins', 'Soins de groupe',
    'Transfert de vie', 'Voile spirituel', 'Zone de vérité'
}

ajoutes, retires = [], []
for s in sorts:
    nom = s.get('n', '')
    cl = s.get('cl', [])
    if nom in AJOUTER and 'Magicien' not in cl:
        cl.append('Magicien')
        s['cl'] = cl
        ajoutes.append(nom)
    if nom in RETIRER and 'Magicien' in cl:
        cl.remove('Magicien')
        s['cl'] = cl
        retires.append(nom)

print(f'Ajoutés ({len(ajoutes)}) :', sorted(ajoutes))
print(f'Retirés ({len(retires)}) :', sorted(retires))

new_json = json.dumps(sorts, ensure_ascii=False, separators=(',', ':'))
with open(SORTS_JS, 'w', encoding='utf-8') as f:
    f.write('window.SORTS = ' + new_json + ';\n')

# Vérification finale
xml_set = {
    'amis','aspersion-d-acide','bouffee-de-poison','contact-glacial','coup-au-but',
    'illusion-mineure','lumiere','lumieres-dansantes','main-de-mage','message','poigne-electrique',
    'prestidigitation','protection-contre-les-armes','rayon-de-givre','reparation','trait-de-feu',
    'alarme','appel-de-familier','armure-de-mage','bouclier','charme-personne',
    'comprehension-des-langues','couleurs-dansantes','deguisement','detection-de-la-magie',
    'disque-flottant-de-tenser','feuille-morte','fou-rire-de-tasha','graisse','grande-foulee',
    'identification','image-silencieuse','mains-brulantes','nappe-de-brouillard','orbe-chromatique',
    'projectile-magique','protection-contre-le-mal-et-le-bien','rayon-empoisonne','repli-expeditif',
    'saut','serviteur-invisible','simulacre-de-vie','sommeil','texte-illusoire','trait-ensorcele',
    'vague-tonnante','agrandissement-rapetissement','arme-magique','aura-magique-de-nystul',
    'bouche-magique','bourrasque','cecite-surdite','corde-enchantee','couronne-du-dement',
    'deblocage','detection-des-pensees','flamme-eternelle','fleche-acide-de-melf','flou',
    'force-fantasmagorique','foulee-brumeuse','fracassement','image-miroir',
    'immobilisation-de-personne','invisibilite','levitation','localisation-d-objet',
    'modification-d-apparence','nuee-de-dagues','pattes-d-araignee','preservation-des-morts',
    'rayon-affaiblissant','rayon-ardent','sphere-de-feu','suggestion','tenebres','toile-d-araignee',
    'verrou-magique','vision-dans-le-noir','voir-l-invisible','animation-des-morts','antidetection',
    'boule-de-feu','cercle-magique','clairvoyance','clignotement','communication-a-distance',
    'contresort','delivrance-des-maledictions','dissipation-de-la-magie','don-des-langues',
    'eclair','forme-gazeuse','glyphe-de-protection','hate','image-majeure','lenteur','malediction',
    'monture-fantome','mort-simulee','motif-hypnotique','nuage-nauseabond','petite-hutte-de-leomund',
    'peur','protection-contre-une-energie','respiration-aquatique','tempete-de-neige',
    'toucher-du-vampire','vol','assassin-imaginaire','bannissement','bouclier-de-feu',
    'chien-de-garde-de-mordenkainen','coffre-secret-de-leomund','confusion','controle-de-l-eau',
    'fabrication','faconnage-de-la-pierre','fletrissement','invisibilite-superieure',
    'invocation-d-elementaires-mineurs','localisation-de-creature','metamorphose','mur-de-feu',
    'oeil-magique','peau-de-pierre','porte-dimensionnelle','sanctuaire-prive-de-mordenkainen',
    'sphere-resiliente-d-otiluke','tempete-de-grele','tentacules-noirs-d-evard',
    'terrain-hallucinatoire','animation-d-objets','apparence-trompeuse','brume-mortelle',
    'cercle-de-teleportation','cone-de-froid','contact-avec-un-autre-plan','contrat','creation',
    'domination-de-personne','double-illusoire','immobilisation-de-monstre','invocation-d-elementaire',
    'lien-telepathique-de-rary','main-de-bigby','modification-de-memoire','mur-de-force',
    'mur-de-pierre','mythes-et-legendes','passe-muraille','quete','scrutation','songe','telekinesie',
    'cercle-de-mort','chaine-d-eclairs','convocations-instantanees-de-drawmij',
    'creation-de-mort-vivant','danse-irresistible-d-otto','desintegration','globe-d-invulnerabilite',
    'illusion-programmee','mauvais-oeil','mur-de-glace','petrification','portail-magique',
    'prevoyance','protections-et-sceaux','rayon-de-soleil','sphere-glaciale-d-otiluke',
    'suggestion-de-groupe','terraformage','urne-magique','vision-supreme',
    'boule-de-feu-a-retardement','cage-de-force','changement-de-plan','dissimulation',
    'doigt-de-mort','epee-de-mordenkainen','forme-etheree','inversion-de-la-gravite',
    'manoir-somptueux-de-mordenkainen','mirage','projection-d-image','rayons-prismatiques',
    'simulacre','symbole','teleportation','aversion-attirance','champ-antimagie','clone',
    'controle-du-climat','dedale','demi-plan','domination-de-monstre','eclat-du-soleil',
    'esprit-faible','esprit-impenetrable','mot-de-pouvoir-etourdissant','nuage-incendiaire',
    'telepathie','arret-du-temps','changement-de-forme','emprisonnement','ennemi-subconscient',
    'metamorphose-supreme','mot-de-pouvoir-mortel','mur-prismatique','nuee-de-meteores',
    'portail','premonition','projection-astrale','souhait'
}
mag_final = {slugify(s['n']) for s in sorts if 'Magicien' in s.get('cl', [])}
manquants = xml_set - mag_final
en_trop = mag_final - xml_set
print(f'\nVérification : manquants={len(manquants)}, en trop={len(en_trop)}')
if manquants:
    print('MANQUANTS:', sorted(manquants))
if en_trop:
    print('EN TROP:', sorted(en_trop))
