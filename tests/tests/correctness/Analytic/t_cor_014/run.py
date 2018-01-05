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
		exprList.append('TEST param: param01 getOr: true get: true')
		exprList.append('TEST param: param02 getOr: false get: false')
		exprList.append('TEST param: param03 getOr: 1 get: 1')
		exprList.append('TEST param: param04 getOr: 0 get: 0')
		exprList.append('TEST param: param05 getOr: -1 get: -1')
		exprList.append('TEST param: param06 getOr: 1.0 get: 1.0')
		exprList.append('TEST param: param07 getOr: 0.0 get: 0.0')
		exprList.append('TEST param: param08 getOr: -1.0 get: -1.0')
		exprList.append('TEST param: param09 getOr: 666 get: 666')
		exprList.append('TEST param: param10 getOr: -666 get: -666')
		exprList.append('TEST param: param11 getOr: TRUE get: TRUE')
		exprList.append('TEST param: param12 getOr: FALSE get: FALSE')
		exprList.append('TEST param: param13 getOr: True get: True')
		exprList.append('TEST param: param14 getOr: False get: False')
		exprList.append('TEST param: param15 getOr: Foo get: Foo')
		exprList.append('TEST param: param16 getOr: {} get: {}')
		exprList.append('TEST param: param17 getOr: \[ get: \[')
		exprList.append('TEST param: param18 getOr: \] get: \]')
		exprList.append('TEST param: param19 getOr: \[\] get: \[\]')
		exprList.append('TEST param: param20 getOr: \[\[\] get: \[\[\]')
		exprList.append('TEST param: param21 getOr: \[\]\] get: \[\]\]')
		exprList.append('TEST param: param22 getOr: \[1\] get: \[1\]')
		exprList.append('TEST param: param23 getOr: \[1.1\] get: \[1.1\]')
		exprList.append('TEST param: param24 getOr: \[foo\] get: \[foo\]')
		exprList.append('TEST param: param25 getOr: \[foo,bar\] get: \[foo,bar\]')
		exprList.append('TEST param: param26 getOr: \["foo"\] get: \["foo"\]')
		exprList.append('TEST param: param27 getOr: \["foo","1"\] get: \["foo","1"\]')
		exprList.append('TEST param: param28 getOr: \["\[\]"\] get: \["\[\]"\]')
		exprList.append('TEST param: param29 getOr:  get: ')
		exprList.append('TEST param: param30 getOr:    get:   ')
		self.assertOrderedGrep("correlator.out", exprList=exprList)

		# Make sure that we got the right number of test results
		self.assertLineCount('correlator.out', expr='TEST param: .*', condition='==30')

		self.checkSanity()