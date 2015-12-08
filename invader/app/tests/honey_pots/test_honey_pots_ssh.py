import os
import paramiko
import pytest
import mock
import honey_pots.ssh.server

class FakeClientSocket():
        def __init__(self, *args, **kwargs):
            pass

        def getsockname(self):
            pass

@pytest.fixture(autouse=True)
def no_sleep(mocker):
    mocker.patch('time.sleep')


@pytest.fixture(autouse=True)
def settings(mocker):
    mocker.patch.dict('os.environ', dict(
        HONEY_POTS_SSH_PORT="6666",
        HONEY_POTS_SSH_VERSION="SSH-2.0-OpenSSH_4.3"
    ))


@pytest.fixture(autouse=True)
def fake_exit(mocker):
    mocker.patch('sys.exit')


@pytest.fixture(autouse=True)
def socket_obj(mocker):
    socket_mock = mocker.patch('honey_pots.ssh.server.socket').return_value
    return socket_mock


@pytest.fixture(autouse=True)
def paramiko_obj(mocker):
    paramiko_mock = mocker.patch('honey_pots.ssh.server.paramiko').return_value
    return paramiko_mock


@pytest.fixture
def thread_obj(mocker):
    thread_mock = mocker.patch('honey_pots.ssh.server.threading').return_value
    return thread_mock


@pytest.fixture
def incoming_connection_obj(mocker):
    incoming_connection_mock = mocker.patch('honey_pots.ssh.server.incoming_connection').return_value
    return incoming_connection_mock

@pytest.fixture
def server_obj(mocker):
    server_mock = mocker.patch('honey_pots.ssh.server.Server').return_value
    return server_mock

@pytest.fixture
def server_obj2(mocker):
    class FakeServer:
        def __init__(self, *args, **kwargs):
            raise paramiko.SSHException

    server_mock = mocker.patch('honey_pots.ssh.server.Server')
    server_mock.return_value = FakeServer
    return server_mock


#def test_start_server(thread_obj, incoming_connection_obj):
#    honey_pots.ssh.server.start_server()


def test_incoming_connection(mocker, server_obj):
    

    honey_pots.ssh.server.incoming_connection(FakeClientSocket())

    mocker.patch.dict('os.environ', dict(
        HONEY_POTS_SSH_RSA_KEY="{0}/real_rsa".format(os.path.dirname(os.path.realpath(__file__))),
    ))

    honey_pots.ssh.server.incoming_connection(FakeClientSocket())


    mocker.patch.dict('os.environ', dict(
        HONEY_POTS_SSH_RSA_KEY="{0}/fake_rsa".format(os.path.dirname(os.path.realpath(__file__))),
    ))


def test_error_incoming_connection(mocker, server_obj2):
    mocker.patch.dict('os.environ', dict(
        HONEY_POTS_SSH_RSA_KEY="{0}/real_rsa".format(os.path.dirname(os.path.realpath(__file__))),
    ))

    honey_pots.ssh.server.incoming_connection(FakeClientSocket())


def test_server():
    class fakePublicKey():
        def __init__(self, *args, **kwargs):
            pass

        def get_base64(self):
            pass

    sshd = honey_pots.ssh.server.Server(("127.0.0.1", 6666))
    sshd.check_channel_request("", "")
    sshd.check_channel_request("session", "")
    sshd.check_auth_interactive("", "")
    sshd.check_auth_password("", "")
    sshd.check_auth_publickey("", fakePublicKey())
    sshd.check_auth_interactive_response("")
    sshd.get_allowed_auths("")
    sshd.check_channel_shell_request("")
    sshd.check_channel_pty_request("", "", "", "", "", "", "")
    
    sshd.has_authenticated_before = True
    sshd.check_auth_interactive("", "")

