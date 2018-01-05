# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectSpike(correlator)
		self.ready(correlator)
		correlator.receive(filename='MovingAverage.evt', channels=['MovingAverage'])
		correlator.receive(filename='Variance.evt', channels=['Variance'])
		correlator.receive(filename='StandardDeviation.evt', channels=['StandardDeviation'])
		correlator.receive(filename='LowerBollinger.evt', channels=['LowerBollinger'])
		correlator.receive(filename='UpperBollinger.evt', channels=['UpperBollinger'])
		correlator.receive(filename='Output.evt', channels=['SpikeResult'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Spike started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Output.evt',
						   expr='com.industry.analytics\.Data',
						   condition='==12',
						   timeout=5)

		
	def validate(self):
		self.assertDiff('Output.evt', 'Output.evt')
		self.assertDiff('MovingAverage.evt', 'MovingAverage.evt')
		self.assertDiff('Variance.evt', 'Variance.evt')
		self.assertDiff('StandardDeviation.evt', 'StandardDeviation.evt')
		self.assertDiff('LowerBollinger.evt', 'LowerBollinger.evt')
		self.assertDiff('UpperBollinger.evt', 'UpperBollinger.evt')
		self.checkSanity()	
