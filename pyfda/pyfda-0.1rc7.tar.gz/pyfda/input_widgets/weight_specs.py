# -*- coding: utf-8 -*-
"""
Widget for entering weight specifications

Author: Julia Beike, Christian Münker
"""
from __future__ import print_function, division, unicode_literals
import sys
import logging
logger = logging.getLogger(__name__)

from ..compat import (QtCore,
                      QWidget, QLabel, QLineEdit, QFrame, QFont, QToolButton,
                      QVBoxLayout, QHBoxLayout, QGridLayout, pyqtSignal, QEvent)

import pyfda.filterbroker as fb
from pyfda.pyfda_lib import rt_label, safe_eval
from pyfda.pyfda_qt_lib import qstyle_widget
from pyfda.pyfda_rc import params # FMT string for QLineEdit fields, e.g. '{:.3g}'


class WeightSpecs(QWidget):
    """
    Build and update widget for entering the weight
    specifications like W_SB, W_PB etc.
    """

    sigSpecsChanged = pyqtSignal()

    def __init__(self, parent):

        super(WeightSpecs, self).__init__(parent)

        self.qlabels = [] # list with references to QLabel widgets
        self.qlineedit = [] # list with references to QLineEdit widgets

        self.spec_edited = False # flag whether QLineEdit field has been edited

        self._construct_UI()

#------------------------------------------------------------------------------
    def _construct_UI(self):
        """
        Construct User Interface  
        """

        self.layGSpecs   = QGridLayout() # Sublayout for spec fields, populated
                                         # dynamically in _show_entries()
        title = "Weight Specifications"
        bfont = QFont()
        bfont.setBold(True)

        lblTitle = QLabel(self) # field for widget title
        lblTitle.setText(str(title))
        lblTitle.setFont(bfont)
        lblTitle.setWordWrap(True)

        self.butReset = QToolButton(self)
        self.butReset.setText("Reset")
        self.butReset.setToolTip("Reset weights to 1")
                
        layHTitle = QHBoxLayout()       # Layout for title and reset button
        layHTitle.addWidget(lblTitle)
        layHTitle.addWidget(self.butReset)
        
         # set the title as the first (fixed) entry in grid layout. The other
         # fields are added and hidden dynamically in _show_entries and _hide_entries()
        self.layGSpecs.addLayout(layHTitle, 0, 0, 1, 2)
        
        # This is the top level widget, encompassing the other widgets
        frmMain = QFrame(self)
        frmMain.setLayout(self.layGSpecs)

        self.layVMain = QVBoxLayout()   # Widget main vertical layout
        self.layVMain.addWidget(frmMain)
        self.layVMain.setContentsMargins(*params['wdg_margins'])

        self.setLayout(self.layVMain)

        # - Build a list from all entries in the fil_dict dictionary starting
        #   with "W" (= weight specifications of the current filter)
        # - Pass the list to setEntries which recreates the widget
        # ATTENTION: Entries need to be converted from QString to str for Py 2
        self.n_cur_labels = 0 # number of currently visible labels / qlineedits
        new_labels = [str(l) for l in fb.fil[0] if l[0] == 'W']
        self.update_UI(new_labels = new_labels)


        #----------------------------------------------------------------------
        # SIGNALS & SLOTs / EVENT FILTER
        #----------------------------------------------------------------------
        self.butReset.clicked.connect(self._reset_weights)
        #       ^ this also initializes the weight text fields
        # DYNAMIC EVENT MONITORING
        # Every time a field is edited, call self._store_entry and
        # self.load_dict. This is achieved by dynamically installing and
        # removing event filters when creating / deleting subwidgets.
        # The event filter monitors the focus of the input fields.

#------------------------------------------------------------------------------

    def eventFilter(self, source, event):
        """
        Filter all events generated by the QLineEdit widgets. Source and type
        of all events generated by monitored objects are passed to this eventFilter,
        evaluated and passed on to the next hierarchy level.

        - When a QLineEdit widget gains input focus (QEvent.FocusIn`), display
          the stored value from filter dict with full precision
        - When a key is pressed inside the text field, set the `spec_edited` flag
          to True.
        - When a QLineEdit widget loses input focus (QEvent.FocusOut`), store
          current value in linear format with full precision (only if
          `spec_edited`== True) and display the stored value in selected format
        """
        if isinstance(source, QLineEdit): # could be extended for other widgets
            if event.type() == QEvent.FocusIn:
                self.spec_edited = False
                self.load_dict()
                # store current entry in case new value can't be evaluated:
                fb.data_old = source.text()
            elif event.type() == QEvent.KeyPress:
                self.spec_edited = True # entry has been changed
                key = event.key()
                if key in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    self._store_entry(source)
                elif key == QtCore.Qt.Key_Escape: # revert changes
                    self.spec_edited = False                    
                    self.load_dict()

            elif event.type() == QEvent.FocusOut:
                self._store_entry(source)
        # Call base class method to continue normal event processing:
        return super(WeightSpecs, self).eventFilter(source, event)


#-------------------------------------------------------------
    def update_UI(self, new_labels = []):
        """
        Set labels and get corresponding values from filter dictionary.
        When number of entries has changed, the layout of subwidget is rebuilt,
        using

        - `self.qlabels`, a list with references to existing QLabel widgets,
        - `new_labels`, a list of strings from the filter_dict for the current
                  filter design
        - 'num_new_labels`, their number
        - `self.n_cur_labels`, the number of currently visible labels / qlineedit
          fields
        """
        state = new_labels[0]
        new_labels = new_labels[1:]

        num_new_labels = len(new_labels)
        if num_new_labels < self.n_cur_labels: # less new labels/qlineedit fields than before
            self._hide_entries(num_new_labels)

        elif num_new_labels > self.n_cur_labels: # more new labels, create / show new ones
            self._show_entries(num_new_labels)

        for i in range(num_new_labels):
            # Update ALL labels and corresponding values 
            self.qlabels[i].setText(rt_label(new_labels[i]))

            self.qlineedit[i].setText(str(fb.fil[0][new_labels[i]]))
            self.qlineedit[i].setObjectName(new_labels[i])  # update ID
            self.qlineedit[i].setToolTip("<span>Relative weight (importance) for approximating this band.</span>")
            qstyle_widget(self.qlineedit[i], state)

        self.n_cur_labels = num_new_labels # update number of currently visible labels
        self.load_dict() # display rounded filter dict entries

#------------------------------------------------------------------------------
    def load_dict(self):
        """
        Reload textfields from filter dictionary to update changed settings
        """
        for i in range(len(self.qlineedit)):
            weight_value = fb.fil[0][str(self.qlineedit[i].objectName())]

            if not self.qlineedit[i].hasFocus():
                # widget has no focus, round the display
                self.qlineedit[i].setText(params['FMT'].format(weight_value))
            else:
                # widget has focus, show full precision
                self.qlineedit[i].setText(str(weight_value))


#------------------------------------------------------------------------------
    def _store_entry(self, widget):
        """
        When the textfield of `widget` has been edited (`self.spec_edited` =  True),
        store the weight spec in filter dict. This is triggered by `QEvent.focusOut`
        """
        if self.spec_edited:
            w_label = str(widget.objectName())
            w_value = safe_eval(widget.text(), fb.data_old)
            fb.fil[0].update({w_label:w_value})
            self.sigSpecsChanged.emit() # -> filter_specs
            self.spec_edited = False # reset flag
        self.load_dict()
        

#-------------------------------------------------------------
    def _hide_entries(self, num_new_labels):
        """
        Hide subwidgets so that only `len_new_labels` subwidgets are visible
        """
        for i in range (num_new_labels, len(self.qlabels)):
            self.qlabels[i].hide()
            self.qlineedit[i].hide()
            

#------------------------------------------------------------------------
    def _show_entries(self, num_new_labels):
        """
        - check whether enough subwidgets (QLabel und QLineEdit) exist for the 
          the required number of `num_new_labels`: 
              - create new ones if required 
              - initialize them with dummy information
              - install eventFilter for new QLineEdit widgets so that the filter 
                  dict is updated automatically when a QLineEdit field has been 
                  edited.
        - if enough subwidgets exist already, make enough of them visible to
          show all spec fields
        """
        num_tot_labels = len(self.qlabels) # number of existing labels / qlineedit fields

        if num_tot_labels < num_new_labels: # new widgets need to be generated
            for i in range(num_tot_labels, num_new_labels):                   
                self.qlabels.append(QLabel(self))
                self.qlabels[i].setText(rt_label("dummy"))
    
                self.qlineedit.append(QLineEdit(""))
                self.qlineedit[i].setObjectName("dummy")
                self.qlineedit[i].installEventFilter(self)  # filter events

                # first entry is title and reset button
                self.layGSpecs.addWidget(self.qlabels[i],i+1,0)
                self.layGSpecs.addWidget(self.qlineedit[i],i+1,1)

        else: # make the right number of widgets visible
            for i in range(self.n_cur_labels, num_new_labels):
                self.qlabels[i].show()
                self.qlineedit[i].show()
                
#------------------------------------------------------------------------------
    def _reset_weights(self):
        """
        Reset all entries to "1.0" and store them in the filter dictionary
        """
        for i in range(len(self.qlineedit)):
            self.qlineedit[i].setText("1")

            w_label = str(self.qlineedit[i].objectName())
            fb.fil[0].update({w_label:1})

        self.load_dict()
        self.sigSpecsChanged.emit() # -> filter_specs


#------------------------------------------------------------------------------

if __name__ == '__main__':

    from ..compat import QApplication
    app = QApplication(sys.argv)
    mainw = WeightSpecs(None)

    mainw.update_UI(new_labels = ['W_SB','W_SB2','W_PB','W_PB2'])
    mainw.update_UI(new_labels = ['W_PB','W_PB2'])

    app.setActiveWindow(mainw)
    mainw.show()
    sys.exit(app.exec_())
