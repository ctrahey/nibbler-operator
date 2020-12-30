#! /bin/sh
FILENAME=.mysql_pass.txt
head -c 14 /dev/urandom | base64 | LC_CTYPE=C sed 's/[^a-zA-Z0-9]//' | tr -d '\n' > $FILENAME
FILENAME=.mysql_user.txt
head -c 6 /dev/urandom | base64 | LC_CTYPE=C sed 's/[^a-zA-Z0-9]//' | tr -d '\n' > $FILENAME
