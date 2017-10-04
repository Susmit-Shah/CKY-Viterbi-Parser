import tree
import operator
import math

class Parser:
    unique_rules_and_their_count_dict = dict()
    unique_LHS_count = dict()

    def __init__(self):
        self.all_lines = self.read_file('train.trees.pre.unk')
        self.generate_rule_count_dict()


    def print_data(self):
        for line in self.all_lines:
            print line

    def print_dict(self):
        for rule in self.unique_rules_and_their_count_dict:
            print rule, "=", self.unique_rules_and_their_count_dict[rule]

    def read_file(self, file_name):
        fh = open(file_name, 'r')
        data = fh.read()
        lines = data.strip().split('\n')
        return lines

    def get_children(self, parent):
        """
        It traverses children of inout node and adds labels to list.
        :param parent: Node
        :return: list
        """

        child_names = []
        for child in parent.children:
            child_names.append(child.label)
        return child_names

    def generate_rule_count_dict(self):
        for each_rule_str in self.all_lines:
            rule_tree = tree.Tree.from_str(each_rule_str)
            self.generate_and_add_key_from_rule(rule_tree.root)
        # str = '(TOP (S_VP (VB <unk>) (NP (NP* (DT the) (NN fare)) (NNS codes))) (PUNC .))'
        # str1 = '(TOP (S_VP (VP* (VB Show) (NP_PRP me)) (NP (NP* (NP (DT the) (NNS flights)) (PP (IN from) (NP_NNP Montreal))) (PP (TO to) (NP_NNP Chicago)))) (PUNC .))'
        # rule_tree = tree.Tree.from_str(str)
        # self.generate_and_add_key_from_rule(rule_tree.root)
        # rule_tree = tree.Tree.from_str(str1)
        # self.generate_and_add_key_from_rule(rule_tree.root)
        # str3 = '(TOP (S_VP (VP* (VB Show) (NP_PRP me)) (NP (NP* (NP (DT the) (NNS flights)) (PP (IN from) (NP_NNP Chicago))) (PP (TO to) (NP_NNP Indianapolis)))) (PUNC .))'
        # rule_tree = tree.Tree.from_str(str3)
        # self.generate_and_add_key_from_rule(rule_tree.root)

    def generate_and_add_key_from_rule(self, root):
        """
        This function takes label of parent and its children and combines them to add in the dictionary with its count.
        It follow DFS traversal for tree exploration.

        :param root: Node
        :return:
        """
        if root.children:
            childrens = self.get_children(root)
            all_child_label = " ".join(childrens)
            #print s

            if root.label in self.unique_LHS_count:
                self.unique_LHS_count[root.label] += 1
            else:
                self.unique_LHS_count[root.label] = 1

            key = root.label+'-->'+all_child_label

            if key in self.unique_rules_and_their_count_dict:
                self.unique_rules_and_their_count_dict[key] += 1
            else:
                self.unique_rules_and_their_count_dict[key] = 1

            for each_child in root.children:
                self.generate_and_add_key_from_rule(each_child)
        else:
            return


    def output1(self):
        # self.generate_rule_count_dict();
        print "Total number of rules: ", len(self.unique_rules_and_their_count_dict)
        max_rule = max(self.unique_rules_and_their_count_dict.iteritems(), key=operator.itemgetter(1))[0]
        print "Most frequent rule: ", max_rule
        print "Count of ", max_rule, " : ", \
        max(self.unique_rules_and_their_count_dict.iteritems(), key=operator.itemgetter(1))[1]


parser = Parser()
# parser.print_data()

# Call this to generate basic dictionaries
# parser.generate_rule_count_dict()

parser.output1()
