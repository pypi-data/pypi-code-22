# -*- coding: utf-8 -*-
"""
Widget for plotting phase frequency response phi(f)

Author: Christian Muenker 2015
"""
from __future__ import print_function, division, unicode_literals, absolute_import

from ..compat import QCheckBox, QWidget, QComboBox, QHBoxLayout, QFrame


import numpy as np

import pyfda.filterbroker as fb
from pyfda.pyfda_rc import params
from pyfda.plot_widgets.plot_utils import MplWidget
from pyfda.pyfda_lib import calc_Hcomplex

# TODO: ax.clear() should not be neccessary for each replot?
# TODO: Canvas should be grey when disabled


class PlotPhi(QWidget):

    def __init__(self, parent):
        super(PlotPhi, self).__init__(parent)

        self.cmbUnitsPhi = QComboBox(self)
        units = ["rad", "rad/pi",  "deg"]
        scales = [1.,   1./ np.pi, 180./np.pi]
        for unit, scale in zip(units, scales):
            self.cmbUnitsPhi.addItem(unit, scale)
        self.cmbUnitsPhi.setObjectName("cmbUnitsA")
        self.cmbUnitsPhi.setToolTip("Set unit for phase.")
        self.cmbUnitsPhi.setCurrentIndex(0)
        self.cmbUnitsPhi.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.chkWrap = QCheckBox("Wrapped Phase", self)
        self.chkWrap.setChecked(False)
        self.chkWrap.setToolTip("Plot phase wrapped to +/- pi")
        
        layHControls = QHBoxLayout()
#        layHControls.addStretch(10)
        layHControls.addWidget(self.cmbUnitsPhi)
        layHControls.addWidget(self.chkWrap)
        layHControls.addStretch(10)
        
        # This widget encompasses all control subwidgets:
        self.frmControls = QFrame(self)
        self.frmControls.setObjectName("frmControls")
        self.frmControls.setLayout(layHControls)


        #----------------------------------------------------------------------
        # mplwidget
        #----------------------------------------------------------------------
        self.mplwidget = MplWidget(self)
        self.mplwidget.layVMainMpl.addWidget(self.frmControls)
        self.mplwidget.layVMainMpl.setContentsMargins(*params['wdg_margins'])
        self.setLayout(self.mplwidget.layVMainMpl)

        self.init_axes()

        self.draw() # initial drawing

#        #=============================================
#        # Signals & Slots
#        #=============================================
        self.chkWrap.clicked.connect(self.draw)
        self.cmbUnitsPhi.currentIndexChanged.connect(self.draw)
        self.mplwidget.mplToolbar.sigEnabled.connect(self.enable_ui)        

#------------------------------------------------------------------------------
    def init_axes(self):
        """
        Initialize and clear the axes
        """
#        self.ax = self.mplwidget.ax
        self.ax = self.mplwidget.fig.add_subplot(111)
        self.ax.clear()
        self.ax.get_xaxis().tick_bottom() # remove axis ticks on top
        self.ax.get_yaxis().tick_left() # remove axis ticks right

#------------------------------------------------------------------------------
    def calc_hf(self):
        """
        (Re-)Calculate the complex frequency response H(f)
        """
        # calculate H_cplx(W) (complex) for W = 0 ... 2 pi:
        self.W, self.H_cmplx = calc_Hcomplex(fb.fil[0], params['N_FFT'], wholeF=True)
        # replace nan and inf by finite values, otherwise np.unwrap yields
        # an array full of nans
        self.H_cmplx = np.nan_to_num(self.H_cmplx) 

#------------------------------------------------------------------------------
    def enable_ui(self):
        """
        Triggered when the toolbar is enabled or disabled
        """
        self.frmControls.setEnabled(self.mplwidget.mplToolbar.enabled)
        if self.mplwidget.mplToolbar.enabled:
            self.init_axes()
            self.draw()

#------------------------------------------------------------------------------
    def draw(self):
        """
        Main entry point: 
        Re-calculate |H(f)| and draw the figure if enabled
        """
        if self.mplwidget.mplToolbar.enabled:
            self.calc_hf()
            self.update_view()

#------------------------------------------------------------------------------
    def update_view(self):
        """
        Draw the figure with new limits, scale etc without recalculating H(f)
        """

        self.unitPhi = self.cmbUnitsPhi.currentText()

        f_S2 = fb.fil[0]['f_S'] / 2.

        #========= select frequency range to be displayed =====================
        #=== shift, scale and select: W -> F, H_cplx -> H_c
        F = self.W * f_S2 / np.pi

        if fb.fil[0]['freqSpecsRangeType'] == 'sym':
            # shift H and F by f_S/2
            H = np.fft.fftshift(self.H_cmplx)
            F -= f_S2
        elif fb.fil[0]['freqSpecsRangeType'] == 'half':
            # only use the first half of H and F
            H = self.H_cmplx[0:params['N_FFT']//2]
            F = F[0:params['N_FFT']//2]
        else: # fb.fil[0]['freqSpecsRangeType'] == 'whole'
            # use H and F as calculated
            H = self.H_cmplx

        y_str = r'$\angle H(\mathrm{e}^{\mathrm{j} \Omega})$ in '
        if self.unitPhi == 'rad':
            y_str += 'rad ' + r'$\rightarrow $'
            scale = 1.
        elif self.unitPhi == 'rad/pi':
            y_str += 'rad' + r'$ / \pi \;\rightarrow $'
            scale = 1./ np.pi
        else:
            y_str += 'deg ' + r'$\rightarrow $'
            scale = 180./np.pi
        fb.fil[0]['plt_phiLabel'] = y_str
        fb.fil[0]['plt_phiUnit'] = self.unitPhi
        
        if self.chkWrap.isChecked():
            phi_plt = np.angle(H) * scale
        else:
            phi_plt = np.unwrap(np.angle(H)) * scale

        #---------------------------------------------------------
        self.ax.clear() # need to clear, doesn't overwrite 
        line_phi, = self.ax.plot(F, phi_plt)
        #---------------------------------------------------------

        self.ax.set_title(r'Phase Frequency Response')
        self.ax.set_xlabel(fb.fil[0]['plt_fLabel'])
        self.ax.set_ylabel(y_str)
        self.ax.set_xlim(fb.fil[0]['freqSpecsRange'])

        self.redraw()
        
#------------------------------------------------------------------------------
    def redraw(self):
        """
        Redraw the canvas when e.g. the canvas size has changed
        """
        self.mplwidget.redraw()

#------------------------------------------------------------------------------

def main():
    import sys
    from ..compat import QApplication
    
    app = QApplication(sys.argv)
    mainw = PlotPhi(None)
    app.setActiveWindow(mainw) 
    mainw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
