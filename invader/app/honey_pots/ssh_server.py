#!/usr/bin/env python

from __future__ import unicode_literals
import os
import socket
import threading
import traceback
import paramiko
import sys
import time
import logging
from logging.handlers import RotatingFileHandler



# log init
logger = logging.getLogger(__name__)

# Set up logging
#paramiko.util.log_to_file('{0}/paramiko_error_log'.format(os.environ["LOG_DIR"]))


class Server (paramiko.ServerInterface):
    def __init__(self, info_server):
        self.address, self.port = info_server
        self.event = threading.Event()
        self.has_authenticated_before = False
        self.banner = os.environ.get("HONEY_POTS_SSH_BANNER", "")

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_interactive(self, username, submethods):
        if self.has_authenticated_before:
            return paramiko.AUTH_FAILED
        else:
            self.has_authenticated_before = True
            return paramiko.InteractiveQuery('', self.banner)

    def check_auth_password(self, username, password):
        logger.info("check authentification with password")
        logger.info("username: {0} :: password {1}".format(username.encode("utf8"), password.encode("utf8")))
        time.sleep(3)
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        logger.info("check authentification with public key")
        logger.info(key.get_base64())
        time.sleep(3)
        return paramiko.AUTH_FAILED

    def check_auth_interactive_response(self, responses):
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'keyboard-interactive,publickey,password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


def incoming_connection(client):
    try:
        sshd = paramiko.Transport(client)
        rsa_key = os.environ.get("HONEY_POTS_SSH_RSA_KEY", None)
        if rsa_key is not None:
            host_key = paramiko.RSAKey(filename=rsa_key)
        else:
            host_key = paramiko.RSAKey.generate(1024)
            host_key.write_private_key_file("rsa")

        sshd.local_version = os.environ.get("HONEY_POTS_SSH_VERSION")

        # Start the server & negotiate with the client
        server = Server(client.getsockname())
        sshd.add_server_key(host_key)
    except paramiko.SSHException, e:
        logger.error("Caught exception: {0}: {1}".format(str(e.__class__), str(e)))
        traceback.print_exc()
        sys.exit(1)

    try:
        sshd.start_server(server=server)
    except paramiko.SSHException:
        logger.error("SSH negotiation failed")
        sshd.close()
        return False

    # Wait for auth
    sshd.accept(60)
    sshd.close()


def start_server():
    port = int(os.environ.get("HONEY_POTS_SSH_PORT"))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the port
    try:
        sock.bind(('', port))
    except socket.error:
        logger.info("Could not bind to port: {0}".format(port))
        traceback.print_exc()

    while 42:
        try:
            sock.listen(os.environ.get("HONEY_POTS_SSH_MAX_CONNECTIONS", 4))
            logger.info("Waiting for connection")
            client, addr = sock.accept()

            logger.info("Client connected")
            threading.Thread(target=incoming_connection, args=[client]).start()
        except Exception, e:
            logger.error("Couldn't wait for connection: {0}".format(str(e)))
            traceback.print_exc()

    sock.close()