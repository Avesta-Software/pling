
from functools import reduce

from pling.bitmath import ones_complement_add

class BitmathTest:
    def test_ones_compliment_easy(self):
        """Test adding 2 numbers where no carrying is needed"""
        assert ones_complement_add(7, 3, bits=16) == 10

    def test_ones_compliment_wrap(self):
        """Test adding 2 numbers that should wrap around to 1"""
        n1 = int("1111", 2)
        n2 = int("0001", 2)

        result = ones_complement_add(n1, n2, bits=4)

        assert result == int("0001", 2)

    def test_ones_compliment_add_arbitrary(self):
        """Test the rfc1071 Internet Checksum example

        http://tools.ietf.org/html/rfc1071#section-3
        """
        inputs = [
            int("0001", 16),
            int("f203", 16),
            int("f4f5", 16),
            int("f6f7", 16)
        ]

        result = reduce(ones_complement_add, inputs)

        assert result == int("ddf2", 16)
