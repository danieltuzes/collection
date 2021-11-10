reset
x_0 = 1
y_0 = 2

length(x,y) = sqrt(x**2+y**2)

x_1 = -1+sqrt(2)
y_1 = 1
lambda_1 = 3 + 2*sqrt(2)

x_2 = -1-sqrt(2)
y_2 = 1
lambda_2 = 3 - 2*sqrt(2)

scale_1 = sqrt(lambda_1) / length(x_1,y_1)
scale_2 = sqrt(lambda_2) / length(x_2,y_2)

x_1p = x_0 + x_1 * scale_1
y_1p = y_0 + y_1 * scale_1

x_2p = x_0 + x_2 * scale_2
y_2p = y_0 + y_2 * scale_2


print(length(x_1p - x_0, y_1p - y_0))
print(lambda_1)
print(length(x_2p - x_0, y_2p - y_0))
print(lambda_2)


set arrow 1 from x_0, y_0 to x_1p, y_1p lw 2 front
set arrow 2 from x_0, y_0 to x_2p, y_2p lw 2 front

set size ratio 2
set style circle radius 0.05
set style fill transparent solid 0.1 noborder
set key left box
set xlabel "x"
set ylabel "y"
p [-3:4][-6:8] "res.txt" w circles t "data points with correlation"