def next_valid_line(f):
	while True:
		ln = f.readline()
		if len(ln) == 0:
			return ""
		if len(ln.strip()) == 0:
			continue
		if ln.strip().startswith("*"):
			continue
		if len(ln.split()) != 3:
			continue
		return ln.strip()

def extract_vals(ln):
	return list(map(float, ln.split()))

if __name__ == "__main__":
	import sys
	
	if len(sys.argv) < 4:
		print("Usage:", sys.argv[0], "FRD_FILENAME DIFFRACTION_FILENAME OUTPUT_FILENAME")
		sys.exit(-1)

	in_frd = open(sys.argv[1], "rt")
	in_diffract = open(sys.argv[2], "rt")
	out_frd = open(sys.argv[3], "wt")
	
	#
	# here's what we're going to do:
	# we read each entry from the input FRD file, then find out how many DB we need to add/subtract
	# from this measurement, according to the nearest frequency we read from the baffle diffraction
	# file. since the frequencies of the files are not always going to match, we always save two
	# frequency values, the two nearest frequencies we can find to the original one
	#
	
	prev_freq_diffract = 0
	prev_db_diffract = 0
	next_freq_diffract = 0
	next_db_diffract = 0

	df_line = next_valid_line(in_diffract)
	[next_freq_diffract, next_db_diffract, bogus] = extract_vals(df_line)

	while True:
		frd_line = next_valid_line(in_frd)
		if len(frd_line) == 0:
			break

		[freq, db, phase] = extract_vals(frd_line)

		# read the diffraction file until we find two frequencies that wrap the current one
		while next_freq_diffract < freq:
			df_line = next_valid_line(in_diffract)
			if len(df_line) == 0:
				break
			prev_freq_diffract = next_freq_diffract
			prev_db_diffract = next_db_diffract
			[next_freq_diffract, next_db_diffract, bogus] = extract_vals(df_line)

		db += next_db_diffract
		out_frd.write("\t".join(list(map(str, [freq, db, phase]))) + "\n")
	
	out_frd.close()
	in_frd.close()
	in_diffract.close()
