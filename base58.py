# taken and adapted from https://github.com/jgarzik/python-bitcoinlib/blob/master/bitcoin/base58.py
import binascii
alphabets = [
    '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
    '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
]


def b58decode(s, alphabet=alphabets[0]):
    """Decode a base58-encoding string, returning bytes"""
    if not s:
        return b''

    # Convert the string to an integer
    n = 0
    for c in s:
        n *= 58
        if c not in alphabet:
            raise binascii.Error
        digit = alphabet.index(c)
        n += digit

    # Convert the integer to bytes
    h = '%x' % n
    if len(h) % 2:
        h = '0' + h
    res = binascii.unhexlify(h.encode('utf8'))

    # Add padding back.
    pad = 0
    for c in s[:-1]:
        if c == alphabet[0]:
            pad += 1
        else:
            break
    return b'\x00' * pad + res
