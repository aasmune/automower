# from transitions import Machine
from transitions.extensions import LockedHierarchicalGraphMachine as Machine

class AutomowerStateMachine(Machine):

    STATE_INITIAL = 'INITIAL'
    STATE_MOWING = 'MOWING'
    STATE_SEARCHING = 'SEARCHING'
    STATE_CHARGING = 'CHARGING'
    STATE_PARKED = 'PARKED'
    STATE_STOPPED = 'STOPPED'

    STATES = [STATE_INITIAL,
              STATE_MOWING,
              STATE_SEARCHING,
              STATE_CHARGING,
              STATE_PARKED,
              STATE_STOPPED]

    def __init__(self):

        # Actual status of automower. Is updated before each run
        self.actual_automower_status = AutomowerStateMachine.STATE_INITIAL

        super().__init__(states=AutomowerStateMachine.STATES, initial=AutomowerStateMachine.STATE_INITIAL)

        # Transitions from initialize
        self.add_transition(trigger='initialize', 
                            source=AutomowerStateMachine.STATE_INITIAL, 
                            dest=AutomowerStateMachine.STATE_MOWING,
                            prepare='_update_actual_mower_status',
                            conditions='_is_mowing')

        self.add_transition(trigger='initialize', 
                            source=AutomowerStateMachine.STATE_INITIAL, 
                            dest=AutomowerStateMachine.STATE_SEARCHING,
                            prepare='_update_actual_mower_status',
                            conditions=['_is_searching'])

        self.add_transition(trigger='initialize', 
                            source=AutomowerStateMachine.STATE_INITIAL, 
                            dest=AutomowerStateMachine.STATE_CHARGING,
                            prepare='_update_actual_mower_status',
                            conditions=['_is_charging'])

        self.add_transition(trigger='initialize', 
                            source=AutomowerStateMachine.STATE_INITIAL, 
                            dest=AutomowerStateMachine.STATE_PARKED,
                            prepare='_update_actual_mower_status',
                            conditions=['_is_parked'])

        self.add_transition(trigger='initialize', 
                            source=AutomowerStateMachine.STATE_INITIAL, 
                            dest=AutomowerStateMachine.STATE_STOPPED,
                            prepare='_update_actual_mower_status',
                            conditions=['_is_stopped'])

        # park automower
        self.add_transition(trigger='rain',
                            source=AutomowerStateMachine.STATE_MOWING,
                            dest=AutomowerStateMachine.STATE_SEARCHING,
                            prepare='_update_actual_mower_status',
                            before='_park')

        self.add_transition(trigger='rain',
                            source='*',
                            dest='=',
                            prepare='_update_actual_mower_status',
                            before='_park')
        
        # start automower
        self.add_transition(trigger='clear', 
                            source=AutomowerStateMachine.STATE_PARKED,
                            dest=AutomowerStateMachine.STATE_CHARGING,
                            prepare='_update_actual_mower_status',
                            conditions='_is_docked',
                            before='_start')

        self.add_transition(trigger='clear', 
                            source=AutomowerStateMachine.STATE_PARKED,
                            dest=AutomowerStateMachine.STATE_MOWING,
                            prepare='_update_actual_mower_status',
                            unless='_is_docked',
                            before='_start')

        self.add_transition(trigger='clear', 
                            source="*",
                            dest="=",
                            prepare='_update_actual_mower_status',
                            before='_start')

        self.initialize()

    def _update_actual_mower_status(self):
        """ Get the actual mower status before transition begins"""

        # Hardcoded status for proof of concept.
        self.actual_automower_status = AutomowerStateMachine.STATE_STOPPED

    def _is_mowing(self):
        return self.actual_automower_status == AutomowerStateMachine.STATE_MOWING

    def _is_searching(self):
        return self.actual_automower_status == AutomowerStateMachine.STATE_SEARCHING

    def _is_charging(self):
        return self.actual_automower_status == AutomowerStateMachine.STATE_CHARGING

    def _is_parked(self):
        return self.actual_automower_status == AutomowerStateMachine.STATE_PARKED

    def _is_stopped(self):
        return self.actual_automower_status == AutomowerStateMachine.STATE_STOPPED

    def _is_docked(self):
        return self._is_parked() or self._is_charging()

    def _start(self):
        """ Start automower"""
        print("Automower start")
    
    def _park(self):
        """ Park automower"""
        print("Automower park")

if __name__ == '__main__':
    automower = AutomowerStateMachine()
    print(automower.state)
    automower.start()
    print(automower.state)
    automower.rain()
    print(automower.state)

    #automower.get_graph().draw('state_diagram.png', prog='dot')
    
    
