reset
set terminal postscript portrait color enhanced 12
set o "smooth.eps"
set palette defined (-6.0 "#1B66B1",\
                     -4.8 "#2A85DF",\
                     -3.6 "#5FA3E7",\
                     -2.4 "#95C2EF",\
                     -1.2 "#C9E0F7",\
                     0.0 "#FFFFFF",\
                     1.2 "#F6D5CB",\
                     2.4 "#EDAB96",\
                     3.6 "#E48062",\
                     4.8 "#DC562E",\
                     6.0 "#AE3F1E")
set samples 20
set isosamples 20
splot sin(sqrt(x**2+y**2))/sqrt(x**2+y**2) w pm3d
set o
set term wxt