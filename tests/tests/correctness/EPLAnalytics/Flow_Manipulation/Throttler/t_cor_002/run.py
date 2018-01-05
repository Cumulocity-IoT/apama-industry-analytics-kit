# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectDataSourceService(correlator)
		self.injectAnalytic(correlator)
		self.injectThrottler(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output1.evt', channels=['Output1'])
		correlator.receive(filename='Output2.evt', channels=['Output2'])

		correlator.send('Config.evt')
		correlator.send('Events.evt')
		self.waitForSignal('correlator.out', expr='Analytic Throttler started for inputDataNames', condition='==2', timeout=5)
		
	def validate(self):
		self.assertDiff('Output1.evt', 'Output1.evt')
		self.assertDiff('Output2.evt', 'Output2.evt')
		self.checkSanity()	
