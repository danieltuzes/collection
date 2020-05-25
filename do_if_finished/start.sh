#!/bin/bash
# végrehajt egy parancsot és e-mail küld, hogyha elfogynak az adott minátjú programok, ehhez pedig bekér egy e-mail account jelszót

pattern="BiSiSeX.*"	# milyen reguláris kifejezést keressen?
export pattern

command="killall -s CONT -r '2D4'"	# a parancs, amit végrehajt
export command

processcount=0	# hánynál több kell, hogy fusson, hogy ne számítson befejezettnek
export processcount

mypath=`dirname $0`	# kelleni fog a mappa helye, ahonnan fut
export mypath

read -s -p "Írd be a eltecomputeservers@gmail.com jelszavát: " eltecomputeserverspassword	# bekéri a jelszót, és nem írja ki a terminálra
export eltecomputeserverspassword
echo ""

nohup ${mypath}/send_mail.sh "Értesítés beállítva a $(hostname) gépen" \
"Értesítés fog érkezni, ha a $(hostname) gépen a $pattern reguláris kifejezésű folyamatok száma $processcount alá csökken, és végrehajtja a $command parancsot." \
&>> ${mypath}/send_mail.nohup &

nohup ${mypath}/checking.sh &>> ${mypath}/do_if_finished.nohup &	# addig fut, amíg van folyamat, de le van választva a terminálról