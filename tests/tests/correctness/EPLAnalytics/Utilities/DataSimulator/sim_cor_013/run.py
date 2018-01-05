# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


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
		correlator.incrementTime(60.1)
		self.waitForSignal('OutputDataOnly.evt', expr='Received Data:', condition='>=59', timeout=5)

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Received Data: 30')
		exprList.append('Received Data: 25.84176618364479')
		exprList.append('Received Data: 21.86526713848402')
		exprList.append('Received Data: 18.24429495415054')
		exprList.append('Received Data: 15.13710349045211')
		exprList.append('Received Data: 12.67949192431124')
		exprList.append('Received Data: 10.97886967409693')
		exprList.append('Received Data: 10.10956209263453')
		exprList.append('Received Data: 10.10956209263453')
		exprList.append('Received Data: 10.97886967409693')
		exprList.append('Received Data: 12.67949192431123')
		exprList.append('Received Data: 15.1371034904521')
		exprList.append('Received Data: 18.24429495415052')
		exprList.append('Received Data: 21.86526713848401')
		exprList.append('Received Data: 25.84176618364478')
		exprList.append('Received Data: 30')
		exprList.append('Received Data: 34.15823381635519')
		exprList.append('Received Data: 38.134732861516')
		exprList.append('Received Data: 41.75570504584946')
		exprList.append('Received Data: 44.86289650954788')
		exprList.append('Received Data: 47.32050807568878')
		exprList.append('Received Data: 49.02113032590307')
		exprList.append('Received Data: 49.89043790736547')
		exprList.append('Received Data: 49.89043790736547')
		exprList.append('Received Data: 49.02113032590307')
		exprList.append('Received Data: 47.32050807568878')
		exprList.append('Received Data: 44.86289650954789')
		exprList.append('Received Data: 41.75570504584947')
		exprList.append('Received Data: 38.13473286151601')
		exprList.append('Received Data: 34.1582338163552')
		self.assertOrderedGrep("OutputDataOnly.evt", exprList=exprList)

		self.assertLineCount('OutputDataOnly.evt', expr='Received Data:', condition='>=59')

		# Check for invalid data values
		self.assertLineCount('OutputDataOnly.evt', expr='INVALID DATA RECEIVED!', condition='==0')

		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("DataSimulator",\[\],\["OutputData"\],{"rangeLower":"10","rangeUpper":"50","simulationType":"sin"}\)')
		exprList.append('Analytic DataSimulator started for inputDataNames \[\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of analytics created
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic', condition='==1')
		self.assertLineCount('correlator.out', expr='Analytic DataSimulator started', condition='==1')

		# Basic sanity checks
		self.checkSanity()
