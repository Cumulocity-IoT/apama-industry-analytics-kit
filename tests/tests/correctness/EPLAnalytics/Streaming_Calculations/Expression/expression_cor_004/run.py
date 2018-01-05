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

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Expression started for inputDataNames',
						   condition='==5',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Output1.evt', expr='com.industry.analytics\.Data', condition='==12', timeout=5)
		self.waitForSignal('Output2.evt', expr='com.industry.analytics\.Data', condition='==12', timeout=5)
		self.waitForSignal('Output3.evt', expr='com.industry.analytics\.Data', condition='==12', timeout=5)
		self.waitForSignal('Output4.evt', expr='com.industry.analytics\.Data', condition='==12', timeout=5)
		self.waitForSignal('Output5.evt', expr='com.industry.analytics\.Data', condition='==12', timeout=5)

		
	def validate(self):
		self.assertDiff('Output1.evt', 'Output1.evt')
		self.assertDiff('Output2.evt', 'Output2.evt')
		self.assertDiff('Output3.evt', 'Output3.evt')
		self.assertDiff('Output4.evt', 'Output4.evt')
		self.assertDiff('Output5.evt', 'Output5.evt')
		self.checkSanity()	
