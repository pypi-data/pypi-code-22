"""
Managing all `EXECUTE <https://technet.microsoft.com/fr-fr/library/ms186691(v=sql.110).aspx>`_ requests and responses
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import re
from collections import OrderedDict

import numpy as np
import xmlwitch

from six.moves import zip

from olapy.core.mdx.parser.parse import Parser


class XmlaExecuteTools():
    """XmlaExecuteTools for generating xmla execute responses."""

    def __init__(self, executor, convert2formulas=False):
        self.executor = executor
        self.convert2formulas = convert2formulas
        if convert2formulas:
            self.mdx_execution_result = self._execute_convert_formulas_query()
        else:
            # todo remove executor.mdx_query
            self.mdx_execution_result = executor.execute_mdx(executor.mdx_query)
        if isinstance(self.mdx_execution_result, dict):
            self.columns_desc = self.mdx_execution_result.get('columns_desc')

    def _execute_convert_formulas_query(self):
        """
        <Cell CellOrdinal="0">
                <Value>[Measures].[Amount]</Value>
            </Cell>
            <Cell CellOrdinal="1">
                <Value>Amount</Value>
            </Cell>
            <Cell CellOrdinal="2">
                <Value>[Measures]</Value>
            </Cell>
            <Cell CellOrdinal="3">
                <Value>[Geography].[Geo].[All Regions].&amp;[America]</Value>
            </Cell>
            <Cell CellOrdinal="4">
                <Value>America</Value>
            </Cell>
            <Cell CellOrdinal="5">
                <Value>[Geography].[Geo].[Continent]</Value>
            </Cell>
            <Cell CellOrdinal="6">
                <Value>[Geography].[Geo].[All Regions].&amp;[America].&amp;[US]</Value>
            </Cell>
            <Cell CellOrdinal="7">
                <Value>United States</Value>
            </Cell>
            <Cell CellOrdinal="8">
                <Value>[Geography].[Geo].[Country]</Value>
            </Cell>
            <Cell CellOrdinal="9">
                <Value>[Product].[Prod].[Company].&amp;[Crazy Development ]</Value>
            </Cell>
            <Cell CellOrdinal="10">
                <Value>Crazy Development </Value>
            </Cell>
            <Cell CellOrdinal="11">
                <Value>[Product].[Prod].[Company]</Value>
            </Cell>
            <Cell CellOrdinal="12">
                <Value>[Product].[Prod].[Company].&amp;[Crazy Development ].&amp;[icCube]</Value>
            </Cell>
            <Cell CellOrdinal="13">
                <Value>icCube</Value>
            </Cell>
            <Cell CellOrdinal="14">
                <Value>[Product].[Prod].[Article]</Value>
            </Cell>
            <Cell CellOrdinal="15">
                <Value>[Geography].[Geo].[All Regions].&amp;[Europe]</Value>
            </Cell>
            <Cell CellOrdinal="16">
                <Value>Europe</Value>
            </Cell>
            <Cell CellOrdinal="17">
                <Value>[Geography].[Geo].[Continent]</Value>
            </Cell>
        :return:
        """

        # todo check
        return [tup[0] for tup in re.compile(Parser.regex).findall(self.executor.mdx_query)
                if '[Measures].[XL_SD' not in tup[0] and tup[1]][::3]

    def split_dataframe(self):
        """Split DataFrame into multiple ones by dimension.

        Example::

            in :

            +-------------+----------+----------+---------+---------+
            | Continent   | Country  | Company  |Article  | Amount  |
            +=============+==========+==========+=========+=========+
            | America     | US       | MS       |Crazy De | 35150   |
            +-------------+----------+----------+---------+---------+

            out :

            'Geography':

                +-------------+----------+---------+
                | Continent   | Country  | Amount  |
                +=============+==========+=========+
                | America     | US       | 35150   |
                +-------------+----------+---------+


            'Product':

                +----------+---------+---------+
                | Company  |Article  | Amount  |
                +==========+=========+=========+
                | MS       |Crazy De | 35150   |
                +----------+---------+---------+


        :return: dict with multiple DataFrame
        """
        return OrderedDict(
            (key, self.mdx_execution_result['result'].reset_index()[list(value)])
            for key, value in self.columns_desc['all'].items()
        )

    @staticmethod
    def get_tuple_without_nan(tuple):
        """Remove nan from tuple.

        Example:

            in  : ['Geography','Continent','-1']

            out : ['Geography','Continent']

        :param tuple: tuple as list
        :return: tuple as list without -1

        """
        for att in tuple[::-1]:
            if att != -1:
                return tuple[:tuple.index(att) + 1]

        return tuple

    def _generate_tuples_xs0(self, splited_df, mdx_query_axis):

        first_att = None
        # in python 3 it returns odict_keys(['Facts']) instead of ['Facts']
        if list(self.columns_desc[mdx_query_axis].keys()) == [self.executor.facts]:
            if len(self.columns_desc[mdx_query_axis][self.executor.facts]) == 1:
                # to ignore for tupls in itertools.chain(*tuples)
                tuples = []
            else:
                # ['Facts', 'Amount', 'Amount']
                tuples = [[[[self.executor.facts] + [mes] + [mes]]] for mes in self.executor.selected_measures]
                first_att = 3

        # query with on columns and on rows (without measure)
        elif self.columns_desc['columns'] and self.columns_desc['rows']:
            # ['Geography','America']
            tuples = [
                zip(* [[[key] + list(row)
                        for row in splited_df[key].itertuples(index=False)]
                       for key in splited_df.keys()
                       if key is not self.executor.facts]),
            ]

            first_att = 2

        # query with on columns and on rows (many measures selected)
        else:
            # ['Geography','Amount','America']
            tuples = [
                zip(* [[[key] + [mes] + list(row)
                        for row in splited_df[key].itertuples(index=False)]
                       for key in splited_df.keys()
                       if key is not self.executor.facts])
                for mes in self.executor.selected_measures
            ]
            first_att = 3

        return tuples, first_att

    def _gen_measures_xs0(self, xml, tupls):
        with xml.Member(Hierarchy="[Measures]"):
            xml.UName(
                '[Measures].[{0}]'.format(tupls[0][1]), )
            xml.Caption('{0}'.format(tupls[0][1]))
            xml.LName('[Measures]')
            xml.LNum('0')
            xml.DisplayInfo('0')
            if 'HIERARCHY_UNIQUE_NAME' in self.executor.mdx_query:
                xml.HIERARCHY_UNIQUE_NAME('[Measures]')

    def tuples_2_xs0(self, tuples, splited_df, first_att, axis):
        xml = xmlwitch.Builder()
        with xml.Axis(name=axis):
            with xml.Tuples:
                for tupls in itertools.chain(*tuples):
                    with xml.Tuple:
                        if tupls[0][1] in self.executor.measures and len(self.executor.selected_measures) > 1:
                            self._gen_measures_xs0(xml, tupls)
                            if tupls[0][-1] in self.executor.measures:
                                continue

                        for tupl in tupls:
                            tuple_without_minus_1 = self.get_tuple_without_nan(tupl)
                            with xml.Member(Hierarchy="[{0}].[{0}]".format(tuple_without_minus_1[0])):
                                xml.UName('[{0}].[{0}].[{1}].{2}'.format(
                                    tuple_without_minus_1[0],
                                    splited_df[tuple_without_minus_1[0]].columns[
                                        len(tuple_without_minus_1) - first_att],
                                    '.'.join(['[' + str(i) + ']' for i in tuple_without_minus_1[first_att - 1:]])))
                                xml.Caption(str((tuple_without_minus_1[-1])))
                                xml.LName('[{0}].[{0}].[{1}]'.format(
                                    tuple_without_minus_1[0],
                                    splited_df[tuple_without_minus_1[0]].columns[
                                        len(tuple_without_minus_1) - first_att]))
                                xml.LNum(str(len(tuple_without_minus_1) - first_att))
                                xml.DisplayInfo('131076')

                                if 'PARENT_UNIQUE_NAME' in self.executor.mdx_query.upper():
                                    parent = '.'.join(
                                        map(lambda x: '[' + str(x) + ']', tuple_without_minus_1[first_att - 1:-1]))
                                    if parent:
                                        parent = '.' + parent
                                    xml.PARENT_UNIQUE_NAME(
                                        '[{0}].[{0}].[{1}]{2}'.format(
                                            tuple_without_minus_1[0],
                                            splited_df[tuple_without_minus_1[0]].columns[0],
                                            parent))
                                if 'HIERARCHY_UNIQUE_NAME' in self.executor.mdx_query.upper():
                                    xml.HIERARCHY_UNIQUE_NAME('[{0}].[{0}]'.format(tuple_without_minus_1[0]))

                        # Hierarchize'
                        if not self.executor.parser.hierarchized_tuples():
                            self._gen_measures_xs0(xml, tupls)
        return xml

    def _gen_xs0_grouped_tuples(self, axis, tuples_groups):
        xml = xmlwitch.Builder()
        with xml.Axis(name=axis):
            with xml.Tuples:
                for group in tuples_groups:
                    with xml.Tuple:
                        for tupl in self.executor.parser.split_group(group):
                            splited_tupl = self.executor.parser.split_tuple(tupl)
                            if splited_tupl[0].upper() == 'MEASURES':
                                hierarchy = '[Measures]'
                                l_name = '[' + splited_tupl[0] + ']'
                                lvl = 0
                                displayinfo = '0'
                            else:
                                hierarchy = '[{0}].[{0}]'.format(splited_tupl[0])
                                l_name = "[{0}]".format('].['.join(splited_tupl[:3]))
                                lvl = len(splited_tupl[4:])
                                displayinfo = '131076'

                            with xml.Member(Hierarchy=hierarchy):
                                xml.UName('{0}'.format(tupl.strip(' \t\n')))
                                xml.Caption('{0}'.format(splited_tupl[-1]))
                                xml.LName(l_name)
                                xml.LNum(str(lvl))
                                xml.DisplayInfo(displayinfo)
        return str(xml)

    def generate_xs0_one_axis(
            self,
            splited_df,
            mdx_query_axis='all',
            axis="Axis0",):
        """

        :param splited_df:
        :return:
        """

        # patch 4 select (...) (...) (...) from bla bla bla
        if self.executor.check_nested_select():
            return self._gen_xs0_grouped_tuples(axis, self.executor.parser.get_nested_select())

        xml = xmlwitch.Builder()

        tuples, first_att = self._generate_tuples_xs0(splited_df, mdx_query_axis)
        if tuples:
            xml = self.tuples_2_xs0(tuples, splited_df, first_att, axis)
        elif self.columns_desc['columns'].keys() == [self.executor.facts]:
            with xml.Axis(name=axis):
                with xml.Tuples:
                    with xml.Tuple:
                        with xml.Member(Hierarchy="[Measures]"):
                            xml.UName('[Measures].[{0}]'.format(self.executor.selected_measures[0]))
                            xml.Caption(str(self.executor.selected_measures[0]))
                            xml.LName('[Measures]')
                            xml.LNum('0')
                            xml.DisplayInfo('0')
        return str(xml)

    def _generate_xs0_convert2formulas(self):
        xml = xmlwitch.Builder()
        with xml.Axis(name="Axis0"):
            with xml.Tuples:
                if isinstance(self.mdx_execution_result, list):
                    for idx in range(len(self.mdx_execution_result) * 3):
                        with xml.Tuple:
                            with xml.Member(Hierarchy="[Measures]"):
                                xml.UName('[Measures].[{0}]'.format('XL_SD' + str(idx)))
                                xml.Caption('XL_SD' + str(idx))
                                xml.LName('[Measures]')
                                xml.LNum('0')
                                xml.DisplayInfo('0')
        return str(xml)

    def _generate_slicer_convert2formulas(self):
        """
        <Axis name="SlicerAxis">
            <Tuples>
                <Tuple>
                    <Member Hierarchy="[Geography].[Geo]">
                        <UName>[Geography].[Geo].[All Regions]</UName>
                        <Caption>All Regions</Caption>
                        <LName>[Geography].[Geo].[All-Level]</LName>
                        <LNum>0</LNum>
                        <DisplayInfo>2</DisplayInfo>
                    </Member>
                    <Member Hierarchy="[Geography].[Economy]">
                        <UName>[Geography].[Economy].[All]</UName>
                        <Caption>All</Caption>
                        <LName>[Geography].[Economy].[All-Level]</LName>
                        <LNum>0</LNum>
                        <DisplayInfo>3</DisplayInfo>
                    </Member>
                    <Member Hierarchy="[Product].[Prod]">
                        <UName>[Product].[Prod].[Company].&amp;[Crazy Development ]</UName>
                        <Caption>Crazy Development </Caption>
                        <LName>[Product].[Prod].[Company]</LName>
                        <LNum>0</LNum>
                        <DisplayInfo>1</DisplayInfo>
                    </Member>
                    <Member Hierarchy="[Time].[Calendar]">
                        <UName>[Time].[Calendar].[Year].&amp;[2010]</UName>
                        <Caption>2010</Caption>
                        <LName>[Time].[Calendar].[Year]</LName>
                        <LNum>0</LNum>
                        <DisplayInfo>4</DisplayInfo>
                    </Member>
                </Tuple>
            </Tuples>
        </Axis>

        :return:
        """
        xml = xmlwitch.Builder()
        with xml.Axis(name="SlicerAxis"):
            with xml.Tuples:
                with xml.Tuple:
                    for dim_diff in self.executor.get_all_tables_names(ignore_fact=True):
                        column_attribut = self.executor.tables_loaded[dim_diff].iloc[0][0]
                        with xml.Member(Hierarchy="[{0}].[{0}]".format(dim_diff)):
                            xml.UName('[{0}].[{0}].[{1}].[{2}]'.format(dim_diff,
                                                                       self.executor.tables_loaded[dim_diff].columns[0],
                                                                       column_attribut))
                            xml.Caption(str(column_attribut))
                            xml.LName('[{0}].[{0}].[{1}]'.format(dim_diff,
                                                                 self.executor.tables_loaded[dim_diff].columns[0]))
                            xml.LNum('0')
                            xml.DisplayInfo('2')

        return str(xml)

    def _generate_axes_convert2formulas(self):
        return self._generate_xs0_convert2formulas()

    def generate_xs0(self):
        """
        Example of xs0::

             <Axis name="Axis0">
                <Tuples>
                    <Tuple>
                        <Member Hierarchy="[Geography].[Geography]">
                            <UName>[Geography].[Geography].[Continent].[America]</UName>
                            <Caption>America</Caption>
                            <LName>[Geography].[Geography].[Continent]</LName>
                            <LNum>0</LNum>
                            <DisplayInfo>131076</DisplayInfo>
                        <HIERARCHY_UNIQUE_NAME>[Geography].[Geography]</HIERARCHY_UNIQUE_NAME>
                        </Member>

                        <Member Hierarchy="[Product].[Product]">
                            <UName>[Product].[Product].[Company].[Crazy Development]</UName>
                            <Caption>Crazy Development</Caption>
                            <LName>[Product].[Product].[Company]</LName>
                            <LNum>0</LNum>
                            <DisplayInfo>131076</DisplayInfo>
                        <HIERARCHY_UNIQUE_NAME>[Product].[Product]</HIERARCHY_UNIQUE_NAME>
                        </Member>
                        </Tuple>

                    <Tuple>
                        <Member Hierarchy="[Geography].[Geography]">
                            <UName>[Geography].[Geography].[Continent].[Europe]</UName>
                            <Caption>Europe</Caption>
                            <LName>[Geography].[Geography].[Continent]</LName>
                            <LNum>0</LNum>
                            <DisplayInfo>131076</DisplayInfo>
                        <HIERARCHY_UNIQUE_NAME>[Geography].[Geography]</HIERARCHY_UNIQUE_NAME>
                        </Member>

                        <Member Hierarchy="[Product].[Product]">
                            <UName>[Product].[Product].[Company].[Crazy Development]</UName>
                            <Caption>Crazy Development</Caption>
                            <LName>[Product].[Product].[Company]</LName>
                            <LNum>0</LNum>
                            <DisplayInfo>131076</DisplayInfo>
                        <HIERARCHY_UNIQUE_NAME>[Product].[Product]</HIERARCHY_UNIQUE_NAME>
                        </Member>
                    </Tuple>
                </Tuples>
             </Axis>

        :return: xs0 xml as string
        """
        # TODO must be OPTIMIZED every time!!!!!

        if self.convert2formulas:
            return self._generate_axes_convert2formulas()

        dfs = self.split_dataframe()
        if self.columns_desc['rows'] and self.columns_desc['columns']:
            return """
            {0}
            {1}
            """.format(self.generate_xs0_one_axis(dfs, mdx_query_axis='columns', axis="Axis0"),
                       self.generate_xs0_one_axis(dfs, mdx_query_axis='rows', axis="Axis1"))

        # only one measure selected
        elif not self.columns_desc['rows'] and not self.columns_desc['columns'] and self.columns_desc['where']:
            return self.generate_xs0_one_axis(dfs, mdx_query_axis='where', axis="Axis0")

        # one axis
        return self.generate_xs0_one_axis(dfs, mdx_query_axis='columns', axis="Axis0")

    def _generate_cells_data_convert2formulas(self):
        """
        for each tuple:
        <Cell CellOrdinal="0">
            <Value>[Measures].[Amount]</Value>
        </Cell>
        <Cell CellOrdinal="1">
            <Value>Amount</Value>
        </Cell>
        <Cell CellOrdinal="2">
            <Value>[Measures]</Value>
        </Cell>
        """

        xml = xmlwitch.Builder()
        index = 0
        for tupl in self.mdx_execution_result:
            with xml.Cell(CellOrdinal=str(index)):
                xml.Value(tupl)
            index += 1
            with xml.Cell(CellOrdinal=str(index)):
                xml.Value(self.executor.parser.split_tuple(tupl)[-1])
            index += 1

            tupl2list = tupl.split('.')
            if tupl2list[0].upper() == '[MEASURES]':
                value = '[Measures]'
            else:
                value = '{0}.{0}.[{1}]'.format(
                    tupl2list[0],
                    self.executor.tables_loaded[
                        tupl2list[0].replace('[', '', ).replace(']', '')].columns[len(tupl2list[4:])]
                )

            with xml.Cell(CellOrdinal=str(index)):
                xml.Value(value)
            index += 1

        return str(xml)

    def generate_cell_data(self):
        """
        Example of CellData::

            <Cell CellOrdinal="0">
                <Value xsi:type="xsi:long">768</Value>
            </Cell>

            <Cell CellOrdinal="1">
                <Value xsi:type="xsi:long">255</Value>
            </Cell>

        :return: CellData as string
        """

        if self.convert2formulas:
            return self._generate_cells_data_convert2formulas()

        if (len(self.columns_desc['columns'].keys()) == 0 or len(self.columns_desc['rows'].keys()) == 0) \
                and self.executor.facts in self.columns_desc['all'].keys():
            # iterate DataFrame horizontally
            columns_loop = itertools.chain(*[
                self.mdx_execution_result['result'][measure] for measure in self.mdx_execution_result['result'].columns
            ])

        else:
            # iterate DataFrame vertically
            columns_loop = itertools.chain(*[
                tuple for tuple in self.mdx_execution_result['result'].itertuples(index=False)
            ])

        xml = xmlwitch.Builder()
        index = 0

        for value in columns_loop:
            if np.isnan(value):
                value = ''
            with xml.Cell(CellOrdinal=str(index)):
                xml.Value(str(value), **{'xsi:type': 'xsi:long'})

            index += 1

        return str(xml)

    def _generate_axes_info_sliver_convert2formulas(self):
        xml = xmlwitch.Builder()
        with xml.AxisInfo(name='SlicerAxis'):
            for dim in self.executor.get_all_tables_names(ignore_fact=True):
                to_write = "[{0}].[{0}]".format(dim)
                with xml.HierarchyInfo(name=to_write):
                    xml.UName(name=to_write + ".[MEMBER_UNIQUE_NAME]", **{'type': 'xs:string'})
                    xml.Caption(name=to_write + ".[MEMBER_CAPTION]", **{'type': 'xs:string'})
                    xml.LName(name=to_write + ".[LEVEL_UNIQUE_NAME]", **{'type': 'xs:string'})
                    xml.LNum(name=to_write + ".[LEVEL_NUMBER]", **{'type': 'xs:int'})
                    xml.DisplayInfo(name=to_write + ".[DISPLAY_INFO]", **{'type': 'xs:unsignedInt'})

        return str(xml)

    def generate_axes_info_slicer(self):
        """
        Not used dimensions.

        Example AxisInfo::

            <AxesInfo>
                <AxisInfo name="SlicerAxis">
                    <HierarchyInfo name="[Time].[Time]">
                        <UName name="[Time].[Time].[MEMBER_UNIQUE_NAME]" type="xs:string"/>
                        <Caption name="[Time].[Time].[MEMBER_CAPTION]" type="xs:string"/>
                        <LName name="[Time].[Time].[LEVEL_UNIQUE_NAME]" type="xs:string"/>
                        <LNum name="[Time].[Time].[LEVEL_NUMBER]" type="xs:int"/>
                        <DisplayInfo name="[Time].[Time].[DISPLAY_INFO]" type="xs:unsignedInt"/>
                    </HierarchyInfo>
                    <HierarchyInfo name="[Measures]">
                        <UName name="[Measures].[MEMBER_UNIQUE_NAME]" type="xs:string"/>
                        <Caption name="[Measures].[MEMBER_CAPTION]" type="xs:string"/>
                        <LName name="[Measures].[LEVEL_UNIQUE_NAME]" type="xs:string"/>
                        <LNum name="[Measures].[LEVEL_NUMBER]" type="xs:int"/>
                        <DisplayInfo name="[Measures].[DISPLAY_INFO]" type="xs:unsignedInt"/>
                    </HierarchyInfo>
                </AxisInfo>
            </AxesInfo>

        :return: AxisInfo as string
        """

        if self.convert2formulas:
            return self._generate_axes_info_sliver_convert2formulas()

        all_dimensions_names = self.executor.get_all_tables_names(ignore_fact=True)
        all_dimensions_names.append('Measures')

        xml = xmlwitch.Builder()

        slicer_list = sorted(list(set(all_dimensions_names) - set(
            table_name for table_name in self.columns_desc['all'])))

        if 'Measures' in slicer_list:
            slicer_list.insert(len(slicer_list), slicer_list.pop(slicer_list.index('Measures')))

        if slicer_list:
            with xml.AxisInfo(name='SlicerAxis'):
                for dim_diff in slicer_list:
                    to_write = "[{0}].[{0}]".format(dim_diff)
                    if dim_diff == 'Measures':

                        # if measures > 1 we don't have to write measure
                        # Hierarchize
                        if self.executor.facts in self.columns_desc['all'] and (len(
                            self.columns_desc['all'][self.executor.facts]) > 1) or (
                                not self.executor.parser.hierarchized_tuples() and not self.columns_desc['where']):
                            continue

                        else:
                            to_write = "[Measures]"

                    with xml.HierarchyInfo(name=to_write):
                        xml.UName(name=to_write + ".[MEMBER_UNIQUE_NAME]", **{'type': 'xs:string'})
                        xml.Caption(name=to_write + ".[MEMBER_CAPTION]", **{'type': 'xs:string'})
                        xml.LName(name=to_write + ".[LEVEL_UNIQUE_NAME]", **{'type': 'xs:string'})
                        xml.LNum(name=to_write + ".[LEVEL_NUMBER]", **{'type': 'xs:int'})
                        xml.DisplayInfo(name=to_write + ".[DISPLAY_INFO]", **{'type': 'xs:unsignedInt'})

        return str(xml)

    def _gen_measures_one_axis_info(self, xml):
        with xml.HierarchyInfo(name='[Measures]'):
            xml.UName(name="[Measures].[MEMBER_UNIQUE_NAME]", **{'type': 'xs:string'})
            xml.Caption(name="[Measures].[MEMBER_CAPTION]", **{'type': 'xs:string'})
            xml.LName(name="[Measures].[LEVEL_UNIQUE_NAME]", **{'type': 'xs:string'})
            xml.LNum(name="[Measures].[LEVEL_NUMBER]", **{'type': 'xs:int'})
            xml.DisplayInfo(name="[Measures].[DISPLAY_INFO]", **{'type': 'xs:unsignedInt'})
            if 'PARENT_UNIQUE_NAME' in self.executor.mdx_query:
                xml.PARENT_UNIQUE_NAME(name="[Measures].[PARENT_UNIQUE_NAME]", **{'type': 'xs:string'})
            if 'HIERARCHY_UNIQUE_NAME' in self.executor.mdx_query:
                xml.HIERARCHY_UNIQUE_NAME(name="[Measures].[HIERARCHY_UNIQUE_NAME]", **{'type': 'xs:string'})
        return xml

    def generate_one_axis_info(self, mdx_query_axis='columns', Axis='Axis0'):
        """
        Example AxisInfo::

            <AxesInfo>
                <AxisInfo name="Axis0">
                    <HierarchyInfo name="[Geography].[Geography]">
                        <UName name="[Geography].[Geography].[MEMBER_UNIQUE_NAME]" type="xs:string"/>
                        <Caption name="[Geography].[Geography].[MEMBER_CAPTION]" type="xs:string"/>
                        <LName name="[Geography].[Geography].[LEVEL_UNIQUE_NAME]" type="xs:string"/>
                        <LNum name="[Geography].[Geography].[LEVEL_NUMBER]" type="xs:int"/>
                        <DisplayInfo name="[Geography].[Geography].[DISPLAY_INFO]" type="xs:unsignedInt"/>
                        <PARENT_UNIQUE_NAME name="[Geography].[Geography].[PARENT_UNIQUE_NAME]" type="xs:string"/>
                        <HIERARCHY_UNIQUE_NAME name="[Geography].[Geography].[HIERARCHY_UNIQUE_NAME]" type="xs:string"/>
                    </HierarchyInfo>

                    <HierarchyInfo name="[Product].[Product]">
                        <UName name="[Product].[Product].[MEMBER_UNIQUE_NAME]" type="xs:string"/>
                        <Caption name="[Product].[Product].[MEMBER_CAPTION]" type="xs:string"/>
                        <LName name="[Product].[Product].[LEVEL_UNIQUE_NAME]" type="xs:string"/>
                        <LNum name="[Product].[Product].[LEVEL_NUMBER]" type="xs:int"/>
                        <DisplayInfo name="[Product].[Product].[DISPLAY_INFO]" type="xs:unsignedInt"/>
                        <PARENT_UNIQUE_NAME name="[Product].[Product].[PARENT_UNIQUE_NAME]" type="xs:string"/>
                        <HIERARCHY_UNIQUE_NAME name="[Product].[Product].[HIERARCHY_UNIQUE_NAME]" type="xs:string"/>
                    </HierarchyInfo>
                </AxisInfo>
            </AxesInfo>

        :param mdx_query_axis:  columns or rows (columns by default)
        :param Axis: Axis0 or Axis1 (Axis0 by default)
        :return:
        """
        # Hierarchize !!
        axis_tables = self.columns_desc[mdx_query_axis]
        xml = xmlwitch.Builder()
        # measure must be written at the top
        if axis_tables:
            with xml.AxisInfo(name=Axis):
                # many measures , then write this on the top
                if self.executor.facts in axis_tables.keys() and len(axis_tables[self.executor.facts]) > 1:
                    self._gen_measures_one_axis_info(xml)

                for table_name in axis_tables:
                    if table_name != self.executor.facts:
                        with xml.HierarchyInfo(name='[{0}].[{0}]'.format(table_name)):
                            xml.UName(name="[{0}].[{0}].[MEMBER_UNIQUE_NAME]".format(table_name),
                                      **{'type': 'xs:string'})
                            xml.Caption(name="[{0}].[{0}].[MEMBER_CAPTION]".format(table_name), **{'type': 'xs:string'})
                            xml.LName(name="[{0}].[{0}].[LEVEL_UNIQUE_NAME]".format(table_name),
                                      **{'type': 'xs:string'})
                            xml.LNum(name="[{0}].[{0}].[LEVEL_NUMBER]".format(table_name), **{'type': 'xs:int'})
                            xml.DisplayInfo(name="[{0}].[{0}].[DISPLAY_INFO]".format(table_name),
                                            **{'type': 'xs:unsignedInt'})

                            if 'Hierarchize' in self.executor.mdx_query:
                                xml.PARENT_UNIQUE_NAME(name="[{0}].[{0}].[PARENT_UNIQUE_NAME]".format(table_name),
                                                       **{'type': 'xs:string'})
                                xml.HIERARCHY_UNIQUE_NAME(name="[{0}].[{0}].[HIERARCHY_UNIQUE_NAME]".format(table_name),
                                                          **{'type': 'xs:string'})

                # Hierarchize
                if not self.executor.parser.hierarchized_tuples() and len(
                        self.columns_desc['columns'].get(self.executor.facts, [1, 1])) == 1:
                    self._gen_measures_one_axis_info(xml)

        return str(xml)

    def _generate_axes_info_convert2formulas(self):
        """
        always:

        <AxisInfo name="Axis0">
            <HierarchyInfo name="[Measures]">
                <UName name="[Measures].[MEMBER_UNIQUE_NAME]" type="xsd:string"/>
                <Caption name="[Measures].[MEMBER_CAPTION]" type="xsd:string"/>
                <LName name="[Measures].[LEVEL_UNIQUE_NAME]" type="xsd:string"/>
                <LNum name="[Measures].[LEVEL_NUMBER]" type="xsd:int"/>
                <DisplayInfo name="[Measures].[DISPLAY_INFO]" type="xsd:unsignedInt"/>
            </HierarchyInfo>
        </AxisInfo>
        <AxisInfo name="SlicerAxis">
            <HierarchyInfo name="[Geography].[Geo]">
                <UName name="[Geography].[Geo].[MEMBER_UNIQUE_NAME]" type="xsd:string"/>
                <Caption name="[Geography].[Geo].[MEMBER_CAPTION]" type="xsd:string"/>
                <LName name="[Geography].[Geo].[LEVEL_UNIQUE_NAME]" type="xsd:string"/>
                <LNum name="[Geography].[Geo].[LEVEL_NUMBER]" type="xsd:int"/>
                <DisplayInfo name="[Geography].[Geo].[DISPLAY_INFO]" type="xsd:unsignedInt"/>
            </HierarchyInfo>
            <HierarchyInfo name="[Geography].[Economy]">
                <UName name="[Geography].[Economy].[MEMBER_UNIQUE_NAME]" type="xsd:string"/>
                <Caption name="[Geography].[Economy].[MEMBER_CAPTION]" type="xsd:string"/>
                <LName name="[Geography].[Economy].[LEVEL_UNIQUE_NAME]" type="xsd:string"/>
                <LNum name="[Geography].[Economy].[LEVEL_NUMBER]" type="xsd:int"/>
                <DisplayInfo name="[Geography].[Economy].[DISPLAY_INFO]" type="xsd:unsignedInt"/>
            </HierarchyInfo>
            <HierarchyInfo name="[Product].[Prod]">
                <UName name="[Product].[Prod].[MEMBER_UNIQUE_NAME]" type="xsd:string"/>
                <Caption name="[Product].[Prod].[MEMBER_CAPTION]" type="xsd:string"/>
                <LName name="[Product].[Prod].[LEVEL_UNIQUE_NAME]" type="xsd:string"/>
                <LNum name="[Product].[Prod].[LEVEL_NUMBER]" type="xsd:int"/>
                <DisplayInfo name="[Product].[Prod].[DISPLAY_INFO]" type="xsd:unsignedInt"/>
            </HierarchyInfo>
            <HierarchyInfo name="[Time].[Calendar]">
                <UName name="[Time].[Calendar].[MEMBER_UNIQUE_NAME]" type="xsd:string"/>
                <Caption name="[Time].[Calendar].[MEMBER_CAPTION]" type="xsd:string"/>
                <LName name="[Time].[Calendar].[LEVEL_UNIQUE_NAME]" type="xsd:string"/>
                <LNum name="[Time].[Calendar].[LEVEL_NUMBER]" type="xsd:int"/>
                <DisplayInfo name="[Time].[Calendar].[DISPLAY_INFO]" type="xsd:unsignedInt"/>
            </HierarchyInfo>
        </AxisInfo>
        :return:
        """
        xml = xmlwitch.Builder()
        with xml.AxisInfo(name='Axis0'):
            # many measures , then write this on the top
            with xml.HierarchyInfo(name='[Measures]'):
                xml.UName(name="[Measures].[MEMBER_UNIQUE_NAME]", **{'type': 'xs:string'})
                xml.Caption(name="[Measures].[MEMBER_CAPTION]", **{'type': 'xs:string'})
                xml.LName(name="[Measures].[LEVEL_UNIQUE_NAME]", **{'type': 'xs:string'})
                xml.LNum(name="[Measures].[LEVEL_NUMBER]", **{'type': 'xs:int'})
                xml.DisplayInfo(name="[Measures].[DISPLAY_INFO]", **{'type': 'xs:unsignedInt'})

        return str(xml)

    def generate_axes_info(self):
        """
        :return: AxisInfo as string
        """

        if self.convert2formulas:
            return self._generate_axes_info_convert2formulas()

        if self.columns_desc['rows']:
            return """
            {0}
            {1}
            """.format(self.generate_one_axis_info(mdx_query_axis='columns', Axis='Axis0'),
                       self.generate_one_axis_info(mdx_query_axis='rows', Axis='Axis1'))

        return self.generate_one_axis_info()

    def _generate_cell_info_convert2formuls(self):
        xml = xmlwitch.Builder()
        with xml.CellInfo:
            xml.Value(name="VALUE")

        return str(xml)

    def generate_cell_info(self):

        if self.convert2formulas:
            return self._generate_cell_info_convert2formuls()

        xml = xmlwitch.Builder()
        with xml.CellInfo:
            xml.Value(name="VALUE")
            xml.FormatString(name="FORMAT_STRING", **{'type': 'xs:string'})
            xml.Language(name="LANGUAGE", **{'type': 'xs:unsignedInt'})
            xml.BackColor(name="BACK_COLOR", **{'type': 'xs:unsignedInt'})
            xml.ForeColor(name="FORE_COLOR", **{'type': 'xs:unsignedInt'})
            xml.FontFlags(name="FONT_FLAGS", **{'type': 'xs:int'})

        return str(xml)

    def generate_slicer_axis(self):
        """
        Example SlicerAxis::

            <Axis name="SlicerAxis">
                <Tuples>
                    <Tuple>
                        <Member Hierarchy="[Time].[Time]">
                            <UName>[Time].[Time].[Year].[2010]</UName>
                            <Caption>2010</Caption>
                            <LName>[Time].[Time].Year]</LName>
                            <LNum>0</LNum>
                            <DisplayInfo>2</DisplayInfo>
                        </Member>
                        <Member Hierarchy="[Measures]">
                            <UName>[Measures].[Amount]</UName>
                            <Caption>Amount</Caption>
                            <LName>[Measures]</LName>
                            <LNum>0</LNum>
                            <DisplayInfo>0</DisplayInfo>
                        </Member>
                    </Tuple>
                </Tuples>
            </Axis>

        :return: SlicerAxis as string
        """
        # not used dimensions

        if self.convert2formulas:
            return self._generate_slicer_convert2formulas()

        unused_dimensions = sorted(list(
            set(self.executor.get_all_tables_names(ignore_fact=True)) - set(
                table_name for table_name in self.columns_desc['all']))
        )
        xml = xmlwitch.Builder()
        if unused_dimensions:
            with xml.Axis(name="SlicerAxis"):
                with xml.Tuples:
                    with xml.Tuple:
                        for dim_diff in unused_dimensions:
                            column_attribut = self.executor.tables_loaded[dim_diff].iloc[0][0]
                            with xml.Member(Hierarchy="[{0}].[{0}]".format(dim_diff)):
                                xml.UName('[{0}].[{0}].[{1}].[{2}]'.format(
                                    dim_diff, self.executor.tables_loaded[dim_diff].columns[0], column_attribut))
                                xml.Caption(str(column_attribut))
                                xml.LName('[{0}].[{0}].[{1}]'.format(
                                    dim_diff, self.executor.tables_loaded[dim_diff].columns[0]))
                                xml.LNum('0')
                                xml.DisplayInfo('2')

                        # Hierarchize
                        if len(self.executor.selected_measures) <= 1 and (
                                self.executor.parser.hierarchized_tuples() or self.executor.facts in self.columns_desc['where']):
                            with xml.Member(Hierarchy="[Measures]"):
                                xml.UName('[Measures].[{0}]'.format(self.executor.measures[0]))
                                xml.Caption('{0}'.format(self.executor.measures[0]))
                                xml.LName('[Measures]')
                                xml.LNum('0')
                                xml.DisplayInfo('0')

        return str(xml)
