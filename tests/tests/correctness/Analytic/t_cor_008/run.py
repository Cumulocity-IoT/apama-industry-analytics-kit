# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['AnalyticTest.mon'], self.input)
		self.waitForSignal('correlator.out', expr='TEST 2: .*', condition='==1', timeout=5)
		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		# Testing with mandatory values
		exprList.append('Validating com.industry.analytics.Analytic\("Test",\[.*\],\[.*\],{.*}\)')
		exprList.append('TEST 1: true')
		# Testing with non-mandatory values		
		exprList.append('Validating com.industry.analytics.Analytic\("Test",\[.*\],\[.*\],{.*}\)')
		exprList.append('TEST 2: true')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that we got no errors
		self.assertLineCount('correlator.out', expr='Unable to parse param .*', condition='==0')

		self.checkSanity()