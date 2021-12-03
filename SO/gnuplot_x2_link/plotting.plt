reset
set link x2 via 1000./x inverse 1000./x
set x2tics 50 
plot [0.60:0.70] 'Data.dat' u 1:2
