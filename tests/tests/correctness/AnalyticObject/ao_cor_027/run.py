# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile="correlator.log")
		self.injectAnalytic(correlator)
		self.injectAverage(correlator)
		self.injectDelta(correlator)
		self.ready(correlator)

		# Send the test configuration
		correlator.send('Config.evt')

		# Wait for the test to complete
		self.waitForSignal('correlator.log', expr='Analytic Average started', timeout=5)
		
	def validate(self):
		self.checkSanity()

		# Ensure the test output was correct
		exprList=[]
		exprList.append('ERROR \[.*\] - .* Received Analytic setup request for unrecognised analytic mytestanalytic. Either the analytic has not yet been loaded into the correlator or the name is incorrect.')
		exprList.append('ERROR \[.*\] - .* Received Analytic setup request for unrecognised analytic foo. Either the analytic has not yet been loaded into the correlator or the name is incorrect.')
		self.assertOrderedGrep("correlator.log", exprList=exprList)

		self.assertLineCount('correlator.log', expr='Analytic [d|D]elta started for inputDataNames', condition='==3')
		self.assertLineCount('correlator.log', expr='Analytic [a|A]verage started for inputDataNames', condition='==3')
		self.assertLineCount('correlator.log', expr='Received Analytic setup request for unrecognised analytic', condition='==2')
		self.assertLineCount('correlator.log', expr='Analytic .* started for inputDataNames', condition='==6')


