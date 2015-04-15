default.py : Default system. It takes the path to the turker translations in the data directory as an argument. The output is the first turker translation.
python default.py  > default.out

compute-bleu.py and bleu.py : Objective function. It takes the path to LDC translations in the data directory as an argument, output of the translation system as an input, and outputs the BLEU score.
python compute-bleu < default.out
