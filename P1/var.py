############################
### Autor: Carlos Arenas
### Contacto: f22arrac@uco.es
############################

class var ():
    # Para variables independientes, ya sean medidas de laboratorio, parámetros o constantes.
    def __init__ (self, value, err, name = "", axes = (), units = "", str_format = "{:.2f}", *args):
        import numpy as np
        import sympy as sp
        import random
        import string

        # Sobre el manejo de datos:
        self.value = np.array(value)
        self.err = np.array(err)

        if axes == ():
            self.dim = np.ndim(self.value)
            axes_dicc = {0:(), 1:(0,), 2:(0,1), 3:(0,1,2)}
            self.axes = axes_dicc[self.dim]
        else:
            self.axes = axes
            self.dim = len(axes)
        
        # Sobre el cálculo simbólico:
        self.name = name
        self.units = units

        code_name = ''.join(random.choice(string.ascii_letters) for i in range(16))
        self.sym = sp.symbols(code_name)
        self.err_sym = sp.symbols(code_name + "_{err}")

        self.variables = [self]
        self.f = self.sym

        # Otros:
        self.str_format = str_format


    def calculate(self):
        import sympy as sp

        # It's always easier to do it as it is supposed to...
        vsyms = [v.sym for v in self.variables]
        err_syms = [v.err_sym for v in self.variables]

        f = sp.lambdify(vsyms, self.f)
        err_f = sp.lambdify(vsyms + err_syms, self.err_f)

        # ! The power of Broadcasting !
        data = [v.value for v in self.variables]
        err_data = data + [v.err for v in self.variables]

        self.value = f(*data)
        self.err = err_f(*err_data)


    def show (self):
        import numpy as np

        print("==========")
        print(f"Name: {self.name} \nValues:")
        b = np.broadcast(self.value, self.err)
        for x,e in b:
            #print(rf"{self.value[i]}\t$\pm$\t{self.err[i]}")
            print(f"{x} \t\t {e}")
        print("==========")


    def vs (self, v, options = {}, plot_args = {}):
        # Por ahora solo disponible para arrays de dimension igual o menor a 2.

        import matplotlib.pyplot as plt

        options = {
            "columns": [],
            "holdon": False,
            "fitlm": True,
            "axes": []
            } | options
            
        import matplotlib.ticker as mticker
        ax = plt.gca()

        """
        ax.yaxis.set_major_formatter(mticker.EngFormatter(
            useOffset=True,
            #unit= self.units
            ))
        ax.xaxis.set_major_formatter(mticker.EngFormatter(
            useOffset=True,
            #unit= v.units
            ))
        """
        ax.set_box_aspect(1.0)
        
        # Todas estas funciones no son más que wrappers de funciones de la clase axes.
        
        plt.xlabel(rf"{v.name} ({v.units})")
        plt.ylabel(rf"{self.name} ({self.units})")
        plt.grid(visible = True)
        plt.minorticks_on()
        
        if options["fitlm"]:
            from scipy import stats
            import numpy as np

            # Asegurar que los datos tengan el mismo tamaño.
            data = np.broadcast_arrays(v.value, self.value, v.err, self.err)

            # Calcular parámetros del ajuste lineal.
            result = stats.linregress(data[0], data[1], nan_policy = "omit")
            m = var(result.slope, result.stderr)
            n = var(result.intercept, result.intercept_stderr)

            plot_args = {"marker": "o",
                "capsize": 4,
                "markerfacecolor": "None",
                "linestyle": "",
                "zorder": 0,   # Orden frontal
                "alpha": 1     # Opacidad
                } | plot_args
            
            # Problemas:
            # 1. plt.errorbar parece no admitir broadcasting. Raro porque plt.pot sí lo hace.
            # 2. El broadcasting necesita que las dimensiones que concuerdan estén dispuestas en último lugar y en el mismo orden.
            # 3. plt.plot solo admite arrays 2D
            # 
            # Conclusión: Hay que hacer una cuidadosa selección y tratamiento de los datos que se van a plotear.

            a = min(data[0] - data[2])
            b = max(data[0] + data[2])
            e = (b-a)/10

            f = lambda t: m.value*t + n.value
                
            plt.plot([a-e,b+e], [f(a-e),f(b+e)])
            plt.errorbar(data[0], data[1], data[3], data[2], color = ax.lines[-1].get_color(), **plot_args)

            if not options["holdon"]:
                pass
            return m,n

        else:
            plot_args = {"marker": "o",
                        "linestyle": "-"} | plot_args
            plt.plot(v.value, self.value, **plot_args)

            if not options["holdon"]:
                pass

    def redefine(self, f, new_units = ""):
        if new_units != "":
            self.units = new_units

        self.f = f([self.sym])
        self.err_f = gauss(self.f, [self])

        # Esto no es muy elegante porque borra la dependencia anterior
        # Que en verdad no deberia de necesitarla más, pero no es bonito.
        self.variables = [self]
        self.calculate()

    def split(self):
        # Estoy creando esta función sin supervisión. No te fíes.
        return [var(self.value[i], self.err[i], self.name + f"_{i}", units = self.units) for i in range(self.value.shape[0])]
    
    def get_value(self):
        return self.value
    def get_error(self):
        return self.error


class f_var (var):
    # Para variables dependientes.
    # Realmente es la misma clase que var, solo que diferente constructor.
    def __init__ (self, f, variables, name = "", units = "", str_format = "{:.2f}", *args):
        import sympy as sp
        import random
        import string

        self.name = name
        self.units = units

        code_name = ''.join(random.choice(string.ascii_letters) for i in range(16))
        self.sym = sp.symbols(code_name)
        self.err_sym = sp.symbols(code_name + "_{err}")

        self.str_format = str_format

        self.variables = variables
        syms = [variable.sym for variable in variables]
        self.f = f(syms)
        self.err_f = gauss(self.f, self.variables)

        self.calculate()


def gauss (f, variables):
    import sympy as sp

    # Propagación de error de gauss:
    # \Delta y = \sqrt{ \sum_i \left( \frac{\partial y}{\partial x_i} \, \Delta x_i \right)^2 }
    
    g = sum([(sp.diff(f,variable.sym)*variable.err_sym)**2 for variable in variables])
    return sp.simplify(sp.sqrt(g))


def var2latex(variables):
    # Solo para variables 1-D, 2-D, y sin errores.
    for i, v in enumerate(variables):
        if v.dim == 2:
            variables = variables[:i] + v.split() + variables[i+1:]

    n = len(variables)
    template = """
\\begin{table}
    \\centering
    \\begin{tabular}"""


    template += ("{" + "".join(["c"]*n) + "}\n")
    template += "\t \\toprule\n"
    template += "\t" + " & ".join([v.name + " (" + v.units + ")" for v in variables]) + " \\\\ \n"

    template += "\t\\bottomrule \\toprule \n"

    for i in range(len(variables[-1].value)):
        template += "\t" + " & ".join([v.str_format.format(v.value[i]) for v in variables]) + " \\\\ \n"

    template += "\t \\bottomrule"

    template += """
    \\end{tabular}
\\end{table}
    """

    print(template)