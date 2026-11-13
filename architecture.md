[← Back to README](README.md)

# EOO-KG — Architecture Overview

## EOO-KG

**Earth Observation Ontology for Knowledge Graphs**

EOO-KG is a governed Earth Observation ontology resource for representing scientific concepts in a form suitable for canonical identity resolution, semantic interoperability, and knowledge-graph construction.

EOO-KG is developed within **CADENCE (Cognitive Analysis by Data-Enabled Neural Computation and Evaluation)**.

## Architecture at a Glance

![EOO-KG Architecture Overview](assets/ARCHITECTURE_EOO-KG.png)

## Purpose

Earth Observation knowledge is expressed through curated ontology and lexical resources rather than embedded directly in application logic.

The architectural principle is:

> **The code is universal.**  
> **The JSON defines the science.**

This separation allows domain knowledge to remain explicit, inspectable, versionable, and reusable across knowledge-engineering workflows.

EOO-KG is designed to support:

- canonical resolution of scientific terminology;
- controlled handling of lexical variants and aliases;
- separation of distinct scientific entity families;
- scientifically meaningful hierarchy where appropriate;
- normalization of units and domain terminology;
- machine-resolvable representations suitable for knowledge graphs.

## Ontology Resource Families

EOO-KG organizes Earth Observation knowledge into eight governed resource families:

| Resource | Semantic role |
|---|---|
| `params_map.json` | Scientific variables and parameters, including canonical parameter identity and associated units where applicable |
| `processes_map.json` | Physical, environmental, analytical, and computational processes |
| `methods_map.json` | Scientific, algorithmic, analytical, and modeling methods |
| `regions_map.json` | Geographic and spatial entities, including hierarchical relationships where appropriate |
| `sensors_map.json` | Sensors and observing instruments |
| `systems_map.json` | Platforms, systems, organizations, products, and other source-related entities represented by the ontology |
| `units_map.json` | Controlled scientific units used to normalize quantitative representations |
| `trend_tokens.json` | Controlled lexical vocabulary for directional and trend-related language |

Together, these resources provide the semantic vocabulary used to resolve Earth Observation terminology into stable, machine-readable concepts.

## Canonical Identity

A central goal of EOO-KG is to distinguish the scientific concept from the many surface forms by which that concept may appear in literature, metadata, products, or analytical outputs.

Canonicalization allows multiple lexical forms to resolve to a common scientific identity while preserving semantic distinctions among different entity classes.

For example, a parameter may appear under abbreviations, expanded names, common variants, or discipline-specific wording. EOO-KG provides a governed representation through which those forms can be associated with a single canonical concept.

This supports more consistent integration of independently produced scientific information.

## Semantic Organization

EOO-KG keeps major scientific entity families distinct rather than collapsing them into a single undifferentiated vocabulary.

The ontology therefore distinguishes concepts such as:

- **parameters** — what is measured, estimated, or derived;
- **processes** — what occurs physically, environmentally, analytically, or computationally;
- **methods** — how observations or derived information are produced or analyzed;
- **regions** — where an observation, process, or result applies;
- **sensors** — which observing instrument is involved;
- **systems** — which broader platform, source, organization, or operational system is involved;
- **units** — how quantitative values are expressed;
- **trend language** — how directional change is represented lexically.

This separation helps prevent semantically different concepts from being treated as interchangeable simply because they appear in similar linguistic contexts.

## Hierarchy and Relationships

Some EOO-KG resources support hierarchical organization where it is scientifically meaningful.

Regional concepts, for example, may be represented through parent–child relationships so that a specific geographic entity can remain connected to a broader spatial context.

Other resources may similarly encode structured relationships needed for consistent semantic resolution.

The objective is not merely to maintain vocabulary lists, but to preserve enough scientific structure for the represented concepts to participate meaningfully in machine-readable knowledge systems.

## Lexical Resolution

Scientific language is variable.

The same concept may be expressed through:

- abbreviations;
- acronyms;
- alternate spellings;
- expanded names;
- discipline-specific terminology;
- product or instrument naming conventions.

EOO-KG uses governed mappings to connect such lexical forms to canonical scientific concepts.

The controlled `trend_tokens.json` resource serves a related but distinct role: it captures directional or trend-related language as lexical knowledge without requiring every linguistic token to become a standalone ontology entity.

## Units

Scientific parameters and quantitative statements require consistent treatment of units.

`units_map.json` provides controlled unit representations that can be used to normalize heterogeneous scientific expressions and associate compatible units with ontology concepts where appropriate.

Separating unit knowledge from free text improves consistency when information originating from different publications, datasets, or processing systems is brought into a common semantic representation.

## Knowledge-Graph Use

EOO-KG is designed so that resolved scientific concepts can participate in knowledge-graph representations.

Instead of treating terms found in scientific material as isolated strings, EOO-KG provides canonical entities and semantic organization that can be used to connect scientific statements through stable identities.

This supports downstream graph representations in which observations, parameters, methods, processes, regions, sensors, systems, and related concepts can be connected without losing their semantic type. The ontology supplies governed identities and vocabulary structure; extraction, graph construction, and validation are performed by separate CADENCE systems that are not part of this public repository.

The result is a stronger foundation for interoperable scientific knowledge representation, graph-based exploration, and downstream reasoning.

## Design Principles

EOO-KG follows several core principles:

1. **Canonical identity**  
   Scientific concepts should resolve to stable canonical representations rather than remain uncontrolled lexical variants.

2. **Explicit domain knowledge**  
   Earth Observation semantics should be represented in governed resources that can be inspected, reviewed, and versioned.

3. **Semantic separation**  
   Parameters, processes, methods, regions, sensors, systems, units, and lexical concepts should remain distinguishable.

4. **Hierarchy where scientifically appropriate**  
   Parent–child structure should be used where it represents meaningful scientific or geographic organization.

5. **Machine readability**  
   Ontology resources should support deterministic programmatic use and knowledge-graph construction.

6. **Interoperability**  
   Scientific identity should remain usable across independently produced documents, datasets, analytical outputs, and knowledge representations.

7. **Governed evolution**  
   Ontology content should be able to expand as scientific coverage grows while preserving stable semantic organization.

## Release Model

EOO-KG is under active development.

The manuscript-associated **v0 (September 2026)** snapshot is the candidate for the initial public release. **v1 — next version (near future)** is a planned successor, **subject to Manuscript Acceptance and Release Approval**; its ontology data are not included in the v0 release.

Authorized public ontology resources will be released as explicit, versioned snapshots so that changes in vocabulary and semantic structure can be tracked over time.

Each release can therefore serve as a reproducible reference point for scientific applications that depend on a particular state of the ontology.

## Provenance

EOO-KG is a scientific ontology resource developed within the **CADENCE** research framework for Earth Observation knowledge representation and knowledge-graph applications.


---

[← Back to README](README.md)
