# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017 by University of Kassel and Fraunhofer Institute for Wind Energy and
# Energy System Technology (IWES), Kassel. All rights reserved. Use of this source code is governed
# by a BSD-style license that can be found in the LICENSE file.



import copy
import pandas as pd
import numpy as np

try:
    import pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)

import pandapower.topology as top
from pandapower.run import runpp
from pandapower.diagnostic_reports import diagnostic_report
from pandapower.toolbox import get_connected_elements
from pandapower.powerflow import LoadflowNotConverged

# separator between log messages
log_message_sep = ("\n --------\n")


def diagnostic(net, report_style='detailed', warnings_only=False, return_result_dict=True,
               overload_scaling_factor=0.001, lines_min_length_km=0, lines_min_z_ohm=0,
               nom_voltage_tolerance=0.3, numba_tolerance=1e-5):
    """
    Tool for diagnosis of pandapower networks. Identifies possible reasons for non converging loadflows.

    INPUT:
     **net** (pandapowerNet) : pandapower network

    OPTIONAL:
     - **report_style** (string, 'detailed') : style of the report, that gets ouput in the console

      'detailled': full report with high level of additional descriptions

      'compact'  : more compact report, containing essential information only

      'None'     : no report


     - **warnings_only** (boolean, False): Filters logging output for warnings

      True: logging output for errors only

      False: logging output for all checks, regardless if errors were found or not


     - **return_result_dict** (boolean, True): returns a dictionary containing all check results

      True: returns dict with all check results

      False: no result dict

     - **overload_scaling_factor** (float, 0.001): downscaling factor for loads and generation \
     for overload check

     - **lines_min_length_km** (float, 0): minimum length_km allowed for lines

     - **lines_min_z_ohm** (float, 0): minimum z_ohm allowed for lines

     - **nom_voltage_tolerance** (float, 0.3): highest allowed relative deviation between nominal \
     voltages and bus voltages

    OUTPUT:
     - **diag_results** (dict): dict that contains the indeces of all elements where errors were found

      Format: {'check_name': check_results}

    EXAMPLE:

    <<< pandapower.diagnostic(net, report_style='compact', warnings_only=True)

    """
    diag_functions = ["missing_bus_indeces(net)",
                      "disconnected_elements(net)",
                      "different_voltage_levels_connected(net)",
                      "lines_with_impedance_close_to_zero(net, lines_min_length_km, lines_min_z_ohm)",
                      "nominal_voltages_dont_match(net, nom_voltage_tolerance)",
                      "invalid_values(net)",
                      "overload(net, overload_scaling_factor)",
                      "wrong_switch_configuration(net)",
                      "multiple_voltage_controlling_elements_per_bus(net)",
                      "no_ext_grid(net)",
                      "wrong_reference_system(net)",
                      "deviation_from_std_type(net)",
                      "numba_comparison(net, numba_tolerance)",
                      "parallel_switches(net)"]
    bus_index_dependent_checks = ["disconnected_elements(net)",
                                  "different_voltage_levels_connected(net)",
                                  "nominal_voltages_dont_match(net, nom_voltage_tolerance)",
                                  "multiple_voltage_controlling_elements_per_bus(net)"]
    invalid_value_dependent_checks = ["wrong_reference_system(net)"]

    diag_results = {}
    for diag_function in diag_functions:
        if (diag_function in bus_index_dependent_checks) and ("missing_bus_indeces" in diag_results.keys()):
            diag_result = "check skipped"
        elif 'invalid_values' in diag_results.keys():
            if (diag_function in invalid_value_dependent_checks) and (set(['gen', 'load', 'sgen'])
                                                                      & set(diag_results['invalid_values'].keys())):
                diag_result = "check skipped"
            else:
                diag_result = eval(diag_function)
                if diag_result:
                    diag_results[diag_function.split("(")[0]] = diag_result
        else:
            diag_result = eval(diag_function)
            if diag_result:
                diag_results[diag_function.split("(")[0]] = diag_result

    diag_params = {
        "overload_scaling_factor": overload_scaling_factor,
        "lines_min_length_km": lines_min_length_km,
        "lines_min_z_ohm": lines_min_z_ohm,
        "nom_voltage_tolerance": nom_voltage_tolerance,
        "numba_tolerance": numba_tolerance
    }
    if warnings_only:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)
    logger.propagate = False

    if report_style == 'detailed':
        diagnostic_report(net, diag_results, diag_params, compact_report=False)
    elif report_style == 'compact':
        diagnostic_report(net, diag_results, diag_params, compact_report=True)
    if return_result_dict:
        return diag_results


def check_greater_zero(element, element_index, column):
    """
     functions that check, if a certain input type restriction for attribute values of a pandapower
     elements are fulfilled. Exemplary description for all type check functions.

     INPUT:
        **element (pandas.Series)** - pandapower element instance (e.g. net.bus.loc[1])

        **element_index (int)**     - index of the element instance

        **column (string)**         - element attribute (e.g. 'vn_kv')


     OUTPUT:
        **element_index (index)**   - index of element instance, if input type restriction is not
                                      fulfilled


    """

    if check_number(element, element_index, column) is None:

        if (element[column] <= 0):
            return element_index

    else:
        return element_index


def check_greater_equal_zero(element, element_index, column):
    if check_number(element, element_index, column) is None:

        if (element[column] < 0):
            return element_index

    else:
        return element_index


def check_smaller_zero(element, element_index, column):
    if check_number(element, element_index, column) is None:

        if (element[column] >= 0):
            return element_index

    else:
        return element_index


def check_smaller_equal_zero(element, element_index, column):
    if check_number(element, element_index, column) is None:

        if (element[column] > 0):
            return element_index

    else:
        return element_index


def check_boolean(element, element_index, column):
    valid_values = [True, False, 0, 1, 0.0, 1.0]
    if element[column] not in valid_values:
        return element_index


def check_pos_int(element, element_index, column):
    if check_number(element, element_index, column) is None:
        if not ((element[column] % 1 == 0) and element[column] >= 0):
            return element_index

    else:
        return element_index


def check_number(element, element_index, column):
    try:
        nan_check = np.isnan(element[column])
        if nan_check or isinstance(element[column], bool):
            return element_index
    except TypeError:
        return element_index


def check_between_zero_and_one(element, element_index, column):
    if check_number(element, element_index, column) is None:

        if not (0 <= element[column] <= 1):
            return element_index

    else:
        return element_index


def check_switch_type(element, element_index, column):
    valid_values = ['b', 'l', 't']
    if element[column] not in valid_values:
        return element_index


def invalid_values(net):
    """
    Applies type check functions to find violations of input type restrictions.

     INPUT:
        **net** (pandapowerNet)         - pandapower network

        **detailed_report** (boolean)   - True: detailed report of input type restriction violations
                                          False: summary only

     OUTPUT:
        **check_results** (dict)        - dict that contains all input type restriction violations
                                          grouped by element (keys)
                                          Format: {'element': [element_index, 'element_attribute',
                                                    attribute_value]}

    """

    check_results = {}

    # Contains all element attributes that are necessary to initiate a power flow calculation.
    # There's a tuple with the structure (attribute_name, input type restriction)
    # for each attribute according to pandapower data structure documantation
    # (see also type_checks function)

    important_values = {'bus': [('vn_kv', '>0'), ('in_service', 'boolean')],
                        'line': [('from_bus', 'positive_integer'),
                                 ('to_bus', 'positive_integer'),
                                 ('length_km', '>0'), ('r_ohm_per_km', '>=0'),
                                 ('x_ohm_per_km', '>=0'), ('c_nf_per_km', '>=0'),
                                 ('max_i_ka', '>0'), ('df', '0to1'), ('in_service', 'boolean')],
                        'trafo': [('hv_bus', 'positive_integer'), ('lv_bus', 'positive_integer'),
                                  ('sn_kva', '>0'), ('vn_hv_kv', '>0'), ('vn_lv_kv', '>0'),
                                  ('vscr_percent', '>=0'),
                                  ('vsc_percent', '>0'), ('pfe_kw', '>=0'), ('i0_percent', '>=0'),
                                  ('in_service', 'boolean')],
                        'trafo3w': [('hv_bus', 'positive_integer'), ('mv_bus', 'positive_integer'),
                                    ('lv_bus', 'positive_integer'),
                                    ('sn_hv_kva', '>0'), ('sn_mv_kva', '>0'), ('sn_lv_kva', '>0'),
                                    ('vn_hv_kv', '>0'), ('vn_mv_kv', '>0'), ('vn_lv_kv', '>0'),
                                    ('vscr_hv_percent', '>=0'), ('vscr_mv_percent', '>=0'),
                                    ('vscr_lv_percent', '>=0'), ('vsc_hv_percent', '>0'),
                                    ('vsc_mv_percent', '>0'), ('vsc_lv_percent', '>0'),
                                    ('pfe_kw', '>=0'), ('i0_percent', '>=0'),
                                    ('in_service', 'boolean')],
                        'load': [('bus', 'positive_integer'), ('p_kw', 'number'),
                                 ('q_kvar', 'number'),
                                 ('scaling', '>=0'), ('in_service', 'boolean')],
                        'sgen': [('bus', 'positive_integer'), ('p_kw', 'number'),
                                 ('q_kvar', 'number'),
                                 ('scaling', '>=0'), ('in_service', 'boolean')],
                        'gen': [('bus', 'positive_integer'), ('p_kw', 'number'),
                                ('scaling', '>=0'), ('in_service', 'boolean')],
                        'ext_grid': [('bus', 'positive_integer'), ('vm_pu', '>0'),
                                     ('va_degree', 'number')],
                        'switch': [('bus', 'positive_integer'), ('element', 'positive_integer'),
                                   ('et', 'switch_type'), ('closed', 'boolean')]}

    # matches a check function to each single input type restriction
    type_checks = {'>0': check_greater_zero,
                   '>=0': check_greater_equal_zero,
                   '<0': check_smaller_zero,
                   '<=0': check_smaller_equal_zero,
                   'boolean': check_boolean,
                   'positive_integer': check_pos_int,
                   'number': check_number,
                   '0to1': check_between_zero_and_one,
                   'switch_type': check_switch_type
                   }

    for key in important_values:
        if len(net[key]) > 0:
            for value in important_values[key]:
                for i, element in net[key].iterrows():
                    check_result = type_checks[value[1]](element, i, value[0])
                    if check_result is not None:
                        if key not in check_results:
                            check_results[key] = []
                        # converts np.nan to str for easier usage of assert in pytest
                        nan_check = pd.isnull(net[key][value[0]].at[i])
                        if nan_check:
                            check_results[key].append((i, value[0],
                                                       str(net[key][value[0]].at[i]), value[1]))
                        else:
                            check_results[key].append((i, value[0],
                                                       net[key][value[0]].at[i], value[1]))
    return check_results


def no_ext_grid(net):
    """
    Checks, if at least one external grid exists.

     INPUT:
        **net** (pandapowerNet)         - pandapower network

    """

    if not len(net.ext_grid) > 0:
        return True


def multiple_voltage_controlling_elements_per_bus(net):
    """
    Checks, if there are buses with more than one generator and/or more than one external grid.

     INPUT:
        **net** (pandapowerNet)         - pandapower network

        **detailed_report** (boolean)   - True: detailed report of errors found
                                      l    False: summary only

     OUTPUT:
        **check_results** (dict)        - dict that contains all buses with multiple generator and
                                          all buses with multiple external grids
                                          Format: {'mult_ext_grids': [buses]
                                                   'buses_with_mult_gens', [buses]}

    """
    check_results = {}
    buses_with_mult_ext_grids = list(net.ext_grid.groupby("bus").count().query("vm_pu > 1").index)
    if buses_with_mult_ext_grids:
        check_results['buses_with_mult_ext_grids'] = buses_with_mult_ext_grids
    buses_with_gens_and_ext_grids = set(net.ext_grid.bus).intersection(set(net.gen.bus))
    if buses_with_gens_and_ext_grids:
        check_results['buses_with_gens_and_ext_grids'] = list(buses_with_gens_and_ext_grids)

    if check_results:
        return check_results


def overload(net, overload_scaling_factor):
    """
    Checks, if a loadflow calculation converges. If not, checks, if an overload is the reason for
    that by scaling down the loads, gens and sgens to 0.1%.

     INPUT:
        **net** (pandapowerNet)         - pandapower network


     OUTPUT:
        **check_results** (dict)        - dict with the results of the overload check
                                          Format: {'load_overload': True/uncertain
                                                   'generation_overload', True/uncertain}

    """
    check_result = {}
    load_scaling = copy.deepcopy(net.load.scaling)
    gen_scaling = copy.deepcopy(net.gen.scaling)
    sgen_scaling = copy.deepcopy(net.sgen.scaling)
    try:
        runpp(net)

    except LoadflowNotConverged:
        try:
            net.load.scaling = overload_scaling_factor
            runpp(net)
            net.load.scaling = load_scaling
            check_result['load'] = True

        except LoadflowNotConverged:
            net.load.scaling = load_scaling
            check_result['load'] = 'uncertain'

        try:
            net.gen.scaling = overload_scaling_factor
            net.sgen.scaling = overload_scaling_factor
            runpp(net)
            net.gen.scaling = gen_scaling
            net.gen.scaling = sgen_scaling
            check_result['generation'] = True

        except LoadflowNotConverged:
            net.gen.scaling = gen_scaling
            check_result['generation'] = 'uncertain'

    if check_result:
        return check_result


def wrong_switch_configuration(net):
    """
    Checks, if a loadflow calculation converges. If not, checks, if the switch configuration is
    the reason for that by closing all switches

     INPUT:
        **net** (pandapowerNet)         - pandapower network

     OUTPUT:
        **check_result** (boolean)

    """
    switch_configuration = copy.deepcopy(net.switch.closed)
    try:
        runpp(net)

    except (ValueError, LoadflowNotConverged):
        try:
            net.switch.closed = 1
            runpp(net)
            net.switch.closed = switch_configuration
            return True
        except LoadflowNotConverged:
            net.switch.closed = switch_configuration
            return 'uncertain'


def missing_bus_indeces(net):
    """
        Checks for missing bus indeces.

         INPUT:
            **net** (PandapowerNet)    - pandapower network


         OUTPUT:
            **check_results** (list)   - List of tuples each containing missing bus indeces.
                                         Format:
                                         [(element_index, bus_name (e.g. "from_bus"),  bus_index]

    """
    check_results = {}
    bus_indeces = set(net.bus.index)
    element_bus_names = {"ext_grid": ["bus"], "load": ["bus"], "gen": ["bus"], "sgen": ["bus"],
                         "trafo": ["lv_bus", "hv_bus"], "trafo3w": ["lv_bus", "mv_bus", "hv_bus"],
                         "switch": ["bus", "element"], "line": ["from_bus", "to_bus"]}
    for element in element_bus_names.keys():
        element_check = []
        for i, row in net[element].iterrows():
            for bus_name in element_bus_names[element]:
                if row[bus_name] not in bus_indeces:
                    if not ((element == "switch") and (bus_name == "element") and (row.et in ['l', 't'])):
                        element_check.append((i, bus_name, row[bus_name]))
        if element_check:
            check_results[element] = element_check

    if check_results:
        return check_results


def different_voltage_levels_connected(net):
    """
    Checks, if there are lines or switches that connect different voltage levels.

     INPUT:
        **net** (pandapowerNet)         - pandapower network

     OUTPUT:
        **check_results** (dict)        - dict that contains all lines and switches that connect
                                          different voltage levels.
                                          Format: {'lines': lines, 'switches': switches}

    """
    check_results = {}
    inconsistent_lines = []
    for i, line in net.line.iterrows():
        buses = net.bus.loc[[line.from_bus, line.to_bus]]
        if buses.vn_kv.iloc[0] != buses.vn_kv.iloc[1]:
            inconsistent_lines.append(i)

    inconsistent_switches = []
    for i, switch in net.switch[net.switch.et == "b"].iterrows():
        buses = net.bus.loc[[switch.bus, switch.element]]
        if buses.vn_kv.iloc[0] != buses.vn_kv.iloc[1]:
            inconsistent_switches.append(i)

    if inconsistent_lines:
        check_results['lines'] = inconsistent_lines
    if inconsistent_switches:
        check_results['switches'] = inconsistent_switches
    if check_results:
        return check_results


def lines_with_impedance_close_to_zero(net, lines_min_length_km, lines_min_z_ohm):
    """
    Checks, if there are lines with an impedance value of zero

     INPUT:
        **net** (pandapowerNet)         - pandapower network


     OUTPUT:
        **implausible_lines** (list)    - list that contains the indeces of all lines with an
                                          impedance value of zero.


    """
    implausible_lines = net.line[(net.line.length_km <= lines_min_length_km)
                                 | ((net.line.r_ohm_per_km + net.line.x_ohm_per_km)
                                    <= lines_min_z_ohm)]

    if len(implausible_lines) > 0:
        return list(implausible_lines.index)


def nominal_voltages_dont_match(net, nom_voltage_tolerance):
    """
    Checks, if there are components whose nominal voltages differ from the nominal voltages of the
    buses they're connected to. At the moment, only trafos and trafo3w are checked.
    Also checks for trafos with swapped hv and lv connectors.

     INPUT:
        **net** (pandapowerNet)         - pandapower network

     OUTPUT:
        **check_results** (dict)        - dict that contains all components whose nominal voltages
                                          differ from the nominal voltages of the buses they're
                                          connected to.

                                          Format:

                                          {trafo': {'hv_bus' : trafos_indeces,
                                                    'lv_bus' : trafo_indeces,
                                                    'hv_lv_swapped' : trafo_indeces},
                                           trafo3w': {'hv_bus' : trafos3w_indeces,
                                                      'mv_bus' : trafos3w_indeces
                                                      'lv_bus' : trafo3w_indeces,
                                                      'connectors_swapped_3w' : trafo3w_indeces}}

    """
    results = {}
    trafo_results = {}
    trafo3w_results = {}

    hv_bus = []
    lv_bus = []
    hv_lv_swapped = []

    hv_bus_3w = []
    mv_bus_3w = []
    lv_bus_3w = []
    connectors_swapped_3w = []

    for i, trafo in net.trafo.iterrows():
        hv_bus_violation = False
        lv_bus_violation = False
        connectors_swapped = False
        hv_bus_vn_kv = net.bus.vn_kv.at[trafo.hv_bus]
        lv_bus_vn_kv = net.bus.vn_kv.at[trafo.lv_bus]

        if abs(1-(trafo.vn_hv_kv / hv_bus_vn_kv)) > nom_voltage_tolerance:
            hv_bus_violation = True
        if abs(1-(trafo.vn_lv_kv / lv_bus_vn_kv)) > nom_voltage_tolerance:
            lv_bus_violation = True
        if hv_bus_violation and lv_bus_violation:
            trafo_voltages = np.array(([trafo.vn_hv_kv, trafo.vn_lv_kv]))
            bus_voltages = np.array([hv_bus_vn_kv, lv_bus_vn_kv])
            trafo_voltages.sort()
            bus_voltages.sort()
            if all((abs(trafo_voltages - bus_voltages) / bus_voltages) < (nom_voltage_tolerance)):
                connectors_swapped = True

        if connectors_swapped:
            hv_lv_swapped.append(i)
        else:
            if hv_bus_violation:
                hv_bus.append(i)
            if lv_bus_violation:
                lv_bus.append(i)

    if hv_bus:
        trafo_results['hv_bus'] = hv_bus
    if lv_bus:
        trafo_results['lv_bus'] = lv_bus
    if hv_lv_swapped:
        trafo_results['hv_lv_swapped'] = hv_lv_swapped
    if trafo_results:
        results['trafo'] = trafo_results

    for i, trafo3w in net.trafo3w.iterrows():
        hv_bus_violation = False
        mv_bus_violation = False
        lv_bus_violation = False
        connectors_swapped = False
        hv_bus_vn_kv = net.bus.vn_kv.at[trafo3w.hv_bus]
        mv_bus_vn_kv = net.bus.vn_kv.at[trafo3w.mv_bus]
        lv_bus_vn_kv = net.bus.vn_kv.at[trafo3w.lv_bus]

        if abs(1-(trafo3w.vn_hv_kv / hv_bus_vn_kv)) > nom_voltage_tolerance:
            hv_bus_violation = True
        if abs(1-(trafo3w.vn_mv_kv / mv_bus_vn_kv)) > nom_voltage_tolerance:
            mv_bus_violation = True
        if abs(1-(trafo3w.vn_lv_kv / lv_bus_vn_kv)) > nom_voltage_tolerance:
            lv_bus_violation = True
        if hv_bus_violation and mv_bus_violation and lv_bus_violation:
            trafo_voltages = np.array(([trafo3w.vn_hv_kv, trafo3w.vn_mv_kv, trafo3w.vn_lv_kv]))
            bus_voltages = np.array([hv_bus_vn_kv, mv_bus_vn_kv, lv_bus_vn_kv])
            trafo_voltages.sort()
            bus_voltages.sort()
            if all((abs(trafo_voltages - bus_voltages) / bus_voltages) < (nom_voltage_tolerance)):
                connectors_swapped = True

        if connectors_swapped:
            connectors_swapped_3w.append(i)
        else:
            if hv_bus_violation:
                hv_bus_3w.append(i)
            if mv_bus_violation:
                mv_bus_3w.append(i)
            if lv_bus_violation:
                lv_bus_3w.append(i)

    if hv_bus_3w:
        trafo3w_results['hv_bus'] = hv_bus_3w
    if mv_bus_3w:
        trafo3w_results['mv_bus'] = mv_bus_3w
    if lv_bus_3w:
        trafo3w_results['lv_bus'] = lv_bus_3w
    if connectors_swapped_3w:
        trafo3w_results['connectors_swapped_3w'] = connectors_swapped_3w
    if trafo3w_results:
        results['trafo3w'] = trafo3w_results

    if len(results) > 0:
        return results


def disconnected_elements(net):
    """
    Checks, if there are network sections without a connection to an ext_grid. Returns all network
    elements in these sections, that are in service. Elements belonging to the same disconnected
    networks section are grouped in lists (e.g. disconnected lines: [[1, 2, 3], [4, 5]]
    means, that lines 1, 2 and 3 are in one disconncted section but are connected to each other.
    The same stands for lines 4, 5.)

     INPUT:
        **net** (pandapowerNet)         - pandapower network

     OUTPUT:
        **disc_elements** (dict)        - list that contains all network elements, without a
                                          connection to an ext_grid.

                                          format: {'disconnected buses'   : bus_indeces,
                                                   'disconnected switches' : switch_indeces,
                                                   'disconnected lines'    : line_indeces,
                                                   'disconnected trafos'   : trafo_indeces
                                                   'disconnected loads'    : load_indeces,
                                                   'disconnected gens'     : gen_indeces,
                                                   'disconnected sgens'    : sgen_indeces}

    """

    mg = top.create_nxgraph(net)
    sections = top.connected_components(mg)
    disc_elements = []

    for section in sections:
        section_dict = {}

        if not section & set(net.ext_grid.bus) and any(net.bus.in_service.loc[section]):
            section_buses = list(net.bus[net.bus.index.isin(section)
                                         & (net.bus.in_service == True)].index)
            section_switches = list(net.switch[net.switch.bus.isin(section_buses)].index)
            section_lines = list(get_connected_elements(net, 'line', section_buses,
                                                        respect_switches=True,
                                                        respect_in_service=True))
            section_trafos = list(get_connected_elements(net, 'trafo', section_buses,
                                                         respect_switches=True,
                                                         respect_in_service=True))

            section_trafos3w = list(get_connected_elements(net, 'trafo3w', section_buses,
                                                           respect_switches=True,
                                                           respect_in_service=True))
            section_gens = list(net.gen[net.gen.bus.isin(section)
                                        & (net.gen.in_service == True)].index)
            section_sgens = list(net.sgen[net.sgen.bus.isin(section)
                                          & (net.sgen.in_service == True)].index)
            section_loads = list(net.load[net.load.bus.isin(section)
                                          & (net.load.in_service == True)].index)

            if section_buses:
                section_dict['buses'] = section_buses
            if section_switches:
                section_dict['switches'] = section_switches
            if section_lines:
                section_dict['lines'] = section_lines
            if section_trafos:
                section_dict['trafos'] = section_trafos
            if section_trafos3w:
                section_dict['trafos3w'] = section_trafos3w
            if section_loads:
                section_dict['loads'] = section_loads
            if section_gens:
                section_dict['gens'] = section_gens
            if section_sgens:
                section_dict['sgens'] = section_sgens

            if any(section_dict.values()):
                disc_elements.append(section_dict)

    open_trafo_switches = net.switch[(net.switch.et == 't') & (net.switch.closed == 0)]
    isolated_trafos = set(
        (open_trafo_switches.groupby("element").count().query("bus > 1").index))
    isolated_trafos_is = isolated_trafos.intersection((set(net.trafo[net.trafo.in_service == True]
                                                           .index)))
    if isolated_trafos_is:
        disc_elements.append({'isolated_trafos': list(isolated_trafos_is)})

    isolated_trafos3w = set(
        (open_trafo_switches.groupby("element").count().query("bus > 2").index))
    isolated_trafos3w_is = isolated_trafos3w.intersection((
        set(net.trafo[net.trafo.in_service == True].index)))
    if isolated_trafos3w_is:
        disc_elements.append({'isolated_trafos3w': list(isolated_trafos3w_is)})

    if disc_elements:
        return disc_elements


def wrong_reference_system(net):
    """
    Checks usage of wrong reference system for loads, sgens and gens.

     INPUT:
        **net** (pandapowerNet)    - pandapower network

     OUTPUT:
        **check_results** (dict)        - dict that contains the indeces of all components where the
                                          usage of the wrong reference system was found.

                                          Format: {'element_type': element_indeces}

    """
    check_results = {}
    neg_loads = list(net.load[net.load.p_kw < 0].index)
    pos_gens = list(net.gen[net.gen.p_kw > 0].index)
    pos_sgens = list(net.sgen[net.sgen.p_kw > 0].index)

    if neg_loads:
        check_results['loads'] = neg_loads
    if pos_gens:
        check_results['gens'] = pos_gens
    if pos_sgens:
        check_results['sgens'] = pos_sgens

    if check_results:
        return check_results


def numba_comparison(net, numba_tolerance):
    """
        Compares the results of loadflows with numba=True vs. numba=False.

         INPUT:
            **net** (pandapowerNet)    - pandapower network

         OPTIONAL:
            **tol** (float, 1e-5)      - Maximum absolute deviation allowed between
                                         numba=True/False results.

         OUTPUT:
            **check_result** (dict)    - Absolute deviations between numba=True/False results.
    """
    check_results = {}
    try:
        runpp(net, numba=True)
    except LoadflowNotConverged:
        pass
    if net.converged:
        try:
            result_numba_true = copy.deepcopy(net)
            runpp(net, numba=False)
            result_numba_false = copy.deepcopy(net)
            res_keys = [key for key in result_numba_true.keys() if (key in ['res_bus', 'res_ext_grid',
                                                                            'res_gen', 'res_impedance',
                                                                            'res_line', 'res_load',
                                                                            'res_sgen', 'res_shunt',
                                                                            'res_trafo', 'res_trafo3w',
                                                                            'res_ward', 'res_xward'])]
            for key in res_keys:
                diffs = abs(result_numba_true[key] - result_numba_false[key]) > numba_tolerance
                if any(diffs.any()):
                    if (key not in check_results.keys()):
                        check_results[key] = {}
                    for col in diffs.columns:
                        if (col not in check_results[key].keys()) and (diffs.any()[col]):
                            check_results[key][col] = {}
                            numba_true = result_numba_true[key][col][diffs[col]]
                            numba_false = result_numba_false[key][col][diffs[col]]
                            check_results[key][col] = abs(numba_true - numba_false)
        except LoadflowNotConverged:
            pass

    if check_results:
        return check_results


def deviation_from_std_type(net):
    """
        Checks, if element parameters match the values in the standard type library.

         INPUT:
            **net** (pandapowerNet)    - pandapower network


         OUTPUT:
            **check_results** (dict)   - All elements, that don't match the values in the
                                         standard type library

                                         Format: (element_type, element_index, parameter)


    """
    check_results = {}
    for key in net.std_types.keys():
        for i, element in net[key].iterrows():
            std_type = element.std_type
            if std_type in net.std_types[key].keys():
                std_type_values = net.std_types[key][std_type]
                for param in std_type_values.keys():
                    if param == "tp_pos":
                        continue
                    if param in net[key].columns:
                        if not element[param] == std_type_values[param]:
                            if key not in check_results.keys():
                                check_results[key] = {}
                            check_results[key][i] = {'param': param, 'e_value': element[param],
                                                     'std_type_value': std_type_values[param],
                                                     'std_type_in_lib': True}
            elif std_type is not None:
                if key not in check_results.keys():
                    check_results[key] = {}
                check_results[key][i] = {'std_type_in_lib': False}

    if check_results:
        return check_results


def parallel_switches(net):
    """
        Checks for parallel switches.

         INPUT:
            **net** (PandapowerNet)    - pandapower network


         OUTPUT:
            **parallel_switches** (list)   - List of tuples each containing parallel switches.




    """
    parallel_switches = []
    compare_parameters = ['bus', 'element']
    parallels_bus_and_element = list(net.switch.groupby(compare_parameters).count().query('et > 1').index)
    for bus, element in parallels_bus_and_element:
        parallel_switches.append(list(net.switch[(net.switch.bus == bus)
                                                 & (net.switch.element == element)].index))
    if parallel_switches:
        return parallel_switches
