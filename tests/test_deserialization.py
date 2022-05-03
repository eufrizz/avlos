import yaml
import importlib.resources
from avlos.deserializer import deserialize
import marshmallow
import pint
import unittest
from pprint import pprint


class TestDeserialization(unittest.TestCase):
    def test_success(self):
        def_path_str = str(
            importlib.resources.files("tests").joinpath("definition/good_device.yaml")
        )
        with open(def_path_str) as device_description:
            obj = deserialize(yaml.safe_load(device_description))
            obj.set_getter_cb(lambda: 0)
            obj.set_setter_cb(lambda: 0)
            print(obj)

    def test_undefined_unit(self):
        def_path_str = str(
            importlib.resources.files("tests").joinpath(
                "definition/bad_device_unit.yaml"
            )
        )
        with open(def_path_str) as device_description:
            with self.assertRaises(pint.errors.UndefinedUnitError):
                deserialize(yaml.safe_load(device_description))

    def test_validation_fail(self):
        def_path_str = str(
            importlib.resources.files("tests").joinpath(
                "definition/bad_device_name.yaml"
            )
        )
        with open(def_path_str) as device_description:
            with self.assertRaises(marshmallow.exceptions.ValidationError):
                deserialize(yaml.safe_load(device_description))
