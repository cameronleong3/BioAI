# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:49:50 2022

@author: cameronleong
"""
import time
import sys
import os
from vina import Vina
db_choice = int(input("Which library?\n[1] Maybridge General Fragments\n[2] Maybridge Screening Fragments\n[3] Life Chemicals\n"))


#Depending on which database chosen, choose the correct fragment names,
# library size, scores file, and list of error files
if 	db_choice == 1:
	ligand_base = 'maybridge_fragment_'
	print("You chose Maybridge")
	lib_size = 269
	scores_file = open('Maybridge_scores.txt','w')
	errors = [3,9,11,12,14,60,65,72,101,109,112,115,
	124,177,202,218,234,248,260,266]

elif db_choice == 2:
	ligand_base = "newMaybridge_fragment_"
	print("You chose the new Maybridge library")
	lib_size = 400
	scores_file = open('new_Maybridge_scores.txt','w')
	errors = []
	#errors = [305,391,396,403,495,496,503,590,598,665,671]

elif db_choice == 3:
	ligand_base = "LC_fragment_"
	print("You chose the Life Chemicals library")
	lib_size = 500
	scores_file = open('LC_scores.txt','w')
	errors = []
	"""
	errors = [3,4,9,19,20,21,22,24,25,26,27,28,49,66,
	148,193,194,201,205,208,209,211,212,213,214,215,216,217,
	235,334,343,345,347,348,349,364,446]
	"""
else:
	print("invalid option\n")
	sys.exit()



protein = '2kid.pdbqt'
v = Vina(sf_name='vina')
#files that contain errors and can't be simulated

log_file = open('log.txt','w')
import time

def score_ligand(ligand_name,idx):
	print("setting receptor_____")
	v.set_receptor(protein)
	print("setting ligand_______")
	v.set_ligand_from_file(ligand_name)
	v.compute_vina_maps(center=[0,0,0], box_size=[100, 100, 100])
	energy_minimized = v.optimize()
	scores_file.write("fragment "+str(idx)+"\tscore: "+str(energy_minimized[7])+"\n")
	print("fragment "+str(idx)+"\tenergy score: "+str(energy_minimized[7])+"\n")
	return energy_minimized[7]

def dock_ligand(ligand_name):
	print("docking_function__________", flush = True)
	v.dock(exhaustiveness=32, n_poses=20) #increased num of poses


#can go through 269 maybridge fragments
def loop(min, max):
	#go through all fragments that don't have errors and score them.
	#If the energy score > 0, simulate docking with sortase A
	for i in range(min,max):
		if i in errors:
			continue
		print("START\n\n\n")
		ligand = ligand_base+str(i)+'.pdbqt'
		file_size = os.path.getsize(ligand)
		if file_size == 0:
			print("empty file...\n")
			print(i)
			continue
		print("Ligand: "+ligand+"\n")
		energy_score = score_ligand(ligand,i)
		if energy_score <= 0: #only docks if energy > 0
			print("energy score is zero, not docking...")
			continue
		dock_ligand(ligand)
		print("____________________________________________")

if int(db_choice) == 2:
	start = 300
else:
	start = 0

end = start + lib_size

loop(start,end)
scores_file.close()
sys.exit()



