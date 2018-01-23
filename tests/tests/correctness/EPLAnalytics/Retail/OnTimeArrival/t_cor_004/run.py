# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectDataSourceService(correlator)
		self.injectAnalytic(correlator)
		self.injectCommonRetail(correlator)
		self.injectOnTimeArrival(correlator)
		self.ready(correlator)
		correlator.receive(filename='OnArrival.evt', channels=['OnArrival'])
		correlator.receive(filename='OnETA.evt', channels=['OnETA'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out', expr='Analytic OnTimeArrival started for inputDataNames', condition='==2', timeout=5)

		correlator.send('Events.evt')
		self.waitForSignal('OnETA.evt', expr='com\.industry\.analytics\.Data', condition='==4', timeout=5)

		
	def validate(self):
		self.assertDiff('OnArrival.evt', 'OnArrival.evt')
		self.assertDiff('OnETA.evt', 'OnETA.evt')
		self.checkSanity()	
