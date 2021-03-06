# Copyright 2019 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
"""Test Suite for inbound filters for providers."""
import pytest

from rbac.providers.common.common import escape_user_input
from rbac.providers.common.inbound_filters import (
    inbound_group_filter,
    inbound_user_filter,
)

HTML_ESCAPE_CASES = [
    ("<html>hello</html>", "&lt;html&gt;hello&lt;/html&gt;"),
    (
        ["<script>Malicious Script Here</script>", "<div>More malicious content</div>"],
        [
            "&lt;script&gt;Malicious Script Here&lt;/script&gt;",
            "&lt;div&gt;More malicious content&lt;/div&gt;",
        ],
    ),
    (
        {"user_input<>": '<img src=1 href=1 onerror="javascript:alert(1)"></img>'},
        {
            "user_input&lt;&gt;": "&lt;img src=1 href=1 onerror=&quot;javascript:alert(1)&quot;&gt;&lt;/img&gt;"
        },
    ),
    (None, None),
]


def test_inbound_user_filter():
    """Test the inbound user filter for azure transforms and returns a user dict."""
    result = inbound_user_filter({"id": "123-456-abs3"}, "azure")
    assert isinstance(result, dict) is True
    assert result["remote_id"] == "123-456-abs3"
    assert "id" not in result


def test_inbound_bad_provider():
    """Test the inbound user filter with bad provider throws error"""
    with pytest.raises(TypeError):
        inbound_user_filter({"id": "123-456-abs3"}, "potato")


def test_inbound_group_filter():
    """Test the inbound group filter for azure transforms and returns a group dict."""
    result = inbound_group_filter({"id": "123-456-abs3"}, "azure")
    assert isinstance(result, dict) is True
    assert result["remote_id"] == "123-456-abs3"
    assert "id" not in result


def test_inbound_group_provider():
    """Test the inbound group filter with bad provider throws error"""
    with pytest.raises(TypeError):
        inbound_group_filter({"id": "123-456-abs3"}, "potato")


def test_user_data_type_correct():
    """Test that a list stays a list when a single value is in it."""
    result = inbound_user_filter(
        {"id": "123-456-abs3", "manager": ["123-456-abs3"]}, "azure"
    )
    assert result["manager_id"] == ["123-456-abs3"]


def test_data_kept_with_empty_lst():
    """Test that a list stays a list when there is no value in it."""
    result = inbound_user_filter({"id": "123-456-abs3", "manager": []}, "azure")
    assert result["manager_id"] == []


def test_data_is_kept_when_null():
    """Test that a user list stays null when it is None."""
    result = inbound_user_filter({"id": "123-456-abs3", "manager": None}, "azure")
    assert result["manager_id"] is None


def test_group_data_type_correct():
    """Test that a group list stays a list when a single value is in it."""
    result = inbound_group_filter(
        {"id": "123-456-abs3", "members": ["123-456-abs3"]}, "azure"
    )
    assert result["members"] == ["123-456-abs3"]


def test_role_data_with_empty_lst():
    """Test that a group list stays a list when there is no value in it."""
    result = inbound_group_filter({"id": "123-456-abs3", "members": []}, "azure")
    assert result["members"] == []


def test_role_data_when_null():
    """Test that a group list stays null when it is None."""
    result = inbound_group_filter({"id": "123-456-abs3", "members": None}, "azure")
    assert result["members"] is None


@pytest.mark.parametrize("user_input, expected_result", HTML_ESCAPE_CASES)
def test_html_escape(user_input, expected_result):
    """ Test that escape_user_input() function properly escapes various
    user inputs.

    Args:
        user_input: (str, list, dict, None) A user generated input received
            by an API endpoint or imported LDAP objects.
        expected_result: (str, list, dict, None) The user_input with escaped
            HTML code.
    """
    assert expected_result == escape_user_input(user_input)
