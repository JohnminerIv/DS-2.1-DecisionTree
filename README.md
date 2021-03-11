# Decision Tree
Use the app [here](https://decision-tree.dev.john-the-fourth.engineer/).

## What is a Decision Tree?
A decision tree is a decision support tool that uses a tree-like model of decisions and their possible consequences, including chance event outcomes, resource costs, and utility. It is one way to display an algorithm that only contains conditional control statements. Decision trees are commonly used in operations research, specifically in decision analysis, to help identify a strategy most likely to reach a goal, but are also a popular tool in machine learning.

## How to Use Our Python Module
To use our Python module, first add an important statement that reads "from decisiontree import *" so that you can use any parts of the module. Next, import a dataset and modify it such that the "target" values are the last column. Then, create a Decision Tree and fit the data to the tree using ".fit". After, you may use a for loop to display the tree row by row. However, this visual isn't the easiest to read and we highly reccommend you use the web app when trying to actually visualize the tree.

## How to Use Our App
Visit the web application with the link in the first section. Scroll to the bottom and use the upload feature to upload a dataset ending in ".csv" that has the "target" values as the last column. The visualization will either be a static image or an interactive visualization depending on which upload feature you used. For the interactive visualization, the nodes are expandable and collapsable so be sure to examine each node to see the entire visualization.

## Built With
* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Heroku](https://devcenter.heroku.com/) - Used to deploy to production
* [Bootstrap](https://getbootstrap.com/) - Used to style web app
* [scikit-learn](https://scikit-learn.org/) - Used various parts to build visualization

## Authors
* **Subal Pant** - [soundreaper](https://github.com/soundreaper)
* **John Miner** - [JohnminerIv](https://github.com/JohnminerIv)