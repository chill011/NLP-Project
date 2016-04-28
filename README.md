# NLP-Project
Creating Dictionary (Word sense disambiguation)
This project seeks to create a dictionary from raw text. Your system should take as input some number of instances of a given target word, and should automatically cluster those instances into groups, where each member of a group is using the target word with the same meaning. Once clusters are formed, your system should generate a definition from the contents of each cluster, and your system should also select one instance from each cluster to serve as an example of that meaning or sense. Your system should be unsupervised, meaning that it does not use any pre-labeled training examples to learn how to cluster those instances. You should withhold all knowledge of the correct senses in your Senseval-2 data until evaluation. 

During Stage 1 your goal will be to develop a baseline system. This means a system that satisfies all the requirements of the project, but does so in a straightforward yet reasonable way. Your Stage 1 system must produce clusters, definitions, and examples. Your Stage 2 system will then seek to improve upon those results.

To summarize then, your system should take N instances of a target word and produce each of the following: 

1) K clusters, where each cluster corresponds to a sense. The value of K must be determined automatically. 

2) An automatically written definition for each cluster. This definition should be a complete sentence/s, and should not simply be copied from the instances. 

3) The instance from within each cluster/sense that best illustrates the meaning of the sense. 

The input to your system should be in Senseval-2 format. The clusters output by your system should also be in SenseEval-2 format, and scored by the SenseClusters scorer. The definitions created by your system should be found in a plain text file, along with a selected example for each sense. You should create a single definition example file for each word (which should contain all the senses of that word). 

Your system should only use the N instances plus (optionally) other raw untagged training text in arriving at a solution. Please do not refer to existing dictionaries, the WWW, or other online resources as a part of your solution.If you do use additional untagged text in your system, it must not be dependent on the target words you are processing, rather it should be a generic corpus of untagged text that could apply to any word your system might be processing. 

As a part of this project each team member will create data that can be used to develop and evaluate your system. 
