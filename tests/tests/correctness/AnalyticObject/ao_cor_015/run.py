# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest
from pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['test.mon'], self.input)

		self.waitForSignal('correlator.out', expr='PROCESS DATA CALLED:', condition='==16', timeout=5)

	def validate(self):
		# Basic sanity checks
		self.checkSanity()
		
		# Ensure the test output was correct
		exprList=[]
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input1","r","TEST_ASSET_1",0,111.1,"TEST_STRING_1",1,2,3,{}\)')
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input1","r","TEST_ASSET_2",0,222.2,"TEST_STRING_2",1,2,3,{}\)')
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input2","r","TEST_ASSET_3",0,333.3,"TEST_STRING_3",1,2,3,{}\)')
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input2","r","TEST_ASSET_4",0,444.4,"TEST_STRING_4",1,2,3,{}\)')
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input1","r","TEST_ASSET_1",0,111.1,"TEST_STRING_1",1,2,3,{}\)')
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input1","r","TEST_ASSET_2",0,222.2,"TEST_STRING_2",1,2,3,{}\)')
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input2","r","TEST_ASSET_3",0,333.3,"TEST_STRING_3",1,2,3,{}\)')
		exprList.append('PROCESS DATA CALLED: com.industry.analytics.Data\("Input2","r","TEST_ASSET_4",0,444.4,"TEST_STRING_4",1,2,3,{}\)')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of actions/listeners called
		self.assertLineCount('correlator.out', expr='PROCESS DATA CALLED: com.industry.analytics.Data\("Input1","r","TEST_ASSET_1",0,111.1,"TEST_STRING_1",1,2,3,{}\)', condition='==4')
		self.assertLineCount('correlator.out', expr='PROCESS DATA CALLED: com.industry.analytics.Data\("Input1","r","TEST_ASSET_2",0,222.2,"TEST_STRING_2",1,2,3,{}\)', condition='==4')
		self.assertLineCount('correlator.out', expr='PROCESS DATA CALLED: com.industry.analytics.Data\("Input2","r","TEST_ASSET_3",0,333.3,"TEST_STRING_3",1,2,3,{}\)', condition='==4')
		self.assertLineCount('correlator.out', expr='PROCESS DATA CALLED: com.industry.analytics.Data\("Input2","r","TEST_ASSET_4",0,444.4,"TEST_STRING_4",1,2,3,{}\)', condition='==4')
		self.assertLineCount('correlator.out', expr='PROCESS DATA CALLED:', condition='==16')
	