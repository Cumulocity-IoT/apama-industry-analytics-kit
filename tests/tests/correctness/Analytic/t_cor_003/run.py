# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['AnalyticTest.mon'], self.input)
		self.waitForSignal('correlator.out', expr='TEST 10: .*', condition='==1', timeout=5)
		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('TEST 1: true')
		exprList.append('TEST 2: false')
		exprList.append('TEST 3: false')
		exprList.append('TEST 4: false')
		exprList.append('TEST 5: false')
		exprList.append('TEST 6: false')
		exprList.append('TEST 7: false')
		exprList.append('TEST 8: false')
		exprList.append('TEST 9: false')
		exprList.append('TEST 10: true')
		self.assertOrderedGrep("correlator.out", exprList=exprList)

		self.checkSanity()