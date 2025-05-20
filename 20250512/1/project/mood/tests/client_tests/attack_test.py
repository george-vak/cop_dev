import pytest
from unittest.mock import MagicMock

from client.commands import CommandHandler

@pytest.fixture()
def handler_and_mocks():
    fake_net = MagicMock()
    fake_ui = MagicMock()
    handler = CommandHandler(fake_net, fake_ui)
    handler.arsenal = ["sword", "axe", "spear"]
    return handler, fake_net, fake_ui

@pytest.mark.parametrize(
    "cmd, expected_send, expected_error",
    [
        ("attack www with axe", "attack www axe", None),
        ("attack eyes", "attack eyes sword", None),
        ("attack tux with mop", None, "Unknown weapon"),
        ("attack", None, "Укажите имя монстра для атаки"),
    ]
)
def test(handler_and_mocks, cmd, expected_send, expected_error):
    handler, fake_net, fake_ui = handler_and_mocks

    result = handler.handle_command(cmd)
    assert result is True

    if expected_send is not None:
        fake_net.send_command.assert_called_once_with(expected_send)
        sent = fake_net.send_command.call_args[0][0]
    else:
        assert fake_net.send_command.call_count == 0
        sent = None

    if expected_error is not None:
        fake_ui._print_error.assert_called_once_with(expected_error)
        err = fake_ui._print_error.call_args[0][0]
    else:
        fake_ui._print_error.assert_not_called()
        err = None

    print(f"\nCommand: '{cmd}' --> Sent: '{sent}' error: '{err}'\n excepted '{expected_send}'::'{expected_error}'")