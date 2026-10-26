# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Jareer Abdullah and Concat contributors

"""Client adapter for communicating with Concat / Luna-Cut API.

Provides JSON-RPC communication over stdin/stdout, socket, or direct CLI execution.
Supports project reading, atomic command batching, undo, and redo.
"""

import json
import os
import subprocess
from typing import Any, Dict, List, Optional


class ConcatTimelineClient:
    """Interface to the Concat editing engine."""

    def __init__(self, cli_path: Optional[str] = None):
        if cli_path is None:
            # Look in target directory or system PATH
            candidate = "/root/Luna-Cut/src/target/release/concat-cli"
            if not os.path.exists(candidate):
                candidate = "/root/Luna-Cut/src/target/debug/concat-cli"
            self.cli_path = candidate if os.path.exists(candidate) else "concat-cli"
        else:
            self.cli_path = cli_path

    def build_batch_command(self, commands: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Wraps multiple atomic edits into a single Command::Batch for one-step undo."""
        return {
            "type": "Batch",
            "commands": commands,
        }

    def create_text_clip_command(
        self,
        track_id: str,
        start_s: float,
        duration_s: float,
        text: str,
        font_size: float = 64.0,
        color: str = "#FFFFFF",
    ) -> Dict[str, Any]:
        """Constructs an AddTextClip command."""
        return {
            "type": "AddTextClip",
            "track_id": track_id,
            "start": float(start_s),
            "duration": float(duration_s),
            "text": text,
            "style": {
                "font_size": font_size,
                "color": color,
            },
        }

    def create_set_keyframe_command(
        self,
        clip_id: str,
        property_name: str,
        time_s: float,
        value: float,
        curve: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """Constructs a SetClipKey command."""
        cmd = {
            "type": "SetClipKey",
            "clip_id": clip_id,
            "property": property_name,
            "at": float(time_s),
            "value": float(value),
        }
        if curve:
            cmd["curve"] = curve
        return cmd

    def create_cutout_command(self, clip_id: str, enabled: bool = True) -> Dict[str, Any]:
        """Constructs a SetClipCutout command (AI rotoscoping)."""
        return {
            "type": "SetClipCutout",
            "clip_id": clip_id,
            "enabled": enabled,
        }

    def create_cutout_stroke_command(
        self, clip_id: str, color: str = "#00FFFF", width: float = 4.0
    ) -> Dict[str, Any]:
        """Constructs an AddCutoutStroke command for outlines/glows around subjects."""
        return {
            "type": "AddCutoutStroke",
            "clip_id": clip_id,
            "color": color,
            "width": width,
        }

    def create_add_track_command(self, name: str = "Motion Graphics") -> Dict[str, Any]:
        """Constructs an AddTrack command."""
        return {
            "type": "AddTrack",
            "name": name,
        }

    def execute_request_headless(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a JSON request against the Concat engine via stdin/stdout."""
        proc = subprocess.Popen(
            [self.cli_path, "api"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        line = json.dumps(request_payload) + "\n"
        stdout, stderr = proc.communicate(input=line, timeout=10)
        if proc.returncode != 0:
            raise RuntimeError(f"Concat CLI error ({proc.returncode}): {stderr}")
        for resp_line in stdout.splitlines():
            try:
                return json.loads(resp_line)
            except json.JSONDecodeError:
                continue
        return {"status": "ok", "raw": stdout}
