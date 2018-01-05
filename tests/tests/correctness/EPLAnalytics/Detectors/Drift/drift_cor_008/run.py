# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest
from pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile='correlator.log', logLevel="DEBUG")
		self.injectAnalytic(correlator)
		self.injectDrift(correlator)
		self.ready(correlator)
		correlator.injectMonitorscript(['test.mon'], self.input)

		self.waitForSignal('correlator.log', expr='  _boundaries: ', condition='==2', timeout=5)


	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("Drift",\["Input"\],\["Output"\],{"offset":"100","offsetPeriod":"1"}\)')
		exprList.append('Boundaries for sourceId asset1: com.industry.analytics.detectors.Boundaries\(1,1\)')
		exprList.append('Drift Pre-Reset State:')
		exprList.append('_calculations: {"asset2":com.industry.analytics.detectors.BaselineCalculation\(1,com.industry.analytics.TimeWeightedVariance\(com.industry.analytics.TimeWeightedMovingAverage\(2\.2,optional\(\),0,1,2\.2,1,1,0\),0,0,0\)\)}')
		exprList.append('_boundaries: {"asset1":com.industry.analytics.detectors.Boundaries\(1,1\)}')
		exprList.append('Drift Post-Reset State:')
		exprList.append('_calculations: {}')
		exprList.append('_boundaries: {}')
		self.assertOrderedGrep("correlator.log", exprList=exprList)

		# Make sure that the we got the right log lines
		self.assertLineCount('correlator.log', expr='Validating com.industry.analytics.Analytic\("Drift",', condition='==1')

		self.checkSanity()	
		