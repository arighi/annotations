import unittest

from tests import utils

from kconfig.annotations import Annotation


class TestLoadAnnotations(unittest.TestCase):
    def test_load(self):
        for d in ("annotations.override.1",):
            f = "tests/data/" + d
            a = Annotation(f)
            r = utils.load_json(f + ".result")
            self.assertEqual(utils.to_dict(a), r)
