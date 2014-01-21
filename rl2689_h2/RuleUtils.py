__author__ = 'rogersjeffrey'
import logging
import json
import TreeUtils
from decimal import *
import pprint

"""
  This class contains the utility methods  that read the rules count file and populate the various count dictionaries

"""
class RuleUtils:



    tag_names = ('NONTERMINAL', 'UNARYRULE', 'BINARYRULE')

    def __init__(self, count_file, log_file):

        self.count_file = count_file
        self.word_count_dictionary = {}
        self.nonterminal_count_dictionary={}
        self.binary_rules_dictionary={}
        self.unary_rules_dictionary={}
        self.cky_dp_table={}
        self.bp_dp_table={}
        self.logger = log_file[:-3]
        self.last_index_of_input=0
        self.sentence="test sentence"
        #logging.basicConfig(format='%(asctime)s %(message)s', filename=log_file + '.log', level=logging.DEBUG)


    """
      Update the counts of the words that occur in the fringe of the tree

    """

    def  update_word_count_dict(self,word,rule_count):

         if self.word_count_dictionary.has_key(word):

            count = int(self.word_count_dictionary[word])

            self.word_count_dictionary[word]=count+rule_count
         else:
             self.word_count_dictionary.update({word:rule_count})


   #This method reads the counts file and populates the appropriate rule  dictionaries(unary,binary)
    def populate_count_dictionaries(self):

        with open(self.count_file) as f:
            for line in f:
                if line.strip():
                    rule_lists = line.split(" ")
                    rule_type = rule_lists[1].strip()
                    if rule_type == RuleUtils.tag_names[0]:
                        non_terminal = rule_lists[2].strip()
                        non_terminal_count=int(rule_lists[0].strip())
                        self.nonterminal_count_dictionary.update({non_terminal:non_terminal_count})
                    elif rule_type == RuleUtils.tag_names[1]:
                         rule_count=int(rule_lists[0].strip())
                         terminal_word=rule_lists[3].strip()
                         non_terminal=rule_lists[2]
                         if terminal_word  in self.unary_rules_dictionary:
                            self.unary_rules_dictionary[terminal_word][non_terminal]=rule_count
                         else:
                            self.unary_rules_dictionary[terminal_word]={}
                            self.unary_rules_dictionary[terminal_word][non_terminal]=rule_count
                         self.update_word_count_dict(terminal_word,rule_count)

                    elif rule_type == RuleUtils.tag_names[2]:
                         rule_count=int(rule_lists[0].strip())
                         left_non_terminal=rule_lists[2].strip()
                         first_non_terminal=rule_lists[3].strip()
                         second_non_terminal=rule_lists[4].strip()
                         if left_non_terminal not in self.binary_rules_dictionary:
                            self.binary_rules_dictionary[left_non_terminal]={}
                         if first_non_terminal not in self.binary_rules_dictionary[left_non_terminal]:
                            self.binary_rules_dictionary[left_non_terminal][first_non_terminal]={}

                         self.binary_rules_dictionary[left_non_terminal][first_non_terminal][second_non_terminal]=rule_count


        f.close()
    #Modifies the training json with the words whose count is lesser than 5 with _RARE_
    def modify_training_data_with_rare(self, training_file,modified_train_file):

        modified_json_file=open(modified_train_file, 'w')
        tree_utils_instance=TreeUtils.TreeUtils()
        with open(training_file) as training_data:
            for line in training_data:
                if line.strip():
                    tree = json.loads(line)
                    new_tree=tree_utils_instance.parse_tree(tree,self.word_count_dictionary)
                    json.dump(new_tree,modified_json_file)
                    modified_json_file.write("\n")
                else:
                    print line,

        training_data.close()
        modified_json_file.close()

    # calculated the maximum likelihood for a binary rule
    def calculate_mle_for_binary_rule(self,x,y,z):
         mle=float(0)
         if x in self.binary_rules_dictionary:
            rules_for_x=self.binary_rules_dictionary[x]
            if y in rules_for_x:
               rules_with_y=self.binary_rules_dictionary[x][y]
               if  z in rules_with_y:
                   mle=float(self.binary_rules_dictionary[x][y][z] )/float(self.nonterminal_count_dictionary[x])
         return mle

    # Calculates the mle for  rule
    def calculate_mle_for_unary_rule(self,x,terminal):
        derivation_count=0
        if terminal in self.unary_rules_dictionary:
           if x in self.unary_rules_dictionary[terminal]:
              derivation_count = self.unary_rules_dictionary[terminal][x]
           else:
               derivation_count = 0
        else:
            if x in self.unary_rules_dictionary["_RARE_"]:
              derivation_count = self.unary_rules_dictionary["_RARE_"][x]
        return float(derivation_count) / float(self.nonterminal_count_dictionary[x])


    # Cky dynamic programming algorithm that  calculates the max probability parse tree for a input sentence
    # THis also stores the arg max and the  split pointers

    def cky(self,input_sentence):
        self.cky_dp_table={}
        self.bp_dp_table={}
        self.sentence=input_sentence
        input_sentence_words=input_sentence.split()
        #initialize cky
        length=len(input_sentence_words)
        #print length
        last_index=length-1
        self.last_index_of_input=last_index
        for i in range(0,length):

                for key in self.nonterminal_count_dictionary:
                    word=input_sentence_words[i].strip()
                    new_word=word
                    self.cky_dp_table[i,i,key]=self.calculate_mle_for_unary_rule(key,word)

        #Continue CKY
        for l in range(0,last_index):
            for i in range(0,last_index-l):
                j=i+l+1
                for key in self.binary_rules_dictionary:
                    max_pi_value_for_nt=-1
                    max_z_val=""
                    max_y_val=""
                    max_split=0
                    all_rules_for_x=self.binary_rules_dictionary[key]
                    for y in  all_rules_for_x.keys():
                        for z in all_rules_for_x[y].keys():
                            mle=self.calculate_mle_for_binary_rule(key,y,z)
                            for split in range(i,j):
                                left_split_pi=0
                                right_split_pi=0
                                if (i,split,y) in self.cky_dp_table and (split+1,j,z) in self.cky_dp_table:
                                   left_split_pi=self.cky_dp_table[(i,split,y)]
                                   right_split_pi=self.cky_dp_table[(split+1,j,z)]
                                   pi_value = mle*left_split_pi*right_split_pi
                                else:
                                   pi_value=float(0)

                                if pi_value>max_pi_value_for_nt:
                                   max_pi_value_for_nt=pi_value
                                   max_split=split
                                   max_y_val=y
                                   max_z_val=z
                    self.cky_dp_table[i,j,key]=max_pi_value_for_nt
                    self.bp_dp_table[i,j,key]=max_y_val,max_z_val,max_split

        max_nt="S"

        # If the pi value for 'S' is zero then  choose a different non terminal for which pi(1,n,NT)
        if self.cky_dp_table[1,last_index,max_nt]==0:

           max_pi=0.0

           for non_terminal in self.nonterminal_count_dictionary:

               curr_pi=0.0
               if (0,last_index,non_terminal)not in self.cky_dp_table:
                  continue
               else:
                  curr_pi=self.cky_dp_table[0,last_index,non_terminal]
               if curr_pi>max_pi:
                  max_pi=curr_pi
                  max_nt=non_terminal

        #print max_nt
        tree=self.get_back_pointer(0,last_index,max_nt)
        return tree

    # Method to traverse the back pointer list and returns the  tree with the  max probability
    def get_back_pointer(self,left,right,non_terminal):

         words=self.sentence.split()
         #print self.sentence
         if left==right:
            return '["'+non_terminal+'", "' + words[left]+'"]'
         else:
            backpointer_value = self.bp_dp_table[left,right,non_terminal]
            return '["'+non_terminal+'", '+ self.get_back_pointer(left,backpointer_value[2],backpointer_value[0]) + ", " + self.get_back_pointer(backpointer_value[2]+1,right,backpointer_value[1]) + "]"


