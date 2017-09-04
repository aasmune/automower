from automower import Automower
from apscheduler.schedulers.blocking import BlockingScheduler
def foo():
    print("Hello world")
def main():
    sched = BlockingScheduler()
    automower = Automower()
    # sched.add_job(automower.execute, 'cron', second="10")
    sched.add_job(automower.execute, 'cron', second="0-30/5")
    sched.start()

if __name__ == "__main__":
    main()