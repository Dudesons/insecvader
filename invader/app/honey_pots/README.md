# Honey pot SSH

Environment variables :
 * HONEY_POTS_SSH_PORT : the tcp port wwhere the honey pots ssh will be binded (maybe gen random port)d
 * HONEY_POTS_SSH_BANNER : the banner to display when the connection begin, default empty
 * HONEY_POTS_SSH_RSA_KEY : the path where is store the private rsa key, default None
 * HONEY_POTS_SSH_MAX_CONNECTIONS: Represent the maximum number of queued connections, default 4
 * HONEY_POTS_SSH_VERSION: this is the ssh version server to indicate (eg: "SSH-2.0-OpenSSH_4.3")