import matplotlib.backends.backend_qt5agg as mplAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets

from puzzlestream.backend.stream import PSStream


class PSPlotView(QtWidgets.QMainWindow):

    def __init__(self, manager, puzzleItem, parent=None, numberOfViewers=1):
        super().__init__(parent)
        self.__viewers = []
        self.__viewerWindows = []
        self.__manager = manager
        self.__config = manager.config
        self.__puzzleItem = puzzleItem
        self.__autotile = self.__config["autotilePlots"]
        self.__createGUI(numberOfViewers)

        if puzzleItem is None:
            self.setWindowTitle("Plot view - complete stream")
        else:
            self.setWindowTitle("Plot view - " + str(puzzleItem))
        self.show()

    def __createGUI(self, numberOfViewers=1):
        self.mdi = QtWidgets.QMdiArea()
        self.setCentralWidget(self.mdi)

        self.toolbar = QtWidgets.QToolBar()
        addAction = self.toolbar.addAction("Add viewer")
        tileAction = self.toolbar.addAction("Tile windows")

        tileChkBox = QtWidgets.QCheckBox("auto tile")
        tileChkBox.setChecked(self.__config["autotilePlots"])
        tileChkBox.stateChanged.connect(self.__autotileChanged)
        self.toolbar.addWidget(tileChkBox)

        addAction.triggered.connect(self.__addViewer)
        tileAction.triggered.connect(self.mdi.tileSubWindows)
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        for i in range(numberOfViewers):
            self.__addViewer()

    def __addViewer(self):
        viewer = PSSinglePlotView(self.__manager, self.__puzzleItem, self)
        window = QtWidgets.QMdiSubWindow()
        window.setWidget(viewer)
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.__viewers.append(viewer)
        self.__viewerWindows.append(window)
        self.mdi.addSubWindow(window)
        window.show()

        if self.__autotile:
            self.mdi.tileSubWindows()

    def __autotileChanged(self, state):
        self.__autotile = state == 2

    def updatePlots(self):
        for viewer in self.__viewers:
            viewer.updatePlots()

    def closeEvent(self, event):
        self.__config["autotilePlots"] = self.__autotile
        self.setParent(None)
        event.accept()


class PSSinglePlotView(QtWidgets.QWidget):

    def __init__(self, manager, puzzleItem=None, parent=None):
        super().__init__(parent)
        self.__manager = manager
        self.__stream = manager.stream
        self.__modules = manager.scene.modules
        self.__puzzleItem = puzzleItem

        if puzzleItem is None:
            self.__data = self.__stream
        else:
            self.__data = puzzleItem.streamSection.data

        self.__parent = parent
        self.box = QtWidgets.QGridLayout()
        self.setLayout(self.box)
        self.__plots = []

        self.combo = QtWidgets.QComboBox()
        self.combo.currentIndexChanged.connect(self.__selectionChanged)
        self.box.addWidget(self.combo, 0, 0)

        self.canvas, self.mpltoolbar = None, None
        self.updatePlots()

    def __translateKeyToUser(self, key):
        if isinstance(self.__data, PSStream):
            ID = key.split("-")[0]
            return key.replace(ID + "-", self.__modules[int(ID)].name + ": ")
        return key

    def __translateKeyToInternal(self, key):
        if key in self.__retranslatedKeys:
            return self.__retranslatedKeys[key]

    def updatePlots(self):
        plotList = []

        for key in self.__data:
            if isinstance(self.__data[key], Figure):
                plotList.append((key, self.__data[key]))

        self.__retranslatedKeys = {self.__translateKeyToUser(item[0]): item[0]
                                   for item in plotList}

        self.__plots = sorted(plotList, key=lambda x: x[0])
        self.combo.clear()
        for plot in self.__plots:
            self.combo.addItem(self.__translateKeyToUser(plot[0]))
        self.__setFigure()

    def __setFigure(self, index=0):
        if self.canvas is not None:
            self.canvas.hide()
            self.mpltoolbar.hide()
            self.box.removeWidget(self.canvas)
            self.box.removeWidget(self.mpltoolbar)
            del self.canvas
            del self.mpltoolbar

        if len(self.__plots) > 0:
            fig = self.__plots[index][1]
            self.canvas = mplAgg.FigureCanvasQTAgg(fig)
            self.canvas.setParent(self.__parent)
            self.box.addWidget(self.canvas, 1, 0)

            self.mpltoolbar = mplAgg.NavigationToolbar2QT(self.canvas,
                                                          self.__parent)
            self.box.addWidget(self.mpltoolbar, 2, 0)

    def __selectionChanged(self):
        self.__setFigure(self.combo.currentIndex())
