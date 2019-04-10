# NewsSimilarity

A library written in python, that compares news articles and detects whether information was copied between them.
NewsSimilarity requires the articles to have been processed by NewsFeatures (https://github.com/fhamborg/NewsFeaturesIan) first.
After the processed articles have been exported by NewsFeatures, they can be copy and pasted into /data/ExportedFromFeatures/ 
for the analysis of information reuse.

# Types of information reuse

NewsSimilarity distinguishes between different types of information reuse:
  - Copy paste of a full article
  - Copy paste of a paragraph (a paragraph consists of 2 or more consecutive sentences)
  - Copy paste of a sentence
  - Near copy paste of a full article (at most a few words were changed)
  - Near copy paste of a paragraph
  - Near copy paste of a sentence
  - Paraphrase of a paragraph
  - Paraphrase of a sentence
  
# Getting started
 To run NewsSimilarity, simply clone the repository, run pip3 install -r requirements.txt and run the controller.py file. This will load the articles that were 
 previously processed and exported by NewsFeatures and scoring different methods of determining the information reuse against
 the humanly annotated articles. In order to change the location of the files that should be parsed, the data_path variable in the JsonParser class has to be adjusted accordingly. Similarly, to change the location of the exported file, the variable data_path in the CSVExporter class has to be changed.
 
# Methods
 The methods that are compared are:
  - Token overlap
  - Word level edit distance
  - Longest common named entity sequence
  - Named entity overlap
  - Named entity coupling
  - Greedy named entity tiling
  
# Annotations
In order for NewsSimilarity to work the annotations have to adhere to a particular schema. When using GATE for annotating, the 
schemas can be imported under language resources. The xml files for the information reuse tags currently used (copy paste of an entire article, copy paste of a paragraph, copy paste of a sentence, near copy paste of an entire article, near copy paste of a paragraph, near copy paste of a sentence, paraphrase of a paragraph, paraphrase of a sentence) can be found in /data/AnnotationSchemas. 
Annotations in the source article have 2 fields, besides the tag name, which is also the type of information reuse:
  - The type of phrase, i.e. "source phrase" in this case
  - The phrase id. Each annotation gets a unique phrase id between 0 and n-1 (n = number of annotations in article)
 Annotations in the target article have 4 fields besides the tag name, which is also the type of information reuse:
  - The type of phrase, i.e. "target phrase" in this case
  - The phrase id
  - The publisher of the source article (e.g. if BBC copied information from the New York Times, this field will contain "New York Times")
  - The source id. This is the phrase id of the corresponding phrase in the source article. It is important that these two numbers match

An example of a source and a target annotation can be found in /data/ExampleAnnotations.
In order for NewsSimilarity to work, some meta information annotations are also necessary: Headline, lead paragraph and main body of the article. An example of a meta information annotaton can be found in /data/ExampleAnnotations and the corresponding annotation schema which can be imported in GATE can be found in /data/AnnotationSchemas. 

  
  
# Comparing results
The results are exported to a csv file in /data/Similarity where they can be examined.
