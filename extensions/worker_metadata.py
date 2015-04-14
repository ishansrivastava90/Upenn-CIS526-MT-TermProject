import optparse
from collections import Counter


optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/translations.tsv", help="Turk translations")
optparser.add_option("-r", "--ref", dest="reference", default="data/survey.tsv", help="Worker metadeta file")
#sentence index: ID index
#5:9
#6:10
#7:11
#8:12

(opts, _) = optparser.parse_args()

all_hyps = [line.strip().split('\t')[1:] for line in open(opts.input)][:10]
all_workers = [line.strip().split('\t') for line in  open(opts.reference)][1:]
#all_workers = [line.replace('YES', 1) for line in  open(opts.reference)][1:]
#print all_workers[1]



#print all_workers[0]
#print "Hyp:{0}, ID:{1}".format(all_hyps[1][5], all_hyps[1][9])
workerInfo = {};

for worker in all_workers[0:5]:
	workerData =[0]*6
	workerID = worker[0];
	for (i,metadata) in enumerate(worker[1:4]):
		print i
		if metadata == 'YES':
			workerData[i] = 1;
		else:
			workerData[i] = 0;
	for (i, metadata) in enumerate(worker[5:]):
		if metadata =='UNKNOWN':
			workerData[i+4] = 0;
		else:
			workerData[i+4] = metadata;

	workerInfo[workerID] = workerData;

for hyp in all_hyps[1:]:
	isNativeUrdu=[];
	isNativeEnglish=[];
	numYearsUrdu =[];
	numYearsEnglish =[];
	inIndia =[];
	inPak =[];

	for index in xrange(9,13):
		 
		if hyp[index] in workerInfo:

			isNativeUrdu.append(workerInfo[hyp[index]][1]);
			numYearsUrdu.append(workerInfo[hyp[index]][5]);
			inPak.append(workerInfo[hyp[index]][3]);

			isNativeEnglish.append(workerInfo[hyp[index]][0]);
			numYearsEnglish.append(workerInfo[hyp[index]][4]);	
			inIndia.append(workerInfo[hyp[index]][2]);



	





	


