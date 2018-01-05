# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['AnalyticTest.mon'], self.input)
		self.waitForSignal('correlator.out', expr='TEST 3: .*', condition='==1', timeout=5)
		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		# Testing with mandatory values
		exprList.append('Validating com.industry.analytics.Analytic\("Test",\[.*\],\[.*\],{.*}\)')
		exprList.append('Unable to parse param param01 as sequence<string>')
		exprList.append('Unable to parse param param02 as sequence<string>')
		exprList.append('Unable to parse param param03 as sequence<string>')
		exprList.append('Unable to parse param param04 as sequence<string>')
		exprList.append('Unable to parse param param05 as sequence<string>')
		exprList.append('Unable to parse param param06 as sequence<string>')
		exprList.append('Unable to parse param param07 as sequence<string>')
		exprList.append('Unable to parse param param08 as sequence<string>')
		exprList.append('Unable to parse param param09 as sequence<string>')
		exprList.append('Unable to parse param param10 as sequence<string>')
		exprList.append('Unable to parse param param11 as sequence<string>')
		exprList.append('Unable to parse param param12 as sequence<string>')
		exprList.append('Unable to parse param param13 as sequence<string>')
		exprList.append('Unable to parse param param14 as sequence<string>')
		exprList.append('Unable to parse param param15 as sequence<string>')
		exprList.append('Unable to parse param param17 as sequence<string>')
		exprList.append('Unable to parse param param19 as sequence<string>')
		exprList.append('Unable to parse param param20 as sequence<string>')
		exprList.append('Unable to parse param param21 as sequence<string>')
		exprList.append('Unable to parse param param22 as sequence<string>')
		exprList.append('Unable to parse param param26 as sequence<string>')
		exprList.append('Unable to parse param param27 as sequence<string>')
		exprList.append('TEST 1: false')
		# Testing with non-mandatory values		
		exprList.append('Validating com.industry.analytics.Analytic\("Test",\[.*\],\[.*\],{.*}\)')
		exprList.append('Unable to parse param param01 as sequence<string>')
		exprList.append('Unable to parse param param02 as sequence<string>')
		exprList.append('Unable to parse param param03 as sequence<string>')
		exprList.append('Unable to parse param param04 as sequence<string>')
		exprList.append('Unable to parse param param05 as sequence<string>')
		exprList.append('Unable to parse param param06 as sequence<string>')
		exprList.append('Unable to parse param param07 as sequence<string>')
		exprList.append('Unable to parse param param08 as sequence<string>')
		exprList.append('Unable to parse param param09 as sequence<string>')
		exprList.append('Unable to parse param param10 as sequence<string>')
		exprList.append('Unable to parse param param11 as sequence<string>')
		exprList.append('Unable to parse param param12 as sequence<string>')
		exprList.append('Unable to parse param param13 as sequence<string>')
		exprList.append('Unable to parse param param14 as sequence<string>')
		exprList.append('Unable to parse param param15 as sequence<string>')
		exprList.append('Unable to parse param param17 as sequence<string>')
		exprList.append('Unable to parse param param19 as sequence<string>')
		exprList.append('Unable to parse param param20 as sequence<string>')
		exprList.append('Unable to parse param param21 as sequence<string>')
		exprList.append('Unable to parse param param22 as sequence<string>')
		exprList.append('Unable to parse param param26 as sequence<string>')
		exprList.append('Unable to parse param param27 as sequence<string>')
		exprList.append('TEST 2: false')
		# Testing with only the valid values
		exprList.append('Validating com.industry.analytics.Analytic\("Test",\[.*\],\[.*\],{.*}\)')
		exprList.append('TEST 3: true')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the first two parameters didn't fail parsing
		self.assertLineCount('correlator.out', expr='Unable to parse param param16 as sequence<string>', condition='==0')
		self.assertLineCount('correlator.out', expr='Unable to parse param param18 as sequence<string>', condition='==0')
		self.assertLineCount('correlator.out', expr='Unable to parse param param23 as sequence<string>', condition='==0')
		self.assertLineCount('correlator.out', expr='Unable to parse param param24 as sequence<string>', condition='==0')
		self.assertLineCount('correlator.out', expr='Unable to parse param param25 as sequence<string>', condition='==0')
		# ... and that we got the correct number of errors
		self.assertLineCount('correlator.out', expr='Unable to parse param', condition='==44')

		self.checkSanity()