# labelling_tool
This is the repository storing manual for video labelling tool.

## Installation

### Windows
- Download Anaconda 3.7 python [here](https://www.anaconda.com/products/individual#windows).
- Install Anaconda by following [these](https://docs.anaconda.com/anaconda/install/windows/) instructions.
- Create environment by executing `conda env create --name labelling_tool --file=environment_creation_file.yml` in command line when located in cloned repo directory.
- Launch Spyder from Anaconda when in activated labelling_tool environment.
- Execute script `vid_labeller.py` from Spyder.   


### Ubuntu
- Download Anaconda 3.7 python [here](https://www.anaconda.com/products/individual#linux).
- Install Anaconda by following [these](https://docs.anaconda.com/anaconda/install/linux/) instructions.
- Create environment by executing `conda env create --name labelling_tool --file=environment_creation_file.yml` in command line when located in cloned repo directory.
- Launch Spyder from Anaconda when in activated labelling_tool environment.
- Execute script `vid_labeller.py` from Spyder. 

## Labelling
- Input root directory of videos, ex. `C:\\Users\\klavs\\Desktop\\emo2018videos` for Windows ir `/home/icv/Desktop/emo2018videos` for Linux systems.
- Input unlabelled subject name ex. 1334, 1337, ... , 1338. List of labeled subjects can be seen [here]().
- For each video make on framestamp at start of emotion and one stamp and the end of emotion.
Each video contains emotion, if multiple emotions take first emotion start stop, if no visible emotion then..., etcetcetcetc.
- tralalalal