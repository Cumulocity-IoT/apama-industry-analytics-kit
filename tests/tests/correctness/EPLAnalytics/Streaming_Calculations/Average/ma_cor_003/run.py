# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest
from pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectAverage(correlator)
		self.ready(correlator)
		correlator.injectMonitorscript(['test.mon'], self.input)

		self.waitForSignal('correlator.out', expr='TEST COMPLETE', condition='==1', timeout=5)

	def validate(self):
		# Basic sanity checks
		self.checkSanity()

		# Ensure the test output was correct
		exprList=[]
		exprList.append('FAILED TO CREATE ANALYTIC: 1')
		exprList.append('TEST PASSED: 2')
		exprList.append('FAILED TO CREATE ANALYTIC: 3')
		exprList.append('FAILED TO CREATE ANALYTIC: 4')
		exprList.append('FAILED TO CREATE ANALYTIC: 5')
		exprList.append('FAILED TO CREATE ANALYTIC: 6')
		exprList.append('FAILED TO CREATE ANALYTIC: 7')
		exprList.append('FAILED TO CREATE ANALYTIC: 8')
		exprList.append('FAILED TO CREATE ANALYTIC: 9')
		exprList.append('FAILED TO CREATE ANALYTIC: 10')
		exprList.append('FAILED TO CREATE ANALYTIC: 11')
		exprList.append('FAILED TO CREATE ANALYTIC: 12')
		exprList.append('FAILED TO CREATE ANALYTIC: 13')
		exprList.append('FAILED TO CREATE ANALYTIC: 14')
		exprList.append('FAILED TO CREATE ANALYTIC: 15')
		exprList.append('FAILED TO CREATE ANALYTIC: 16')
		exprList.append('FAILED TO CREATE ANALYTIC: 17')
		exprList.append('TEST PASSED: 18')
		exprList.append('TEST PASSED: 19')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of actions/listeners called
		self.assertLineCount('correlator.out', expr='TEST PASSED', condition='==3')
		self.assertLineCount('correlator.out', expr='FAILED TO CREATE ANALYTIC:', condition='==16')

		