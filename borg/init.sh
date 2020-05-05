#!/usr/bin/env bash

ssh-keygen -A

for key in $(echo "ssh_host_rsa_key ssh_host_ecdsa_key ssh_host_ed25519_key")
do
if [[ ! -f /config/${key} ]]; then
  echo "Copy /etc/ssh/${key} to /config/${key}"
  cp /etc/ssh/${key} /config/${key}
  cp /etc/ssh/${key}.pub /config/${key}.pub
fi
done
# -D in CMD below prevents sshd from becoming a daemon. -e is to log everything to stderr.
/usr/sbin/sshd -D -e
