import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

plt.rcParams["font.family"] = "Arial"


lengths = []
splits = open("data/italiae_viterbi_tract_lengths").readlines()
for line in splits:
    lengths.append(float(line))



# Create a KDE estimator
kde = gaussian_kde(lengths)

# Generate x values for the plot
x_values = np.linspace(min(lengths), max(lengths), 10000)

# Calculate the KDE values for the x values
kde_values = kde(x_values)



# Normalize
kde_values /= kde_values.sum()


# Create the KDE plot using Matplotlib
plt.plot(x_values, kde_values, label="KDE", color=color_scheme["blue"])


# Add labels and a title
plt.xlabel("Ancestral Tract Lengths",  fontsize=12)
plt.ylabel("Density",  fontsize=12)
plt.title("Distribution of Ancestral Tract Lengths", fontsize=12)

# Add gridlines
plt.grid(True, linestyle='--', alpha=0.7)

# Display the plot
plt.show()