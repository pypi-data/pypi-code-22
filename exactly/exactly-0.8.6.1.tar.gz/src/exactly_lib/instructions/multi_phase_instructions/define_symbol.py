from exactly_lib.common.help.instruction_documentation_with_text_parser import \
    InstructionDocumentationThatIsNotMeantToBeAnAssertionInAssertPhaseBase
from exactly_lib.common.help.syntax_contents_structure import InvokationVariant, SyntaxElementDescription
from exactly_lib.help_texts import instruction_arguments, formatting
from exactly_lib.help_texts import syntax_descriptions
from exactly_lib.help_texts.argument_rendering import cl_syntax
from exactly_lib.help_texts.cross_ref import name_and_cross_ref
from exactly_lib.help_texts.doc_format import syntax_text
from exactly_lib.help_texts.entity import types, syntax_elements, concepts
from exactly_lib.help_texts.entity.types import TypeNameAndCrossReferenceId
from exactly_lib.help_texts.test_case.instructions import define_symbol as syntax
from exactly_lib.instructions.multi_phase_instructions.utils import instruction_embryo as embryo
from exactly_lib.instructions.multi_phase_instructions.utils.assert_phase_info import IsAHelperIfInAssertPhase
from exactly_lib.instructions.multi_phase_instructions.utils.instruction_part_utils import PartsParserFromEmbryoParser, \
    MainStepResultTranslatorForErrorMessageStringResultAsHardError
from exactly_lib.instructions.utils.documentation import relative_path_options_documentation as rel_path_doc
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.parser_implementations.instruction_parser_for_single_phase import \
    SingleInstructionInvalidArgumentException
from exactly_lib.section_document.parser_implementations.misc_utils import new_token_stream
from exactly_lib.section_document.parser_implementations.token_stream import TokenStream
from exactly_lib.section_document.parser_implementations.token_stream_parse_prime import TokenParserPrime
from exactly_lib.symbol import symbol_syntax
from exactly_lib.symbol.data.list_resolver import ListResolver
from exactly_lib.symbol.data.string_resolver import StringResolver
from exactly_lib.symbol.resolver_structure import SymbolContainer, DataValueResolver, \
    FileMatcherResolver, LineMatcherResolver
from exactly_lib.symbol.symbol_usage import SymbolDefinition
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep, PhaseLoggingPaths
from exactly_lib.test_case_file_structure.path_relativity import PathRelativityVariants, RelOptionType
from exactly_lib.test_case_utils.file_matcher import parse_file_matcher
from exactly_lib.test_case_utils.line_matcher import parse_line_matcher
from exactly_lib.test_case_utils.lines_transformer import resolvers as line_transformer_resolvers, \
    parse_lines_transformer
from exactly_lib.test_case_utils.lines_transformer.transformers import IdentityLinesTransformer
from exactly_lib.test_case_utils.parse import parse_file_ref, parse_list
from exactly_lib.test_case_utils.parse.parse_string import parse_string_resolver
from exactly_lib.test_case_utils.parse.rel_opts_configuration import RelOptionArgumentConfiguration, \
    RelOptionsConfiguration
from exactly_lib.util.symbol_table import SymbolTable
from exactly_lib.util.textformat.structure import structures as docs


class TheInstructionDocumentation(InstructionDocumentationThatIsNotMeantToBeAnAssertionInAssertPhaseBase,
                                  IsAHelperIfInAssertPhase):
    def __init__(self, name: str, is_in_assert_phase: bool = False):
        self.name = syntax_elements.SYMBOL_NAME_SYNTAX_ELEMENT.argument
        self.string_value = syntax_elements.STRING_SYNTAX_ELEMENT.argument
        super().__init__(name,
                         {
                             'NAME': self.name.name,
                             'current_directory_concept': formatting.concept_(
                                 concepts.CURRENT_WORKING_DIRECTORY_CONCEPT_INFO),
                             'PATH_ARG': _PATH_ARGUMENT.name,
                         },
                         is_in_assert_phase)

    def single_line_description(self) -> str:
        return self._format('Defines a ' + concepts.SYMBOL_CONCEPT_INFO.singular_name)

    def _main_description_rest_body(self) -> list:
        return self._tp.fnap(_MAIN_DESCRIPTION_REST)

    def invokation_variants(self) -> list:
        return [
            InvokationVariant(
                cl_syntax.cl_syntax_for_args(syntax.def_instruction_argument_syntax())
            )
        ]

    def syntax_element_descriptions(self) -> list:
        return ([
                    SyntaxElementDescription(', '.join([syntax.TYPE_SYNTAX_ELEMENT,
                                                        syntax.VALUE_SYNTAX_ELEMENT]),
                                             [self._types_table()]),
                ]
                + rel_path_doc.path_elements(_PATH_ARGUMENT.name,
                                             REL_OPTION_ARGUMENT_CONFIGURATION.options,
                                             self._tp.fnap(_REL_CD_DESCRIPTION))
                +
                [
                    SyntaxElementDescription(self.string_value.name,
                                             self._paragraphs(syntax_descriptions.STRING_SYNTAX_ELEMENT_DESCRIPTION)),
                    SyntaxElementDescription(self.name.name,
                                             self._paragraphs(syntax_descriptions.SYMBOL_NAME_SYNTAX_DESCRIPTION)),
                ])

    def see_also_targets(self) -> list:
        name_and_cross_refs = [concepts.SYMBOL_CONCEPT_INFO,
                               syntax_elements.SYMBOL_NAME_SYNTAX_ELEMENT,
                               concepts.TYPE_CONCEPT_INFO,
                               concepts.CURRENT_WORKING_DIRECTORY_CONCEPT_INFO,
                               ]
        name_and_cross_refs += types.ALL_TYPES_INFO_TUPLE
        return name_and_cross_ref.cross_reference_id_list(name_and_cross_refs)

    @staticmethod
    def _types_table() -> docs.ParagraphItem:
        def type_row(type_info: TypeNameAndCrossReferenceId) -> list:
            type_syntax_info = syntax.ANY_TYPE_INFO_DICT[type_info.value_type]
            return [
                docs.text_cell(syntax_text(type_info.identifier)),
                docs.text_cell(syntax_text(cl_syntax.cl_syntax_for_args(type_syntax_info.value_arguments))),
            ]

        rows = [
            [
                docs.text_cell(syntax.TYPE_SYNTAX_ELEMENT),
                docs.text_cell(syntax.VALUE_SYNTAX_ELEMENT),
            ]
        ]

        rows += map(type_row, types.ALL_TYPES_INFO_TUPLE)

        return docs.first_row_is_header_table(rows)


class TheInstructionEmbryo(embryo.InstructionEmbryo):
    def __init__(self, symbol: SymbolDefinition):
        self.symbol = symbol

    @property
    def symbol_usages(self) -> list:
        return [self.symbol]

    def main(self,
             environment: InstructionEnvironmentForPostSdsStep,
             logging_paths: PhaseLoggingPaths,
             os_services: OsServices):
        self.custom_main(environment.symbols)
        return None

    def custom_main(self, named_elems: SymbolTable):
        named_elems.put(self.symbol.name,
                        self.symbol.resolver_container)


class EmbryoParser(embryo.InstructionEmbryoParser):
    def parse(self, source: ParseSource) -> TheInstructionEmbryo:
        definition = _parse(source)
        return TheInstructionEmbryo(definition)


PARTS_PARSER = PartsParserFromEmbryoParser(EmbryoParser(),
                                           MainStepResultTranslatorForErrorMessageStringResultAsHardError())


def _parse(source: ParseSource) -> SymbolDefinition:
    source_line = source.current_line
    token_stream = new_token_stream(source.remaining_part_of_current_line)
    source.consume_current_line()
    if token_stream.is_null:
        err_msg = 'Missing symbol type.\nExpecting one of ' + _TYPES_LIST_IN_ERR_MSG
        raise SingleInstructionInvalidArgumentException(err_msg)
    type_token = token_stream.head
    if type_token.source_string not in _TYPE_SETUPS:
        err_msg = 'Invalid type :{}\nExpecting one of {}'.format(type_token.source_string, _TYPES_LIST_IN_ERR_MSG)
        raise SingleInstructionInvalidArgumentException(err_msg)
    value_parser = _TYPE_SETUPS[type_token.source_string]
    token_stream.consume()
    if token_stream.is_null:
        err_msg = 'Missing symbol name.'
        raise SingleInstructionInvalidArgumentException(err_msg)
    name_token = token_stream.head
    if name_token.is_quoted:
        raise SingleInstructionInvalidArgumentException('Name cannot be quoted: ' + name_token.source_string)
    name_str = name_token.string
    if not symbol_syntax.is_symbol_name(name_str):
        err_msg = symbol_syntax.invalid_symbol_name_error(name_str)
        raise SingleInstructionInvalidArgumentException(err_msg)
    token_stream.consume()
    if token_stream.is_null or token_stream.head.source_string != syntax.EQUALS_ARGUMENT:
        raise SingleInstructionInvalidArgumentException('Missing ' + syntax.EQUALS_ARGUMENT)
    token_stream.consume()
    value_resolver = value_parser(token_stream)
    if not token_stream.is_null:
        msg = 'Superfluous arguments: ' + token_stream.remaining_part_of_current_line
        raise SingleInstructionInvalidArgumentException(msg)
    return SymbolDefinition(name_str, SymbolContainer(value_resolver, source_line))


_PATH_ARGUMENT = instruction_arguments.PATH_ARGUMENT

REL_OPTIONS_CONFIGURATION = RelOptionsConfiguration(
    PathRelativityVariants(frozenset(RelOptionType), True),
    RelOptionType.REL_CWD)

REL_OPTION_ARGUMENT_CONFIGURATION = RelOptionArgumentConfiguration(REL_OPTIONS_CONFIGURATION,
                                                                   instruction_arguments.PATH_ARGUMENT,
                                                                   syntax.PATH_SUFFIX_IS_REQUIRED)

_MAIN_DESCRIPTION_REST = """\
Defines the symbol {NAME} to be a value of the given type.


{NAME} must not have been defined earlier.
"""

_REL_CD_DESCRIPTION = """\
NOTE: When a {PATH_ARG} is defined to be relative the {current_directory_concept},

it means that it is relative the directory that is current when the symbol is USED,

not when it is defined!
"""


def _parse_path(token_stream: TokenStream) -> DataValueResolver:
    return parse_file_ref.parse_file_ref(token_stream, REL_OPTION_ARGUMENT_CONFIGURATION)


def _parse_string(token_stream: TokenStream) -> StringResolver:
    return parse_string_resolver(token_stream)


def _parse_list(token_stream: TokenStream) -> ListResolver:
    return parse_list.parse_list_from_token_stream_that_consume_whole_source__TO_REMOVE(token_stream)


def _parse_line_matcher(token_stream: TokenStream) -> LineMatcherResolver:
    token_parser = TokenParserPrime(token_stream)
    if token_parser.is_at_eol:
        return parse_line_matcher.CONSTANT_TRUE_MATCHER_RESOLVER
    else:
        return parse_line_matcher.parse_line_matcher_from_token_parser(token_parser)


def _parse_file_matcher(token_stream: TokenStream) -> FileMatcherResolver:
    token_parser = TokenParserPrime(token_stream)
    if token_parser.is_at_eol:
        return parse_file_matcher.SELECTION_OF_ALL_FILES
    else:
        return parse_file_matcher.parse_resolver(token_parser)


def _parse_lines_transformer(token_stream: TokenStream) -> line_transformer_resolvers.LinesTransformerResolver:
    token_parser = TokenParserPrime(token_stream)
    if token_parser.is_at_eol:
        return line_transformer_resolvers.LinesTransformerConstant(IdentityLinesTransformer())
    return parse_lines_transformer.parse_lines_transformer_from_token_parser(token_parser)


_TYPE_SETUPS = {
    types.PATH_TYPE_INFO.identifier: _parse_path,
    types.STRING_TYPE_INFO.identifier: _parse_string,
    types.LIST_TYPE_INFO.identifier: _parse_list,
    types.LINE_MATCHER_TYPE_INFO.identifier: _parse_line_matcher,
    types.FILE_MATCHER_TYPE_INFO.identifier: _parse_file_matcher,
    types.LINES_TRANSFORMER_TYPE_INFO.identifier: _parse_lines_transformer,
}

_TYPES_LIST_IN_ERR_MSG = '|'.join(sorted(_TYPE_SETUPS.keys()))
