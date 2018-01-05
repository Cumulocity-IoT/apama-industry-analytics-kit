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
		exprList.append('Received Data: 0')
		exprList.append('Received Data: 10.39558454088796')
		exprList.append('Received Data: 20.33683215379')
		exprList.append('Received Data: 29.38926261462366')
		exprList.append('Received Data: 37.15724127386971')
		exprList.append('Received Data: 43.30127018922194')
		exprList.append('Received Data: 47.55282581475768')
		exprList.append('Received Data: 49.72609476841367')
		exprList.append('Received Data: 49.72609476841367')
		exprList.append('Received Data: 47.55282581475768')
		exprList.append('Received Data: 43.30127018922194')
		exprList.append('Received Data: 37.15724127386972')
		exprList.append('Received Data: 29.38926261462368')
		exprList.append('Received Data: 20.33683215379002')
		exprList.append('Received Data: 10.395584540888')
		exprList.append('Received Data: 1e-14')
		exprList.append('Received Data: -10.39558454088802')
		exprList.append('Received Data: -20.33683215378995')
		exprList.append('Received Data: -29.38926261462366')
		exprList.append('Received Data: -37.15724127386973')
		exprList.append('Received Data: -43.30127018922191')
		exprList.append('Received Data: -47.55282581475767')
		exprList.append('Received Data: -49.72609476841367')
		exprList.append('Received Data: -49.72609476841368')
		exprList.append('Received Data: -47.55282581475768')
		exprList.append('Received Data: -43.30127018922192')
		exprList.append('Received Data: -37.15724127386976')
		exprList.append('Received Data: -29.38926261462369')
		exprList.append('Received Data: -20.33683215378998')
		exprList.append('Received Data: -10.39558454088806')
		self.assertOrderedGrep("OutputDataOnly.evt", exprList=exprList)

		self.assertLineCount('OutputDataOnly.evt', expr='Received Data:', condition='>=59')

		# Check for invalid data values
		self.assertLineCount('OutputDataOnly.evt', expr='INVALID DATA RECEIVED!', condition='==0')

		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("DataSimulator",\[\],\["OutputData"\],{"rangeLower":"-50","rangeUpper":"50","simulationType":"sin"}\)')
		exprList.append('Analytic DataSimulator started for inputDataNames \[\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of analytics created
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic', condition='==1')
		self.assertLineCount('correlator.out', expr='Analytic DataSimulator started', condition='==1')

		# Basic sanity checks
		self.checkSanity()
