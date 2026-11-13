r"""
CADENCE Earth Observation Ontology (CADENCE-EOO) Explorer
========================================================

Associated Scientific Manuscript:
    Dash, P., and DiGiacomo, P. M.
    CADENCE-EOO: A Corpus-Guided Earth Observation Ontology.
    Manuscript in preparation for Earth Science Informatics (Springer Nature), November 2026.

Scientific Quality Control:
    Human/expert adjudication

Coding Assistance:
    OpenAI ChatGPT

Overview:
    Standalone, read-only scientific ontology explorer developed within
    CADENCE (Cognitive Analysis by Data-Enabled Neural Computation and Evaluation).

    The Explorer provides class-aware browsing, searching, and inspection of canonical
    scientific concepts, aliases, and semantic attributes across six ontology families:

        Parameters, Processes, Methods, Sensors, Systems, Regions

    Units and scientific trend tokens are maintained as supporting ontology resources.

Ontology Versioning:
    Ontology datasets are organized as versioned JSON resources under the repository's ontology/ directory.

    The ontology/cadence_eoo_manifest.json file defines the default version and available ontology versions.

    v0: September 2026 manuscript-associated ontology snapshot.
    v1: Subsequent ontology expansion; provisional and not released.

    Only released and selectable versions can be loaded.
    Future versions may appear in the version selector but remain disabled until their corresponding datasets are released.

Implementation:
    Standalone, read-only ontology explorer using FastAPI and Uvicorn.
    Loads versioned ontology datasets from local JSON resources.

Command-Line Usage:
    python cadence_eo_ontology_explorer.py
    python cadence_eo_ontology_explorer.py -h
    python cadence_eo_ontology_explorer.py --help
    python cadence_eo_ontology_explorer.py -cev v0
    python cadence_eo_ontology_explorer.py --port 8011

Command-Line Options:
    -h, --help
        Display command-line help and exit.

    -cev, --cadence-eoo-version VERSION
        Select the initial ontology dataset version.
        Default: version specified in the ontology manifest.

    --host HOST
        Server bind address.
        Default: 127.0.0.1

    --port PORT
        Local server port.
        Default: 8010

Local Access:
    http://127.0.0.1:8010/cadence-ontology/

Security:
    The server binds to the local loopback interface by default.
    HTTP is intended for local access only.
    Do not expose the development server directly to the public
    Internet.

Attribution:
    CADENCE-EOO ontology datasets and associated scientific work:
    Prasanjit Dash and Paul M. DiGiacomo.

    Repository:
    https://github.com/DrPDash/EOO-KG

Licensing:
    CADENCE-EOO v0 ontology datasets are licensed under CC BY 4.0.
    Refer to the repository LICENSE for dataset attribution terms.
    Software reuse permissions are not established by that dataset
    license.

November 2026
"""

import argparse
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse

CATEGORIES = {'parameters': ('Parameters', 'params_map.json',
                             ('class', 'allowed_units', 'unit_dimension', 'native', 'derived_from', 'aliases',
                              'long_name', 'parent')), 'processes': ('Processes', 'processes_map.json',
                                                                     ('class', 'process_scope', 'long_name', 'aliases',
                                                                      'parent')),
              'methods': ('Methods', 'methods_map.json', ('class', 'parent', 'long_name', 'aliases')),
              'sensors': ('Sensors', 'sensors_map.json', ('class', 'sensor_type', 'platform', 'long_name', 'aliases')),
              'systems': ('Systems', 'systems_map.json', ('class', 'system_type', 'long_name', 'aliases')),
              'regions': ('Regions', 'regions_map.json', ('class', 'parent', 'type', 'aliases', 'long_name'))}

HTML = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n<title>CADENCE Ontology Explorer</title>\n<style>\n:root{color-scheme:light dark;font-family:system-ui,-apple-system,sans-serif}body{margin:0;background:Canvas;color:CanvasText}header{padding:24px max(20px,calc((100% - 1150px)/2));border-bottom:1px solid #8885}h1{margin:0 0 8px;font-size:1.7rem}main{max-width:1150px;margin:25px auto;padding:0 20px}button,input,select{font:inherit}select{padding:8px;margin:8px 0 18px;display:block;background:Canvas;color:CanvasText;border:1px solid #8888;border-radius:8px}input{padding:12px;border:1px solid #8888;border-radius:9px;width:100%;box-sizing:border-box;background:Canvas;color:CanvasText}.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.tabs button{padding:9px 13px;border:1px solid #8887;border-radius:9px;background:transparent;color:inherit;cursor:pointer}.tabs button[aria-pressed=true]{background:#225a9b;color:white}.layout{display:grid;grid-template-columns:minmax(230px,1fr) minmax(320px,2fr);gap:18px}.pane{border:1px solid #8886;border-radius:12px;padding:14px;min-height:230px}.list{max-height:50vh;overflow:auto}.item{display:block;text-align:left;width:100%;padding:10px;margin:2px 0;border:0;border-radius:7px;background:transparent;color:inherit;cursor:pointer}.item:hover,.item[aria-current=true]{background:#8883}.muted{opacity:.7;font-size:.9rem}.field{border-top:1px solid #8884;padding:12px 0;overflow-wrap:anywhere}.field strong{display:block;font-size:.85rem;margin-bottom:5px}.tag{display:inline-block;padding:4px 8px;margin:3px;border-radius:7px;background:#8882}.link{border:0;background:none;color:#3a86c9;cursor:pointer;text-decoration:underline;padding:0;font:inherit}#status{margin:10px 0}@media(max-width:700px){.layout{grid-template-columns:1fr}.list{max-height:30vh}}\n</style></head><body>\n<header>\n    <h1>📚 CADENCE Ontology Explorer</h1>\n    <div class="muted">\n        Scientific concepts and their relationships · Read-only\n        <a href="https://github.com/DrPDash/EOO-KG"\n           target="_blank"\n           rel="noopener noreferrer"\n           title="View EOO-KG on GitHub"\n           style="font-size: 0.85em; margin-left: 12px; display: inline-flex; align-items: center; gap: 5px; vertical-align: middle;">\n            <svg width="14"\n                 height="14"\n                 viewBox="0 0 24 24"\n                 fill="none"\n                 stroke="currentColor"\n                 stroke-width="2"\n                 stroke-linecap="round"\n                 stroke-linejoin="round"\n                 aria-hidden="true">\n                <path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 19 4.77 5.07 5.07 0 0 0 18.91 1S17.73.65 15 2.48a13.38 13.38 0 0 0-7 0C5.27.65 4.09 1 4.09 1A5.07 5.07 0 0 0 4 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 8 18.13V22"/>\n            </svg>\n            EOO-KG ↗\n        </a>\n    </div>\n</header>\n<main><label for="version">Ontology version</label><select id="version" aria-label="Ontology version"></select><label for="search">Search names, classes, and aliases</label><input id="search" type="search" placeholder="Search ontology concepts" autocomplete="off"><nav id="tabs" class="tabs" aria-label="Ontology categories"></nav><div id="status" class="muted" role="status"></div><div class="layout"><section class="pane"><div id="items" class="list"></div></section><section class="pane" id="detail"><p class="muted">Select a concept to inspect its scientific attributes.</p></section></div></main>\n<script>\n\'use strict\';\nconst categories=[\'parameters\',\'processes\',\'methods\',\'sensors\',\'systems\',\'regions\'];\nconst labels={parameters:\'Parameters\',processes:\'Processes\',methods:\'Methods\',sensors:\'Sensors\',systems:\'Systems\',regions:\'Regions\'};\nlet active=\'parameters\',records=[],selected=null,seq=0;\nconst $=id=>document.getElementById(id);\nconst human=s=>s.replace(/_/g,\' \').replace(/\\b\\w/g,x=>x.toUpperCase());\nfunction text(tag,value,cls){const el=document.createElement(tag);el.textContent=String(value);if(cls)el.className=cls;return el;}\nfunction drawTabs(){const el=$(\'tabs\');el.replaceChildren();for(const key of categories){const b=text(\'button\',labels[key]);b.setAttribute(\'aria-pressed\',String(key===active));b.onclick=()=>{active=key;selected=null;drawTabs();load();};el.append(b);}}\nfunction displayName(row){return row.long_name||human(row.name);}\nfunction drawList(){const q=$(\'search\').value.trim().toLowerCase();const found=records.filter(r=>[r.name,r.class,r.long_name,...(r.aliases||[])].filter(x=>typeof x===\'string\').some(x=>x.toLowerCase().includes(q)));const el=$(\'items\');el.replaceChildren();for(const row of found){const b=text(\'button\',displayName(row),\'item\');b.setAttribute(\'aria-current\',String(selected?.name===row.name));b.onclick=()=>{selected=row;drawList();drawDetail();};el.append(b);}if(!found.length)el.append(text(\'p\',\'No matching concepts.\',\'muted\'));$(\'status\').textContent=found.length+\' of \'+records.length+\' \'+labels[active].toLowerCase();}\nfunction drawDetail(){const el=$(\'detail\');el.replaceChildren();if(!selected){el.append(text(\'p\',\'Select a concept to inspect its scientific attributes.\',\'muted\'));return;}el.append(text(\'h2\',displayName(selected)));el.append(text(\'p\',selected.name,\'muted\'));for(const [key,value] of Object.entries(selected)){if(key===\'name\'||key===\'long_name\'||value===null)continue;const field=document.createElement(\'div\');field.className=\'field\';field.append(text(\'strong\',human(key)));const values=Array.isArray(value)?value:[value];for(const val of values){const span=text(\'span\',typeof val===\'boolean\'?(val?\'Yes\':\'No\'):val,\'tag\');field.append(span);}el.append(field);}}\nasync function load(){const id=++seq;$(\'status\').textContent=\'Loading…\';$(\'items\').replaceChildren();$(\'detail\').replaceChildren();try{const response=await fetch(\'/cadence-ontology/api/\'+active+\'?version=\'+encodeURIComponent($(\'version\').value),{cache:\'no-store\'});if(!response.ok)throw Error(\'Ontology access unavailable (\'+response.status+\').\');const data=await response.json();if(id!==seq)return;records=data.items;selected=null;drawList();drawDetail();}catch(e){if(id!==seq)return;records=[];$(\'status\').textContent=e.message;$(\'detail\').append(text(\'p\',\'No ontology records were loaded.\',\'muted\'));}}\nasync function initialize(){try{const response=await fetch(\'/cadence-ontology/api/versions\',{cache:\'no-store\'});if(!response.ok)throw Error(\'Ontology versions unavailable\');const manifest=await response.json();const selector=$(\'version\');selector.replaceChildren();for(const entry of manifest.versions){const option=document.createElement(\'option\');option.value=entry.id;option.textContent=entry.label;option.disabled=entry.selectable!==true||entry.status!==\'released\';selector.append(option);}selector.value=manifest.default_version;const future=manifest.versions.filter(e=>e.status===\'future\');if(future.length){const notice=document.createElement(\'p\');notice.className=\'muted\';notice.textContent=future.map(e=>e.label+\' — \'+e.description).join(\' | \');selector.insertAdjacentElement(\'afterend\',notice);}selector.addEventListener(\'change\',()=>{selected=null;load();});drawTabs();load();}catch(e){$(\'status\').textContent=e.message;}}\n$(\'search\').addEventListener(\'input\',drawList);initialize();\n</script></body></html>'

PROJECT_ROOT = Path(__file__).resolve().parent
ONTOLOGY_ROOT = PROJECT_ROOT / "ontology"
MANIFEST_PATH = ONTOLOGY_ROOT / "cadence_eoo_manifest.json"
DEFAULT_EOO_VERSION = None  # CLI override; otherwise manifest default


def load_manifest():
    try:
        manifest_data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read ontology manifest: {MANIFEST_PATH}") from exc
    versions = manifest_data.get("versions")
    if not isinstance(versions, list) or not versions:
        raise ValueError("Manifest must contain a nonempty versions list")
    ids = []
    for entry in versions:
        if not isinstance(entry, dict):
            raise ValueError("Invalid version entry")
        version = entry.get("id")
        if (not isinstance(version, str) or not version.isascii() or
                not version or not all(c.isalnum() or c in "_-" for c in version) or
                version in (".", "..") or not isinstance(entry.get("label"), str)):
            raise ValueError("Invalid version ID or label")
        if version in ids:
            raise ValueError(f"Duplicate ontology version: {version}")
        if entry.get("status") not in ("released", "future") or type(entry.get("selectable")) is not bool:
            raise ValueError(f"Invalid release metadata for: {version}")
        if entry["status"] == "released" and entry["selectable"] and not (ONTOLOGY_ROOT / version).is_dir():
            raise ValueError(f"Missing released ontology directory: {version}")
        ids.append(version)
    if manifest_data.get("default_version") not in {e["id"] for e in versions if
                                                    e["status"] == "released" and e["selectable"]}:
        raise ValueError("Manifest default_version must be released and selectable")
    return manifest_data


def version_ids():
    return {entry["id"] for entry in load_manifest()["versions"]
            if entry["status"] == "released" and entry["selectable"]}


app = FastAPI(title="CADENCE Standalone Ontology Explorer", docs_url=None, redoc_url=None, openapi_url=None)
NO_CACHE = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"}


@app.get("/cadence-ontology/", response_class=HTMLResponse)
def explorer():
    html = HTML
    return HTMLResponse(
        html,
        headers={
            **NO_CACHE,
            "Content-Security-Policy": (
                "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
                "connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
            ),
        },
    )


@app.get("/cadence-ontology/api/versions")
def available_versions():
    try:
        ontology_manifest = load_manifest()
    except ValueError:
        raise HTTPException(status_code=503, detail="Ontology manifest unavailable")
    return JSONResponse({"versions": [{"id": entry["id"], "label": entry["label"],
                                       "status": entry["status"], "selectable": entry["selectable"],
                                       "description": entry.get("description", "")}
                                      for entry in ontology_manifest["versions"]],
                         "default_version": DEFAULT_EOO_VERSION or ontology_manifest["default_version"]},
                        headers=NO_CACHE)


@app.get("/cadence-ontology/api/{category}")
def category_data(category: str, version: str = Query(default=None)):
    try:
        ontology_manifest = load_manifest()
    except ValueError:
        raise HTTPException(status_code=503, detail="Ontology manifest unavailable")

    version = version or DEFAULT_EOO_VERSION or ontology_manifest["default_version"]
    if version not in {entry["id"] for entry in ontology_manifest["versions"]
                       if entry["status"] == "released" and entry["selectable"]}:
        raise HTTPException(status_code=404, detail="Unknown ontology version")
    if category not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Unknown category")

    label, filename, fields = CATEGORIES[category]
    try:
        raw = json.loads((ONTOLOGY_ROOT / version / filename).read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise HTTPException(status_code=503, detail="Ontology data unavailable")
    if not isinstance(raw, dict):
        raise HTTPException(status_code=503, detail="Ontology data format unsupported")

    items = []
    for name, record in raw.items():
        if not isinstance(name, str) or not isinstance(record, dict):
            continue
        item = {"name": name}
        for field in fields:
            value = record.get(field)
            if type(value) in (str, bool, int, float) or (
                    isinstance(value, list)
                    and all(type(element) in (str, bool, int, float) for element in value)
            ):
                item[field] = value
        items.append(item)
    items.sort(
        key=lambda record_item: str(
            record_item.get("long_name") or record_item["name"]
        ).casefold()
    )
    return JSONResponse({"category": label, "items": items}, headers=NO_CACHE)


def main():
    global DEFAULT_EOO_VERSION
    parser = argparse.ArgumentParser(description="CADENCE-EOO read-only ontology explorer", usage=argparse.SUPPRESS)
    parser.add_argument("-cev", "--cadence-eoo-version", default=None,
                        help="Initial ontology dataset version (default: manifest default)")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8010, help="Local port (default: 8010)")
    args = parser.parse_args()
    try:
        startup_manifest = load_manifest()
    except ValueError as exc:
        parser.error(str(exc))
    if args.cadence_eoo_version and args.cadence_eoo_version not in version_ids():
        parser.error(f"Ontology version is not released: {args.cadence_eoo_version}")
    DEFAULT_EOO_VERSION = args.cadence_eoo_version or startup_manifest["default_version"]

    import uvicorn

    print(f"Ontology data: {ONTOLOGY_ROOT}")
    print(f"Initial ontology version: {DEFAULT_EOO_VERSION}")
    # noinspection HttpUrlsUsage
    print(f"Explorer: http://{args.host}:{args.port}/cadence-ontology/")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
