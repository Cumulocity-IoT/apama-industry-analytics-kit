# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile="correlator.log", inputLog="correlator_input.log")
		self.injectAnalytic(correlator)
		correlator.injectMonitorscript(['AnalyticObjectTest.mon'], self.input)
		correlator.receive(filename="TestOutputData1.evt", channels=['TestOutputData1'])
		correlator.receive(filename="TestOutputData2.evt", channels=['TestOutputData2'])

		correlator.send('Data1.evt')
		correlator.sendEventStrings('"TestInputData1", com.industry.analytics.AnalyticObject_001.StopListeners()',
									'"TestInputData2", com.industry.analytics.AnalyticObject_001.StopListeners()')

		correlator.send('Data2.evt')
		self.waitForSignal('TestOutputData2.evt', expr='com\.industry\.analytics\.Data\(', condition='==1', timeout=5)

		
	def validate(self):
		self.assertDiff('TestOutputData1.evt', 'TestOutputData1.evt',)
		self.assertDiff('TestOutputData2.evt', 'TestOutputData2.evt',)
		self.checkSanity()
