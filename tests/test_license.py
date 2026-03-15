"""test_license.py contains unit tests for the functions in website as well as tests for streamlit."""
import unittest
import numpy as np
import pandas as pd
from pathlib import Path

from streamlit.testing.v1 import AppTest
from website import validation_rules, evaluate_plate, button_output

plates_root = Path(__file__).resolve().parent.parent # -> License-Plates/
data_path = plates_root / "datacleaning" / "master_counts_scores.csv"

df_scores = pd.read_csv(data_path)
evil_list = df_scores['nospace'].tolist()

class TestUnit(unittest.TestCase):
    """A custom exception class for testing website.py's Exceptions.

    Ensures website.py processes correctly with edge cases and error conditions maybe we will use this to test the fuzzy look up and scores
    """
    # def test_evilcheck1(self):
    #     """
    #     Verifies the check_evil method is working correctly.
    #     """
    #     plate = "Happy"
    #     self.assertEqual("This plate does not contain a restricted word", check_evil(plate))

    # def test_evilcheck2(self):
    #     """
    #     Verifies the check_evil method is working correctly.
    #     """
    #     plate = "beaner"
    #     self.assertEqual("This plate contains a restricted word", check_evil(plate))

    def test_validation_rules1(self):
        """
         Verifies the validation_rules method is working correctly.
        """
        result = validation_rules("Class")

        self.assertIsInstance(result, str)

    def test_validation_rules2(self):
        """
         Verifies the validation_rules method is working correctly.
        """
        result = validation_rules("Fluffy5")

        self.assertIsNone(result)

    def test_evaluate_plate1(self):
        """
         Verifies the evaluate_plate method is working correctly.
        """
        result = evaluate_plate("head", evil_list)

        self.assertIsInstance(result, tuple)

        
    def test_evaluate_plate2(self):
        """
         Verifies the evaluate_plate method is working correctly.
        """
        result = evaluate_plate("Fluffy5", evil_list)

        self.assertIsNone(result)
        
    def test_button_output(self):
         """
         Verifies the buttom_output method is working correctly.
        """
         result = button_output("Fluffy5")
         
         self.assertIsInstance(result, str)

class TestWeb():
    """A custom exception class for testing website.py function.

    Ensures website.py processes correctly and displays fuzzy look up and scores
    """
    def test_app_interact1(self):
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("ASSMAN").run()

        assert at.text_input[0].value == "ASSMAN"
        print(at.markdown[0].value)
        assert at.markdown[0].value == "ASSMAN contains the restricted letter combination ASS"

    def test_app_interact2(self):
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("A").run()

        assert at.text_input[0].value == "A"

        assert at.markdown[0].value == "A is an invalid length"

    def test_app_interact3(self):
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("A#$&me").run()

        assert at.text_input[0].value == "A#$&me"

        assert at.markdown[0].value == "A#$&me has invalid characters"

    def test_app_interact4(self):
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("aa2345").run()

        assert at.text_input[0].value == "aa2345"

        assert at.markdown[0].value == "aa2345 must be for Purple Heart Vessels, Disabled Person, or Disabled Veteran"

    def test_app_interact5(self):
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("12345t").run()

        assert at.text_input[0].value == "12345t"

        assert at.markdown[0].value == "12345t must be for a commercial vehical"

    def test_app_interact6(self):
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("12345tb").run()

        assert at.text_input[0].value == "12345tb"

        assert at.markdown[0].value == "12345tb must be for a Disabled Person, or Disabled Veteran"

    def test_app_interact7(self):
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("11111A1").run()

        assert at.text_input[0].value == "11111A1"

        assert at.markdown[0].value == "11111A1 must be for a commercial vehical"

    def test_app_interact8(self):
        """
        Verifies the evaluate_plate method has correct formatting.
        """
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("Girly45").run()

        assert at.text_input[0].value == "Girly45"

        assert at.markdown[0].value == "This plate closely resembles a word or phrase that may be considered inappropriate."
        at.button[0].click().run()
        expected = """
        **Detected similarity**

        - Possible match: girls
        - Similarity score: 83.33333333333334%
        - Detection method: similarity matching
        """

        assert " ".join(at.markdown[1].value.split()) == " ".join(expected.split())


    def test_app_interact9(self):
        """
        Verifies the button_output method has correct formatting.
        """
        at = AppTest.from_file("website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("poop").run()

        assert at.text_input[0].value == "poop"
        assert at.markdown[0].value == "This plate contains a restricted word."
        
        at.button[0].click().run()

        expected = """
        **Detected restricted word**

        - Detected word: poo
        - Detection method: exact match
        """

        assert " ".join(at.markdown[1].value.split()) == " ".join(expected.split())
        
        expected2 = """Your plate contains a word that appeared in
        [92] tweets marked as hatefull or offensive.
        This word appeared in tweets which [32] people marked as
        hatefull and [256] marked as offensive.
        If all of these are zero, then it appeared in no tweets but was
        still captured by our hatefull algorithm."""

        assert " ".join(at.markdown[2].value.split()) == " ".join(expected2.split())