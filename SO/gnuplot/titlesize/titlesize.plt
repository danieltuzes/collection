set pixmap 1 "linux.png" at screen 0.85, 0 width screen 0.15 behind
set rmargin at screen 0.85

# Border line definition
set border lw 1

# Major and Minor grid definition
set style line 100 lt 1 lc rgb "gray" lw 2
set style line 101 lt 0.5 lc rgb "gray" lw 1
set grid mytics ytics ls 100, ls 101
set grid mxtics xtics ls 100, ls 101

set term png
set o "output.png"
set title 'myTitle' font ", 12"
set ylabel 'y [m]' font "Helvetica, 12"
set xlabel 'x [m]' font "Helvetica, 12"
set tics font "Helvetica,10"
plot [-10:10] sin(x),atan(x),cos(atan(x))
set o

