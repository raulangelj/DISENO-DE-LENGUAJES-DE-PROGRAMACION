from src.Tree.Tree import Tree


def genTree():
	tree = Tree("a*b|c*·")
	tree.create_tree()
	tree.render_tree(tree.tree)


if __name__ == "__main__":
	genTree()
