"""various helper functions related to or extending scipy.optimize and curve fitting"""



from scipy.optimize import curve_fit
import numpy as np

def complex_curve_fit(f, xdata, ydata, **kwargs):
    """Use non-linear least squares to fit a complex function, f, to data.
            
            f(x,*params)->complex     function model to fit
            xdata[N][real]            domain data
            ydata[N][complex]         range data

        Returns (vals, pcov)                                           """

    def f_modififed(x, *params):
        x = np.asarray(x)
        y = f(x, *params)[0:int(len(x)/2)]
        return np.append(y.real, y.imag)

    return curve_fit(f_modififed, np.append(xdata,xdata), np.append(ydata.real, ydata.imag), **kwargs)

if __name__ == "__main__":

    # testing complex_curve_fit

    import matplotlib.pyplot as plt
    def f(x,a,b):
        return a*x**2 + b*1j*x**3

    x = np.linspace(0,1,100)
    noise = np.random.normal(scale=0.05, size=(100,))
    noise_i = np.random.normal(scale=0.05, size=(100,))
    y = f(x,1,3) + noise + noise_i*1j

    plt.plot(x, y.real, label = 'real, exact')
    plt.plot(x, y.imag, label = 'imag, exact')

    vals,pcov = complex_curve_fit(f, x, y, p0=(2,2))
    yfit = f(x, *vals)
    print(vals)
    plt.plot(x, yfit.real, label = 'real, fit')
    plt.plot(x, yfit.imag, label = 'imag, fit')


    plt.legend()
    plt.show()
