# SequenceAutocorrelation
Spot repeated motifs in sequences.
This python script performs an autocorrelation on a sequence input and produces a correlation matrix as output.
The script can be run from commandline or use as import in other projects.

# conda environment

```bash
conda create -n SequenceAutocorrelation python=3.10.12 \
    numpy=1.26.2 \
    matplotlib=3.7.1 \
    biopython=1.81 \
    scipy=1.11.4
conda activate SequenceAutocorrelation
```

# running

```bash
python3 main.py --help
```

arguments :
* -f --file <path_to_sequence_file> (path) 
* -ff --file_format <sequence_file_format> (string) 
* -ls --lower_shift <value> (integer) 
* -hs --higher_shift <value> (integer)
* -k --kernel_size <value> (integer)
* -mp --midpoint <value> (float)
* -sp --steepness <value> (float)
* -ps --plot_sigmoid
* -fs --fig_size <value> <value> (float float)

# how it works

### I/O
The script first read an input file and extract the sequence using Biopython routine.

### Autocorrelation
An autocorrelation matrix is then computed. 
This autocorrelation start from a given initial shift (`-ls`) and ends at a given shift (`-hs`). 
By default, `-ls=1` and `-hs=40`. 
If you know the length of the repeated motif you are interested in, make sure it is included between `-ls` and `-hs`.

### Convolution
For each correlation shifts, the signal is convolved using a rectangular kernel.
This is equivalent to a mobile average performed upon gliding a window of given length (`-k`).
This script has been written with nucleic acid sequences in mind. Thus, the default value is `-k=120`.
Since protein sequences are using a richer alphabet, the probability to get a correlation signal from randomness is much lower.
Thus, running the script on amino acid sequences would require some adjustment such as `-k=30`.

### Scoring
In order to translate the previously computed average sequence local identity into meaningful information, I've opted for a projection onto a scoring scale mediated by a sigmoid function.
This sigmoid function can be optimized on two parameters. First, the inflexion point tells about the location of a grey zone in the local identity axis and can be customized by adjusting `-mp`. By default, `-mp=0.5`. Second, the steepness of the sigmoid tells how rapidly the sigmoid switch from zero to one and can be customized by adjusting `-sp`. By default `-sp=20`. You can vizualize the sigmoid function used for scoring using the `-ps` argument.

If you are interested in extremely well conserved motifs in a repeated array, then you can displace the '-md' closer to 1 and `-sp` to higher value.
If you are interested in shallow repeats, then you can consider lowering `-md` down and increasing `-sp`.
If you don't know what to expect, you can let `-md=0.5` and reduce `-sp` down.
