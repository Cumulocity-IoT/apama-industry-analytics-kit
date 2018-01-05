import os, os.path, sys, stat, re, traceback, time, math, logging, string, thread, threading, imp

from pysys import log, ThreadedFileHandler
from pysys.constants import *
from pysys.exceptions import *
from pysys.utils.threadpool import *
from pysys.baserunner import TestContainer
from apama.runner import ApamaRunner
from copy import copy


class IndustrySolutionsRunner(ApamaRunner):
    def __init__(self, record, purge, cycle, mode, threads, outsubdir, descriptors, xargs):
        ApamaRunner.__init__(self, record, purge, cycle, mode, threads, outsubdir, descriptors, xargs)
        self.doneCycles = 1
        if xargs.has_key('level'):
        	Constants.LOG_LEVEL = xargs['level']


#    def setup(self):
#        """Setup method which performs custom setup operations prior to execution of a set of testcases.
#        
#        """
#        ApamaRunner.setup(self)


    def testComplete(self, testObj, dir):
        """Test complete method which performs completion actions after execution of a testcase.
        
        @param testObj: Reference to the L{pysys.basetest.BaseTest} instance of the test just completed
        @param dir: The directory to perform the purge on
                
        """
        # This should be in base PySys
        # Make sure that a NOTVERIFIED is actually recorded so that the output is not purged
        if len(testObj.outcome) == 0: testObj.addOutcome(NOTVERIFIED)
        ApamaRunner.testComplete(self, testObj, dir)


    def cycleComplete(self):
        """Cycle complete method which performs custom operations between the repeated execution of a set of testcases.        
        """
        self.doneCycles += 1
        ApamaRunner.cycleComplete(self)


#    def cleanup(self):
#        """Cleanup method which performs custom cleanup operations after execution of all testcases.
#        
#        """
#        ApamaRunner.cleanup(self)


    # Override the default printSummary() to list tests needing inspection
    # and any with inconsistent results across multiple test cycles. 
    def printSummary(self):
        """Print the output summary at the completion of a test run.
        
        """
        log.critical("")
        if self.threads > 1: 
            log.critical("Test duration (absolute): %.2f (secs)", time.time() - self.startTime)        
            log.critical("Test duration (additive): %.2f (secs)", self.duration)
        else:
            log.critical("Test duration: %.2f (secs)", time.time() - self.startTime)        
        log.critical("")        
        log.critical("Summary of non passes and tests requiring inspection: ")
        fails = 0
        for cycle in self.results.keys():
            for outcome in self.results[cycle].keys():
                if (outcome in FAILS) or outcome == INSPECT : fails = fails + len(self.results[cycle][outcome])
        if fails == 0:
            log.critical("    THERE WERE NO NON PASSES")
        else:
            FAILS_OR_INSPECT = copy(FAILS)
            FAILS_OR_INSPECT.append(INSPECT)
            if len(self.results) == 1:
                for outcome in FAILS_OR_INSPECT:
                    for id in self.results[0][outcome]: log.critical("  %s: %s ", LOOKUP[outcome], id)
            else:
                testFailCount = {}
                testFailList = {}
                testResults = {}
                for key in self.results.keys():
                    for outcome in FAILS_OR_INSPECT:
                        for id in self.results[key][outcome]: 
                            if not testFailCount.has_key(id):
                                testFailCount[id] = 0
                                testFailList[id] = []
                                testResults[id] = set()
                            testFailCount[id] = testFailCount[id] + 1
                            testFailList[id].append(key+1)
                            testResults[id] = testResults[id].union(set([LOOKUP[outcome]]))
                
                for test in testFailCount:
                    if len(testResults[test]) >0:
                        if testFailCount[test] == len(self.results):
                            log.critical(" %s: %s", list(testResults[test])[0], test)
                        else:
                            log.critical(" inconsistent: %s: failures: %s: in runs %s", test, list(testResults[test]),testFailList[test])
