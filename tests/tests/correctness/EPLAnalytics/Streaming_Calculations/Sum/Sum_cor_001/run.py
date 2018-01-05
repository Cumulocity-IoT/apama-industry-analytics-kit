# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectSum(correlator)
		self.ready(correlator)

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Sum started for inputDataNames',
						   condition='==6',
						   timeout=5)

		
	def validate(self):
		self.assertGrep('correlator.out', expr='Mandatory param calculationType missing')
		self.assertGrep('correlator.out', expr='Parameter calculationType value can be either timeWindow or sampleCount')
		self.assertGrep('correlator.out', expr='Parameter calculationValue must be greater than 0.0')
		self.assertGrep('correlator.out', expr='Parameter calculationValue must be greater than or equal to 1.0')
		self.assertGrep('correlator.out', expr='Parameter smoothingFactor value 20 is greater than calculationValue. Using calculationValue value 10 as default',condition='==2')
		self.assertGrep('correlator.out', expr='Value of parameter paramName must be dValue, xValue, yValue or zValue')
		self.checkSanity()	
