#!/usr/bin/env python3
"""Build eval mock files for the Chatbase MCP server from Chatbase's public OpenAPI spec.

The Chatbase MCP server (https://mcp.chatbase.co/api/mcp) needs OAuth even to list its tools, so the
evals can't record its real `tools/list`. Its tools are generated from API v2 operations marked with
`x-mcp` in the spec that ships in the official CLI package (`npm pack chatbase`, file spec/openapi.json).
This script turns those operations into:

  <out>/_tools.json      a tools/list response: name, description, inputSchema, annotations per tool
  <out>/_responses.md    the 200-response shape of each tool, for the agent mock to imitate

    python3 -I gen_mcp_tools.py <path to openapi.json> <out dir>

MCP-only extensions the API spec doesn't carry (from the plugin's own `chatbase` skill) are added at the end:
chatbase_whoami, `searches` on chatbase_search_conversations, `include` on chatbase_export_conversations,
`includeMessages`/`messageTypes` on chatbase_list_tickets. Standard library only.
"""
import copy
import json
import os
import sys


def resolve(node, spec, refs=0):
    """Inline every $ref. `refs` counts nested $ref hops only, so a recursive schema (procedure steps)
    stops at a plain object instead of looping; ordinary nesting is never cut."""
    if isinstance(node, dict):
        if "$ref" in node:
            if refs > 6:
                return {"type": "object"}
            target = spec
            for part in node["$ref"].lstrip("#/").split("/"):
                target = target[part]
            out = resolve(copy.deepcopy(target), spec, refs + 1)
            if isinstance(out, dict):
                out.update({k: v for k, v in node.items() if k != "$ref"})
            return out
        # `pattern` is dropped: Claude Code refuses a tool whose schema has a regex it can't compile
        # (the spec's email and one-line patterns), and the real server validates them anyway.
        return {k: resolve(v, spec, refs) for k, v in node.items() if k not in ("example", "examples", "pattern")}
    if isinstance(node, list):
        return [resolve(v, spec, refs) for v in node]
    return node


def input_schema(op, spec):
    props, required = {}, []
    for prm in op.get("parameters", []):
        prm = resolve(prm, spec)
        sch = prm.get("schema", {})
        if prm.get("description") and "description" not in sch:
            sch["description"] = prm["description"]
        props[prm["name"]] = sch
        if prm.get("required"):
            required.append(prm["name"])
    body = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
    if body:
        body = resolve(body, spec)
        variants = body.get("oneOf") or body.get("anyOf")
        if isinstance(variants, list):
            # A body with several shapes (text / qna / link sources): offer every field, require only
            # what all shapes require, and merge the `type` enums so each shape stays sendable.
            common = None
            for var in variants:
                for k, v in var.get("properties", {}).items():
                    if k in props and "enum" in v and "enum" in props[k]:
                        props[k]["enum"] = sorted(set(props[k]["enum"]) | set(v["enum"]))
                    else:
                        props.setdefault(k, v)
                req = set(var.get("required", []))
                common = req if common is None else common & req
            required += sorted(r for r in (common or []) if r not in required)
        for k, v in body.get("properties", {}).items():
            props[k] = v
        required += [r for r in body.get("required", []) if r not in required]
    schema = {"type": "object", "properties": props}
    if required:
        schema["required"] = required
    return schema


def skeleton(schema, depth=0):
    """A compact, human-readable shape of a response schema."""
    if depth > 5 or not isinstance(schema, dict):
        return "…"
    for key in ("oneOf", "anyOf"):
        if isinstance(schema.get(key), list) and schema[key]:
            return skeleton(schema[key][0], depth)
    if "allOf" in schema:
        merged = {"type": "object", "properties": {}}
        for part in schema["allOf"]:
            merged["properties"].update(part.get("properties", {}))
        return skeleton(merged, depth)
    t = schema.get("type")
    if isinstance(t, list) and "object" in t and "properties" not in schema:
        return "|".join(t)
    if t == "object" or (isinstance(t, list) and "object" in t) or "properties" in schema:
        return {k: skeleton(v, depth + 1) for k, v in schema.get("properties", {}).items()}
    if t == "array" or (isinstance(t, list) and "array" in t):
        return [skeleton(schema.get("items", {}), depth + 1)]
    if "enum" in schema:
        return "|".join(str(e) for e in schema["enum"])
    if isinstance(t, list):
        return "|".join(str(x) for x in t)
    return t or "any"


def main():
    spec_path, out = sys.argv[1], sys.argv[2]
    spec = json.load(open(spec_path))
    os.makedirs(out, exist_ok=True)
    tools, responses = [], []
    for path, ops in spec["paths"].items():
        for method, op in ops.items():
            mcp = op.get("x-mcp") if isinstance(op, dict) else None
            if not mcp:
                continue
            desc = (op.get("summary", "") + ". " + op.get("description", "")).strip(". ").strip()
            tools.append({
                "name": mcp["tool"],
                "description": desc,
                "inputSchema": input_schema(op, spec),
                "annotations": {
                    "readOnlyHint": bool(mcp.get("annotations", {}).get("readOnly")),
                    "destructiveHint": bool(mcp.get("annotations", {}).get("destructive")),
                    "idempotentHint": bool(mcp.get("annotations", {}).get("idempotent")),
                },
            })
            ok = op.get("responses", {}).get("200") or op.get("responses", {}).get("201") or {}
            body = resolve(ok, spec).get("content", {}).get("application/json", {}).get("schema", {})
            shape = skeleton(body)
            # The MCP server trims list items to `x-mcp.fields` (list_agents has no instructions), and caps pages.
            if mcp.get("fields") and isinstance(shape, dict) and isinstance(shape.get("data"), list) and shape["data"] and isinstance(shape["data"][0], dict):
                shape["data"] = [{k: v for k, v in shape["data"][0].items() if k in mcp["fields"]}]
            if mcp.get("maxItems") and isinstance(shape, dict):
                shape["_maxItemsPerPage"] = mcp["maxItems"]
            responses.append((mcp["tool"], method.upper(), path, shape))

    by_name = {t["name"]: t for t in tools}
    tools.append({
        "name": "chatbase_whoami",
        "description": "Who is signed in: the user id, the team, the plan and the scopes this connection was granted.",
        "inputSchema": {"type": "object", "properties": {}},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True},
    })
    responses.append(("chatbase_whoami", "-", "-", {"userId": "string", "teamName": "string", "plan": "string", "scopes": ["string"]}))

    search = by_name.get("chatbase_search_conversations")
    if search:
        single = copy.deepcopy(search["inputSchema"]["properties"])
        single.pop("agentId", None)
        single.pop("cursor", None)
        search["inputSchema"]["properties"]["searches"] = {
            "type": "array", "maxItems": 5,
            "description": "Up to 5 searches run together, each with the same filters as a single search. Results come back per search.",
            "items": {"type": "object", "properties": single},
        }
    export = by_name.get("chatbase_export_conversations")
    if export:
        export["inputSchema"]["properties"].setdefault("include", {
            "type": "string", "enum": ["summary", "messages"],
            "description": "summary (default) omits message bodies; messages returns full transcripts. Use messages with one conversationId.",
        })
        export["inputSchema"]["properties"].setdefault("conversationId", {"type": "string", "description": "Export one conversation."})
    tickets = by_name.get("chatbase_list_tickets")
    if tickets:
        tickets["inputSchema"]["properties"].setdefault("includeMessages", {"type": "boolean", "description": "Attach each ticket's first 25 replies and notes."})
        tickets["inputSchema"]["properties"].setdefault("messageTypes", {"type": "string", "description": "Comma-separated: reply, note, event."})

    json.dump({"tools": tools}, open(os.path.join(out, "_tools.json"), "w"), indent=1)
    with open(os.path.join(out, "_responses.md"), "w") as f:
        f.write("# Chatbase MCP response shapes (generated from the API v2 spec)\n\n")
        for name, method, path, shape in responses:
            f.write(f"- `{name}` ({method} {path}): `{json.dumps(shape, separators=(',', ':'))}`\n")
    print(f"{len(tools)} tools -> {out}")


if __name__ == "__main__":
    main()
