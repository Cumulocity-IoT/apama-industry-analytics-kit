# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile='correlator.log', logLevel="DEBUG")
		self.injectAnalytic(correlator)
		self.injectDrift(correlator)
		self.ready(correlator)
		correlator.receive(filename='OutputValue.evt', channels=['OutputValue'])
		correlator.receive(filename='OutputPercentage.evt', channels=['OutputPercentage'])
		correlator.receive(filename='OutputStandardDeviation.evt', channels=['OutputStandardDeviation'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.log',
						   expr='Analytic Drift started for inputDataNames',
						   condition='==3',
						   timeout=5)

		correlator.send('BaselineMeasures.evt')
		self.waitForSignal('correlator.log',
						   expr='Boundaries for sourceId',
						   condition='==3',
						   timeout=5)

		correlator.send('ThresholdMeasures.evt')
		self.waitForSignal('OutputStandardDeviation.evt',
						   expr='com\.industry\.analytics\.Data',
						   condition='==2',
						   timeout=5)

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("Drift",\["Input"\],\["OutputValue"\],{"offset":"2","offsetType":"absolute"}\)')
		exprList.append('Validating com.industry.analytics.Analytic\("Drift",\["Input"\],\["OutputPercentage"\],{"offset":"10","offsetType":"percentage"}\)')
		exprList.append('Validating com.industry.analytics.Analytic\("Drift",\["Input"\],\["OutputStandardDeviation"\],{"offset":"2","offsetType":"stddev"}\)')
		self.assertOrderedGrep("correlator.log", exprList=exprList)

		# Make sure that the we got the right log lines
		self.assertLineCount('correlator.log', expr='Validating com.industry.analytics.Analytic\("Drift",', condition='==3')
		self.assertLineCount('correlator.log', expr='Analytic Drift started for inputDataNames \["Input"\]', condition='==3')

		self.assertDiff('OutputValue.evt',
						'OutputValue.evt')
		self.assertDiff('OutputPercentage.evt',
						'OutputPercentage.evt')
		self.assertDiff('OutputStandardDeviation.evt',
						'OutputStandardDeviation.evt')
		self.checkSanity()	
