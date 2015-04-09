#! /usr/bin/env python
from math import ceil
from hashlib import sha256

"""
    A simple bloom filter implementation
    More references:
    1. http://en.wikipedia.org/wiki/Bloom_filter
    2. http://maciejczyzewski.me/2014/10/18/bloom-filters-fast-and-simple.html
"""
class SimpleBloomFilter(object):
    """
    doctest: python -m doctest bloomfilter.py
    >>> bfilter = SimpleBloomFilter()
    >>> bfilter.add(1024)
    >>> bfilter.query(1024)
    True
    >>> bfilter.add(3)
    >>> bfilter.query(3)
    True
    >>> bfilter.add(44222211)
    >>> bfilter.query(44222211)
    True
    >>> bfilter.query(3214)
    False
    """
    def __init__(self, bit_array_size=1024 * 8, hash_num = 12):
        self.bitarray = bytearray(int(ceil(bit_array_size / 8)))
        self.bit_num = bit_array_size
        self.hash_num = hash_num

    def _hash(self, value):
        """
        Generate multiple different hash functions by slicing its output into
        multiple bit fields.
        Return
        -------
        A generator of hash functions
        """
        digest = int(sha256(value.__str__()).hexdigest(), 16)
        slice_bit_num = 256 / self.hash_num
        for i in range(self.hash_num):
            # slice digest from low bits to generate different hash values
            yield digest & (2 ** slice_bit_num - 1)
            digest >>= slice_bit_num
    
    def add(self, value):
        """
        Set k bit position from k hash functions to 1
        """
        for hash_val in self._hash(value):
            self.bitarray[(hash_val%self.bit_num)/8] |= 2 ** ((hash_val % self.bit_num) % 8)

    def query(self, value):
        """
        Check whether all of k bit positions from k hash functions are set to 1
        """
        return all(self.bitarray[(hv%self.bit_num)/8] & 2 ** ((hv % self.bit_num) % 8) for hv in self._hash(value))
