import tree
import bigfloat
import operator
import math

class Parser:
    unique_rules_and_their_count_dict = dict()
    unique_LHS_count = dict()
    probability = dict()
    reverse_lookup_dict = dict()
    parse_matrix = dict()
    back_pointers = dict()
    output_string = ''

    def __init__(self):
        self.all_lines = self.read_file('train.trees.pre.unk')
        self.generate_rule_count_dict()
        self.calculate_probability_of_each_rule()
        self.generate_reverse_lookup()


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

    def generate_reverse_lookup(self):

        for each_rule in self.unique_rules_and_their_count_dict:
            LHS = each_rule.split("-->")[0]
            RHS = each_rule.split("-->")[1]
            if RHS in self.reverse_lookup_dict:
                self.reverse_lookup_dict[RHS].append(LHS)
            else:
                self.reverse_lookup_dict[RHS] = []
                self.reverse_lookup_dict[RHS].append(LHS)

    def calculate_probability_of_each_rule(self):
        for each_rule in self.unique_rules_and_their_count_dict:
            #self.probability[each_rule] =float(self.unique_rules_and_their_count_dict[each_rule]) / float(self.unique_LHS_count[each_rule.split("-->")[0]])
            self.probability[each_rule] = math.log(float(self.unique_rules_and_their_count_dict[each_rule])/float(self.unique_LHS_count[each_rule.split("-->")[0]]))
            #self.probability[each_rule] = (float(self.unique_rules_and_their_count_dict[each_rule]) / float(self.unique_LHS_count[each_rule.split("-->")[0]]))
        pass

    def parse_sentence(self):

        #sentence = 'Time flies like an arrow'
        sentence = 'The flight should be eleven a.m tomorrow .'
        #sentence = 'Show me the fare .'
        sentence = sentence.split(' ')

        parse_matrix = dict()
        back_pointers = dict()

        parse_list = list()
        n = len(sentence)

        # Initialize with blank dictionaries
        for i in range(1, n+1):
            parse_matrix[(i-1, i)] = {}
            back_pointers[(i-1, i)] = {}

        for i in range(1, n+1):
            word = sentence[i-1]
            if sentence[i-1] in self.reverse_lookup_dict:
                d = {}
                all_LHS = self.reverse_lookup_dict[sentence[i-1]]
                for each_LHS in all_LHS:
                    if each_LHS in parse_matrix[(i-1, i)]:
                        p = self.probability[each_LHS+'-->'+word]
                        if p > parse_matrix[(i-1, i)][each_LHS]:
                            parse_matrix[(i-1, i)][each_LHS] = p
                            back_pointers[(i-1,i)][each_LHS] = (-1, word, word)
                            #Update backpinter here
                    else:
                        parse_matrix[(i-1, i)][each_LHS] = self.probability[each_LHS+'-->'+word]
                        back_pointers[(i-1, i)][each_LHS] = (-1, word, word)
                        # Add backpointer here

                #    d[each_LHS] = self.probability[each_LHS+'-->'+word]
                # parse_matrix[(i-1, i)] = d

                # parse_matrix[(i-1, i)] = self.reverse_lookup_dict[sentence[i-1]] wrong
            else:
                # parse_matrix[(i-1, i)] = self.reverse_lookup_dict['<unk>'] wrong
                d = {}
                all_LHS = self.reverse_lookup_dict['<unk>']
                for each_LHS in all_LHS:
                    if each_LHS in parse_matrix[(i - 1, i)]:
                        p = self.probability[each_LHS + '-->' + word]
                        if p > parse_matrix[(i - 1, i)][each_LHS]:
                            parse_matrix[(i - 1, i)][each_LHS] = p
                            back_pointers[(i - 1, i)][each_LHS] = (-1, '<unk>', '<unk>')
                            # Update backpinter here
                    else:
                        parse_matrix[(i - 1), i][each_LHS] = self.probability[each_LHS + '-->' + word]
                        back_pointers[(i - 1, i)][each_LHS] = (-1, '<unk>', '<unk>')
                        # Add backpointer here

                #     d[each_LHS] = self.probability[each_LHS+'-->'+word]
                # parse_matrix[(i - 1, i)] = d

            # parse_matrix[(i-1, i)] = sentence[i-1]
            #parse_list.append((i-1, i))
            # parse_matrix[(i - 1, i)] = {}

        for l in range(2, n+1):
            for i in range(0, n+1-l):
                j = i + l
                parse_matrix[(i,j)] = {}
                back_pointers[(i,j)] = {}

        for l in range(2, n+1):
            for i in range(0, n+1-l):
                j = i + l
                for k in range(i+1, j-1+1):
                    print "Filling ", i, j, " with ", i, k, "and", k, j
                    for e in parse_matrix[(i,k)]:
                        for f in parse_matrix[(k,j)]:
                            print e, 'is at ik', i, k
                            print f, 'is at kj', k, j
                            lab = e + ' ' + f
                            #parse_matrix[(i, j)] = lab
                            if lab in self.reverse_lookup_dict:
                                print "Found lab = ", lab, "at ", i, k, k, j
                                for z in self.reverse_lookup_dict[lab]:
                                    print "Prob z",z , self.probability[z+'-->'+e+' '+f]
                                    #parse_matrix[(i, k)][e] * parse_matrix[(k, j)][f]
                                    print 'Prob ik', parse_matrix[(i, k)][e]
                                    print 'Prob kj', parse_matrix[(k,j)][f]
                                    #print 'Total ', self.probability[z+'-->'+e+' '+f] * parse_matrix[(i,k)][e] * parse_matrix[(k,j)][f]
                                    print 'Total ', self.probability[z + '-->' + e + ' ' + f] + parse_matrix[(i, k)][e] + parse_matrix[(k, j)][f]

                                    # if z in de:
                                    #     print "True"
                                    #     de[z] = max(self.probability[z+'-->'+e+' '+f] * parse_matrix[(i,k)][e] * parse_matrix[(k,j)][f], de[z])
                                    # else:
                                    #     print "False"
                                    #     de[z] = self.probability[z+'-->'+e+' '+f] * parse_matrix[(i,k)][e] * parse_matrix[(k,j)][f]

                                    if z in parse_matrix[(i, j)]:
                                        print "True"
                                        # ######################### For Multiplication ###############################
                                        # parse_matrix[(i, j)][z] = max(self.probability[z + '-->' + e + ' ' + f] * parse_matrix[(i, k)][e] * parse_matrix[(k, j)][f], parse_matrix[(i, j)][z])
                                        p = self.probability[z + '-->' + e + ' ' + f] * parse_matrix[(i, k)][e] * \
                                            parse_matrix[(k, j)][f]
                                        if p > parse_matrix[(i, j)][z]:
                                            parse_matrix[(i, j)][z] = p
                                            back_pointers[(i, j)][z] = (k, e, f)


                                        # ######################### FOr Addition #####################################
                                        # parse_matrix[(i, j)][z] = max(self.probability[z + '-->' + e + ' ' + f] + parse_matrix[(i, k)][e] + parse_matrix[(k, j)][f], parse_matrix[(i, j)][z])
                                        # p = self.probability[z + '-->' + e + ' ' + f] + parse_matrix[(i, k)][e] + parse_matrix[(k, j)][f]
                                        # if p > parse_matrix[(i,j)][z]:
                                        #     parse_matrix[(i, j)][z] = p

                                    else:
                                        print "False"
                                        parse_matrix[(i, j)][z] = self.probability[z + '-->' + e + ' ' + f] * parse_matrix[(i, k)][e] * \
                                                                  parse_matrix[(k, j)][f]
                                        #parse_matrix[(i, j)][z] = self.probability[z + '-->' + e + ' ' + f] + parse_matrix[(i, k)][e] + parse_matrix[(k, j)][f]
                                        back_pointers[(i, j)][z] = (k, e, f)
                                    print "===================================="
                                print "Filling ij", i, j, "with ", self.reverse_lookup_dict[lab]
                            else:
                                print "Not Found ", i, k, k, j
                            print "\n"

        self.parse_matrix = parse_matrix
        self.back_pointers = back_pointers

        for k in self.parse_matrix:
            print str(k) + ' = ' + str(self.parse_matrix[k])
        print "\n\n"
        for k in self.back_pointers:
            print str(k) + ' = ' + str(self.back_pointers[k])

        print "\n\n"
        output = self.print_tree(self.back_pointers[(0,n)], 0, n, 'TOP')
        return output

    def print_tree(self, back_pointer, i, j, name):
        # print "\n"
        # print "Received Data :: ", back_pointer, i, j
        # print "Label :: ", name
        self.output_string += '(' + name + ' '
        data = back_pointer[name]
        # print "data :: ", data
        k, node1, node2 = data[0], data[1], data[2]
        if k == -1:
            # print "Final Data :: ", node1
            self.output_string += node1 + ')'
            return
        else:
            self.print_tree(self.back_pointers[(i, k)], i, k, node1)
            self.output_string += ' '
            self.print_tree(self.back_pointers[(k, j)], k, j, node2)
            self.output_string += ')'
        return self.output_string


    def output1(self):

        # self.generate_rule_count_dict();
        print "Total number of rules: ", len(self.unique_rules_and_their_count_dict)
        max_rule = max(self.unique_rules_and_their_count_dict.iteritems(), key=operator.itemgetter(1))[0]
        print "Most frequent rule: ", max_rule
        print "Count of ", max_rule," : ", max(self.unique_rules_and_their_count_dict.iteritems(), key=operator.itemgetter(1))[1]


parser = Parser()
# parser.print_data()

# Call this to generate basic dictionaries
# parser.generate_rule_count_dict()

parser.output1()
# for p in parser.unique_rules_and_their_count_dict:
#     print p, " = ", parser.unique_rules_and_their_count_dict[p]

# print "\n"
#
# for p in parser.probability:
#     print p, " = ", parser.probability[p]


print parser.parse_sentence()

