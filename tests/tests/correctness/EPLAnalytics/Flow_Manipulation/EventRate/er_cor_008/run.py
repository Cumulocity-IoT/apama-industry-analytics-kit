# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest
from pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile='correlator.log')
		self.injectAnalytic(correlator)
		self.injectEventRate(correlator)
		self.ready(correlator)
		correlator.injectMonitorscript(['test.mon'], self.input)

		self.waitForSignal('correlator.log', expr='_eventRateTimestamp: {}:{}', condition='==1', timeout=5)


	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("EventRate",\["Input"\],\["Output"\],{"useCorrelatorTime":"true"}\)')
		exprList.append('Validating com.industry.analytics.Analytic\("EventRate",\["Input"\],\["Output"\],{"useCorrelatorTime":"false"}\)')
		exprList.append('EventRate Pre-Reset State:')
		exprList.append('_eventRateCorrelator: {"asset1":.*,"asset2":.*}:{"asset1":.*,"asset2":.*}')
		exprList.append('_eventRateTimestamp: {"asset1":.*,"asset2":.*}:{"asset1":0.5,"asset2":0.6}')
		exprList.append('EventRate Post-Reset State:')
		exprList.append('_eventRateCorrelator: {}:{}')
		exprList.append('_eventRateTimestamp: {}:{}')
		self.assertOrderedGrep("correlator.log", exprList=exprList)
		
		self.checkSanity()	
