# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['AnalyticTest.mon'], self.input)
		self.waitForSignal('correlator.out', expr='TEST COMPLETE', condition='==1', timeout=5)
		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('TEST param: param01 getOr false: true getOr true: true get: true')
		exprList.append('TEST param: param02 getOr false: false getOr true: false get: false')
		exprList.append('TEST param: param03 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param04 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param05 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param06 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param07 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param08 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param09 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param10 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param11 getOr false: true getOr true: true get: true')
		exprList.append('TEST param: param12 getOr false: false getOr true: false get: false')
		exprList.append('TEST param: param13 getOr false: true getOr true: true get: true')
		exprList.append('TEST param: param14 getOr false: false getOr true: false get: false')
		exprList.append('TEST param: param15 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param16 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param17 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param18 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param19 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param20 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param21 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param22 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param23 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param24 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param25 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param26 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param27 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param28 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param29 getOr false: false getOr true: true get: false')
		exprList.append('TEST param: param30 getOr false: false getOr true: true get: false')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that we got the right number of test results
		self.assertLineCount('correlator.out', expr='TEST param: .*', condition='==30')

		self.checkSanity()