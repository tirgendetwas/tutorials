import csv
import numpy as np
import matplotlib.pyplot as plt


def outfile_to_data(filename):
    csv_file = open(filename, "r")

    csv_reader = csv.reader(csv_file, delimiter=',')

    uu = []
    dtdt = []
    for row in csv_reader:
        print(row)
        u, dt = row[0].split(";")

        uu.append(u)
        dtdt.append(dt)

    u_values = np.array(uu, dtype=float)
    dt_values = np.array(dtdt, dtype=float)


    def unzip(iterable):
        return zip(*iterable)


    paired = list(zip(u_values, dt_values))
    paired.sort(key=lambda x: x[1])
    print(paired)
    return [u for u, _ in paired], [dt for _, dt in paired]


u_values, dt_values = outfile_to_data("wr11_out.txt")

reference_value = u_values[0]

errors = np.abs(u_values - reference_value)

u_values = np.array(u_values)
dt_values = np.array(dt_values)

plt.loglog(dt_values, errors, '.', label='newmark')

u_values, dt_values = outfile_to_data("wr52_lin_out.txt")

errors = np.abs(u_values - reference_value)

u_values = np.array(u_values)
dt_values = np.array(dt_values)

plt.loglog(dt_values[1:], errors[1:], '1', label='wr52_lin')

u_values, dt_values = outfile_to_data("wr52_quad_out.txt")

errors = np.abs(u_values - reference_value)

u_values = np.array(u_values)
dt_values = np.array(dt_values)

plt.loglog(dt_values[1:], errors[1:], '2', label='wr52_quad')


plt.loglog(dt_values[1:], errors[1]/dt_values[1]*dt_values[1:], '--', label='O(h^1)')
plt.loglog(dt_values[1:], errors[1]/dt_values[1]**2*dt_values[1:]**2, ':', label='O(h^2)')
plt.legend()
plt.show()


