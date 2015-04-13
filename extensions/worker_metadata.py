import optparse
from collections import Counter

workerInfo = {};

def worker_data(workerID, workerMetadata):
	workerInfo[workerID] = (workerMetadata)
	pass

def native_speaker(workerID,n):
	if workerID in workerInfo :
		# is a native speaker
		if workerInfo[workerID][n] == 'YES':
			languageFlag= 1; 
		else:
			languageFlag = 0;

		#experience 
		if workerInfo[workerID][n+4] != 'UNKNOWN':
			numYears = workerInfo[workerID][n+4];
		else:
			numYears = 0;

	else:
		languageFlag = 0;
		numYears = 0;
	
	return (languageFlag, numYears);

def worker_location(workerID):
	if workerID in workerInfo:
		#is in PAKISTAN?
		if workerInfo[workerID][3] != 'UNKNOWN':
			inPak = 1;
		else:
			inPak = 0;

		#is in INDIA?
		if workerInfo[workerID][2] != 'UNKNOWN':
			inIndia = 1;
		else:
			inIndia = 0;
	return (inPak, inIndia);
	
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


#print all_workers[0]
#print "Hyp:{0}, ID:{1}".format(all_hyps[1][5], all_hyps[1][9])

for worker in all_workers:
	worker_data(worker[0], worker[1:])


for hyp in all_hyps[1:]:
	isNativeUrdu=[];
	isNativeEnglish=[];
	numYearsUrdu =[];
	numYearsEnglish =[];
	inIndia =[];
	inPak =[];

	for index in xrange(9,13):
		#Urdu 
		(isNativeSpeaker, numYears) = native_speaker(hyp[index],1)
		isNativeUrdu.append(isNativeSpeaker);
		numYearsUrdu.append(numYears);


		#English
		(isNativeSpeaker,numYears) = native_speaker(hyp[index],0);
		isNativeEnglish.append(isNativeSpeaker);
		numYearsEnglish.append(numYears);

		#Location of Turker
		(pak, india) = worker_location(hyp[index]);
		inIndia.append(india);
		inPak.append(pak);
	
	





	


