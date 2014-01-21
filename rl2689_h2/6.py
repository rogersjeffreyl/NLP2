__author__ = 'rogersjeffrey'
"""
  This program invokes the cky algorithm  and  returns a max probability parse tree for  a sentence passed as input
  it takes in as input the following parameters

  1) counts file modified after replacing the words with count <5 with _RARE_
  2) Development data having the sentences
  3) Output file:File containing the tree for the sentences in dev data  , in the json format

  to run this code:

  python 5.py <modified_counts_file_path> <dev_data_path> <tree_file_for_dev_data>

"""

import RuleUtils
import TreeUtils
from sys import  argv

(script_name,modified_rule_counts_path,dev_data_path,dev_output_file)=argv
#Create instance of tree utils
instance=TreeUtils.TreeUtils()
rule_utils=RuleUtils.RuleUtils(modified_rule_counts_path,script_name)
rule_utils.populate_count_dictionaries()
modified_dev_file=open(dev_output_file, 'w')

#Iterating through all sentences in the development file
with open(dev_data_path) as sentences:
   for sentence in sentences:
     # Invoking cky for the  sentence
     new_tree=rule_utils.cky(sentence)
     #writing to the output file
     modified_dev_file.write(new_tree+"\n")

sentences.close()
modified_dev_file.close()