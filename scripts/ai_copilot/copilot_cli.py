#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Jareer Abdullah and Concat contributors

"""Command line interface for the Luna-Cut AI Editing & Motion Graphics Copilot."""

import argparse
import json
import sys

from .copilot_agent import AICopilotAgent


def main():
    parser = argparse.ArgumentParser(
        description="Luna-Cut AI Copilot: Automated Video Editing & Motion Graphics Agent"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        help="Natural language editing instruction (e.g. 'Add kinetic title NEON with 3D dolly zoom')",
    )
    parser.add_argument(
        "--preset",
        choices=["kinetic_title", "3d_dolly_zoom", "3d_orbit", "roto_sandwich", "whip_pan"],
        help="Execute a pre-configured motion graphics preset",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Output the generated Command::Batch JSON without sending to engine",
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start an interactive copilot conversation loop",
    )

    args = parser.parse_args()
    agent = AICopilotAgent()

    if args.preset:
        preset_prompts = {
            "kinetic_title": "Add kinetic title 'FUTURE VISION' with elastic bounce",
            "3d_dolly_zoom": "Apply 3D dolly zoom vertigo effect to active clip",
            "3d_orbit": "Perform 360 degree 3D camera orbit around subject",
            "roto_sandwich": "Rotoscope subject with text 'HYPERDRIVE' placed in depth behind them",
            "whip_pan": "Execute high-velocity 3D whip pan transition to the right",
        }
        prompt = preset_prompts[args.preset]
    elif args.prompt:
        prompt = args.prompt
    elif args.interactive:
        print("=== Luna-Cut AI Copilot Interactive Assistant ===")
        print("Type your editing or motion graphics request (or 'exit' to quit):\n")
        while True:
            try:
                line = input("copilot> ").strip()
                if not line or line.lower() in ["exit", "quit", "q"]:
                    break
                plan = agent.plan_edit(line)
                print(f"\n[AI Plan]: {plan.summary}")
                print(f"[Generated Actions]: {len(plan.actions)} commands batched")
                print(json.dumps(plan.batch_command, indent=2))
                print()
            except (KeyboardInterrupt, EOFError):
                break
        return
    else:
        parser.print_help()
        return

    plan = agent.plan_edit(prompt)
    print("=" * 60)
    print("LUNA-CUT AI COPILOT EXECUTION PLAN")
    print("=" * 60)
    print(f"Prompt:   {prompt}")
    print(f"Summary:  {plan.summary}")
    print(f"Commands: {len(plan.actions)} atomic edits compiled into Command::Batch")
    print("-" * 60)
    print(json.dumps(plan.batch_command, indent=2))
    print("=" * 60)

    if not args.dry_run:
        print("\n[Status]: Batch ready for execution against active project session.")


if __name__ == "__main__":
    main()
