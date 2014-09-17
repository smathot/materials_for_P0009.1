# Analysis recipe

This analysis recipe accompanies the following manuscript:

Mathôt, S., et al. (in preparation). *The Pupillary Light Response Reflects Exogenous Attention and Inhibition of Return*.

Copyright 2014 Sebastiaan Mathôt
<s.mathot@cogsci.nl>
<http://www.cogsci.nl/smathot>

## License

- Analysis code is released under a [GNU General Public License 3](https://www.gnu.org/copyleft/gpl.html).
- Data is released under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

## Usage note

This analysis recipe is provided so that the original analysis can be replicated, and so that further analyses can be performed by third parties with the required expertise. However, there is some fairly heavy scripting involved, which has been written for personal use, relies on custom libraries, and is not extensively documented. Therefore, this analysis recipe is provided *as is*.

## Dependencies

- python
- numpy
- scipy
- matplotlib
- exparser (commit `#a7805ac`)
- R

## Folder structure

- `analyze.py` is the main analysis script.
- `analysis/*.py` is the Python package that contains the actual analysis scripts.
- `EDF/*.lzma` contains the original `.edf` per-participant data files as recorded by the EyeLink, compressed in `.lzma` format.

The following folders are filled with intermediate files by the analysis scripts, but are not necessary to run the analysis from scratch (and therefore not included in the repository).

- `data/` will contain the converted data files in `.asc` format.
- `output/` will contain data summaries in `.csv` format.
- `plots/png/` will contain data plots in `.png` format.
- `plots/svg/` will contain data plots in `.svg` format.
- `traces/` will contain the eye-movement sample traces in `.npy` format.

## Analysis recipe

### Convert `.edf` data to `.asc` data

The EyeLink provides `.edf` files as output. These are not easily readable, but can be converted to a text-based `.asc` format, with the utility `edf2asc`.

Command:

	edf2asc EDF/exp1/*.edf

Input:

- Raw EyeLink data in `.edf` format, stored in `EDF/*.edf`

Output:

- Raw EyeLink data in `.asc` format, stored in `data/*.asc`

### Perform full analysis

The actual analysis is performed by the script `analyze.py`, which takes various optional parameters. The commands below correspond to the analysis as reported in the manuscript. For further details, please refer to the source code of `analyze.py` and `helpers.py`. Note that this script assumes the existence of the folder `stats/exp1` to store intermediate data.

Command:

	python analyze.py @full

Output:

- Various plots in `plots/`
- Various output files in `output/`.
- Information printed to the standard output.

During the analysis, intermediate results are cached and saved in the hidden subfolder `.cache`. To run a clean analysis (i.e. without using the cache) either delete the `.cache` folder or run:

Command:

	python analyze.py @__fullPathway__ --no-cache
