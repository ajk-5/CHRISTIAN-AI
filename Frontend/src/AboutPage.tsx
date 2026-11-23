import { Database, ShieldCheck, Sparkles } from 'lucide-react';

const STEPS = [
  ['Question', 'Vous posez une question en français. Le serveur la transmet à l\'agent AllergyLab.'],
  ['Code', 'L\'agent (un CodeAgent de smolagents) écrit du Python, l\'exécute côté serveur et appelle les outils de l\'équipe.'],
  ['Contrôle', 'Sa réponse finale est vérifiée : trois champs, statut, valeur et justification. Sinon, il recommence.'],
  ['Mémoire', 'Les étapes, les jetons et le coût estimé sont affichés et les questions déjà résolues sont réutilisées sans nouvel appel au modèle.'],
];

export default function AboutPage() {
  return (
    <div className="page page--narrow">
      <header className="page__head">
        <h1>À propos</h1>
        <p>Christian AI est l'agent d'analyse de l'équipe 1 pour la semaine AllergyLab de l'EFREI. Il répond, ou il s'abstient quand les données ne permettent pas de conclure.</p>
      </header>

      <section className="card">
        <header className="card__head"><div><h2><Sparkles size={16} aria-hidden="true" /> Comment il répond</h2></div></header>
        <ol className="flow">
          {STEPS.map(([title, text], index) => (
            <li key={title}>
              <span className="flow__index">{index + 1}</span>
              <div><strong>{title}</strong><p>{text}</p></div>
            </li>
          ))}
        </ol>
      </section>

      <section className="card">
        <header className="card__head"><div><h2><ShieldCheck size={16} aria-hidden="true" /> À savoir</h2></div></header>
        <ul className="plain">
          <li>L'agent exécute du code Python généré pour analyser les données du projet, encadré par les garde-fous de l'équipe.</li>
          <li>Ce n'est pas un bac à sable, ni un outil de diagnostic médical.</li>
          <li>Chaque question coûte des jetons sur la cagnotte de l'équipe. Le coût estimé s'affiche sous chaque réponse.</li>
          <li>La lecture à voix haute utilise la synthèse vocale du navigateur : elle ne coûte rien et n'envoie rien.</li>
          <li>La dictée (le micro) utilise la reconnaissance vocale du navigateur : elle ne coûte rien et n'appelle pas notre modèle. Dans un Chrome à jour, le premier clic installe le français sur l'ordinateur, une seule fois : la dictée marche ensuite sans internet et le son reste sur l'ordinateur. Les autres navigateurs envoient le son à leur propre service en ligne, qui demande internet. Le survol du micro dit lequel des deux est utilisé.</li>
        </ul>
      </section>

      <section className="card">
        <header className="card__head"><div><h2><Database size={16} aria-hidden="true" /> Les données</h2></div></header>
        <p className="card__text">
          Le tableau des patients est le jeu « Allergen Chip Challenge » de la Société Française d'Allergologie (Licence Ouverte 2.0).
          L'équipe y a ajouté, à part, des relevés de pollens du RNSA (calendrier national, tendances annuelles, 125 capteurs)
          et les bulletins de risque allergique de la Métropole de Lyon. L'agent analyse toutes ces tables, pas seulement le tableau des patients :
          voir <code>donnees_complementaires/README.md</code>.
        </p>
      </section>
    </div>
  );
}
