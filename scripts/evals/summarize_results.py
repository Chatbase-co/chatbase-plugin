#!/usr/bin/env python3
"""Print a compact summary of a `claude plugin eval --json` result: per case and arm, the score, each
grader's verdict (failures with their reason), run errors, turns and cost.

    python3 -I summarize_results.py <result.json> [--failures]
"""
import json
import sys


def main():
    d = json.load(open(sys.argv[1]))
    only_fail = "--failures" in sys.argv
    agg = d.get("aggregates", {})
    print(f"overall {agg.get('overallScore')} passed {agg.get('casesPassed')}/{agg.get('casesTotal')} "
          f"cost ${d.get('costUsd', 0):.2f} {d.get('durationSeconds', 0)}s")
    for c in d.get("cases", []):
        a = c.get("aggregates", {})
        print(f"\n== {c['name']}  score {a.get('score')}  " + json.dumps({k: v for k, v in a.items() if k != 'score'}))
        for arm, runs in c.get("arms", {}).items():
            for i, r in enumerate(runs):
                line = f"  [{arm} #{i}] score {r.get('score')} turns {r.get('turns')} ${r.get('costUsd', 0):.2f}"
                if r.get("error"):
                    line += f" ERROR {r['error'][:300]}"
                print(line)
                for g in r.get("graders", r.get("graderResults", [])):
                    ok = g.get("passed", g.get("pass"))
                    if only_fail and ok:
                        continue
                    why = g.get("reason") or g.get("explanation") or g.get("detail") or ""
                    if isinstance(why, (dict, list)):
                        why = json.dumps(why)
                    print(f"     {'PASS' if ok else 'FAIL'} {g.get('name')}: {str(why)[:400]}")


if __name__ == "__main__":
    main()
