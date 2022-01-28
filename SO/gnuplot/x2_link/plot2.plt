reset
set terminal postscript eps enhanced colour font 'Times-Roman,12' size 6in,5in
set output "JNM_2020_F2.eps"
set xtics out scale 1.5 
set ytics out scale 1.5
set tics font ", 16"
set xtics nomirror 
set xlabel "10^{3}{/Symbol \264} 1/T (K^{-1})" font "Times-Bold,20"
set ylabel "y" font "Times-Bold,20"
set key outside right top 
set x2tics out scale 1.5 
set link x2 via 1000./x-273.15 inverse 1000./(x+273.15)
set x2tics 50
set x2label "Temperature [°C]" font "Times-Bold,20"
plot [0.60:0.70] 'Data.dat' u 1:2 with points pt 4 ps 1.75 lt -1 title "Ref. [7]"