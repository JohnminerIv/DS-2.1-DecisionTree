import numpy as np
import pandas as pd
import pydotplus


class DecisionTreeNode(object):
    def __init__(self, name, pointers=None):
        self.name = name
        if pointers is not None and type(pointers) == list():
            self.pointers = pointers
        else:
            self.pointers = list()

    def __repr__(self):
        return f'{self.name}'

    def is_leaf(self):
        """Return True if this node is a leaf (has no children)."""
        return self.pointers == []

    def is_branch(self):
        """Return True if this node is a branch (has at least one child)."""
        return self.pointers == [] and type(self.pointers) == list()

    def add_pointer(self, pointer):
        """Use this to add to a given nodes pointers list. Format as
        ('name', node)."""
        self.pointers.append(pointer)

    def height(self):
        """Return the height of this node (the number of edges on the longest
        downward path from this node to a descendant leaf node)."""
        return max([pointer[1].height() + 1 for pointer in self.pointers]) if len(self.pointers) >= 1 else 0


class DecisionTree(object):

    def __init__(self, max_depth):
        """Initialize this tree"""
        self.root = None
        self.size = 0
        self.max_depth = max_depth

    def __repr__(self):
        """Return a string representation of this tree."""
        return f'desicionTree({self.size} nodes)'

    def is_empty(self):
        """Return True if this tree is empty (has no nodes)."""
        return self.root is None

    def height(self):
        """Return the height of this tree (the number of edges on the longest
        downward path from this tree's root node to a descendant leaf node)."""
        return self.root.height()

    def show_tree(self):
        rows = [[] for i in range(self.height() + 1)]
        index = 0
        queue = []
        queue.append(self.root)
        end = 1
        while queue != []:
            node = queue.pop(0)
            rows[index].append([node, [pointer for pointer in node.pointers]])

            for pointer in node.pointers:
                queue.append(pointer[1])
            end -= 1
            if end == 0:
                index += 1
                end = len(queue)
        new_rows = []
        for row in rows:
            nodes = [i[0] for i in row]
            new_rows.append(nodes)
            pointers = [i[1] for i in row if i[1] != []]
            new_rows.append(pointers)
        return new_rows[0:-1]

    def re_order_show_index_for_dot(self, rows):
        dot_info = []
        nodes = 0
        for i in range(len(rows)):
            if i % 2 == 0:
                for j in range(len(rows[i])):
                    dot_info.append(['N', nodes, rows[i][j]])
                    nodes += 1
            else:
                seen = 0
                for j in range(len(rows[i])):
                    for p in range(len(rows[i][j])):
                        for node_line in dot_info:
                            if node_line[0] == 'N':
                                if str(node_line[2]) == str(rows[i][j][p][2]):
                                    connection = node_line[1]
                        dot_info.append(['L', connection, nodes+seen, rows[i][j][p][0]])
                        seen += 1
        dot_info_sorted = self.reorder_dot_info(dot_info)
        return dot_info_sorted


    def reorder_dot_info(self, dot_info):
        nodes = [i for i in dot_info if i[0] == 'N']
        lines = [i for i in dot_info if i[0] == 'L']
        for i in lines:
            for j in range(len(nodes)):
                if i[2] == nodes[j][1]:
                    nodes.insert(j+1, i)
        return nodes

    def create_dot_png(self, file_name):
        self.create_dot_file(file_name)
        graph = pydotplus.graph_from_dot_file(f'{file_name}.dot')
        graph.write_png(f'{file_name}.png')

    def create_dot_file(self, file_name):
        full_string = """digraph Tree {
node [shape=box] ;"""
        ending = """
}"""
        node_string = """
{node_number} [label="{node_label}"] ;"""
        connection_lines = """
{parent_node} -> {child_node} [headlabel="{label}"] ;"""
        dot_info = self.re_order_show_index_for_dot(self.show_tree())
        f = open(f"{file_name}.dot", "w")
        f.write(full_string)
        for line in dot_info:
            if line[0] == 'N':
                f.write(node_string.format(node_number=line[1], node_label=line[2]))
            else:
                f.write(connection_lines.format(parent_node=line[1], child_node=line[2], label=line[3]))
        f.write(ending)
        f.close()

    def items_level_order(self):
        """Return a level-order list of all items in this tree."""
        items = []
        if not self.is_empty():
            self._traverse_level_order_iterative(self.root, items.append)
        return items

    def _traverse_level_order_iterative(self, start_node, visit):
        """iterative level-order traversal"""
        queue = []
        queue.append(start_node)
        while queue != []:
            node = queue.pop(0)
            visit([node, [pointer for pointer in node.pointers]])

            for pointer in node.pointers:
                queue.append(pointer[1])

    def generate_json_like_structure(self, node=None, condition=None):
        if node is None:
            node = self.root
        if node.pointers != []:
            children = [self.generate_json_like_structure(node=i[1], condition=i[0]) for i in node.pointers]
            if condition:
                return {"name": str(condition)+' -> '+str(node.name), "children": children}
            return {"name": str(node.name), "children": children}
        else:
            return {"name": str(node.name)}

    def generate_json_like_structure_label(self, link=None, node=None):
        if node is None:
            node = self.root
        if node.pointers != []:
            if link is not None:
                child = [self.generate_json_like_structure_label(node=link[1])]
                return {"name": 'If '+str(link[0])+' ->', "children": child}
            children = [self.generate_json_like_structure_label(link=i) for i in node.pointers]
            return {"name": str(node.name), "children": children}
        else:
            return {"name": str(node.name)}

    def fit(self, df, target):
        """Function stub, Calculate info_gain of each column and add nodes to the
        tree."""
        self.root = DecisionTreeNode(self.max_info_gain(df, target)[1])
        self.size += 1
        self._recursive_fit(df, target, self.root)

    def _recursive_fit(self, df, target, parent_node):
        """Call from fit using a head node in order to keep adding more nodes to
        the tree"""
        s = df[parent_node.name].unique()
        for i in s:
            new_df = df[df[parent_node.name] == i].drop(columns=parent_node.name)
            gain_name = self.max_info_gain(new_df, target)
            if gain_name[0] == 0:
                final = self.conditional_prob(df, parent_node.name, target, i)
                new_node = DecisionTreeNode(final)
                self.size += 1
                parent_node.pointers.append((i, new_node, parent_node.name))
            else:
                new_node = DecisionTreeNode(gain_name[1])
                parent_node.pointers.append((i, new_node, parent_node.name))
                self.size += 1
                self._recursive_fit(new_df, target, new_node)

    def _entropy(self, p):
        """Func stub, clac entropy helper function."""
        H = np.array([-i*np.log2(i) for i in p]).sum()
        return H

    def conditional_prob(self, df, c1, c2, condition):
        """Calculate the probability of one thing given another."""
        df_new = df[df[c1] == condition][c2]
        s = df_new.unique()
        population_size = len(df_new)
        pr = {}
        for i in s:
            pr[i] = len(df[(df[c1] == condition) & (df[c2]== i)]) / population_size
        return pr

    def probability(self, df, col):
        """calculate the probability"""
        s = df[col].unique()
        pr = {}
        for i in s:
            pr[i] = len(df[df[col] == i]) / len(df[col])
        return pr

    def info_gain(self, df, feature, target):
        """Find the info gained from on colum to another"""
        # obtain the entropy of the decision
        dict_decision = dict(df[target].value_counts())
        prob_decision = [q for (p,q) in dict_decision.items()]/sum(dict_decision.values())
        entropy_decision = self._entropy(prob_decision)

        # obtain the probabilities of the feature
        dict_feature = dict(df[feature].value_counts())
        dict_prob_feature = {}
        for (p,q) in dict_feature.items():
            dict_prob_feature[p] = q/sum(dict_feature.values())

        # obtain the probability of the decision,
        # for all possible values of the feature (conditions)
        conditions = df[feature].unique()
        dict_ = {}
        for condition in conditions:
            dict_[condition] = self.conditional_prob(df, feature, target, condition)

        # Given the above metrics, calculate the information gain
        # between the feature and the decision using the formula we learned
        S = 0
        for (i,j) in dict_.items():
            prob_condition = list(dict_[i].values())
            S = S + dict_prob_feature[i]*self._entropy(prob_condition)
        return entropy_decision - S

    def max_info_gain(self, df, target, givens=None):
        """find the most info gained from a list of cols"""
        if givens is not None:
            for col, value in givens:
                df = df[df[col] == value]
                df = df.drop(columns=[col])
        info_gains = [(self.info_gain(df, column, target), column) for column in df.columns[0:-1]]
        if len(info_gains) == 0:
            return (0, 'None')
        highest = info_gains[0]
        for this_info_gain in info_gains:
            if this_info_gain[0] > highest[0]:
                highest = this_info_gain
        return highest

    def predict(self, df):
        """Given a df, predict each row's label"""
        y_pred = []
        for index, row in df.iterrows():
            y_pred.append(self.recursive_predict(row, self.root))
        return y_pred

    def recursive_predict(self, row, node):
        if node.name in list(row.keys()):
            point = row[node.name]
            for pointer in node.pointers:
                if pointer[0] == point:
                    return self.recursive_predict(row, pointer[1])
        vals = list(node.name.values())
        return list(node.name.keys())[vals.index(max(vals))]
