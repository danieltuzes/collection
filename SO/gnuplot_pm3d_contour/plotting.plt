set contour both
set pm3d border linewidth 0.2

set linetype 1 lc rgb "black" lw 1.5 dt 1
set linetype 2 lc rgb "black" dt 1
set linetype 3 lc rgb "black" dashtype 2
set linetype 4 lc rgb "black" dashtype 3
set linetype 5 lc rgb "black" dashtype 4
set style line 1 lc rgb 'black' lw 1.5 dt 1
set style line 2 lc rgb 'black' dt 1
set style line 3 lc rgb 'black' dashtype 2
set style line 4 lc rgb 'black' dashtype 3
set style line 5 lc rgb 'black' dashtype 4

set logscale z
set zrange [1e-5:]
set log cb
set cntrparam levels discrete 1, 0.1, 0.002, 0.0005
splot 'jpdfstrW_90.dat' u 1:2:($3+1e-5) w pm3d notitle, "" u 1:2:($3+1e-5) t 'JPDF' with lines nosurf 