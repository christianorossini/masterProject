import os
import pydotplus
from IPython.display import Image

pyPath = os.path.dirname(os.path.abspath(__file__))
path = "{0}/dt/escolhidos".format(pyPath)

files = ['gc']  
for filename in files:
    dotPath = "{0}/{1}.dot".format(path, filename)
    graph = pydotplus.graph_from_dot_file(dotPath)
    graph.write_png("{0}/{1}.png".format(path, filename))
    Image(graph.create_png())