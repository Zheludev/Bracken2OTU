## the script takes as an input a set of bracken output files 
## and extracts the taxon name and new read count values merging them into an OTU count table
## default output will be taxa/OTUs as columns, samples as rows

## written by INZ - 11/15/22
## Stanford Unversity
## provided with no acceptance of liability or promise of functionality
## version 0.1.0


import pandas as pd
import argparse

def main(filenames_list,sum_filename,output_filename):
	
	## define varaibles
	
	##filenames_list = ['SRR5949245.bracken','SRR5950280.bracken','SRR5950313.bracken','SRR5950410.bracken','SRR5963923.bracken', 'SRR5950275.bracken', 'SRR5950308.bracken']
	##sum_filename = 'sum_test'
	##output_filename = 'test.otu'
	
	## first load one dataframe
	
	merge_df = pd.read_csv(filenames_list[0], sep='\t', header=0, usecols = ['name','new_est_reads'])
	col_name = filenames_list[0].split('.')[0]
	merge_df.rename(columns={"new_est_reads": col_name}, inplace=True)
	
	## itertively open each file and merge it to an output pandas dataframe
	
	for filename in filenames_list[1:]:
		temp_df = pd.read_csv(filename, sep='\t', header=0, usecols = ['name','new_est_reads'])
		col_name = filename.split('.')[0]
		temp_df.rename(columns={"new_est_reads": col_name}, inplace=True)
		merge_df = merge_df.merge(temp_df, how='outer', on='name').fillna(0)
	##
	
	## optionally, add together samples by user specification
	
	if (sum_filename != 'nosum'):
		sum_df = pd.read_csv(sum_filename, sep='\t', header=None, names = ['new_name','sum_string'])
		for sum_ind in range(len(sum_df.index)):
			new_name = str(sum_df.iloc[sum_ind]['new_name'])
			sum_string = sum_df.iloc[sum_ind]['sum_string']
			sum_list = sum_string.split('+')
			sum_list = [filename.split('.')[0] for filename in sum_list]
			print('creating ' + new_name + ' by summing samples ' + ', '.join(sum_list))
			merge_df['sum'] = merge_df[sum_list].sum(axis=1)
			merge_df = merge_df.drop(sum_list, axis=1)
			merge_df.rename(columns={"sum": new_name}, inplace=True)
	##
	
	## finalize output
	
	out_df = merge_df.set_index('name').T.astype('Int64')
	
	## save output OTU table
	
	out_df.to_csv(output_filename, sep="\t", index=True, index_label='samples')
	
	## output result:
	
	print('wrote ' + output_filename)
	print('with ' + str(len(out_df)) + ' samples')
	print('and ' + str(len(out_df.columns)) + ' OTUs')
##

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str, nargs="+", help='space-delim list of input bracken filenames e.g.: "SRR1.bracken SRR2.bracken"')
	parser.add_argument('-sum', type=str, default = 'nosum', help='file of two fields (tsv) $1 = name to give merged samples, $2 = sample filenames to merge ("+"" delimited) e.g. if they are from multiple lanes but the same samples e.g.: "merge_by_donor"')
	parser.add_argument('-o', type=str, default = 'merge.otu', help='output filename for OTU table e.g.: "SRRn.otu"')
	args = parser.parse_args()
	main(args.i, args.sum, args.o)
##