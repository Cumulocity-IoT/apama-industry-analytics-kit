# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectMode(correlator)
		self.ready(correlator)

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Mode started for inputDataNames',
						   condition='==5',
						   timeout=5)

		
	def validate(self):
		self.assertGrep('correlator.out', expr='inputDataNames sequence should only have one entry')
		self.assertGrep('correlator.out', expr='outputDataNames sequence should only have one entry')
		self.assertGrep('correlator.out', expr='Mandatory param timeWindow missing')
		self.assertGrep('correlator.out', expr='Parameter bucketCount must be >= 2. Specified value is 1')
		self.assertGrep('correlator.out', expr='Parameter timeWindow must be >= 0.0. Specified value is -1.1')
		self.assertGrep('correlator.out', expr='Parameter dataAttribute must be one of the following dValue, sValue, xValue, yValue, zValue')
		self.checkSanity()	
