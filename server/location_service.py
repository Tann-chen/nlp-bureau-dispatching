import pickle
import os

global instances_location

with open("repo/4w_locations.pickle", 'rb') as f:
	instances_location = pickle.load(f)

def get_instance_location(instance_id):
	if instance_id not in instances_location.keys():
		return None
	else:
		return instances_location[instance_id]