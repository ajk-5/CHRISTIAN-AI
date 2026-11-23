
"""Agent d'analyse des données allergologiques de l'équipe."""

from pathlib import Path

from smolagents import ToolCallingAgent

from equipe import memoire
from equipe.outils.calendrier_pollinique import calendrier_pollinique
from equipe.outils.chercher_colonnes import chercher_colonnes
from equipe.outils.classer_allergenes import classer_allergenes
from equipe.outils.codes_officiels import codes_officiels
from equipe.outils.colonnes_par_famille import colonnes_par_famille
from equipe.outils.compter_codes import compter_codes
from equipe.outils.croiser import croiser
from equipe.outils.decrire_colonne import decrire_colonne
from equipe.outils.positifs import positifs
from equipe.outils.source_allergene import source_allergene
from kit import modele, reponse
from equipe.outils.statistiques import resume_allergene
from equipe.outils.qualite import rapport_qualite

CONSIGNE = (Path(__file__).parent / "consigne.md").read_text(encoding="utf-8")

# Une question déjà posée mot pour mot au même agent et au même modèle reprend
# la réponse de sa trace, sans appel au modèle (equipe/memoire.py).
# False : chaque question appelle le modèle, par exemple pour comparer deux réponses.
REUTILISER_LES_TRACES = True

# Les outils de l'équipe, testés sans le modèle dans equipe/tests/. Chacun rend
# des valeurs simples, jamais le tableau : ils restent valables si l'on ferme l'accès.
OUTILS = [
    chercher_colonnes, decrire_colonne, compter_codes, codes_officiels, croiser,
    positifs, classer_allergenes, source_allergene, colonnes_par_famille, calendrier_pollinique,
]


def verifier_contrat(reponse_finale, memoire, agent=None):
    """Refuse une réponse finale hors contrat (kit/reponse.py).

    L'agent lit alors l'erreur et corrige sa réponse à l'étape suivante, au lieu
    de rendre au kit une réponse illisible.
    """
    reponse.valider(reponse_finale)  # lève une erreur qui dit ce qui ne va pas
    return True


def repondre(question):
    if REUTILISER_LES_TRACES:
        deja = memoire.reponse_enregistree(question)
        if deja:
            reponse_finale, trace = deja
            print(f"Réponse reprise de {trace} : aucun appel au modèle.")
            modele.ajouter_etape(f"# Réponse reprise de {trace} : aucun appel au modèle.", None)  # dans la trace
            return reponse_finale

    agent = CodeAgent(
        model=modele.ModeleKit(),  # le modèle de kit/reglages.toml
        tools=OUTILS,
        instructions=reponse.consigne(CONSIGNE),  # notre consigne, puis le format de réponse du kit
        max_steps=modele.REGLAGES["agent"]["etapes_max"],
        max_print_outputs_length=modele.REGLAGES["agent"]["sortie_max"],
        step_callbacks=[modele.noter_etape],  # recopie chaque étape dans la trace
        final_answer_checks=[verifier_contrat],
        # Accès aux données : le code écrit par le modèle peut importer pandas.
        additional_authorized_imports=["pandas"],
    )
    return agent.run(
        question,
        # Accès aux données : le code écrit par le modèle reçoit le tableau complet, sous le nom tableau.
        additional_args={"tableau": charger()},
    )

    return agent.run(question)
