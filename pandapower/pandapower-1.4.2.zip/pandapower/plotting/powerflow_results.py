# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017 by University of Kassel and Fraunhofer Institute for Wind Energy and
# Energy System Technology (IWES), Kassel. All rights reserved. Use of this source code is governed
# by a BSD-style license that can be found in the LICENSE file.

import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import pandapower.topology as top


def plot_voltage_profile(net, plot_transformers=True, ax=None, xlabel="Distance from Slack [km]",
                         ylabel="Voltage [pu]", x0=0, trafocolor="r", bus_colors=None,
                         line_loading_weight=False, voltage_column=None, bus_size=3, **kwargs):
    if ax is None:
        plt.figure(facecolor="white", dpi=120)
        ax = plt.gca()
    if not net.converged:
        raise ValueError("no results in this pandapower network")
    if voltage_column is None:
        voltage_column = net.res_bus.vm_pu
    for eg in net.ext_grid[net.ext_grid.in_service == True].bus:
        d = top.calc_distance_to_bus(net, eg)
        for lix, line in net.line[net.line.in_service == True].iterrows():
            if line.from_bus not in d.index:
                continue
            if not ((net.switch.element == line.name) & ~net.switch.closed & (
                        net.switch.et == 'l')).any():
                from_bus = line.from_bus
                to_bus = line.to_bus
                x = [x0 + d.at[from_bus], x0 + d.at[to_bus]]
                try:
                    y = [voltage_column.at[from_bus], voltage_column.at[to_bus]]
                except:
                    raise UserWarning
                if "linewidth" in kwargs or not line_loading_weight:
                    ax.plot(x, y, **kwargs)
                else:
                    ax.plot(x, y, linewidth=0.4 * np.sqrt(net.res_line.loading_percent.at[lix]),
                            **kwargs)
                if bus_colors is not None:
                    for bus, x, y in zip((from_bus, to_bus), x, y):
                        if bus in bus_colors:
                            ax.plot(x, y, 'or', color=bus_colors[bus], ms=bus_size)
                kwargs = {k: v for k, v in kwargs.items() if not k == "label"}
        # if plot_transformers:
        #     if hasattr(plot_transformers, "__iter__"):  # if is a list for example
        #         transformers = net.trafo.loc[list(plot_transformers)]
        #     else:
        #         transformers = net.trafo[net.trafo.in_service == True]
        #     for _, transformer in transformers.iterrows():
        #         if transformer.hv_bus not in d.index:
        #             continue
        #         ax.plot([x0 + d.loc[transformer.hv_bus],
        #                  x0 + d.loc[transformer.lv_bus]],
        #                 [voltage_column.loc[transformer.hv_bus],
        #                  voltage_column.loc[transformer.lv_bus]], color=trafocolor,
        #                 **{k: v for k, v in kwargs.items() if not k == "color"})

        # trafo geodata
        if plot_transformers:
            for trafo_table in ['trafo', 'trafo3w']:
                if trafo_table not in net.keys():
                    continue
                transformers = net[trafo_table].query('in_service')
                for tid, tr in transformers.iterrows():
                    t_buses = [tr[b_col] for b_col in ('lv_bus', 'mv_bus', 'hv_bus') if
                               b_col in tr.index]
                    if any([b not in d.index.values or b not in net.res_bus.index.values for b in
                            t_buses]):
                        # logger.info('cannot add trafo %d to plot' % tid)
                        continue

                    for bi, bj in combinations(t_buses, 2):
                        tr_coords = ([x0 + d.loc[bi], x0 + d.loc[bj]],
                                     [net.res_bus.at[bi, 'vm_pu'], net.res_bus.at[bj, 'vm_pu']])
                        ax.plot(*tr_coords, color=trafocolor,
                                **{k: v for k, v in kwargs.items() if not k == "color"})

        if xlabel:
            ax.set_xlabel(xlabel, fontweight="bold", color=(.4, .4, .4))
        if ylabel:
            ax.set_ylabel(ylabel, fontweight="bold", color=(.4, .4, .4))
    return ax


def plot_loading(net, element="line", boxcolor="b", mediancolor="r", whiskercolor="k", ax=None):
    if ax is None:
        plt.figure(facecolor="white", dpi=80)
        ax = plt.gca()
    loadings = net["res_%s" % element].loading_percent.values
    boxplot = ax.boxplot(loadings[~np.isnan(loadings)], whis="range")
    for l in list(boxplot.keys()):
        plt.setp(boxplot[l], lw=3)
        if l == "medians":
            plt.setp(boxplot[l], color=mediancolor)
        elif l == "boxes" or l == "whiskers":
            plt.setp(boxplot[l], color=boxcolor)
        else:
            plt.setp(boxplot[l], color=whiskercolor)


if __name__ == "__main__":
    import pandapower as pp
    import pandapower.networks as nw

    net = nw.create_cigre_network_mv()
    pp.runpp(net)
    plot_voltage_profile(net, line_loading_weight=True)
    plot_loading(net)
    plt.show()
