"""
   test_creation
   ~~~~~~~~~~~~~

    Performance benchmarks that compare ULID instance creation speed to comparable types.
"""
import uuid

import ulid


def test_ulid_new(benchmark):
    """
    Run performance benchmark for ULID instances.
    """
    benchmark(ulid.new)


def test_uuid_v1_new(benchmark):
    """
    Run performance benchmark for creating UUID v1 instances.
    """
    benchmark(uuid.uuid1)


def test_uuid_v4_new(benchmark):
    """
    Run performance benchmark for creating UUID v4 instances.
    """
    benchmark(uuid.uuid4)
