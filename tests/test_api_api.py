"""
    test_api_api
    ~~~~~~~~~~~~

    Tests for the :mod:`~ulid.api.api` module.
"""
import pytest

from ulid import providers
from ulid.api.api import ALL, Api


@pytest.fixture(scope='function')
def mock_provider(mocker):
    """
    Fixture that yields a mock provider.
    """
    provider = mocker.Mock(spec=providers.Provider)
    provider.new = mocker.Mock(side_effect=providers.DEFAULT.new)
    provider.timestamp = mocker.Mock(side_effect=providers.DEFAULT.timestamp)
    provider.randomness = mocker.Mock(side_effect=providers.DEFAULT.randomness)
    return provider


@pytest.fixture(scope='function')
def mock_api(mock_provider):
    """
    Fixture that yields a :class:`~ulid.api.api.Api` instance with a mock provider.
    """
    return Api(mock_provider)


def test_all_defined_expected_methods():
    """
    Assert that :attr:`~ulid.api.api.ALL` exposes expected interface.
    """
    assert ALL == [
        'new',
        'parse',
        'create',
        'from_bytes',
        'from_int',
        'from_str',
        'from_uuid',
        'from_timestamp',
        'from_randomness',
        'MIN_TIMESTAMP',
        'MAX_TIMESTAMP',
        'MIN_RANDOMNESS',
        'MAX_RANDOMNESS',
        'MIN_ULID',
        'MAX_ULID',
        'Timestamp',
        'Randomness',
        'ULID'
    ]


def test_api_new_calls_provider_new(mock_api):
    """
    Assert :meth:`~ulid.api.api.Api.new` calls :meth:`~ulid.providers.base.Provider.new` for timestamp
    and randomness values.
    """
    mock_api.new()

    mock_api.provider.new.assert_called_once_with()


def test_api_from_timestamp_calls_provider_randomness(mocker, mock_api, valid_bytes_48):
    """
    Assert :meth:`~ulid.api.api.Api.from_timestamp` calls :meth:`~ulid.providers.base.Provider.randomness` for a value.
    """
    mock_api.from_timestamp(valid_bytes_48)

    mock_api.provider.timestamp.assert_not_called()
    mock_api.provider.randomness.assert_called_once_with(mocker.ANY)


def test_api_from_randomness_calls_provider_timestamp(mock_api, valid_bytes_80):
    """
    Assert :meth:`~ulid.api.api.Api.from_randomness` calls :meth:`~ulid.providers.base.Provider.timestamp` for a value.
    """
    mock_api.from_randomness(valid_bytes_80)

    mock_api.provider.timestamp.assert_called_once_with()
    mock_api.provider.randomness.assert_not_called()
