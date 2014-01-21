__author__ = 'rogersjeffrey'

import TreeUtils
import RuleUtils
from sys import  argv
import json
rule_file_path='/Users/rogersjeffrey/PycharmProjects/NLPAssignment-2/hw2/cfg.counts'
train_data_path="/Users/rogersjeffrey/PycharmProjects/NLPAssignment-2/hw2/parse_train.dat"
modified_train_file="modified_train.dat"
(script_name)=argv
instance=TreeUtils.TreeUtils()
rule_utils=RuleUtils.RuleUtils(rule_file_path,script_name)
rule_utils.populate_count_dictionaries()
rule_utils.modify_training_data_with_rare(train_data_path,modified_train_file)

