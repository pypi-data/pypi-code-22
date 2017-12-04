from PyQt5 import QtGui, QtWidgets


class PSOutputTextEdit(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFontFamily("monospace")
        scrollbar = self.verticalScrollBar()
        scrollbar.valueChanged.connect(self.__outputScrollbarValueChanged)
        self.textChanged.connect(self.__textChanged)
        self.setReadOnly(True)
        self.activateAutoscroll()

    def __outputScrollbarValueChanged(self, value):
        if value >= 0.95 * self.verticalScrollBar().maximum():
            self.activateAutoscroll()

    def __textChanged(self):
        if self.__autoscroll:
            self.ensureCursorVisible()

    def eventFilter(self, target, event):
        if isinstance(event, QtGui.QWheelEvent):
            self.__autoscroll = False
        return QtWidgets.QTextEdit.eventFilter(self, target, event)

    def activateAutoscroll(self):
        self.__autoscroll = True
