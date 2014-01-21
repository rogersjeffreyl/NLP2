__author__ = 'rogersjeffrey'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
"""
  This class contains the methods for  reading the parse tree in the json format
  The words at the fringe , i.e the terminals are replaced by the '_RARE_' when
  the count is less than five
"""
class  TreeUtils:
     def __init__(self):
         self.rule_dictionary={}
         self.non_terminal_dictionary={}


     def parse_tree(self,json_tree_array,word_count_hash):


             if len(json_tree_array)==3:
                # Rule of type S->YZ
                left_side = (str(json_tree_array[0]))
                left_parse_subtree=json_tree_array[1]
                right_parse_subtree=json_tree_array[2]
                first_non_terminal =str(left_parse_subtree [0])
                second_non_terminal= str(right_parse_subtree [0])

                rule_array=[left_side]
                left_result=self.parse_tree(left_parse_subtree,word_count_hash)
                right_result=self.parse_tree(right_parse_subtree,word_count_hash)
                rule_array.append(left_result)
                rule_array.append(right_result)
                return  rule_array
             elif len(json_tree_array)==2:
                 #Terminal Encountered x->"terminal"
                 left_non_terminal= str(json_tree_array[0])
                 right_terminal= str(json_tree_array[1])
                 if word_count_hash!=None:

                     if word_count_hash.has_key(right_terminal.strip()):
                        counter = word_count_hash[right_terminal.strip()]
                        # Check for the terminal count
                        if counter <5 :
                            right_terminal="_RARE_"
                     else:
                        right_terminal="_RARE_"

                 return [left_non_terminal,right_terminal]


