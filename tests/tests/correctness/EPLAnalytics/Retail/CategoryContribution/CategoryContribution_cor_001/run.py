# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectCategoryContribution(correlator)
		self.ready(correlator)

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic CategoryContribution started for inputDataNames',
						   condition='==3',
						   timeout=5)
		
	def validate(self):
		self.assertGrep('correlator.out', expr='inputDataNames sequence should contain 2 entries', condition='==1')
		self.assertGrep('correlator.out', expr='Unable to parse param ignoreUnknown as boolean', condition='==1')
		self.assertGrep('correlator.out', expr='Param timeWindow must be positive. Given value: 0', condition='==1')
		self.assertGrep('correlator.out', expr='Param timeWindow must be positive. Given value: -1', condition='==1')
		self.assertGrep('correlator.out', expr='Parameter smoothingFactor value 80 is greater than timeWindow. Using timeWindow value 60 as default', condition='==1')
		self.assertGrep('correlator.out', expr='Parameter smoothingFactor must be greater than 0.0', condition='==2')
		self.assertGrep('correlator.out', expr='Error spawning CategoryContribution instance', condition='==6')
		self.checkSanity()	
