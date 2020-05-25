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

nohup ./${mypath}/send_mail.sh "$(hostname) sikeresen lefutott" "Nincs több $pattern mintájú program a $(hostname) gépen.\n${pstext}" &>> ${mypath}/send_mail.nohup &