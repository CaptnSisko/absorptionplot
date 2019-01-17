# Trevor Wong
# NCSSM Online
# Jan 5, 2019
# This script generates plots of molar absorptivity over wavelength from Gaussian log files.
# Must be run with Python 3

# import required libraries
import sys
import matplotlib.pyplot as plt # https://github.com/matplotlib/matplotlib

# show an error if used incorrectly
if len(sys.argv) < 2:
    print('Usage: python3 uvvis.py <Gaussian Log> [FWHM]')
    sys.exit()

# get the log file
log = None
try:
    log = open(sys.argv[1], 'r')
except:
    print('Unable to find log file "' + sys.argv[1] + '". Is it in your working directory?')
    sys.exit()

# get the FWHM value
fwhm = 2.0/3 # Gaussview default, in eV
try:
    fwhm = float(sys.argv[2])
except:
    print('No FWHM value specified, assuming default value of ' + str(fwhm)[:4])

# lists to store energies and intensities respectively
energies = []
intensities = []
for line in log:
    if 'Excited State  ' in line: # find and parse the excited states.
        # WARNING: this method does not work for >100 excited states.
        split = line.split(' ')
        energies.append(float(split[split.index('eV')-1]))
        intensities.append(float(line[line.index('f=')+2:line.index('f=')+8]))
log.close()

# set starting and ending energies (0.5 eV's away from smallest and biggest values)
energy_begin = energies[0] - 0.5
if energy_begin <= 0: energy_begin = 0.01
energy_end = energies[len(energies)-1] + 0.5

# decrease setp size to increase percision. 0.001 is usually small enough
step = 0.001
nsteps = int((energy_end-energy_begin)/step)+1

# define the constant k
k = 10**9/(4.33*8065.54)

# lists to store the x and y axis
x = []
y = []

# loop for each step
for i in range(0,nsteps):
    # start the absorbtion at 0
    absorption = 0
    # get the energy value of this setp
    energy = energy_begin + step*i
    # loop for each excited state energy
    for j in range(len(energies)):
        # sum the Lorentzian function of each excited state
        absorption += (1/3.14159265)*0.5*fwhm/((0.5*fwhm)**2+(energy-energies[j])**2)*k*intensities[j]
    # convert the x axix value from energy in eV to wavelength in nm
    x.append(10**7/(energy*8065.54))
    # plot the absorption on the y axis
    y.append(absorption)

# plot the absorbtion
plt.plot(x, y)
plt.title('Absorption verses Wavelength')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorption ϵ')
plt.show()
