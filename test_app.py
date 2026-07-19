import unittest
from unittest.mock import MagicMock
import sys

# Define a mock class for Streamlit's session_state that supports both dict and attribute access
class SessionStateMock(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)

# Mock columns to prevent unpacking errors when importing app.py
def mock_columns(spec):
    length = spec if isinstance(spec, int) else len(spec)
    return [MagicMock() for _ in range(length)]

# Mock tabs to prevent unpacking errors
def mock_tabs(tab_list):
    return [MagicMock() for _ in range(len(tab_list))]

# Mock input widgets to return clean, expected default values
def mock_text_input(label, value="", **kwargs):
    return value

def mock_selectbox(label, options, **kwargs):
    return options[0] if options else ""

def mock_multiselect(label, options, default=None, **kwargs):
    return default or []

def mock_segmented_control(label, options, default=None, **kwargs):
    return default if default is not None else (options[0] if options else "")

# Mock streamlit before importing app to avoid Streamlit runtime exceptions
mock_st = MagicMock()
mock_session_state = SessionStateMock()

# Initialize mock session state to look already onboarded to bypass the st.stop() gate on import
mock_session_state.onboarded = True
mock_session_state.volunteer_profile = {
    "full_name": "Test Volunteer",
    "active_role": "Guest Relations Specialist",
    "language_proficiency": "English",
    "assigned_zone": "Gate A"
}
mock_session_state.timeline_phase = 0
mock_session_state.vips = []
mock_session_state.directory = []
mock_session_state.activity_feed = []
mock_session_state.chat_history = []
mock_session_state.selected_contingency = None
mock_session_state.show_vio_chat = False
mock_session_state.app_init = True

mock_st.session_state = mock_session_state
mock_st.columns = mock_columns
mock_st.sidebar.columns = mock_columns
mock_st.tabs = mock_tabs
mock_st.text_input = mock_text_input
mock_st.selectbox = mock_selectbox
mock_st.multiselect = mock_multiselect
mock_st.segmented_control = mock_segmented_control
sys.modules['streamlit'] = mock_st

# Import app to test its mappings and constants
import app

class TestVIOApp(unittest.TestCase):
    def setUp(self):
        # Reset mock session state before each test to a clean, logged-in user state
        mock_session_state.clear()
        mock_session_state.onboarded = True
        mock_session_state.volunteer_profile = {
            "full_name": "Test Volunteer",
            "active_role": "Guest Relations Specialist",
            "language_proficiency": "English",
            "assigned_zone": "Gate A"
        }
        mock_session_state.timeline_phase = 0
        mock_session_state.vips = app.VIP_SIMULATION_STEPS[0]
        mock_session_state.directory = [
            {"name": "Sarah Connor", "role": "Central Command Director", "zone": "Command Center", "languages": "English, French", "status": "Active", "beep_count": 0, "id": "sarah"},
            {"name": "Ahmed Al-Masri", "role": "Team Lead", "zone": "VIP Lounges", "languages": "English, Arabic", "status": "Active", "beep_count": 0, "id": "ahmed"},
            {"name": "Maria Delgado", "role": "Liaison Officer", "zone": "Gate C VIP Reception", "languages": "Spanish, English", "status": "Active", "beep_count": 0, "id": "maria"},
            {"name": "Kenji Sato", "role": "Bilingual Escort", "zone": "Gate A Logistics", "languages": "Japanese, English", "status": "Active", "beep_count": 0, "id": "kenji"},
            {"name": "Jean-Pierre", "role": "Transit Coordinator", "zone": "Transport Hub", "languages": "French, English", "status": "Active", "beep_count": 0, "id": "jean"},
            {"name": "Samantha Green", "role": "Royal Box Host", "zone": "Royal Box Corridor", "languages": "English, German", "status": "Active", "beep_count": 0, "id": "samantha"}
        ]
        mock_session_state.activity_feed = []
        mock_session_state.chat_history = []
        mock_session_state.selected_contingency = None
        mock_session_state.show_vio_chat = False
        mock_session_state.app_init = True

    def test_session_state_initialization(self):
        """Verify that basic session state variables initialize correctly."""
        self.assertTrue(mock_session_state.app_init)
        self.assertTrue(mock_session_state.onboarded)
        self.assertEqual(mock_session_state.timeline_phase, 0)
        self.assertIsInstance(mock_session_state.volunteer_profile, dict)
        self.assertEqual(len(mock_session_state.directory), 6)

    def test_logistical_mappings_stable(self):
        """Verify logistical dictionary mappings are stable and contain required keys."""
        self.assertIn("spanish vip wheelchair access path", app.VIO_KNOWLEDGE)
        self.assertIn("emergency medical route", app.VIO_KNOWLEDGE)
        
        # Check Spanish route details
        spanish_route = app.VIO_KNOWLEDGE["spanish vip wheelchair access path"]
        self.assertEqual(spanish_route["title"], "♿ Spanish Guest Wheelchair Route (Gate C → Royal Box)")
        self.assertGreater(len(spanish_route["steps"]), 0)

    def test_avatar_svg_generator(self):
        """Verify make_avatar_svg generates valid XML/SVG output."""
        svg_content = app.make_avatar_svg("Sarah Connor", "Central Command Director")
        self.assertTrue(svg_content.startswith("<svg"))
        self.assertTrue(svg_content.endswith("</svg>"))
        self.assertIn("SC", svg_content)

if __name__ == '__main__':
    unittest.main()
