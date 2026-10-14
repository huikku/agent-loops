#!/usr/bin/env python3
"""fetch_candidates.py: Layer 1 deterministic candidate ingestion and deduplication.
Pulls articles from raw sources (mocked for reproducibility), cross-references
against seen_urls.txt, and stages clean novel candidates for Layer 2.
Zero AI token cost.
"""
import json
import os
import sys

RAW_CANDIDATE_POOL = [
    {
        "url": "https://example.com/already-read-article-101",
        "title": "Old Article On Transformers",
        "source": "TechFeed",
        "body": "A general overview of basic transformer attention."
    },
    {
        "url": "https://arxiv.org/abs/2610.04812",
        "title": "Gated DeltaNet Layer Sizing & Memory Bandwidth Inferences",
        "source": "arXiv cs.LG",
        "body": "Empirical analysis showing a 3:1 linear-to-softmax attention ratio achieves O(1) state memory while maintaining 65k context with only 4GB KV cache."
    },
    {
        "url": "https://techhype.io/top-10-ai-tools-2026",
        "title": "Top 10 AI Tools to Boost Your Daily Hustle in 2026",
        "source": "TechHype",
        "body": "Here are 10 amazing affiliate tools that will completely automate your life with no effort required."
    },
    {
        "url": "https://alienrobot.com/2026-10-14-qwen-3-8-local-hardware-sizing.html",
        "title": "Running Qwen 3.8 locally: from an 8GB RTX 3050 to a 128GB Thor dev kit",
        "source": "Alienrobot Devlog",
        "body": "Benchmarking token decode throughput across consumer GPUs, PCIe bandwidth penalty laws, and speculative decoding draft heads."
    },
    {
        "url": "https://standardco.de/ai-series/volume-5-loops",
        "title": "AI Agent Loops: Automate the Work, Keep the Judgment",
        "source": "Standard Co",
        "body": "Exploring the 3-layer loop engineering architecture: deterministic scripts, agent reasoning, and human policy ownership."
    }
]

def load_seen_urls(seen_file="seen_urls.txt") -> set:
    if not os.path.exists(seen_file):
        return set()
    with open(seen_file, "r") as f:
        return set(line.strip() for line in f if line.strip())

def main():
    seen = load_seen_urls()
    novel_candidates = []

    for item in RAW_CANDIDATE_POOL:
        if item["url"] in seen:
            print(f"[DEDUPED] Skipping already processed URL: {item['url']}")
        else:
            novel_candidates.append(item)

    out_file = "staged_candidates.json"
    with open(out_file, "w") as f:
        json.dump(novel_candidates, f, indent=2)

    print(f"\n[✓] Ingested {len(RAW_CANDIDATE_POOL)} items.")
    print(f"[✓] Filtered {len(RAW_CANDIDATE_POOL) - len(novel_candidates)} duplicates using seen_urls.txt.")
    print(f"[✓] Staged {len(novel_candidates)} novel candidates into {out_file}.")

if __name__ == "__main__":
    main()
