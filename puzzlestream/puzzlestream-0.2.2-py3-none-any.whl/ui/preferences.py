from PyQt5 import QtWidgets


class PSPreferencesWindow(QtWidgets.QMainWindow):

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setGeometry(200, 200, 600, 400)
        self.tab = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab)
        self.__config = config
        self.generalTab = QtWidgets.QWidget()
        self.generalTabLayout = QtWidgets.QGridLayout(self.generalTab)
        self.tab.addTab(self.generalTab, "General")

        self.__generalKeys = ["Test", "Test 2", "Test 3"]

        for i, key in enumerate(self.__generalKeys):
            self.addSetting(key, self.generalTabLayout, i)

    def addSetting(self, key, tabLayout, row):
        label = QtWidgets.QLabel()
        label.setText(key)
        tabLayout.addWidget(label, row, 0)

        value = self.__config[key]

        if isinstance(value, bool):
            item = QtWidgets.QCheckBox()
            item.setChecked(value)
            item.stateChanged.connect(
                lambda info, key=key: self.__edit(key, info))

        elif isinstance(value, str):
            item = QtWidgets.QLineEdit()
            item.setText(value)
            item.returnPressed.connect(
                lambda info=item, key=key: self.__edit(key, info))

        elif isinstance(value, list):
            item = QtWidgets.QComboBox()
            for i in value[1]:
                item.addItem(i)
            item.setEditable(False)
            item.setCurrentIndex(value[0])
            item.currentIndexChanged.connect(
                lambda info, key=key: self.__edit(key, info)
            )

        tabLayout.addWidget(item, row, 1)

    def __edit(self, key, info):
        if isinstance(self.__config[key], bool):
            self.__config[key] = info == 2
        elif isinstance(self.__config[key], str):
            self.__config[key] = info.displayText()
        elif isinstance(self.__config[key], list):
            value = self.__config[key]
            value[0] = info
            self.__config[key] = value
