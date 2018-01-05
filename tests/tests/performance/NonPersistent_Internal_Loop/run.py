# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectDataSourceService(correlator)
		self.injectAverage(correlator)
		self.injectEventRate(correlator)
#		correlator.receive(filename='Input.evt', channels=['Input'])
		correlator.receive(filename='EventRate.evt', channels=['EventRate'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Average started for inputDataNames',
						   condition='==1',
						   timeout=5)
		self.waitForSignal('correlator.out',
						   expr='Analytic EventRate started for inputDataNames',
						   condition='==2',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('EventRate.evt', expr='com.industry.analytics\.Data', condition='==10', timeout=20)

		
	def validate(self):
		self.checkSanity()
		self.addOutcome(INSPECT)
