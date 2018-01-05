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
		correlator.receive(filename='SpikeResult0.evt', channels=['SpikeResult0'])
		correlator.receive(filename='SpikeResult3.evt', channels=['SpikeResult3'])
		correlator.receive(filename='SpikeResult5.evt', channels=['SpikeResult5'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Spike started for inputDataNames',
						   condition='==3',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('SpikeResult0.evt',
						   expr='com.industry.analytics\.Data',
						   condition='==9',
						   timeout=5)
		self.waitForSignal('SpikeResult3.evt',
						   expr='com.industry.analytics\.Data',
						   condition='==6',
						   timeout=5)
		self.waitForSignal('SpikeResult5.evt',
						   expr='com.industry.analytics\.Data',
						   condition='==3',
						   timeout=5)

		
	def validate(self):
		self.assertDiff('SpikeResult0.evt', 'SpikeResult0.evt')
		self.assertDiff('SpikeResult3.evt', 'SpikeResult3.evt')
		self.assertDiff('SpikeResult5.evt', 'SpikeResult5.evt')
		self.checkSanity()	
