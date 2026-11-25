"""Replay frozen upstream evidence and publish Checks on an isolated demo PR."""
import base64
import copy
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_bot_run_request as gate
from ai_test_scope import InferenceHub, PytestTargetSelector, TargetSelectionError

ROOT = Path(__file__).resolve().parents[3]
DESTINATION = "kangbintNV/flashinfer"


class HistoricalSource(gate.Client):
    """Read an actual pinned merge tree; never execute historical PR source."""
    def __init__(self, manifest):
        super().__init__(DESTINATION, timeout=540)
        self.manifest = manifest
        self.pr = copy.deepcopy(manifest["pr"])
        # Reopen only the evidence descriptor for a historical pre-merge replay.
        self.pr["state"] = "open"
        self.pr["base"]["repo"]["full_name"] = DESTINATION

    def get_pr_details(self, number):
        assert number == self.pr["number"]
        return copy.deepcopy(self.pr)

    def get_pr_files(self, number):
        assert number == self.pr["number"]
        return self.manifest["files"]

    def get_current_base_sha(self, pr):
        return self.manifest["source_base_sha"]

    def get_pr_merge_commit(self, repository, number, base_sha, head_sha):
        commit = self.api(f"repos/{DESTINATION}/git/commits/{self.manifest['snapshot_sha']}")
        if [p["sha"] for p in commit["parents"]] != [base_sha, head_sha]:
            raise TargetSelectionError("Replay snapshot parent identity mismatch")
        if commit["tree"]["sha"] != self.manifest["source_merge_tree"]:
            raise TargetSelectionError("Replay snapshot differs from original merged source")
        return commit

    def get_repository_tree(self, repository, sha):
        return self.api(f"repos/{DESTINATION}/git/trees/{sha}?recursive=1")

    def get_repository_blob(self, repository, sha, max_bytes):
        data = self.api(f"repos/{DESTINATION}/git/blobs/{sha}")
        if data.get("encoding") != "base64" or data.get("size", 0) > max_bytes:
            raise TargetSelectionError("Historical evidence blob is unavailable or too large")
        return base64.b64decode(data["content"]).decode("utf-8")


def target_pr(client, head_sha, expected_base):
    for _ in range(30):
        prs = client.request(f"repos/{DESTINATION}/commits/{head_sha}/pulls")
        matches = [p for p in prs if p["state"] == "open" and p["base"]["ref"] == expected_base and p["head"]["sha"] == head_sha]
        if len(matches) == 1:
            return matches[0]
        time.sleep(5)
    raise TargetSelectionError("Demo PR was not associated with this exact head within 150s")


def preflight():
    model = InferenceHub()
    model.deadline = time.monotonic() + 120
    result = model.complete({"purpose": "API connectivity smoke test; no source code"}, 'Return JSON only: {"ok": true}.')
    if result.get("ok") is not True:
        raise TargetSelectionError("Inference API preflight did not return the expected response")
    print("Inference API preflight passed. Secret value was not logged.")
    return {"mode": "preflight", "ok": True, "model": model.model}


def run(manifest):
    source = HistoricalSource(manifest)
    destination = gate.Client(DESTINATION, timeout=660)
    pr = target_pr(destination, os.environ["GITHUB_SHA"], manifest["demo_base_branch"])
    frozen_head = {"number": pr["number"], "head": {"sha": os.environ["GITHUB_SHA"]}}
    memo = {}

    def analyze():
        if "impact" not in memo:
            changed = manifest["files"]
            if gate.docs_only(changed, manifest["pr"]["changed_files"]):
                memo["impact"] = {"classification": "docs_only", "reason": "Only Markdown/RST documentation changed.", "evidence_paths": [f["filename"] for f in changed], "case_gap": "", "targets": []}
            else:
                selector = PytestTargetSelector(source, lambda path: manifest["trusted_ci"][path])
                try:
                    selection = selector.select(source.pr, include_gpu_impact=True)
                    memo["impact"] = {**selection.gpu_impact, "targets": selection.paths}
                finally:
                    source.deadline = time.monotonic() + 60
        return memo["impact"]

    prefix = (f"**Historical replay — upstream [PR #{manifest['upstream_number']}]({manifest['upstream_url']}).**\n\n"
              "Uses frozen original comments with their real author identities. No bot comments were impersonated or posted here.\n\n")
    results = {}
    for name, comments, extra in [
        ("Bot Run Request Check", manifest["comments"], ""),
        ("GPU Impact — no-reply scenario", [], "**Counterfactual:** original replies are withheld to exercise GPU classification. A GPU-related failure is an expected policy result.\n\n"),
    ]:
        gate.CHECK_NAME = name
        check_id = destination.begin(frozen_head)
        result = gate.evaluate(comments, analyze)
        result = replace(result, summary=prefix + extra + result.summary)
        destination.publish(frozen_head, result, check_id, manifest["source_base_sha"])
        results[name] = asdict(result)
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as stream:
            stream.write(f"## {name}\n\n**{result.title}**\n\n{result.summary}\n\n")
        print(name, result.conclusion, result.reason)
    return {"upstream_number": manifest["upstream_number"], "demo_pr": pr["number"], "demo_url": pr["html_url"], "head_sha": os.environ["GITHUB_SHA"], "source_base_sha": manifest["source_base_sha"], "source_head_sha": source.pr["head"]["sha"], "gate_version": manifest["gate_version"], "results": results}


def main():
    output = ROOT / "reports/result.json"
    output.parent.mkdir(exist_ok=True)
    manifest = json.loads((ROOT / "experiments/source.json").read_text())
    try:
        result = preflight() if manifest.get("mode") == "preflight" else run(manifest)
    except Exception as error:
        output.write_text(json.dumps({"mode": manifest.get("mode"), "ok": False, "error": gate._public_prose(str(error), (os.getenv("GH_TOKEN"), os.getenv("INFERENCE_API_KEY")))}, indent=2))
        # Public errors only; no raw HTTP bodies or environment dumps.
        print(gate._public_prose(str(error), (os.getenv("GH_TOKEN"), os.getenv("INFERENCE_API_KEY"))), file=sys.stderr)
        return 1
    output.write_text(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
