#!/bin/bash
# ellenőrizgeti a feltételt, aztán ha már nem teljesül, akkor végrehajta a maradékot

echo "Leszámolom, hány $pattern reguláris kifejezésű folyamat van, és ha nem több, mint $processcount, levelet küldök és végrehajtom az alábbi parancsot:"
echo "$command"

do_count() {
echo `ps -u tuzes | grep "$pattern" | wc -l`
}

for ((count=$(do_count); $count > $processcount; count=$(do_count)))
do
	now=`date`
	echo "$now, count: $count"
	sleep 10
done

now=`date`	# ha már lefutottak a programok
echo "$now, count: %count <= $processcount."
echo "Elindítom az alábbi parancsot:"
echo "$command"

(eval $command)	# elindítja a 2D4 nevű megállított progikat
sleep 10	# vár, hogy biztosan elinduljanak
echo "sleep 10; ps -u tuzes"	# kiírja, hogy mi a frászt csinál
pstext=`ps -u tuzes`	# beleíródik a kimeneti fileba
echo "$pstext"

nohup ${mypath}/send_mail.sh "$(hostname) sikeresen lefutott" "A $(hostname) gépen a $pattern reguláris kifejezésű folyamatok száma $processcount alá csökkent, és végrehajtódott az alábbi parancs:\n$command\n\nTovábbi infót ad: ps -u tuzes\n${pstext}" &>> ${mypath}/send_mail.nohup &
