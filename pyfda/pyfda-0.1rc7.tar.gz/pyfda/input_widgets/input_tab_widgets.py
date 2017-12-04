# -*- coding: utf-8 -*-
"""
Tabbed container with all input widgets

Author: Christian Münker
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys
import logging
logger = logging.getLogger(__name__)

from ..compat import QTabWidget, QWidget, QVBoxLayout, QScrollArea, pyqtSignal

SCROLL = True

from pyfda.pyfda_rc import params
from pyfda.pyfda_lib import mod_version

from pyfda.input_widgets import (filter_specs, file_io, filter_coeffs,
                                filter_info, filter_pz)

if mod_version("myhdl"):
    from pyfda.hdl_generation import hdl_specs
    HAS_MYHDL = True
else:
    HAS_MYHDL = False


class InputTabWidgets(QWidget):
    """
    Create a tabbed widget for various input subwidgets
    """
    # class variables (shared between instances if more than one exists)
    sigViewChanged = pyqtSignal() # emitted when view (e.g. single / double sided f) has changed
    sigSpecsChanged = pyqtSignal()  # emitted when specs have been changed
    sigFilterDesigned = pyqtSignal()  # emitted when filter has been designed


    def __init__(self, parent):
        
        super(InputTabWidgets, self).__init__(parent)

        self.filter_specs = filter_specs.FilterSpecs(self)
        self.filter_specs.setObjectName("filter_specs")

        self.file_io = file_io.File_IO(self)
        self.file_io.setObjectName("inputFiles")
        self.filter_coeffs = filter_coeffs.FilterCoeffs(self)
        self.filter_coeffs.setObjectName("filter_coeffs")
        self.filter_pz = filter_pz.FilterPZ(self)
        self.filter_pz.setObjectName("filter_pz")
        self.filter_info = filter_info.FilterInfo(self)
        self.filter_info.setObjectName("filter_info")

        if HAS_MYHDL:
            self.hdlSpecs = hdl_specs.HDLSpecs(self)

        self._construct_UI()


    def _construct_UI(self):
        """ Initialize UI with tabbed input widgets """
        tabWidget = QTabWidget(self)
        tabWidget.setObjectName("input_tabs")

        tabWidget.addTab(self.filter_specs, 'Specs')
        tabWidget.setTabToolTip(0, "Enter and view filter specifications.")
        tabWidget.addTab(self.filter_coeffs, 'b,a')
        tabWidget.setTabToolTip(1, "Display and edit filter coefficients.")
        tabWidget.addTab(self.filter_pz, 'P/Z')
        tabWidget.setTabToolTip(2, "Display and edit filter poles and zeros.")
        tabWidget.addTab(self.file_io, 'Files')
        tabWidget.setTabToolTip(3, "Import and export filter designs and coefficients.")
        tabWidget.addTab(self.filter_info, 'Info')
        tabWidget.setTabToolTip(4, "<span>Display the achieved filter specifications"
                                   " and more info about the filter design algorithm.</span>")        
        if HAS_MYHDL:
            tabWidget.addTab(self.hdlSpecs, 'HDL')

        layVMain = QVBoxLayout()

        #setContentsMargins -> number of pixels between frame window border
        layVMain.setContentsMargins(*params['wdg_margins']) 

#--------------------------------------
        if SCROLL:
            scroll = QScrollArea(self)
            scroll.setWidget(tabWidget)
            scroll.setWidgetResizable(True) # Size of monitored widget is allowed to grow:

            layVMain.addWidget(scroll)
        else:
            layVMain.addWidget(tabWidget) # add the tabWidget directly

        self.setLayout(layVMain) # set the main layout of the window


        #----------------------------------------------------------------------
        # SIGNALS & SLOTs
        #----------------------------------------------------------------------
        # Collect "specs changed" / "filter designed" signals from all input
        # widgets and route them to plot / input widgets that need to be updated
        #
        # Check:
        #http://www.pythoncentral.io/pysidepyqt-tutorial-creating-your-own-signals-and-slots/#custom-tab-2-pyqt
        #
        # sigSpecsChanged: signal indicating that filter SPECS have changed,
        #       requiring update of some plot widgets and input widgets:
        self.filter_specs.sigSpecsChanged.connect(self.update_specs)
        # sigViewChanged: signal indicating that PLOT VIEW has changed,
        #       requiring update of some plot widgets only:
        self.filter_specs.sigViewChanged.connect(self.update_view)
        #
        # sigFilterDesigned: signal indicating that filter has been DESIGNED,
        #       requiring update of all plot and some input widgets:
        self.filter_specs.sigFilterDesigned.connect(self.update_all)
        self.filter_coeffs.sigFilterDesigned.connect(self.update_all)
        self.filter_pz.sigFilterDesigned.connect(self.update_all)

        # The following three widgets require a reloading of the select_filter
        # widget to update the filter selection:
        self.filter_coeffs.sigFilterDesigned.connect(self.load_all)
        self.filter_pz.sigFilterDesigned.connect(self.load_all)
        self.file_io.sigFilterLoaded.connect(self.load_all)
        #----------------------------------------------------------------------

    def update_view(self):
        """
        Slot for InputSpecs.sigViewChanged

        Propagate new PLOT VIEW (e.g. log scale) to plot widgets via pyfda.py

        Update plot widgets via sigSpecsChanged signal that need new
            specs, e.g. plotHf widget for the filter regions
        """
        self.filter_info.load_dict() # update frequency unit of info widget
        logger.debug("Emit sigViewChanged!")
        self.sigViewChanged.emit() # pyFDA -> PlotTabWidgets.update_specs


    def update_specs(self):
        """
        Slot for FilterSpecs.sigSpecsChanged

        Propagate new filter SPECS from filter dict to other input widgets and
        to plot widgets via pyfda.py

        - Update input widgets that can / need to display specs (except inputSpecs
             - the origin of the signal !!)
        - Update plot widgets via sigSpecsChanged signal that need new
            specs, e.g. plotHf widget for the filter regions
        """

        self.filter_specs.color_design_button("changed")
        self.filter_info.load_dict()
        if HAS_MYHDL:
            self.hdlSpecs.update_UI()
        logger.debug("Emit sigSpecsChanged!")
        self.sigSpecsChanged.emit() # pyFDA -> PlotTabWidgets.update_specs

    def load_all(self):
        """
        Called when a new filter has been LOADED:
        Pass new filter data from the global filter dict
        - Specifically call SelectFilter.load_dict
        - Update the input widgets that can / need to display filter data
        - Update all plot widgets via the signal sigFilterDesigned
        """
        self.filter_specs.color_design_button("ok")
        self.filter_specs.sel_fil.load_dict() # update select_filter widget
        self.update_all()


    def update_all(self):
        """
        Slot for sigFilterDesigned from InputSpecs, FilterCoeffs, FilterPZ

        Called when a new filter has been DESIGNED:
        - Pass new filter data from the global filter dict
        - Update the input widgets that can / need to display filter data
        - Update all plot widgets via the signal sigFilterDesigned

        """
        sender_name = ""
        if self.sender(): # origin of signal that triggered the slot
            sender_name = self.sender().objectName()
        logger.debug("updateAll called by %s", sender_name)

        self.filter_specs.load_dict()
        self.filter_info.load_dict()
        self.filter_coeffs.load_dict()
        self.filter_pz.load_dict()

        logger.debug("Emit sigFilterDesigned!")
        self.sigFilterDesigned.emit() # pyFDA -> PlotTabWidgets.update_data


#------------------------------------------------------------------------

def main():
    from pyfda import pyfda_rc as rc
    from ..compat import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(rc.css_rc)

    mainw = InputTabWidgets(None)
    app.setActiveWindow(mainw)
    mainw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
