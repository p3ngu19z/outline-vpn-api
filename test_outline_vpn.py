"""
Integration tests for the API wrapper
"""

import os

import pytest

from outline_vpn import OutlineVPN


@pytest.fixture
def client() -> OutlineVPN:
    assert os.getenv("OUTLINE_CREDENTIALS")
    client = OutlineVPN(api_url=os.getenv("OUTLINE_CREDENTIALS"))
    yield client


def test_get_keys(client: OutlineVPN):
    """Test for the get keys method"""
    assert len(client.get_keys()) >= 1


def test_cud_key(client: OutlineVPN):
    new_key = client.create_key()
    assert new_key is not None
    assert int(new_key.key_id) > 0

    assert client.rename_key(new_key.key_id, "a_name")

    assert client.delete_key(new_key.key_id)


def test_limits(client: OutlineVPN):
    assert client.add_data_limit(0, 1024 * 1024 * 20)
    assert client.delete_data_limit(0)