"""test_license.py contains unit tests for the functions in website as well as tests for streamlit."""
import unittest
import numpy as np

from streamlit.testing.v1 import AppTest
import website

class TestWeb(unittest.TestCase):
    """A custom exception class for testing website.py's Exceptions.

    Ensures website.py processes correctly with edge cases and error conditions maybe we will use this to test the fuzzy look up and scores
    """

def test_app_interact1():
    at = AppTest.from_file("website.py")
    at.run()

    # Check if app runs
    assert not at.exception

    at.text_input[0].set_value("ASSMAN").run()

    assert at.text_input.value == "ASSMAN"

    assert at.markdown[0].value == "ASSMAN contains the restricted letter combination ASS"

def test_app_interact2():
    at = AppTest.from_file("website.py")
    at.run()

    # Check if app runs
    assert not at.exception

    at.text_input[0].set_value("A").run()

    assert at.text_input.value == "A"

    assert at.markdown[0].value == "A is an invalid length"

def test_app_interact3():
    at = AppTest.from_file("website.py")
    at.run()

    # Check if app runs
    assert not at.exception

    at.text_input[0].set_value("A#$&me").run()

    assert at.text_input.value == "A#$&me"

    assert at.markdown[0].value == "A#$&me has invalid characters"

def test_app_interact4():
    at = AppTest.from_file("website.py")
    at.run()

    # Check if app runs
    assert not at.exception

    at.text_input[0].set_value("aa2345").run()

    assert at.text_input.value == "aa2345"

    assert at.markdown[0].value == "aa2345 must be for Purple Heart Vessels, Disabled Person, or Disabled Veteran"

def test_app_interact5():
    at = AppTest.from_file("website.py")
    at.run()

    # Check if app runs
    assert not at.exception

    at.text_input[0].set_value("12345t").run()

    assert at.text_input.value == "12345t"

    assert at.markdown[0].value == "12345t must be for a commercial vehical"

def test_app_interact6():
    at = AppTest.from_file("website.py")
    at.run()

    # Check if app runs
    assert not at.exception

    at.text_input[0].set_value("12345tb").run()

    assert at.text_input.value == "12345tb"

    assert at.markdown[0].value == "12345tb must be for a Disabled Person, or Disabled Veteran"

def test_app_interact7():
    at = AppTest.from_file("website.py")
    at.run()

    # Check if app runs
    assert not at.exception

    at.text_input[0].set_value("11111A1").run()

    assert at.text_input.value == "11111A1"

    assert at.markdown[0].value == "11111A1  must be for a commercial vehical"

    ##We will add more tests for the 2nd page its just not built out yet
    