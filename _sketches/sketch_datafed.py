import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

G = nx.DiGraph()
# Adding various activity pathways
G.add_path([3, 5, 4, 1, 0, 2, 7, 8, 9, 6])
G.add_path([3, 0, 6, 4, 2, 7, 1, 9, 8, 5])

fig = plt.figure(figsize=(8,6))

pos = nx.circular_layout(G)
nx.draw_networkx(G, pos=pos, with_labels=True, node_shape='s', node_color='yellow', node_size=5000,
                 labels={0:'module 1',1:'module 2',2:'module 3',3:'module 4',4:'module 5',5:'module 6',6:'module 7',7:'module 8',8:'module 9',9:'module 0'})


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

