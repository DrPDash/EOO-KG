# EOO-KG: Earth Observation Ontology for Knowledge Graphs

<h3>CADENCE-EOO: A Corpus-Guided Earth Observation Ontology</h3>
<p><strong>Prasanjit Dash and Paul M. DiGiacomo</strong><br>
<em>Manuscript in preparation for <a href="https://link.springer.com/journal/12145">Earth Science Informatics (Springer Nature), Nov 2026</a></em></p>

EOO-KG provides governed scientific concepts for Earth observation (EO), developed within **CADENCE (Cognitive Analysis by Data-Enabled Neural Computation and Evaluation)**.

![EOO-KG — Eight connected vocabularies for Earth Observation science](assets/HERO_EOO-KG.png)

## Ontology

Eight resources: **parameters, processes, methods, regions, sensors, systems, units, and scientific trends**. They support canonical identities, alias resolution, explicit semantic relationships, deterministic validation, and interoperability.

For the scientific design, see [Architecture Overview](architecture.md).

| Version | Snapshot       | Basis                                                             |
| ------- | -------------- | ----------------------------------------------------------------- |
| `v0`    | September 2026 | Manuscript-associated ontology; 101 research papers               |
| `v1`    | November 2026  | Expanded ontology; approximately 500,000 EO question–answer pairs |

The `ontology/cadence_eoo_manifest.json` defines available ontology snapshots and the default version. Adding a version requires a new data directory and manifest entry.

<blockquote>
  <p><strong>📢 Release Notice:</strong> The CADENCE-EOO Explorer source code and ontology datasets will be made available following manuscript submission, subject to release approval.</p>
</blockquote>

## Repository Structure

```text
EOO-KG/
├── README.md                          Documentation
├── LICENSE                            Dataset licensing terms
├── architecture.md                    Scientific architecture
├── cadence_eo_ontology_explorer.py    Read-only ontology explorer
├── assets/                            Diagrams and hero images
└── ontology/
    ├── cadence_eoo_manifest.json      Version metadata
    ├── v0/                            Eight ontology JSON resources
    └── v1/                            Eight ontology JSON resources
```

## Run the Explorer (local)

```cmd
python -m pip install fastapi uvicorn
python cadence_eo_ontology_explorer.py
python cadence_eo_ontology_explorer.py -cev v1
```

Open http://127.0.0.1:8010/cadence-ontology/ (`-h` for options). The read-only Explorer browses six concept families; units and trends are supporting resources.

## Attribution & Release

**Scientific authors:** Prasanjit Dash and Paul M. DiGiacomo. **Scientific quality control:** Human/expert adjudication. **Coding assistance:** OpenAI ChatGPT.

The manuscript concerns `v0`; `v1` is a separate expanded snapshot, not part of the manuscript's evaluation.

**Citation:** Credit Dash and DiGiacomo, identify the ontology version, and link to [EOO-KG](https://github.com/DrPDash/EOO-KG). For scholarly use, cite the associated paper when available.

**License:** Ontology datasets are designated for [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) upon authorized release and rights clearance; see [LICENSE](LICENSE). The Explorer requires a separate software license.

**Release status:** Local release candidate. The Python Ontology Explorer and v0/v1 datasets are **not yet publicly available**. Private CADENCE systems remain outside the repository's release scope.
