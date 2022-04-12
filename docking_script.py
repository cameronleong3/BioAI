#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:49:50 2022

@author: cameronleong
"""

from vina import Vina
ligand_base = 'maybridge_fragment_'
protein = '2kid.pdbqt'


def dock_ligand(ligand_name):
	print("starting...\n")
	print("Protein: "+protein)
	print("ligand: "+ligand_name)
	v = Vina(sf_name='vina')

	v.set_receptor(protein)

	v.set_ligand_from_file(ligand_name)
	v.compute_vina_maps(center=[0,0,0], box_size=[100, 100, 100])#center = [15.190, 53.903, 16.917], box_size=[20, 20, 20]
	#v.compute_vina_maps(center=[0,0,0], box_size=[100, 100, 100])#center = [15.190, 53.903, 16.917], box_size=[20, 20, 20])



	print("\n\nscore:")
	print(v.score(),"\n")
	print("score after optimization")
	print(v.optimize())
	print("\n\n")
	#Score the current pose
	energy = v.score()


	print('Score before minimization: %.3f (kcal/mol)' % energy[0])

	# Minimized locally the current pose
	energy_minimized = v.optimize()
	print('Score after minimization : %.3f (kcal/mol)' % energy_minimized[0])
	v.write_pose('ex_minimized.pdbqt', overwrite=True)
	file_object.write("ligand: "+ligand_name+"\tscore: "+str(energy_minimized[7])+"\n")
	# Dock the ligand
	v.dock(exhaustiveness=32, n_poses=10)
	v.write_poses('ex_out.pdbqt', n_poses=5, overwrite=True)
	print(v.energies(n_poses = 10))

file_object = open('scores.txt','a')

dock_ligand("actarit.pdbqt")
"""
for i in range(3):
	ligand = ligand_base+str(i)+'.pdbqt'
	dock_ligand(ligand)
	print("DONE")
file_object.close()
"""


"""
#v.write_poses('actarit_out.pdbqt', energy_range = 0)

#optimized scores

actarit: 		0 	0 	0 	0 	0 	.217 	 	0 	 	.217
fragment_0: 	0 	0 	0 	0 	0 	0 		 	0 	 	0
fragment_1: 	0 	0 	0 	0 	0 	189.107  	0 		189.107

"""
