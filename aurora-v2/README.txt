AURORA: Auditing PageRank on Large Graphs
# Overview
This is a Python implementation for the family of AURORA algorithm (AURORA-E, AURORA-N, AURORA-S). The package contains the following files:
-- aurora_e.py: a code file for python implementation of AURORA-E algorithm
-- aurora_n.py: a code file for python implementation of AURORA-N algorithm
-- aurora_s.py: a code file for python implementation of AURORA-S algorithm
-- demo.py: a demo code file to run the family of AURORA algorithm on the provided dataset
-- GrQc.txt: preprocessed CA-GrQc graph
-- load_data.py: a code file for functions to load datasets
-- utils.py: a code file for helper functions


# Prerequisites
The following packages are needed to run the code in Python 3
-- networkx
-- scipy


# Usage
Please refer to the demo code file demo.py and the descriptions in each file for the detailed information. 
The code can be only used for academic purpose and please kindly cite our published paper if you are interested in our work.


# Reference
Kang, Jian, Meijia Wang, Nan Cao, Yinglong Xia, Wei Fan, and Hanghang Tong. "AURORA: Auditing PageRank on Large Graphs." In 2018 IEEE International Conference on Big Data (Big Data), pp. 713-722. IEEE, 2018.
@inproceedings{kang2018aurora,
  title={AURORA: Auditing PageRank on Large Graphs},
  author={Kang, Jian and Wang, Meijia and Cao, Nan and Xia, Yinglong and Fan, Wei and Tong, Hanghang},
  booktitle={2018 IEEE International Conference on Big Data (Big Data)},
  pages={713--722},
  year={2018},
  organization={IEEE}
}

# Notes
In this version of release (version 2), we have fixed some bugs and made several improvements over the conference paper version, including baseline bruteforce, baseline degree and the evaluation steps in aurora.
