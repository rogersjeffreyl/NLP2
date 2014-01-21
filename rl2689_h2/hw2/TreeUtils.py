__author__ = 'rogersjeffrey'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
class  TreeUtils:
     def __init__(self):
         self.rule_dictionary={}
         self.non_terminal_dictionary={}

     def update_non_terminal_dictonary(self,non_terminal):
         if self.non_terminal_dictionary.has_key(non_terminal):
            count=self.non_terminal_dictionary[non_terminal]
            self.non_terminal_dictionary[non_terminal]=count+1
         else:
            self.non_terminal_dictionary.update({non_terminal:1})


     def update_rule_dictionary(self,rule_tuple):
          if self.rule_dictionary.has_key(rule_tuple):
               count=self.rule_dictionary[rule_tuple]
               self.rule_dictionary[rule_tuple]=count+1
          else:
               self.rule_dictionary.update({rule_tuple:1})

          if len(rule_tuple)==3:
             self.update_non_terminal_dictonary(rule_tuple[0])
             self.update_non_terminal_dictonary(rule_tuple[1])
             self.update_non_terminal_dictonary(rule_tuple[2])
          else:
              self.update_non_terminal_dictonary(rule_tuple[0])

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
                    if counter <5 :
                        right_terminal="_RARE_"
                 else:
                    right_terminal="_RARE_"

             return [left_non_terminal,right_terminal]


