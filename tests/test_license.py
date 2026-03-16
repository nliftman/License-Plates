# pylint: disable=E1101
# pylint: disable=E0401
# these are disabled bc pylint is confused!
#pylint cannot figure out how to import and pylint
#thinks that we are using panda's set_value()
#which is depricated but we are using streamlit and it donest get it

"""test_license.py contains unit tests for the functions in website 
as well as tests for streamlit."""
import unittest
from pathlib import Path
import io
from unittest.mock import patch
from pandas import read_csv

from streamlit.testing.v1 import AppTest
from license_plates.website import validation_rules, evaluate_plate, button_output

plates_root = Path(__file__).resolve().parent.parent  # -> License-Plates/
data_path = plates_root / "datacleaning" / "master_counts_scores.csv"

df_scores = read_csv(data_path)
evil_list = df_scores['nospace'].tolist()


class TestUnit(unittest.TestCase):
    """A custom exception class for testing website.py's Exceptions.
    Ensures website.py processes correctly with edge cases and error
    conditions maybe we will use this to test the fuzzy look up and scores
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

    def test_button_output2(self):
        """
         Verifies the button_output method is working correctly when there is a match.
        """
        plate = "poop"
        self.assertEqual("""Your plate contains a word that appeared in
        [6] tweets marked as hatefull or offensive.
        This word appeared in tweets which [3] people marked as
        hatefull and [13] marked as offensive.
        If all of these are zero, then it appeared in no tweets but was
        still captured by our hatefull algorithm.""", button_output(plate))

    def test_button_output3(self):
        """
         Verifies the button_output method is working correctly when no match.
        """
        plate = "Fluffy5"
        self.assertEqual("This plate does not contain a restricted word", button_output(plate))

### We Should add a tests for the evaluate plate method

class TestWeb():
    """A custom exception class for testing website.py function. 
    Ensures website.py processes correctly and displays fuzzy look 
    up and scores
    """

    def test_app_interact1(self):
        """
        Verifies the validation_rules elifs.
        """
        at = AppTest.from_file("license_plates/website.py")
        at.run()
        # Check if app runs
        assert not at.exception
        at.text_input[0].set_value("ASSMAN").run()
        assert at.text_input[0].value == "ASSMAN"
        print(at.markdown[0].value)
        assert at.markdown[0].value == "ASSMAN contains the restricted letter combination ASS"

    def test_app_interact2(self):
        """
        Verifies the validation_rules elifs.
        """
        at = AppTest.from_file("license_plates/website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("A").run()

        assert at.text_input[0].value == "A"

        assert at.markdown[0].value == "A is an invalid length"

    def test_app_interact3(self):
        """
        Verifies the validation_rules elifs.
        """
        at = AppTest.from_file("license_plates/website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("A#$&me").run()

        assert at.text_input[0].value == "A#$&me"

        assert at.markdown[0].value == "A#$&me has invalid characters"

    def test_app_interact4(self):
        """
        Verifies the validation_rules elifs.
        """
        at = AppTest.from_file("license_plates/website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("aa2345").run()

        assert at.text_input[0].value == "aa2345"

        assert (at.markdown[0].value == "aa2345 must be for Purple Heart Vessels"
                ", Disabled Person, or Disabled Veteran")

    def test_app_interact5(self):
        """
        Verifies the validation_rules elifs.
        """
        at = AppTest.from_file("license_plates/website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("12345t").run()

        assert at.text_input[0].value == "12345t"

        assert at.markdown[0].value == "12345t must be for a commercial vehical"

    def test_app_interact6(self):
        """
        Verifies the validation_rules elifs.
        """
        at = AppTest.from_file("license_plates/website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("12345tb").run()

        assert at.text_input[0].value == "12345tb"

        assert at.markdown[0].value == "12345tb must be for a Disabled Person, or Disabled Veteran"

    def test_app_interact7(self):
        """
        Verifies the validation_rules elifs.
        """
        at = AppTest.from_file("license_plates/website.py")
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
        at = AppTest.from_file("license_plates/website.py")
        at.run()

        # Check if app runs
        assert not at.exception

        at.text_input[0].set_value("Girly45").run()

        assert at.text_input[0].value == "Girly45"

        assert "This plate closely resembles a word or phrase that" in at.markdown[0].value
        assert "may be considered inappropriate." in at.markdown[0].value
        at.button[0].click().run()
        expected = """
        **Detected similarity**

        - Possible match: girls
        - Similarity score: 83.33333333333334%
        - Detection method: similarity matching
        """

        assert " ".join(at.markdown[1].value.split()
                        ) == " ".join(expected.split())

    def test_app_interact9(self):
        """
        Verifies the button_output method has correct formatting.
        """
        at = AppTest.from_file("license_plates/website.py")
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

        assert " ".join(at.markdown[1].value.split()
                        ) == " ".join(expected.split())

        expected2 = """Your plate contains a word that appeared in
        [60] tweets marked as hatefull or offensive.
        This word appeared in tweets which [29] people marked as
        hatefull and [154] marked as offensive.
        If all of these are zero, then it appeared in no tweets but was
        still captured by our hatefull algorithm."""

        assert " ".join(at.markdown[2].value.split()
                        ) == " ".join(expected2.split())

    def test_app_interact10(self):
        """
        Verifies the csv tab works.
        """
        at = AppTest.from_file("license_plates/website.py")
        at.run()

        assert not at.exception
        assert at.tabs[1].label == "Batch CSV"

    def test_app_interact11(self):
        """
        Verifies the csv tab works correctly when a csv is loaded.
        """

        input_csv = io.StringIO("plate\nABC123\nBITCH1\n")

        with patch("streamlit.file_uploader", return_value=input_csv):

            at = AppTest.from_file("license_plates/website.py")
            at.run()

            assert at is not None
            #assert len(at.dataframe) > 0
            df = at.dataframe[0].value
            assert len(df) == 2

            assert "plate" in df.columns
            assert "approved?" in df.columns
            assert "reason" in df.columns
            assert "notes" in df.columns

    def test_response1(self):
        """Verifies the valid length"""
        at = AppTest.from_file("license_plates/website.py")
        at.run()
        at.text_input[0].set_value("A").run()
        assert at.text_input[0].value == "A"
        assert at.markdown[0].value == "A is an invalid length"
