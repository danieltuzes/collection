# Mi ez?
Ez egy kis leírás a `do_if_finished` mappában található fájlokhoz. Ha lefutnak bizonyos parancsok, akkor e-mailt küld róla és végrehajt egy parancsot is.

## Melyik fájl mire való?
A `start.sh` fájlt elindítva, az abban szereplő reguláris kifejezésű programokat keres, majd ha nincs belőlük egy sem, akkor végrehajt egy parancsot, és küld egy e-mailt. A levélküldéshez szükséges e-mail account jelszavát bekéri.

A `start.sh` meghívja a `checking.sh` szkriptet, ami 10 másodpercenként ellenőrizgeti, hogy hány fut az adott regexpű folyamatból, és nohup fájlba ki is írja. Ha már 0 fut, akkor a `send_mail.sh` szkript segítségével e-mailt küld.

## Mik vannak a fájlokban?
Ennek a dokumentumnak a készítésekor az alábbiak voltak a fájlok tartalmai?

### `start.sh`
```bash
#!/bin/bash
# végrehajt egy parancsot és e-mail küld, hogyha lejártak az adott minátjú programok, ehhez pedig bekér egy e-mail account jelszót

pattern="BiSiSeX.*"	# milyen reguláris kifejezést keressen?
export pattern

command="killall -s CONT -r '2D4'"	# a parancs, amit végrehajt
export command

mypath=`dirname $0`	# kelleni fog a mappa helye, ahonnan fut
export mypath

read -s -p "Írd be a eltecomputeservers@gmail.com jelszavát: " eltecomputeserverspassword
export eltecomputeserverspassword
echo ""

nohup ./${mypath}/send_mail.sh 'Értesítés beállítva' 'Értesítés fog érkezni, mihelyst a szkript odajut, hogy e-mailt küldjön.' &>> ${mypath}/send_mail.nohup &

nohup ./${mypath}/checking.sh &>> ${mypath}/do_if_finished.nohup &	# addig fut, amíg van folyamat, de le van választva a terminálról
```

### `checking.sh`
```bash
#!/bin/bash
# ellenőrizgeti a feltételt, aztán ha már nem teljesül, akkor végrehajta a maradékot

printf "Leszámolom, hány $pattern mintájú folyamat van, és ha 0, lefuttatom a szkriptet.\n"

do_count() {
echo `ps -u tuzes | grep "$pattern" | wc -l`
}

for ((count=$(do_count); $count > 0; count=$(do_count)))
do
	now=`date`
	printf "%s, count: %d\n" "$now" $count
	sleep 10
done

now=`date`	# ha már lefutottak a programok
eval $command	# elindítja a 2D4 nevű megállított progikat
sleep 10	# vár, hogy biztosan elinduljanak
printf "%s, elindítottam mindet 10 másodperce, nézd csak, kapsz egy kis infót\n" "$now"
pstext=`ps -u tuzes`	# beleíródik a kimeneti fileba
printf "${pstext}\n"

nohup ./${mypath}/send_mail.sh 't2 sikeresen lefutott' "Nincs több $pattern mintájú program.\n${pstext}" &>> ${mypath}/send_mail.nohup &
```

### `send_mail.sh`
```bash
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
```