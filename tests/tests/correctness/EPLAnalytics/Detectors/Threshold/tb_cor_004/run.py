# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(inputLog="input.log")
		self.injectAnalytic(correlator)
		self.injectThreshold(correlator)
		self.ready(correlator)
		correlator.receive(filename='OutputRising.evt', channels=['OutputRising'])
		correlator.receive(filename='OutputFalling.evt', channels=['OutputFalling'])
		correlator.receive(filename='OutputCrossing.evt', channels=['OutputCrossing'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Threshold started for inputDataNames',
						   condition='==3',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('input.log', expr='"Input1",com.industry.analytics\.Data', condition='==36', timeout=5)

		
	def validate(self):
		self.assertDiff('OutputRising.evt', 'OutputRising.evt')
		self.assertDiff('OutputFalling.evt', 'OutputFalling.evt')
		self.assertDiff('OutputCrossing.evt', 'OutputCrossing.evt')
		self.assertDiff('correlator.out', 'correlator.log',
						sort=True,
						includes=['ThresholdService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	
