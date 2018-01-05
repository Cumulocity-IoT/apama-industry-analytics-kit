# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest
from pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectFFTAnalysis(correlator)
		self.ready(correlator)

		correlator.receive(filename='FFT.evt', channels=['Output1'])

		correlator.injectMonitorscript(['test.mon'], self.input)

		self.waitForSignal('correlator.out',
						   expr='Analytic FFT started for inputDataNames',
						   condition='==1',
						   timeout=5)
		
		correlator.sendLiteral('com.industry.analytics.streaming_calculations.FFTAnalysis_cor_011.StartDataGenerator()')

		self.waitForSignal('FFT.evt', expr='com.industry.analytics\.Data', condition='==27', timeout=10)

		
	def validate(self):
		# Make sure there were no errors in the logs
		self.checkSanity()

		# Make sure that the we got the right number of Data events called
		self.assertLineCount('FFT.evt', expr='com.industry.analytics\.Data', condition='==27')
		self.assertLineCount('FFT.evt', expr='com.industry.analytics\.Data\("Output1","c","sourceId",0,0,"",.*,0,0,{}\)', condition='==9')
		self.assertLineCount('FFT.evt', expr='com.industry.analytics\.Data\("Output1","c","sourceId",0,120,"",.*,0,0,{}\)', condition='==9')
		self.assertLineCount('FFT.evt', expr='com.industry.analytics\.Data\("Output1","c","sourceId",0,50,"",.*,0,0,{}\)', condition='==9')
		
		# Make sure that the Data events were as expected
		self.assertDiff('FFT.evt', 'FFT.evt')
		
	
	