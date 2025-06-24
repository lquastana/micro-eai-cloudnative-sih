# 🧩 micro-eai-cloudnative-sih

> Un squelette de micro-EAI moderne, extensible et cloud-native, dédié aux besoins des Systèmes d'Information Hospitaliers (SIH)

---

## 🎯 Objectif

Ce projet propose une **base technique prête à l'emploi** pour construire une architecture de micro-EAI orientée **interopérabilité en santé**, avec une stack **moderne**, **légère** et **cloud-native**.  
Il permet de gérer efficacement les **flux entrants/sortants**, la **transformation des messages**, la **visualisation**, la **supervision** et le **rejeu contrôlé**.

---

## 🏗️ Architecture fonctionnelle

```

```
    ┌──────────────┐       ┌──────────────┐
    │ Connecteurs  │ ───▶  │   Pivot/     │
    │ Entrée/Sortie│       │   Filtres    │
    └──────────────┘       └──────────────┘
             │                     │
             ▼                     ▼
       ┌────────────┐       ┌────────────┐
       │ Supervision│ ◀──▶  │   Journal   │
       └────────────┘       └────────────┘
             │
             ▼
      ┌──────────────┐
      │ Visualisation│
      │   & Rejeu    │
      └──────────────┘
```

````

---

## ⚙️ Stack technique

| Composant             | Technologie choisie       | Rôle |
|-----------------------|---------------------------|------|
| **Langage**           | Python 3.11+              | Légèreté, lisibilité, maturité dans le domaine santé |
| **Parser HL7v2**      | `hl7apy`                  | Parsing/validation/génération de messages HL7 |
| **MLLP**              | `python-mllp` / `socket`  | Communication bas-niveau HL7 v2 |
| **SFTP**              | `paramiko`                | Échange de fichiers sécurisés |
| **API REST (optionnel)** | FastAPI               | Webhooks, supervision, visualisation |
| **Routage / Jobs**    | Celery + Redis            | Traitements asynchrones, rejeu, enchaînement |
| **Base de données**   | PostgreSQL / SQLite       | Historique, rejets, traçabilité |
| **Monitoring**        | Loguru / Loki             | Journalisation structurée |
| **Déploiement**       | Docker / Docker Compose   | Exécution locale, CI, Cloud (K8s ready) |

---

## 🚀 Fonctionnalités incluses

✅ Réception de messages HL7 via MLLP  
✅ Récupération et dépôt de fichiers HL7 via SFTP (polling automatique si `SFTP_*` configuré)
✅ Parsing/validation HL7 v2 (segments personnalisés inclus)
✅ Support des messages FHIR (JSON) et CDA (XML)
✅ Routage conditionnel (MSH.9, PID.3, etc.)
ℹ️  Les règles sont déclarées dans `routes.yml` et chargées dynamiquement.
✅ Archivage, logs détaillés, base des messages
✅ Visualisation des messages reçus (API ou mini Web UI)
✅ Rejeu manuel ou automatique des messages en erreur  
✅ Conteneurisation complète via Docker Compose  

---

## 🧪 Exécution rapide (mode dev)

```bash
git clone https://github.com/votre-org/micro-eai-cloudnative-sih.git
cd micro-eai-cloudnative-sih
cp .env.sample .env
# personnaliser les règles de routage et les accès SFTP si besoin
cp routes.yml.sample routes.yml
pip install -r requirements.txt
docker-compose up --build
````

L'application expose :

* MLLP sur le port `2575`
* Acceptation des messages FHIR (JSON) ou CDA (XML)
* API REST (FastAPI) sur `http://localhost:8000`
  * `GET /messages` : liste des messages stockés
  * `GET /messages/{id}` : détail d'un message
  * `POST /messages/{id}/replay` : rejeu d'un message
  * `GET /messages/export?format=csv` : export CSV
* Interface Web sur `http://localhost:8000/ui/messages`
* Redis en local sur `6379`

---

## 📁 Structure du projet

```
micro-eai-cloudnative-sih/
├── app/
│   ├── mllp/              # Serveur/Client MLLP
│   ├── sftp/              # Polling ou watcher de fichiers
│   ├── hl7/               # Parsing, validation, routage HL7
│   ├── api/               # FastAPI - Visualisation et rejeu
│   ├── jobs/              # Workers Celery
│   └── db/                # Modèles SQLAlchemy / ORM
├── tests/                 # Tests unitaires et d'intégration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📚 Roadmap

* [x] Intégration d’un moteur de règles YAML
* [x] UI Web pour visualisation + rejeu
* [x] Export CSV / JSON pour suivi
* [x] Support des formats FHIR / CDA
* [ ] Intégration Prometheus + Grafana

---

## 👥 Contribuer

Les contributions sont bienvenues !
Consulte le fichier [`CONTRIBUTING.md`](CONTRIBUTING.md) pour les bonnes pratiques.

---

## 🏥 Utilisation cible

Ce projet vise des usages dans :

* Des hôpitaux ou GHT souhaitant maîtriser leur interopérabilité
* Des plateformes MSSanté/DMP locales ou régionales
* Des connecteurs légers entre logiciels métiers

---

## 📄 Licence

MIT – Libre pour modification, usage commercial et redistribution.


