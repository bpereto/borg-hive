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

#
# POPULATE PASSWD & SHADOW
#
if [[ ! -f /config/passwd ]]; then
cat << EOF > /config/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
borg:x:1000:1000:Borghive User:/home/borg:/bin/bash
EOF
fi
chown borg:borg /config/passwd

if [[ ! -f /config/shadow ]]; then
cat << EOF > /config/shadow
root:*:18374:0:99999:7:::
daemon:*:18374:0:99999:7:::
bin:*:18374:0:99999:7:::
sys:*:18374:0:99999:7:::
nobody:*:18374:0:99999:7:::
sshd:*:18384:0:99999:7:::
borg:*:18384:0:99999:7:::
EOF
fi
chown borg:borg /config/shadow

setfacl -R -d -m u:borg:rwx /repos

# -D in CMD below prevents sshd from becoming a daemon. -e is to log everything to stderr.
/usr/sbin/sshd -D -e
