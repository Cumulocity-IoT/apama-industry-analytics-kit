# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['test.mon'], self.input)
		self.ready(correlator)

		self.waitForSignal('output.log',
						   expr='com.industry.analytics.CurrentVersion\(".*",false\)',
						   condition='==1',
						   timeout=5)

		
	def validate(self):
		self.assertLineCount('output.log', expr='com.industry.analytics.CurrentVersion\(".*",true\)', condition='>=1')
		self.assertLineCount('output.log', expr='com.industry.analytics.CurrentVersion\(".*",false\)', condition='==1')
		self.assertGrep('correlator.out', expr='ERROR \[.*\] - com.industry.analytics.VersioningService \[.*\] The version provided \(.*\) is not compatible with this version of the Industry Analytics Kit. Minimum supported version is .*', contains=0)
		self.assertGrep('correlator.out', expr='WARN  \[.*\] - com.industry.analytics.VersioningService \[.*\] The version provided \(.*\) may not be compatible with this version of the Industry Analytics Kit as it is newer. Current version is .*', contains=1)
		self.checkSanity()	
