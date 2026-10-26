# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Jareer Abdullah and Concat contributors

"""Unit and Integration Tests for Luna-Cut AI Copilot."""

import unittest
from .copilot_agent import AICopilotAgent
from .motion_graphics_generator import (
    BezierCurve,
    Camera3DChoreographer,
    KineticTypographyEngine,
    RotoSandwichBuilder,
)


class TestBezierCurves(unittest.TestCase):
    def test_preset_curves(self):
        bounce = BezierCurve.from_tuple(BezierCurve.EASE_OUT_BACK)
        self.assertEqual(bounce.p1x, 0.175)
        self.assertEqual(bounce.p2y, 1.275)  # Overshoot > 1.0
        d = bounce.to_dict()
        self.assertIn("p1x", d)
        self.assertIn("p2y", d)


class TestCamera3DChoreographer(unittest.TestCase):
    def test_dolly_zoom_generation(self):
        steps = Camera3DChoreographer.dolly_zoom(start_time=0.0, duration=2.0, start_z=-1200.0, end_z=-400.0)
        self.assertGreater(len(steps), 10)
        first_step = steps[0]
        last_step = steps[-1]
        self.assertEqual(first_step["time"], 0.0)
        self.assertEqual(first_step["camera_z"], -1200.0)
        # Verify camera moved closer
        self.assertGreater(last_step["camera_z"], first_step["camera_z"])
        # Verify FOV widened to preserve subject size
        self.assertGreater(last_step["camera_fov"], first_step["camera_fov"])

    def test_orbit_360_trigonometry(self):
        orbit = Camera3DChoreographer.orbit_360(start_time=1.0, duration=4.0, radius=500.0)
        self.assertEqual(len(orbit), 37)
        self.assertEqual(orbit[0]["time"], 1.0)
        self.assertEqual(orbit[-1]["time"], 5.0)
        # End rotation should be close to 360 degrees
        self.assertAlmostEqual(orbit[-1]["rotation_y"], 360.0, places=0)


class TestKineticTypography(unittest.TestCase):
    def test_staggered_title(self):
        clips = KineticTypographyEngine.generate_staggered_title(
            text="AI MOTION ENGINE",
            start_time=2.0,
            stagger_delay=0.1,
            style="elastic_bounce",
        )
        self.assertEqual(len(clips), 3)
        self.assertEqual(clips[0]["text"], "AI")
        self.assertEqual(clips[1]["text"], "MOTION")
        self.assertEqual(clips[2]["text"], "ENGINE")
        # Staggered start times
        self.assertEqual(clips[0]["start"], 2.0)
        self.assertEqual(clips[1]["start"], 2.1)
        self.assertEqual(clips[2]["start"], 2.2)


class TestRotoSandwichBuilder(unittest.TestCase):
    def test_sandwich_spec(self):
        sandwich = RotoSandwichBuilder.build_sandwich_spec(
            video_clip_id="c_bg",
            media_id="m_video",
            start_time=0.0,
            duration=5.0,
            text="SUPERNOVA",
            stroke_color="#FF00FF",
            stroke_width=6.0,
        )
        self.assertEqual(sandwich["type"], "roto_depth_sandwich")
        self.assertEqual(sandwich["base_video"]["track_index"], 0)
        self.assertEqual(sandwich["kinetic_text"]["track_index"], 1)
        self.assertEqual(sandwich["cutout_foreground"]["track_index"], 2)
        self.assertTrue(sandwich["cutout_foreground"]["cutout_enabled"])
        self.assertEqual(sandwich["cutout_foreground"]["stroke"]["color"], "#FF00FF")


class TestAICopilotAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AICopilotAgent()

    def test_plan_kinetic_title_prompt(self):
        plan = self.agent.plan_edit("Add a kinetic title 'NEON GLOW' with bounce")
        self.assertIn("kinetic typography", plan.summary.lower())
        self.assertEqual(plan.batch_command["type"], "Batch")
        self.assertGreater(len(plan.batch_command["commands"]), 3)

    def test_plan_3d_camera_prompt(self):
        plan = self.agent.plan_edit("Create a 3D camera 360 orbit around the subject")
        self.assertIn("3d camera orbit", plan.summary.lower())
        self.assertEqual(plan.batch_command["type"], "Batch")
        self.assertTrue(any(c.get("property") == "rotation_y" for c in plan.batch_command["commands"]))

    def test_plan_roto_prompt(self):
        plan = self.agent.plan_edit("Roto the subject and place text 'CYBER' behind them")
        self.assertIn("3d depth sandwich", plan.summary.lower())
        self.assertEqual(plan.batch_command["type"], "Batch")
        self.assertTrue(any(c.get("type") == "SetClipCutout" for c in plan.batch_command["commands"]))
        self.assertTrue(any(c.get("type") == "AddCutoutStroke" for c in plan.batch_command["commands"]))


if __name__ == "__main__":
    unittest.main()
