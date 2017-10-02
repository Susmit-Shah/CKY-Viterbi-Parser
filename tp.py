import tree

#str = '(TOP (S (VP (VB Show) (NP (PRP me)) (NP (NP (DT the) (NNS flights)) (SBAR (WHNP (WDT that)) (S (VP (VBP accept) (NP (JJ frequent) (NN flyer) (NNS tickets)))))))) (PUNC .))'
str = '(TOP (S_VP (VB <unk>) (NP (NP* (DT the) (NN fare)) (NNS codes))) (PUNC .))'
str1 = '(TOP (S_VP (VP* (VB Show) (NP_PRP me)) (NP (NP* (NP (DT the) (NNS flights)) (PP (IN from) (NP_NNP Montreal))) (PP (TO to) (NP_NNP Chicago)))) (PUNC .))'
#(TOP (S_VP (VB <unk>) (NP (NP* (DT the) (NN fare)) (NNS codes))) (PUNC .))

t = tree.Tree.from_str(str)
# fh = open('tp.txt','w')
# fh.write(t)


def get_children(parent):
    """
    It traverses children of inout node and adds labels to list.
    :param root: Node
    :return: list
    """

    child_names = []
    for child in parent.children:
        child_names.append(child.label)
    return child_names


rules = {}
rules_key = {}
rule_count = {}
#child_names = []

root = t.root
#print "ROOT: ", root
# children = list(root.children)
# print children
#
# punc = children[1]
# dot = punc.children[0]
# print dot.children

# for child in root.children:
#     child_names.append(child.label)


# rules[root.label] = get_children(root)
# for child in root.children:
#     rules[child.label] = get_children(child)
#
# print rules

def add_rules_with_value_as_list(root):
    """
    This function takes a parent of element and adds its label to dictionary as key (type: string) and its children labels
    as value (type: list). Its follow DFS traversal
    """

    if root.children:
        rules[root.label] = get_children(root)
        for each_child in root.children:
            #rules[each_child.label] = get_children(each_child)
            add_rules_with_value_as_list(each_child)
    else:
        return


def add_rules_with_value_as_label(root):
    """
    This function takes a parent of element and adds its label to dictionary as key (type: string) and its children labels
    as value (type: list). Its follow DFS traversal
    """

    if root.children:
        childrens = get_children(root)
        s = " ".join(childrens)
        rules[root.label] = s
        for each_child in root.children:
            add_rules_with_value_as_label(each_child)
    else:
        return


def generate_key_from_rule(root):
    """
    This function takes a parent of element and adds its label to dictionary as key (type: string) and its children labels
    as value (type: list). Its follow DFS traversal
    """

    if root.children:
        childrens = get_children(root)
        s = " ".join(childrens)
        #print s

        if root.label in rule_count:
            rule_count[root.label] += 1
        else:
            rule_count[root.label] = 1

        key = root.label+'-->'+s
        print 'Rule :: ', key
        if key in rules_key:
            rules_key[key] += 1
        else:
            rules_key[key] = 1
        for each_child in root.children:
            generate_key_from_rule(each_child)
    else:
        return


def parse_and_add_rules(str_rule):

    all_rules = dict()
    rule_tree = tree.Tree.from_str(str_rule)
    # add_rules_with_value_as_label(rule_tree.root)
    generate_key_from_rule(rule_tree.root)


parse_and_add_rules(str)
parse_and_add_rules(str1)
# add_rules(t.root)
# print rules
# for rule in rules:
#     print rule, "-->", rules[rule]

# print "\n\n"
# for rule in rules_key:
#     print rule, "=", rules_key[rule]
#     print rule.split('-->')[0]
#     print rule_count[rule.split('-->')[0]], "\n"
#
# print rule_count

d = {1:{'VP': 1, 'NP':2}}

print d[1]['NP']

# if z in parse_matrix[(i, j)]:
#     print "True"
#     # d[z] = max(self.probability[z+'-->'+e+' '+f] * parse_matrix[(i,k)][e] * parse_matrix[(k,j)][f], d[z])
#     parse_matrix[(i, j)][z] = max(
#         self.probability[z + '-->' + e + ' ' + f] * parse_matrix[(i, k)][e] * parse_matrix[(k, j)][f],
#         parse_matrix[(i, j)][z])
# else:
#     print "False"
#     # d[z] = self.probability[z+'-->'+e+' '+f] * parse_matrix[(i,k)][e] * parse_matrix[(k,j)][f]
#     parse_matrix[(i, j)][z] = self.probability[z + '-->' + e + ' ' + f] * parse_matrix[(i, k)][e] * \
#                               parse_matrix[(k, j)][f]


if lab in self.reverse_lookup_dict:
    print "Found lab = ", lab, "at ", i, k, k, j
    for z in self.reverse_lookup_dict[lab]:
        print "Prob z", z, self.probability[z + '-->' + e + ' ' + f]
        # parse_matrix[(i, k)][e] * parse_matrix[(k, j)][f]
        print 'Prob ik', parse_matrix[(i, k)][e]
        print 'Prob kj', parse_matrix[(k, j)][f]
        # print 'Total ', self.probability[z+'-->'+e+' '+f] * parse_matrix[(i,k)][e] * parse_matrix[(k,j)][f]
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


                # ######################### FOr Addition #####################################
                # parse_matrix[(i, j)][z] = max(self.probability[z + '-->' + e + ' ' + f] + parse_matrix[(i, k)][e] + parse_matrix[(k, j)][f], parse_matrix[(i, j)][z])
                # p = self.probability[z + '-->' + e + ' ' + f] + parse_matrix[(i, k)][e] + parse_matrix[(k, j)][f]
                # if p > parse_matrix[(i,j)][z]:
                #     parse_matrix[(i, j)][z] = p

        else:
            print "False"
            parse_matrix[(i, j)][z] = self.probability[z + '-->' + e + ' ' + f] * parse_matrix[(i, k)][e] * \
                                      parse_matrix[(k, j)][f]
            # parse_matrix[(i, j)][z] = self.probability[z + '-->' + e + ' ' + f] + parse_matrix[(i, k)][e] + parse_matrix[(k, j)][f]
        print "===================================="
    print "Filling ij", i, j, "with ", self.reverse_lookup_dict[lab]
else:
    print "Not Found ", i, k, k, j