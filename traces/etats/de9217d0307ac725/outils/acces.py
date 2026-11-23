"""Pas un outil : ce que tous les outils partagent. Le tableau et les fichiers de référence, lus une seule fois.

Les outils lisent le tableau ici et ne rendent que des valeurs simples (un
nombre, un texte, une courte liste, un petit dictionnaire), jamais le tableau
lui-même : un outil qui rendrait le tableau rouvrirait tout l'accès aux données.
"""

import difflib
from functools import cache
from pathlib import Path

import pandas as pd

from kit.donnees import COLONNE_PUCE, FICHIER, NB_CLINIQUES, charger

RACINE = Path(__file__).resolve().parents[2]
ANALYSE = RACINE / "equipe" / "analyse"
COMPLEMENTS = RACINE / "donnees_complementaires"

# Le fichier que lisent les outils. Les tests le remplacent par la table inventée de kit/exemple/.
CHEMIN = FICHIER


@cache
def tableau():
    """Le tableau complet, chargé au premier appel d'un outil, puis gardé en mémoire."""
    return charger(CHEMIN)


@cache
def reference(chemin):
    """Un fichier CSV de référence, lu en texte : equipe/analyse/ ou donnees_complementaires/."""
    return pd.read_csv(chemin, encoding="utf-8", dtype=str, keep_default_na=False)


def verifier_colonne(nom):
    """Lève une erreur claire si la colonne n'existe pas : l'agent la lit et corrige son appel."""
    colonnes = list(tableau().columns)
    if nom not in colonnes:
        proches = difflib.get_close_matches(nom, colonnes, n=3)
        conseil = f" Noms proches : {', '.join(proches)}." if proches else ""
        raise ValueError(f"Colonne inconnue : {nom!r}.{conseil} Cherche le nom exact avec chercher_colonnes.")


def colonnes_dosage():
    """Les noms des colonnes de dosage : toutes celles qui suivent les quinze colonnes cliniques."""
    return list(tableau().columns[NB_CLINIQUES:])


def filtrer_puce(puce):
    """Le tableau d'une seule puce, ou tout le tableau si puce est vide."""
    t = tableau()
    if not puce:
        return t
    puces = sorted(t[COLONNE_PUCE].dropna().unique())
    if puce not in puces:
        raise ValueError(f"Puce inconnue : {puce!r}. Puces du tableau : {', '.join(puces)}, ou \"\" pour toutes.")
    return t[t[COLONNE_PUCE] == puce]


def en_texte(valeur):
    """Une valeur du tableau en texte court : 1.0 devient « 1 »."""
    if isinstance(valeur, float) and valeur.is_integer():
        return str(int(valeur))
    return str(valeur)
