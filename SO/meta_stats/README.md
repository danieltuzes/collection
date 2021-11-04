# Stackoverflow analysis

It would be great to analyze the reputation distribution and have nice graphs.

```gnuplot
f(x) = 5e6*x**-1.5                   
p "rep_distr_part.csv" every ::1,f(x)
```

This fits well more or less.
