Files 
------

1) baseline-solution (Baseline System)
It takes the path to the turker translations in the data directory as an argument. The output is the translation with the least average edit distance. Here, we used words as entities rather than characters in the string while calculating the edit distance.

2) compute-bleu (Grader)
It takes the path to LDC translations in the data directory as an argument, output of the translation system as an input, and outputs the BLEU score.

3) baseline (Baseline Skeleton)
Baseline code with the edit distance function removed which the students would have to implement

Command to Run
----------------
./baseline-solution |  ./compute-bleu 
