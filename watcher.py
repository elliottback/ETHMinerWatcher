import subprocess
import os
import time
import re
import sys
import atexit
import logging
import signal
from yaml import CLoader as Loader
from yaml import load, dump

class Watcher:
    proc = None
    minerExecutable = None
    minerExecutableArgs = None
    afterBurnerUnclockCommand = None
    afterBurnerClockCommand = None
    dagComplete = None

    def __init__(self, config):
        self.minerExecutable = '%s' % config['miner']['executable']
        self.minerExecutableArgs = config['miner']['executable_args']
        self.afterBurnerUnclockCommand = '"%s" -%s' % (config['afterburner']['executable'], config['afterburner']['profile_normal'])
        self.afterBurnerClockCommand = '"%s" -%s' % (config['afterburner']['executable'], config['afterburner']['profile_overclocked'])
        self.dagComplete = re.compile(config['miner']['dag_complete'], flags = re.IGNORECASE )
        self.minerError = re.compile("|".join(config['miner']['error_phrases']), flags = re.IGNORECASE )

        # cleanup
        def shutdown():
            logging.warning("Shutting down...")
            if self.proc is not None:
                self.proc.kill()

        atexit.register(shutdown)

    def startMiner(self):
        cwd = os.path.dirname(self.minerExecutable)
        logging.info("Starting miner %s in %s with args %s" % (self.minerExecutable, cwd, self.minerExecutableArgs))
        self.proc = subprocess.Popen([self.minerExecutable] + self.minerExecutableArgs, cwd=cwd, stdout=subprocess.PIPE, text=True, shell=True)

    def afterburnerUnclock(self):
        logging.info("Unclocking GPU with %s" % self.afterBurnerUnclockCommand)
        if os.system(self.afterBurnerUnclockCommand) != 0:
            raise RuntimeError('Failed to unclock')
        time.sleep(1)

    def afterburnerClock(self):
        logging.info("Overclocking GPU with %s" % self.afterBurnerClockCommand)
        if os.system(self.afterBurnerClockCommand) != 0:
            raise RuntimeError('Failed to overclock')
        time.sleep(1)

    def operate(self):
        self.afterburnerUnclock()
        self.startMiner()

        while self.proc.poll() is None:
            line = self.proc.stdout.readline()

            # log them
            print(line, file=sys.stdout, end ="")

            # Matching logic
            if self.dagComplete.search(line) is not None:
                logging.info("Registered DAG complete")
                self.afterburnerClock()

            if self.minerError.search(line) is not None:
                logging.error("Registered Miner Error, giving up and trying again...")
                self.proc.send_signal(signal.SIGINT)
                time.sleep(5)
                self.proc.kill()
                return

    def run(self):
        while True:
            try:
                self.operate()
            except Exception as e:
                logging.error(e)
                time.sleep(5)


# Configuration
configFile = open( 'config.yaml', 'r' )
configData = load(configFile, Loader=Loader)

# log the config
logging.basicConfig(level=logging.INFO)
logging.info( dump( configData ) )

# Run
Watcher(configData).run();