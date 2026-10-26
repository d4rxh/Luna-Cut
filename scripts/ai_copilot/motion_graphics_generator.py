# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Jareer Abdullah and Concat contributors

"""Motion Graphics, 3D Camera, and Kinetic Typography Generator for Luna-Cut.

Provides mathematical trajectory generators, Bezier easing curves,
kinetic typography layout engines, and multi-layer depth sandwich builders.
"""

from dataclasses import dataclass, field
import math
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class BezierCurve:
    """Cubic Bezier curve definition for keyframe velocity interpolation."""
    p1x: float
    p1y: float
    p2x: float
    p2y: float

    # Standard Motion Graphics Presets
    EASE_OUT_BACK = (0.175, 0.885, 0.32, 1.275)      # Elastic overshoot / bounce
    WHIP_SNAP = (0.05, 0.9, 0.15, 1.0)               # High-velocity whip pan
    SMOOTH_CINEMATIC = (0.4, 0.0, 0.2, 1.0)          # Standard cinematic ease
    AGGRESSIVE_POP = (0.0, 0.0, 0.2, 1.0)            # Sharp pop-in
    SLOW_DRIFT = (0.25, 0.1, 0.25, 1.0)              # Subtle floating motion

    @classmethod
    def from_tuple(cls, t: Tuple[float, float, float, float]) -> "BezierCurve":
        return cls(p1x=t[0], p1y=t[1], p2x=t[2], p2y=t[3])

    def to_dict(self) -> Dict[str, float]:
        return {"p1x": self.p1x, "p1y": self.p1y, "p2x": self.p2x, "p2y": self.p2y}


@dataclass
class KeyframePoint:
    """Individual animated property keyframe."""
    time_s: float
    value: float
    curve: BezierCurve = field(default_factory=lambda: BezierCurve.from_tuple(BezierCurve.SMOOTH_CINEMATIC))

    def to_command_dict(self) -> Dict[str, Any]:
        return {
            "at": self.time_s,
            "value": self.value,
            "curve": self.curve.to_dict(),
        }


class Camera3DChoreographer:
    """Generates 3D spatial transformations and camera trajectories."""

    @staticmethod
    def dolly_zoom(start_time: float, duration: float, start_z: float = -1200.0, end_z: float = -300.0,
                   fov_initial: float = 45.0) -> List[Dict[str, Any]]:
        """Dolly-zoom (Vertigo effect): moves camera Z while inversely adjusting FOV to keep subject size constant."""
        frames = 30
        commands = []
        dt = duration / frames

        for i in range(frames + 1):
            t = start_time + (i * dt)
            progress = i / frames
            # Smooth cinematic easing
            smooth_progress = 0.5 * (1.0 - math.cos(progress * math.pi))
            current_z = start_z + (end_z - start_z) * smooth_progress
            
            # Constant sensor projection scale factor: scale = 2 * tan(fov / 2) * distance
            # For constant subject framing: tan(fov/2) * dist = const
            dist_init = abs(start_z)
            dist_curr = abs(current_z)
            ratio = dist_init / max(dist_curr, 1.0)
            current_fov = math.degrees(2.0 * math.atan(math.tan(math.radians(fov_initial / 2.0)) * ratio))

            commands.append({
                "time": round(t, 3),
                "camera_z": round(current_z, 2),
                "camera_fov": round(current_fov, 2),
            })
        return commands

    @staticmethod
    def orbit_360(start_time: float, duration: float, radius: float = 800.0,
                  elevation: float = 150.0) -> List[Dict[str, Any]]:
        """360-degree orbit around the central point of interest."""
        steps = 36
        dt = duration / steps
        trajectory = []
        for i in range(steps + 1):
            t = start_time + (i * dt)
            angle = (i / steps) * 2.0 * math.pi
            x = radius * math.sin(angle)
            z = -radius * math.cos(angle)
            trajectory.append({
                "time": round(t, 3),
                "position": [round(x, 2), elevation, round(z, 2)],
                "look_at": [0.0, 0.0, 0.0],
                "rotation_y": round(math.degrees(angle), 2),
            })
        return trajectory

    @staticmethod
    def whip_pan(start_time: float, duration: float = 0.4, direction: str = "right") -> Dict[str, Any]:
        """Generates high-velocity whip pan transition keyframes."""
        sign = 1.0 if direction == "right" else -1.0
        return {
            "start_time": start_time,
            "duration": duration,
            "rotation_y_delta": 45.0 * sign,
            "motion_blur": 0.85,
            "curve": BezierCurve.from_tuple(BezierCurve.WHIP_SNAP).to_dict(),
        }


class KineticTypographyEngine:
    """Generates expressive kinetic typography layouts and animations."""

    @staticmethod
    def generate_staggered_title(
        text: str,
        start_time: float,
        word_duration: float = 1.2,
        stagger_delay: float = 0.08,
        style: str = "elastic_bounce",
        font_size: float = 64.0,
        text_color: str = "#FFFFFF",
    ) -> List[Dict[str, Any]]:
        """Generates kinetic word-by-word staggered entrance animations."""
        words = text.strip().split()
        clips = []

        curve = (
            BezierCurve.from_tuple(BezierCurve.EASE_OUT_BACK)
            if style == "elastic_bounce"
            else BezierCurve.from_tuple(BezierCurve.AGGRESSIVE_POP)
        )

        for idx, word in enumerate(words):
            word_start = start_time + (idx * stagger_delay)
            clips.append({
                "kind": "text",
                "text": word,
                "start": round(word_start, 3),
                "duration": round(word_duration, 3),
                "font_size": font_size,
                "color": text_color,
                "word_index": idx,
                "animation": {
                    "style": style,
                    "curve": curve.to_dict(),
                    "initial_scale": 0.2,
                    "target_scale": 1.0,
                    "initial_opacity": 0.0,
                    "target_opacity": 1.0,
                },
            })
        return clips


class RotoSandwichBuilder:
    """Builds multi-layer 3D depth sandwiches using AI subject cutout."""

    @staticmethod
    def build_sandwich_spec(
        video_clip_id: str,
        media_id: str,
        start_time: float,
        duration: float,
        text: str,
        stroke_color: str = "#00FFFF",
        stroke_width: float = 4.0,
    ) -> Dict[str, Any]:
        """Creates the 3-layer sandwich:
        Layer 1 (Bottom): Original background video track
        Layer 2 (Middle): Kinetic text / 3D graphics positioned in depth
        Layer 3 (Top): Cutout video track (isolated foreground subject with optional stroke outline)
        """
        return {
            "type": "roto_depth_sandwich",
            "base_video": {
                "media_id": media_id,
                "track_index": 0,
                "start": start_time,
                "duration": duration,
            },
            "kinetic_text": {
                "text": text,
                "track_index": 1,
                "start": start_time,
                "duration": duration,
                "z_depth": 150.0,  # Positioned behind the foreground subject
            },
            "cutout_foreground": {
                "source_clip_id": video_clip_id,
                "media_id": media_id,
                "track_index": 2,
                "start": start_time,
                "duration": duration,
                "cutout_enabled": True,
                "stroke": {
                    "enabled": True,
                    "color": stroke_color,
                    "width": stroke_width,
                },
            },
        }
