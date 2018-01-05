# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['test.mon'], self.input)

		self.waitForSignal('correlator.out', expr='RECEIVED DATA ON TEST_DATA', condition='==6', timeout=5)

	def validate(self):
		# Basic sanity checks
		self.checkSanity()
		
		# Ensure the test output was correct
		exprList=[]
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("TEST_DATA_1","r","TEST_ASSET",0,666.6,"TEST_STRING",1,2,3,{}\)')
		exprList.append('DATA CALLBACK 1 CALLED: com.industry.analytics.Data\("TEST_DATA_2","r","TEST_ASSET",0,666.6,"TEST_STRING",1,2,3,{}\)')
		exprList.append('DATA CALLBACK 1 CALLED: com.industry.analytics.Data\("TEST_DATA_2","r","TEST_ASSET",0,666.6,"TEST_STRING",1,2,3,{}\)')
		exprList.append('DATA CALLBACK 2 CALLED: com.industry.analytics.Data\("TEST_DATA_3","r","TEST_ASSET",0,666.6,"TEST_STRING",1,2,3,{}\)')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of actions/listeners called
		self.assertLineCount('correlator.out', expr='PROCESS DATA CALLED', condition='==1')
		self.assertLineCount('correlator.out', expr='DATA CALLBACK 1 CALLED', condition='==2')
		self.assertLineCount('correlator.out', expr='DATA CALLBACK 2 CALLED', condition='==1')
		self.assertLineCount('correlator.out', expr='RECEIVED DATA ON TEST_DATA_1: com.industry.analytics.Data\("TEST_DATA_1","r","TEST_ASSET",0,666.6,"TEST_STRING",1,2,3,{}\)', condition='==3')
		self.assertLineCount('correlator.out', expr='RECEIVED DATA ON TEST_DATA_2: com.industry.analytics.Data\("TEST_DATA_2","r","TEST_ASSET",0,666.6,"TEST_STRING",1,2,3,{}\)', condition='==1')
		self.assertLineCount('correlator.out', expr='RECEIVED DATA ON TEST_DATA_3: com.industry.analytics.Data\("TEST_DATA_3","r","TEST_ASSET",0,666.6,"TEST_STRING",1,2,3,{}\)', condition='==2')
		self.assertLineCount('correlator.out', expr='RECEIVED DATA ON com.apama.queries', condition='==0')
	