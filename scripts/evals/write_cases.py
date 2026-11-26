#!/usr/bin/env python3
"""Write a plugin's eval cases from a compact Python spec (one dict per case).

    python3 -I write_cases.py <cases.py> <plugin dir>

The spec file defines PLUGIN, SERVER and CASES, and optionally APPEND_SYSTEM_PROMPT (added to every case). Each case: name, prompt, optional tags/max_turns/runs,
skill (the skill that should fire), used / unused (tools that must / must not be called: a name, or {tool, match, min}),
order (pairs of tools), llm (a PASS/FAIL rubric on the final reply), regex (extra regex graders).
Tool names are the MCP tool names; this script adds the plugin prefix.
"""
import json
import os
import runpy
import shutil
import sys


def yaml_str(s):
    return json.dumps(s)  # a JSON string is a valid YAML double-quoted scalar


def main():
    spec = runpy.run_path(sys.argv[1])
    plugin_dir = sys.argv[2]
    prefix = f"mcp__plugin_{spec['PLUGIN']}_{spec['SERVER']}__"
    root = os.path.join(plugin_dir, "evals")
    for c in spec["CASES"]:
        d = os.path.join(root, c["name"])
        if os.path.isdir(os.path.join(d, "graders")):
            shutil.rmtree(os.path.join(d, "graders"))
        os.makedirs(os.path.join(d, "graders"), exist_ok=True)
        fm = [f"name: {c['name']}", f"tags: {json.dumps(c.get('tags', []))}",
              f"max_turns: {c.get('max_turns', 40)}", f"runs: {c.get('runs', 3)}",
              f"timeout_seconds: {c.get('timeout', 900)}"]
        if spec.get("APPEND_SYSTEM_PROMPT"):
            # Pins the date and setting the mock account is written for, so results don't shift with the clock.
            fm.append(f"append_system_prompt: {yaml_str(spec['APPEND_SYSTEM_PROMPT'])}")
        if c.get("expected"):
            fm.append(f"expected_outcome: {yaml_str(c['expected'])}")
        open(os.path.join(d, "prompt.md"), "w").write("---\n" + "\n".join(fm) + "\n---\n" + c["prompt"].strip() + "\n")
        g = {}
        if c.get("skill"):
            pattern = '"skill"' + r'\s*:\s*"(?:[\w-]+:)?' + c["skill"] + '"'
            g["skill-fired"] = "---\ntype: tool_used\ntool: Skill\narm: with-only\ninput_match: " + yaml_str(pattern) + "\n---\n"
        for i, t in enumerate(c.get("used", [])):
            t = t if isinstance(t, dict) else {"tool": t}
            body = f"---\ntype: tool_used\ntool: {prefix}{t['tool']}\nmin: {t.get('min', 1)}\n"
            if t.get("match"):
                body += f"input_match: {yaml_str(t['match'])}\n"
            g[f"uses-{i}-{t['tool'].replace('chatbase_', '')}"] = body + "---\n"
        for i, t in enumerate(c.get("unused", [])):
            t = t if isinstance(t, dict) else {"tool": t}
            body = f"---\ntype: tool_used\ntool: {prefix}{t['tool']}\nmin: 0\nmax: 0\n"
            if t.get("match"):
                body += f"input_match: {yaml_str(t['match'])}\n"
            g[f"never-{i}-{t['tool'].replace('chatbase_', '')}"] = body + "---\n"
        for i, (a, b) in enumerate(c.get("order", [])):
            g[f"order-{i}"] = f"---\ntype: tool_order\nbefore: {prefix}{a}\nafter: {prefix}{b}\n---\n"
        for i, r in enumerate(c.get("regex", [])):
            body = f"---\ntype: regex\npattern: {yaml_str(r['pattern'])}\n"
            for k in ("match", "flags", "target"):
                if r.get(k):
                    body += f"{k}: {r[k]}\n"
            g[r.get("name", f"regex-{i}")] = body + "---\n"
        if c.get("llm"):
            g["reply-quality"] = "---\ntype: llm\nweight: 2\n---\n" + c["llm"].strip() + "\n"
        for name, body in g.items():
            open(os.path.join(d, "graders", f"{name}.md"), "w").write(body)
    print(f"{len(spec['CASES'])} cases -> {root}")


if __name__ == "__main__":
    main()
