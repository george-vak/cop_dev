import pytest
from unittest.mock import MagicMock

from client.commands import CommandHandler

@pytest.fixture()
def handler_and_mocks():
    fake_net = MagicMock()
    fake_ui = MagicMock()
    handler = CommandHandler(fake_net, fake_ui)
    return handler, fake_net, fake_ui

@pytest.mark.parametrize(
    "cmd, expected", [
    ("down",  "move 0 1"),
    ("up",    "move 0 -1"),
    ("left",  "move -1 0"),
    ("right", "move 1 0"),
])

def test(handler_and_mocks, cmd, expected):
    handler, fake_net, fake_ui = handler_and_mocks

    result = handler.handle_command(cmd)
    assert result is True

    if fake_net.send_command.call_count:
        sent = fake_net.send_command.call_args[0][0]
        fake_net.send_command.assert_called_once_with(expected)
        fake_ui._print_error.assert_not_called()
    else:
        sent = None

    print(f"\nCommand: '{cmd}' --> Sent: '{sent}' expected '{expected}'")

