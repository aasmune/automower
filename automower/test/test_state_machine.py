import pytest
from automower.state_machine import AutomowerStateMachine

class TestStateMachine(object):

    def test_correct_states_after_initialiation(self):

        class TestAutomowerStateMachineInitialization(AutomowerStateMachine):
            def _update_actual_mower_status(self):
                # Hardcoded status for testing.
                self.actual_automower_status = AutomowerStateMachine.STATE_MOWING

        machine = TestAutomowerStateMachineInitialization()
        assert len(machine.states) == len(AutomowerStateMachine.STATES)
        assert machine.state == AutomowerStateMachine.STATE_MOWING
        