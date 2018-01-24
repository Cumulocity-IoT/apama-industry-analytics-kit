# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectFootFall(correlator)
		self.ready(correlator)

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic FootFall started for inputDataNames',
						   condition='==3',
						   timeout=5)

		
	def validate(self):
		self.assertGrep('correlator.out', expr='Mandatory param geoFenceLatitude missing', condition='==1')
		self.assertGrep('correlator.out', expr='Mandatory param geoFenceLongitude missing', condition='==2')
		self.assertGrep('correlator.out', expr='Mandatory param geoFenceRadius missing', condition='==3')
		self.checkSanity()