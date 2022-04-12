#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:49:50 2022

@author: cameronleong
"""

from vina import Vina
ligand_base = 'maybridge_fragment_'
protein = '2kid.pdbqt'
v = Vina(sf_name='vina')
#files that contain errors and can't be simulated
errors = [3,9,11,12,14,60,65,72,101,109,112,115,124,177,202,218,234,248,260,266]
scores_file = open('scores.txt','w')
import time

def score_ligand(ligand_name):
	#print("setting receptor_____")
	v.set_receptor(protein)
	#print("setting ligand________")
	v.set_ligand_from_file(ligand_name)
	#print("computing vina maps________")
	v.compute_vina_maps(center=[0,0,0], box_size=[100, 100, 100])
	#print("optimizing energy________")
	energy_minimized = v.optimize()
	#print("writing scores to file________")
	scores_file.write("fragment "+str(i)+"\tscore: "+str(energy_minimized[7])+"\n")
	#v.write_pose('ex_minimized.pdbqt', overwrite=True)

def dock_ligand(ligand_name):
	#print("docking_________")
	v.dock(exhaustiveness=32, n_poses=10)
	print("Protein: "+protein)
	print("ligand: "+ligand)
	#v.write_poses('ex_out.pdbqt', n_poses=5, overwrite=True)
	#print(v.energies(n_poses = 10))




#main


#can go through 269 maybridge fragments
for i in range(1,4):
	print("START\n\n\n")
	while i in errors:
		i += 1
	ligand = ligand_base+str(i)+'.pdbqt'
	energy_score = score_ligand(ligand)
	#dock_ligand(ligand)
	print("____________________________________________")

#close files
scores_file.close()



