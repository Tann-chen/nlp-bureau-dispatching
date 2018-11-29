global label_agency_mapping

label_agency_mapping = dict()


def load_label_mapping_cfg(cfg_file):
	with open(cfg_file, 'r') as cfg:
		content = cfg.read()

	entries = content.split('\n')
	for e in entries:
		agency = e.split(',')[0]
		label = int(e.split(',')[1])
		label_agency_mapping[label] = agency
		


def get_label_mapping_val(label):
	if label not in label_agency_mapping.keys():
		return None
	else:
		return label_agency_mapping[label]



load_label_mapping_cfg('label_mapping.cfg')
