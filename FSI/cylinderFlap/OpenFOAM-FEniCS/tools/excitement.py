from __future__ import division

import argparse
import numpy as np
import precice_future as precice

omega_excitement = 4

# beam geometry
L = 0.35  # length
H = 0.02  # height
y_bottom = 0.2 - 0.5 * H  # y coordinate of bottom surface of beam
y_top = y_bottom + H  # y coordinate of top surface of beam
x_left = 0.25  # x coordinate of left surface of beam
x_right = x_left + L  # x coordinate of right surface of beam
x_attack = x_right
y_attack = .5 * (y_bottom + y_top)


def compute_force(time, force_excitement):
    omega = omega_excitement
    force_0 = force_excitement
    return force_0 * np.sin(omega * time)


parser = argparse.ArgumentParser()
parser.add_argument("--wr-tag", "-wr", help="wr tag", choices=["11", "52"], default="11", type=str)

try:
    args = parser.parse_args()
except SystemExit:
    print("")
    print("Usage: python ./solverdummy precice-config participant-name mesh-name")
    quit()

configuration_file_name = "tools/precice-config_wr{wr_tag}.xml".format(wr_tag=args.wr_tag)
participant_name = "Excitement"
mesh_name = "Excitement-Mesh"

n_vertices = 1

solver_process_index = 0
solver_process_size = 1

interface = precice.Interface(participant_name, solver_process_index, solver_process_size)
interface.configure(configuration_file_name)

mesh_id = interface.get_mesh_id(mesh_name)

dimensions = interface.get_dimensions()
force_excitement = np.zeros((n_vertices, dimensions))
force_excitement[:, 0] = 0
force_excitement[:, 1] = 10

vertices = np.zeros((n_vertices, dimensions))
vertices[:, 0] = x_attack
vertices[:, 1] = y_attack

vertex_ids = interface.set_mesh_vertices(mesh_id, vertices)

dt = interface.initialize()
t = 0

if interface.is_action_required(precice.action_write_initial_data()):
    forces = compute_force(t + dt, force_excitement)
    interface.write_block_vector_data(write_data_id, vertex_ids, forces)
    interface.fulfilled_action(precice.action_write_initial_data())

interface.initialize_data()

while interface.is_coupling_ongoing():

    if interface.is_action_required(precice.action_write_iteration_checkpoint()):
        print("DUMMY: Writing iteration checkpoint")
        interface.fulfilled_action(precice.action_write_iteration_checkpoint())

    if args.wr_tag == "11":
        forces = compute_force(t+dt, force_excitement)
        print("sending forces: {}".format(forces))
        interface.write_block_vector_data(interface.get_data_id("Forces1", mesh_id), vertex_ids, forces)
    elif args.wr_tag == "52":
        forces = compute_force(t+.5 * dt, force_excitement)
        print("sending forces: {}".format(forces))
        interface.write_block_vector_data(interface.get_data_id("Forces1", mesh_id), vertex_ids, forces)

        forces = compute_force(t+dt, force_excitement)
        print("sending forces: {}".format(forces))
        interface.write_block_vector_data(interface.get_data_id("Forces2", mesh_id), vertex_ids, forces)

    dt = interface.advance(dt)

    if interface.is_action_required(precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.fulfilled_action(precice.action_read_iteration_checkpoint())
    else:
        t += dt
        print("DUMMY: Advancing in time")

interface.finalize()
print("DUMMY: Closing python solver dummy...")

