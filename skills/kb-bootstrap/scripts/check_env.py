#!/usr/bin/env python3
"""
Environment checker for OpenClaw KB Bootstrap.
Validates that the runtime has the required dependencies before setup.

Exit codes:
  0 — all checks passed
  1 — one or more checks failed (details printed to stdout as JSON)
"""

import json
import os
import shutil
import subprocess
import sys


def check_results():
    results = {
        "passed": [],
        "failed": [],
        "warnings": [],
    }

    # 1. Check OpenClaw is running (we're inside it, but verify workspace path)
    workspace = os.environ.get("OPENCLAW_WORKSPACE") or os.path.expanduser(
        "~/.openclaw/workspace"
    )
    if os.path.isdir(workspace):
        results["passed"].append(
            {
                "check": "workspace",
                "detail": f"Workspace directory exists: {workspace}",
            }
        )
    else:
        results["failed"].append(
            {
                "check": "workspace",
                "detail": f"Workspace directory not found: {workspace}",
                "fix": "Ensure OpenClaw is installed and initialized. Run: openclaw init",
            }
        )

    # 2. Check write access
    test_file = os.path.join(workspace, ".kb_write_test")
    try:
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        results["passed"].append(
            {"check": "write_access", "detail": "Workspace is writable"}
        )
    except (IOError, OSError) as e:
        results["failed"].append(
            {
                "check": "write_access",
                "detail": f"Cannot write to workspace: {e}",
                "fix": "Check file permissions on the workspace directory",
            }
        )

    # 3. Check LLM configuration
    openclaw_config = os.path.expanduser("~/.openclaw/openclaw.json")
    llm_configured = False
    lark_configured = False

    if os.path.isfile(openclaw_config):
        try:
            with open(openclaw_config) as f:
                config = json.load(f)

            # Check for any LLM provider key — check both env section and models.providers
            llm_found = []

            # Method 1: env section (e.g., GEMINI_API_KEY=...)
            env_section = config.get("env", {})
            env_llm_keys = [
                k
                for k in env_section
                if any(
                    p in k.upper()
                    for p in [
                        "GEMINI",
                        "OPENAI",
                        "ANTHROPIC",
                        "VOLCENGINE",
                        "DEEPSEEK",
                    ]
                )
            ]
            llm_found.extend(env_llm_keys)

            # Method 2: models.providers.*.apiKey (OpenClaw native config)
            providers = config.get("models", {}).get("providers", {})
            for name, prov in providers.items():
                if isinstance(prov, dict) and prov.get("apiKey"):
                    llm_found.append(f"models.providers.{name}")

            if llm_found:
                llm_configured = True
                results["passed"].append(
                    {
                        "check": "llm_config",
                        "detail": f"LLM provider(s) found: {', '.join(llm_found)}",
                    }
                )
            else:
                results["failed"].append(
                    {
                        "check": "llm_config",
                        "detail": "No LLM provider API key found in openclaw.json",
                        "fix": "Add at least one LLM provider in openclaw.json (env section or models.providers)",
                    }
                )

            # Check for Lark/Feishu channel config
            channels = config.get("channels", {})
            lark_channel = channels.get("lark") or channels.get("feishu")
            if lark_channel:
                lark_configured = True
                results["passed"].append(
                    {
                        "check": "lark_plugin",
                        "detail": "Lark/Feishu channel is configured",
                    }
                )
            else:
                results["warnings"].append(
                    {
                        "check": "lark_plugin",
                        "detail": "Lark/Feishu channel not found in config",
                        "fix": "If you plan to use Feishu, add a lark channel config to openclaw.json",
                    }
                )

        except (json.JSONDecodeError, KeyError) as e:
            results["failed"].append(
                {
                    "check": "config_parse",
                    "detail": f"Failed to parse openclaw.json: {e}",
                    "fix": "Ensure openclaw.json is valid JSON",
                }
            )
    else:
        results["failed"].append(
            {
                "check": "config_file",
                "detail": f"Config file not found: {openclaw_config}",
                "fix": "Run openclaw init or create openclaw.json manually",
            }
        )

    # 4. Check OpenClaw CLI version
    openclaw_bin = shutil.which("openclaw")
    if openclaw_bin:
        try:
            version_out = subprocess.check_output(
                ["openclaw", "--version"], stderr=subprocess.STDOUT, timeout=5
            ).decode().strip()
            results["passed"].append(
                {"check": "openclaw_cli", "detail": f"OpenClaw CLI: {version_out}"}
            )
        except Exception:
            results["warnings"].append(
                {
                    "check": "openclaw_cli",
                    "detail": "OpenClaw CLI found but --version failed",
                }
            )
    else:
        results["warnings"].append(
            {
                "check": "openclaw_cli",
                "detail": "OpenClaw CLI not in PATH (may be running embedded)",
            }
        )

    # 5. Check memory directory
    memory_dir = os.path.join(workspace, "memory")
    if not os.path.isdir(memory_dir):
        try:
            os.makedirs(memory_dir, exist_ok=True)
            results["passed"].append(
                {
                    "check": "memory_dir",
                    "detail": f"Created memory directory: {memory_dir}",
                }
            )
        except OSError as e:
            results["failed"].append(
                {
                    "check": "memory_dir",
                    "detail": f"Cannot create memory directory: {e}",
                }
            )
    else:
        results["passed"].append(
            {
                "check": "memory_dir",
                "detail": "Memory directory exists",
            }
        )

    return results


def main():
    results = check_results()
    print(json.dumps(results, indent=2, ensure_ascii=False))

    if results["failed"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
