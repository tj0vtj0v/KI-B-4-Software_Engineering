from src.helper.Action import Action
from src.program.DefrostingProgram import DefrostingProgram
from src.program.Program import Program


class MockUserInteractionHandler:
    run_once = False

    def get_interactions(self) -> tuple[Action | None, Program | None]:
        if not self.run_once:
            self.run_once = True
            return Action.START, DefrostingProgram()

        return None, None

    def update_display(self, program_name: str, running: bool, finished: bool, paused: bool):
        pass
