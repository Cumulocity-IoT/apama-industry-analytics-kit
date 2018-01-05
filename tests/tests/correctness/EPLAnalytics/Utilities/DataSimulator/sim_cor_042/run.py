# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest
from pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectDataSimulator(correlator)
		self.ready(correlator)
		correlator.receive(filename='RawOutputData.evt',  channels=['OutputData'])
		correlator.receive(filename='OutputDataOnly.evt', channels=['OUTPUT_DATA_ONLY'])
		correlator.injectMonitorscript(['test.mon'], self.input)

		# Run the simulator for just over 60 seconds so that we get 60 data points generated
		correlator.incrementTime(61)
		self.waitForSignal('OutputDataOnly.evt', expr='Received Data: sourceId:ID_1 dValue:', condition='>=59', timeout=5)
		self.waitForSignal('OutputDataOnly.evt', expr='Received Data: sourceId:ID_2 dValue:', condition='>=59', timeout=5)
		self.waitForSignal('OutputDataOnly.evt', expr='Received Data: sourceId:ID_3 dValue:', condition='>=59', timeout=5)

		
	def validate(self):
		# If there are extra JAR files to include
		for sourceId in [1,2,3] :
			# Ensure the test output was correct
			exprList=[]
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:0'%sourceId)
			exprList.append('Received Data: sourceId:ID_%s dValue:50'%sourceId)
			self.assertOrderedGrep("OutputDataOnly.evt", exprList=exprList)

			self.assertLineCount('OutputDataOnly.evt', expr='Received Data: sourceId:ID_%s dValue:'%sourceId, condition='>=59')

		# Check for invalid data values
		self.assertLineCount('OutputDataOnly.evt', expr='INVALID DATA RECEIVED!', condition='==0')

		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("DataSimulator",\[\],\["OutputData"\],{"dataRateUnit":"perMinute","dataRateValue":"60","rangeLower":"0","rangeUpper":"50","simulationType":"square","sourceIdCount":"3","sourceIdPrefix":"ID_"}\)')
		exprList.append('Analytic DataSimulator started for inputDataNames \[\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of analytics created
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic', condition='==1')
		self.assertLineCount('correlator.out', expr='Analytic DataSimulator started', condition='==1')

		# Basic sanity checks
		self.checkSanity()
