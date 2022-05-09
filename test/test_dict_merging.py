import unittest
from typing import List

from utils.dict_merging import merge_dict, merge_dicts, merge_fromkeys_dicts


class TestDictMerging(unittest.TestCase):
    dict_a: dict

    KEY_A_ONE = "A1"
    KEY_A_TWO = "A2"
    KEY_A_THREE = "A3"

    A_KEYS = [KEY_A_ONE, KEY_A_TWO, KEY_A_THREE]

    VALUE_A_ONE = 1
    VALUE_A_TWO = 2
    VALUE_A_THREE = 3

    dict_b: dict

    KEY_B_ONE = "B1"
    KEY_B_TWO = "B2"

    B_KEYS = [KEY_B_ONE, KEY_B_TWO]

    VALUE_B_ONE = 4
    VALUE_B_TWO = 5

    dict_c: dict

    KEY_C_ONE = "C1"
    KEY_C_TWO = "C2"
    KEY_C_THREE = "C3"
    KEY_C_FOUR = "C4"

    C_KEYS = [KEY_C_ONE, KEY_C_TWO, KEY_C_THREE, KEY_C_FOUR]

    VALUE_C_ONE = 6
    VALUE_C_TWO = 7
    VALUE_C_THREE = 8
    VALUE_C_FOUR = 9

    def setUp(self) -> None:
        self.dict_a = {
            self.KEY_A_ONE: self.VALUE_A_ONE,
            self.KEY_A_TWO: self.VALUE_A_TWO,
            self.KEY_A_THREE: self.VALUE_A_THREE
        }

        self.dict_b = {
            self.KEY_B_ONE: self.VALUE_B_ONE,
            self.KEY_B_TWO: self.VALUE_B_TWO
        }

        self.dict_c = {
            self.KEY_C_ONE: self.VALUE_C_ONE,
            self.KEY_C_TWO: self.VALUE_C_TWO,
            self.KEY_C_THREE: self.VALUE_C_THREE,
            self.KEY_C_FOUR: self.VALUE_C_FOUR
        }

    def test_merge_dict(self):
        expected_dict: dict = {
            self.KEY_A_ONE: self.VALUE_A_ONE,
            self.KEY_A_TWO: self.VALUE_A_TWO,
            self.KEY_A_THREE: self.VALUE_A_THREE,
            self.KEY_B_ONE: self.VALUE_B_ONE,
            self.KEY_B_TWO: self.VALUE_B_TWO
        }

        self.assertEqual(merge_dict(self.dict_a, self.dict_b), expected_dict)

        expected_dict = {
            self.KEY_B_ONE: self.VALUE_B_ONE,
            self.KEY_B_TWO: self.VALUE_B_TWO,
            self.KEY_C_ONE: self.VALUE_C_ONE,
            self.KEY_C_TWO: self.VALUE_C_TWO,
            self.KEY_C_THREE: self.VALUE_C_THREE,
            self.KEY_C_FOUR: self.VALUE_C_FOUR
        }

        self.assertEqual(merge_dict(self.dict_b, self.dict_c), expected_dict)

    def test_merge_dicts(self):
        expected_dict: dict = {
            self.KEY_A_ONE: self.VALUE_A_ONE,
            self.KEY_A_TWO: self.VALUE_A_TWO,
            self.KEY_A_THREE: self.VALUE_A_THREE,
            self.KEY_B_ONE: self.VALUE_B_ONE,
            self.KEY_B_TWO: self.VALUE_B_TWO,
            self.KEY_C_ONE: self.VALUE_C_ONE,
            self.KEY_C_TWO: self.VALUE_C_TWO,
            self.KEY_C_THREE: self.VALUE_C_THREE,
            self.KEY_C_FOUR: self.VALUE_C_FOUR
        }

        dicts: List[dict] = [self.dict_a, self.dict_b, self.dict_c]
        self.assertEqual(merge_dicts(dicts), expected_dict)

        expected_dict = {
            self.KEY_B_ONE: self.VALUE_B_ONE,
            self.KEY_B_TWO: self.VALUE_B_TWO,
            self.KEY_A_ONE: self.VALUE_A_ONE,
            self.KEY_A_TWO: self.VALUE_A_TWO,
            self.KEY_A_THREE: self.VALUE_A_THREE,
            self.KEY_C_ONE: self.VALUE_C_ONE,
            self.KEY_C_TWO: self.VALUE_C_TWO,
            self.KEY_C_THREE: self.VALUE_C_THREE,
            self.KEY_C_FOUR: self.VALUE_C_FOUR
        }

        dicts = [self.dict_b, self.dict_a, self.dict_c]
        self.assertEqual(merge_dicts(dicts), expected_dict)

        self.assertEqual(merge_dicts([self.dict_b]), self.dict_b)

        expected_dict = {
            self.KEY_B_ONE: self.VALUE_B_ONE,
            self.KEY_B_TWO: self.VALUE_B_TWO,
            self.KEY_C_ONE: self.VALUE_C_ONE,
            self.KEY_C_TWO: self.VALUE_C_TWO,
            self.KEY_C_THREE: self.VALUE_C_THREE,
            self.KEY_C_FOUR: self.VALUE_C_FOUR
        }

        dicts = [self.dict_b, self.dict_c]
        self.assertEqual(merge_dicts(dicts), expected_dict)

    def test_merge_fromkeys_dicts(self):
        def assert_fail(key_sets: List[list], values: list):
            try:
                merge_fromkeys_dicts(key_sets, values)
                self.fail()
            except ValueError:
                pass

        assert_fail([self.A_KEYS, self.B_KEYS], [self.VALUE_A_ONE])
        assert_fail([self.A_KEYS], [self.VALUE_A_ONE, self.VALUE_B_TWO])

        try:
            merge_fromkeys_dicts([self.C_KEYS, self.B_KEYS], [self.VALUE_C_TWO, self.VALUE_B_TWO])
        except ValueError:
            self.fail()

        expected_dict: dict = {
            self.KEY_A_ONE: self.VALUE_A_ONE,
            self.KEY_A_TWO: self.VALUE_A_ONE,
            self.KEY_A_THREE: self.VALUE_A_ONE,
            self.KEY_B_ONE: self.VALUE_B_ONE,
            self.KEY_B_TWO: self.VALUE_B_ONE,
            self.KEY_C_ONE: self.VALUE_C_ONE,
            self.KEY_C_TWO: self.VALUE_C_ONE,
            self.KEY_C_THREE: self.VALUE_C_ONE,
            self.KEY_C_FOUR: self.VALUE_C_ONE
        }

        self.assertEqual(merge_fromkeys_dicts([self.A_KEYS, self.B_KEYS, self.C_KEYS],
                                              [self.VALUE_A_ONE, self.VALUE_B_ONE, self.VALUE_C_ONE]),
                         expected_dict)

        expected_dict = {
            self.KEY_B_ONE: self.VALUE_B_TWO,
            self.KEY_B_TWO: self.VALUE_B_TWO,
            self.KEY_A_ONE: self.VALUE_A_THREE,
            self.KEY_A_TWO: self.VALUE_A_THREE,
            self.KEY_A_THREE: self.VALUE_A_THREE
        }

        self.assertEqual(merge_fromkeys_dicts([self.B_KEYS, self.A_KEYS],
                                              [self.VALUE_B_TWO, self.VALUE_A_THREE]),
                         expected_dict)


if __name__ == '__main__':
    unittest.main()
