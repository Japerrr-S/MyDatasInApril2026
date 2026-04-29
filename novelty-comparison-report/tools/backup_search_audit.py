from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import requests


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def search_openalex(query: str, limit: int) -> list[dict[str, Any]]:
    response = requests.get(
        "https://api.openalex.org/works",
        params={
            "search": query,
            "per-page": limit,
            "sort": "relevance_score:desc",
        },
        timeout=30,
    )
    response.raise_for_status()
    works = response.json().get("results", [])
    papers = []
    for work in works:
        host_venue = work.get("primary_location") or {}
        source = (host_venue.get("source") or {}) if isinstance(host_venue, dict) else {}
        papers.append(
            {
                "title": work.get("title"),
                "year": work.get("publication_year"),
                "venue": source.get("display_name"),
                "citationCount": work.get("cited_by_count"),
                "url": work.get("doi") or work.get("id"),
                "source": "openalex",
            }
        )
    return papers


def search_arxiv(query: str, limit: int) -> list[dict[str, Any]]:
    encoded = urllib.parse.urlencode(
        {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    )
    response = requests.get(
        f"https://export.arxiv.org/api/query?{encoded}",
        timeout=30,
        headers={"User-Agent": "novelty-comparison-report/0.1"},
    )
    response.raise_for_status()
    root = ET.fromstring(response.text)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    for entry in root.findall("atom:entry", namespace):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=namespace) or "").split())
        published = entry.findtext("atom:published", default="", namespaces=namespace) or ""
        link = entry.findtext("atom:id", default="", namespaces=namespace)
        papers.append(
            {
                "title": title,
                "year": int(published[:4]) if published[:4].isdigit() else None,
                "venue": "arXiv",
                "citationCount": None,
                "url": link,
                "source": "arxiv",
            }
        )
    return papers


def unique_queries(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    selected = []
    for event in events:
        query = (event.get("query") or "").strip()
        if not query or query in seen:
            continue
        seen.add(query)
        selected.append(event)
    return selected


def run_backup_search(input_path: Path, out_dir: Path, sources: list[str], limit: int, sleep: float) -> None:
    events = unique_queries(read_jsonl(input_path))
    rows = []
    summary: list[dict[str, Any]] = []
    for event in events:
        query = event["query"]
        for source in sources:
            error = None
            papers: list[dict[str, Any]] = []
            try:
                if source == "openalex":
                    papers = search_openalex(query, limit)
                elif source == "arxiv":
                    papers = search_arxiv(query, limit)
                else:
                    raise ValueError(f"Unknown source: {source}")
            except Exception as exc:
                error = str(exc)
            row = {
                "idea_name": event.get("idea_name"),
                "checker": event.get("checker"),
                "round_index": event.get("round_index"),
                "original_query": query,
                "backup_source": source,
                "papers": papers,
            }
            if error:
                row["error"] = error
            rows.append(row)
            summary.append(
                {
                    "idea_name": event.get("idea_name"),
                    "checker": event.get("checker"),
                    "round_index": event.get("round_index"),
                    "query": query,
                    "backup_source": source,
                    "num_results": len(papers),
                    "titles": [paper.get("title") for paper in papers if paper.get("title")],
                    "error": error,
                }
            )
            if sleep > 0:
                time.sleep(sleep)
    append_jsonl(out_dir / "backup_search_events.jsonl", rows)
    write_json(out_dir / "backup_search_audit.json", summary)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run backup literature searches for captured novelty queries.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--sources", default="openalex,arxiv")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--sleep", type=float, default=1.0)
    args = parser.parse_args()
    sources = [source.strip().lower() for source in args.sources.split(",") if source.strip()]
    run_backup_search(args.input, args.out_dir, sources=sources, limit=args.limit, sleep=args.sleep)


if __name__ == "__main__":
    main()
