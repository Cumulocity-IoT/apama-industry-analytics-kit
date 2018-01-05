# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile='correlator.log', inputLog='input.log')
		self.injectAnalytic(correlator)
		self.injectDataSimulator(correlator)
		self.ready(correlator)
		correlator.receive(filename='OutputData.evt', channels=['OutputData'])
		correlator.injectMonitorscript(['test.mon'], self.input)
		
		correlator.send('Config.evt')
		self.waitForSignal('correlator.log', expr='Analytic DataSimulator started for inputDataNames', condition='==1', timeout=5)
		self.wait(10.0)

		
	def validate(self):
		self.assertGrep('OutputData.evt', expr='com.industry.analytics.Data.*', condition='>=3')
		self.assertGrep('correlator.log', expr='Incorrect data generated', contains=0)
		self.checkSanity()	

