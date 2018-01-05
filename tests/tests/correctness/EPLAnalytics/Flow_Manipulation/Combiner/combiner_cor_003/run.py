# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectCombiner(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output1.evt', channels=['Output1'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Combiner started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Output1.evt', expr='com.industry.analytics\.Data', condition='==12', timeout=5)

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("Combiner",\["Input1","Input2","Input3"\],\["Output1"\],{"aggregatedSourceId":"aS"}\)')
		exprList.append('Analytic Combiner started for inputDataNames \["Input1","Input2","Input3"\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		# Make sure that the we got the right number of Analytics started
		self.assertLineCount('correlator.out', expr='Analytic Combiner started', condition='==1')

		# Check the events output are correct
		self.assertDiff('Output1.evt', 'Output1.evt')
		
		self.checkSanity()	
