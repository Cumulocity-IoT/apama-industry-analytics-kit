# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectExpression(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output1.evt', channels=['Output1'])
		correlator.receive(filename='Output2.evt', channels=['Output2'])
		correlator.receive(filename='Output3.evt', channels=['Output3'])
		correlator.receive(filename='Output4.evt', channels=['Output4'])
		correlator.receive(filename='Output5.evt', channels=['Output5'])
		correlator.receive(filename='Output6.evt', channels=['Output6'])

		correlator.send('Config.evt')
		correlator.send('Events.evt')

		self.waitForSignal('correlator.out',
						   expr='Analytic Expression started for inputDataNames',
						   condition='==6',
						   timeout=5)

		
	def validate(self):
		# Basic sanity checks
		self.checkSanity()
		
		# Make sure that the test output was correct
		self.assertDiff('Output1.evt', 'Output1.evt')
		self.assertDiff('Output2.evt', 'Output2.evt')
		self.assertDiff('Output3.evt', 'Output3.evt')
		self.assertDiff('Output4.evt', 'Output4.evt')
		self.assertDiff('Output5.evt', 'Output5.evt')
		self.assertDiff('Output6.evt', 'Output6.evt')
		
		# Make sure that the we got the right number of passes/fails
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic\("Expression",.*\)', condition='==8')
		self.assertLineCount('correlator.out', expr='Error spawning Expression instance.', condition='==2')
		self.assertLineCount('correlator.out', expr='Analytic Expression started for inputDataNames', condition='==6')

		
