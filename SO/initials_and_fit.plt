reset
f(x)=A*exp(-b*x)*sin(2.*pi*x/T+phi)+S

    A = 40.
    b = 1/500.
    T = 400.
    phi = 1.
    S = 170.

f_bad_guess(x) = 40. * exp(-x/500.) * sin(2.*pi*x/150+3.) + 170.
f_good_guess(x) = 40. * exp(-x/500.) * sin(2.*pi*x/400+1.) + 170.

fit f(x) "data.txt" via A,b,T,phi,S

set samples 1000
p "data.txt" t "data", f(x) t "fitted function", f_good_guess(x) t "good initial guess set manually", f_bad_guess(x) t "bad initial guess set manually"
