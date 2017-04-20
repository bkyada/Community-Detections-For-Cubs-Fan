# Project Title
Community Detection for Cubs Fan

## Goal
Find common communities between friends of Chicago cubs fan’s. Do sentiment Analysis to get views of people on Cubs(Chicago Baseball Team). 

### Prerequisites 
What things you need to install
```
Python 2.7
```
```
TwitterAPI
```
```
Numpy
```

### Data Resource 
```
Twitter
```
### Process
* Collect Data
* Processing Data 
* Clustering
* Classify Data
* Sentiment Analysis

### Files
* collect.py: This file collects data used in analysis. This is submitting queries to Twitter API. This is a raw data.
* cluster.py: This file read the data collected in the previous steps and use community detection algorithm to cluster users into communities. 
* classify.py: This file classify data(tweets) into positive and negative.
* summarize.py: This file read the output of the previous methods to write a textfile called summary.txt.

### Data
The pickle file here store the data after filter and processing. You can get the result directly from the pickle file.


