"""Test OutputPanelHandler."""

from EasyClangComplete.plugin.utils import output_panel_handler
from unittest import TestCase

import time
import imp
import sublime

imp.reload(output_panel_handler)

OutputPanelHandler = output_panel_handler.OutputPanelHandler


class TestOutputPanelHandler(TestCase):
    """Test that we can create an output panel."""

    def tearDown(self):
        """Cleanup method run after every test."""
        window = sublime.active_window()
        window.run_command("show_panel", {"panel": "output.UnitTesting"})

    def test_panel_creation(self):
        """Test that we can open a panel."""
        OutputPanelHandler.show("hello world")
        window = sublime.active_window()
        self.assertIsNotNone(window.active_panel())
        self.assertEqual(window.active_panel(), OutputPanelHandler.PANEL_NAME)
        panel_view = window.find_output_panel(OutputPanelHandler.PANEL_TAG)
        contents = panel_view.substr(sublime.Region(0, panel_view.size()))
        self.assertEqual(contents, "hello world")

    def test_panel_closing(self):
        """Test that we can close a panel."""
        OutputPanelHandler.show("hello world")
        window = sublime.active_window()
        self.assertEqual(window.active_panel(), OutputPanelHandler.PANEL_NAME)
        OutputPanelHandler.hide_panel()
        self.assertIsNone(window.active_panel())

    def test_not_closing_panel(self):
        """Test that we don't close a panel with a wrong name."""
        window = sublime.active_window()
        current_panel = window.active_panel()
        if not current_panel:
            window.run_command("show_panel", {"panel": "output.UnitTesting"})
            time.sleep(0.2)
        self.assertIsNotNone(current_panel)
        self.assertNotEqual(current_panel, OutputPanelHandler.PANEL_NAME)
        OutputPanelHandler.hide_panel()
        self.assertIsNotNone(window.active_panel())
        self.assertEqual(current_panel, window.active_panel())
