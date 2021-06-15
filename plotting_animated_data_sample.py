
import matplotlib as mpl
#Para graficar los datos
import matplotlib.pyplot as plt
#Para las animaciones de las graficas
#Herramientas por si se ocupa a la hora de graficar datos
import numpy as np
# Import animation package
from matplotlib.animation import FuncAnimation


# Fermi-Dirac Distribution
#Regresa un flotante
#Esta es la función de actualización
def fermi(E: float, E_f: float, T: float) -> float:
    k_b = 8.617 * (10**-5) # eV/K
    return 1/(np.exp((E - E_f)/(k_b * T)) + 1)


# Función de animación
def animate(i):
    x = np.linspace(0, 1, 100)
    y = fermi(x, 0.5, T[i])
    #Trato de limpiar la data
    f_d.set_data([], [])
    #####
    f_d.set_data(x, y)
    f_d.set_color(colors(i))
    temp.set_text(str(int(T[i])) + ' K')
    temp.set_color(colors(i))

    

# General plot parameters
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['ytick.major.width'] = 2 

# Create figure and add axes
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)

# Temperature values
T = np.linspace(100, 1000, 10)

# Get colors from coolwarm colormap
colors = plt.get_cmap('coolwarm', 10)



# Create variable reference to plot
f_d, = ax.plot([], [], linewidth=2.5)
# Add text annotation and create variable reference
temp = ax.text(1, 1, '', ha='right', va='top', fontsize=24)




# Plot F-D data
for i in range(len(T)):
    x = np.linspace(0, 1, 100)
    y = fermi(x, 0.5, T[i])
    ax.plot(x, y, color=colors(i), linewidth=2.5)

    




# Add legend
labels = ['100 K', '200 K', '300 K', '400 K', '500 K', '600 K', 
          '700 K', '800 K', '900 K', '1000 K']
ax.legend(labels, bbox_to_anchor=(1.05, -0.1), loc='lower left', 
          frameon=False, labelspacing=0.2)


# Animation call
ani = FuncAnimation(fig=fig, func=animate, frames=range(len(T)), interval=300, repeat=True)




# Ensure the entire plot is visible
fig.tight_layout()


plt.show()