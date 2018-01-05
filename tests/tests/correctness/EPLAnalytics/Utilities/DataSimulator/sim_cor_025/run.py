# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest


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
		self.waitForSignal('OutputDataOnly.evt', expr='Received Data: ', condition='>=59', timeout=5)

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Received Data: -50')
		exprList.append('Received Data: -49')
		exprList.append('Received Data: -48')
		exprList.append('Received Data: -47')
		exprList.append('Received Data: -46')
		exprList.append('Received Data: -45')
		exprList.append('Received Data: -44')
		exprList.append('Received Data: -43')
		exprList.append('Received Data: -42')
		exprList.append('Received Data: -41')
		exprList.append('Received Data: -40')
		exprList.append('Received Data: -39')
		exprList.append('Received Data: -38')
		exprList.append('Received Data: -37')
		exprList.append('Received Data: -36')
		exprList.append('Received Data: -35')
		exprList.append('Received Data: -34')
		exprList.append('Received Data: -33')
		exprList.append('Received Data: -32')
		exprList.append('Received Data: -31')
		exprList.append('Received Data: -30')
		exprList.append('Received Data: -29')
		exprList.append('Received Data: -28')
		exprList.append('Received Data: -27')
		exprList.append('Received Data: -26')
		exprList.append('Received Data: -25')
		exprList.append('Received Data: -24')
		exprList.append('Received Data: -23')
		exprList.append('Received Data: -22')
		exprList.append('Received Data: -21')
		exprList.append('Received Data: -50')
		self.assertOrderedGrep("OutputDataOnly.evt", exprList=exprList)

		self.assertLineCount('OutputDataOnly.evt', expr='Received Data: ', condition='>=59')

		# Check for invalid data values
		self.assertLineCount('OutputDataOnly.evt', expr='INVALID DATA RECEIVED!', condition='==0')

		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("DataSimulator",\[\],\["OutputData"\],{"rangeLower":"-50","rangeUpper":"-20","simulationType":"sawrising"}\)')
		exprList.append('Analytic DataSimulator started for inputDataNames \[\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of analytics created
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic', condition='==1')
		self.assertLineCount('correlator.out', expr='Analytic DataSimulator started', condition='==1')

		# Basic sanity checks
		self.checkSanity()