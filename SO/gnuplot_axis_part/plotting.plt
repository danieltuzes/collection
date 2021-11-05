# https://stackoverflow.com/questions/69856751/how-can-i-get-axes-not-touching-each-other/69857890#69857890
reset
f(x) = x>2 ? ( x<4 ? x**2 : 1/0) : 1/0
set xrange [0:5]
set yrange [0:20]
set ytics 4,2,16 nomirror
set xtics 2,1,4 nomirror
unset border
set arrow from 2,0 to 4,0 nohead
set arrow from 0,4 to 0,16 nohead
p f(x)