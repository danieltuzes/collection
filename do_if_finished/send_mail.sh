#!/bin/bash

emailFname="email_for_curl.txt"	# a hülye curl csak fájlt tud küldeni, szöveget nem, így bele kell írni egy fájlba a tartalmat
echo "Content-Type: text/plain; charset=utf-8
From: eltecomputeservers@gmail.com
To: tuzes@metal.elte.hu
Subject: $1

$2
" > ${mypath}/${emailFname}	# a fájl így létrejön, de majd törölni kell

curl --url 'smtps://smtp.gmail.com:465' --ssl-reqd \
  --mail-from 'eltecomputeservers@gmail.com' \
  --mail-rcpt 'tuzes@metal.elte.hu' \
  --user eltecomputeservers@gmail.com:${eltecomputeserverspassword} \
  -T ${mypath}/${emailFname}
  
rm ${mypath}/${emailFname}	# a curl elküldte a fájlt, most már lehet törölni