
def ones_complement_add(num1, num2, bits=16):
    """Implementation of 1's complement addition"""
    ceil = int("1" * bits, 2)
    result = num1 + num2

    if result <= ceil:
        return result
    else:
        return result % ceil
