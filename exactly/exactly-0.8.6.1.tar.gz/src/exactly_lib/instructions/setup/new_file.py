from exactly_lib.common.instruction_setup import SingleInstructionSetup
from exactly_lib.instructions.multi_phase_instructions import new_file as new_file_utils
from exactly_lib.instructions.setup.utils import instruction_from_parts


def setup(instruction_name: str) -> SingleInstructionSetup:
    return SingleInstructionSetup(
        instruction_from_parts.Parser(new_file_utils.PARTS_PARSER),
        new_file_utils.TheInstructionDocumentation(instruction_name))
