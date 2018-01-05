# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		correlator.injectMonitorscript(['BucketSystem.mon'], self.COMPONENTS)
		
		correlator.injectMonitorscript(['BucketSystemCreationFailure.mon'], self.input)
		self.waitForSignal('correlator.out', expr='Test finished', condition='==1', timeout=5)

		
	def validate(self):
		self.assertLineCount('correlator.out', expr='Successfully threw exception:', condition='==11')
		self.assertLineCount('correlator.out', expr='Test Failed', condition='==0')
		self.checkSanity()	