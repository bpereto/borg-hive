#!/usr/bin/env bash

ssh-keygen -A

# -D in CMD below prevents sshd from becoming a daemon. -e is to log everything to stderr.
/usr/sbin/sshd -D -e
