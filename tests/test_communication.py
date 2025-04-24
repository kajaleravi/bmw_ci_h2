import unittest
from communication_channel import CommunicationChannel

class TestBMWCommunication(unittest.TestCase):
    def setUp(self):
        self.channel = CommunicationChannel("BMW_Test_Plant")

    def test_message_processing(self):
        result, msg = self.channel.process_message(
            "Engine_Team", 
            "Assembly_Line", 
            "M5_engine_failure detected"
        )
        self.assertTrue(result)
        self.assertIn("BMW_Test_Plant", msg)

    def test_invalid_message(self):
        result, msg = self.channel.process_message("", "Assembly_Line", "X5_assembly_delay")
        self.assertFalse(result)
        self.assertIn("cannot be empty", msg)

    def test_stats_tracking(self):
        self.channel.process_message("Engine_Team", "Assembly_Line", "i4_production started")
        stats = self.channel.get_production_stats()
        self.assertEqual(stats["Engine_Team"][0], 1)  # Sent
        self.assertEqual(stats["Assembly_Line"][1], 1)  # Received

if __name__ == "__main__":
    unittest.main()