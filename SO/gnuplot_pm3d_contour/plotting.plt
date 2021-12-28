reset
set contour both
set pm3d border linewidth 0.2

set logscale z
set zrange [1e-5:]

splot 'jpdfstrW_90.dat' u 1:2:($3+1e-5) w pm3d notitle, "" u 1:2:($3+1e-5) t 'JPDF' with lines nosurf lw 2