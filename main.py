import sys
import math
import random
import pyqtgraph as pg
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui

class GraphWidget(QtWidgets.QWidget):
    '''
    The GraphWidget Class implements Qt framework for the interface and 
    pyqtgraph for creating charts 
    '''
    def __init__(self):
        super().__init__()

        # dictionary for the pmf, and pdf distributions
        self.recipe =  [{
                'name': 'exponential distribution',
                'elem': ['lambda'],
                'type': 'continuous',
                'func': self.exponential
            },{
                'name': 'poisson distribution',
                'elem': ['lambda'],
                'type': 'discrete',
                'func': self.poisson
            }
            ]

        self.inputs = ['lambda']

        # initialize QtWidgets you need
        self.combo = QtWidgets.QComboBox()
        self.button = QtWidgets.QPushButton('Show Graph')
        self.clear = QtWidgets.QPushButton('Clear Graph')
        self.xlabel = QtWidgets.QLabel('x', alignment = QtCore.Qt.AlignCenter)
        self.xtext = QtWidgets.QLineEdit(self, '0.0')
        self.gridLayout = QtWidgets.QGridLayout()
        self.window = pg.plot()

        # add the widgets to the layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.xlabel)
        self.layout.addWidget(self.xtext)
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.window)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.clear)

        # add distribution names to the combobox
        for r in self.recipe:
            self.combo.addItem(r['name'])

        # initialize the inputs or parameters widgets and hide
        for inp in enumerate(self.inputs):
            label = QtWidgets.QLabel(inp[1], alignment = QtCore.Qt.AlignCenter)
            text = QtWidgets.QLineEdit(self, '0.0')
            if inp[0]!= 0:
                label.hide()
                text.hide()
            self.inpwidgets[inp[1]] = {
                'label':label,
                'text': text
            }
            self.gridLayout.addWidget(label, *(inp[0], 0))
            self.gridLayout.addWidget(text, *(inp[0], 1))

        # preload the parameter widgets
        self.changePDF()

        # attach function to buttons
        self.button.clicked.connect(self.compute)
        self.clear.clicked.connect(self.reset)
        self.combo.currentIndexChanged.connect(self.changePDF)

    # for loading parameters based on the recipe
    def changePDF(self):
        for i in self.recipe[self.combo.currentIndex()]['elem']:
            self.inpwidgets[i]['label'].show()
            self.inpwidgets[i]['text'].show()
        return

    # for loading the functions of the distributions
    def compute(self):
        vars = dict()
        f = self.recipe[self.combo.currentIndex()]['type']
        if f == 'discrete':
            vars['x'] = np.arange(0, int(self.xtext.text()), 1)
        else:
            vars['x'] = np.linspace(0.0, int(self.xtext.text()))
        for i in self.recipe[self.combo.currentIndex()]['elem']:
            vars[i] = float(self.inpwidgets[i]['text'].text())
        y = self.recipe[self.combo.currentIndex()]['func'](vars)

        self.plot(vars['x'], y, f)

    # exponential pdf
    def exponential(self, vars):
        print(vars['lambda'], vars['x'])
        y = vars['lambda']* np.exp(-vars['lambda']*vars['x'])
        return y

    # poisson pmf
    def poisson(self, vars):
        p = []
        print(vars['lambda'], vars['x'])
        for i in vars['x']:
            x = int(i)
            p.append((np.exp(-vars['lambda'])*(vars['lambda']*x))/np.math.factorial(x))
        return p
    
    # for plotting the distributions to pyqtgraph
    def plot(self, x, y, f):
        pen = pg.mkPen(color = (255, 0, 0), width=3)
        if f == 'discrete':
            bargraph = pg.BarGraphItem(x = x, height = y, width = 0.7, brush = 'b')
            self.window.addItem(bargraph)
        else:
            # plotgraph = pg.PlotItem(x, y, pen=pen)
            # self.window.addItem(plotgraph)
            self.window.plot(x, y, pen=pen)
        
        self.window.showGrid(x=True, y=True)

    # clear graph
    def reset(self):
        self.window.clear()

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = GraphWidget()
    widget.resize(800, 600)

    widget.show()

    sys.exit(app.exec())