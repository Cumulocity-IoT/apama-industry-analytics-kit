# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectVolatility(correlator)
		self.ready(correlator)
		correlator.receive(filename='Variance.evt', channels=['Variance'])
		correlator.receive(filename='StandardDeviation.evt', channels=['StandardDeviation'])
		correlator.receive(filename='MovingAverage.evt', channels=['MovingAverage'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Volatility started for inputDataNames',
						   condition='==2',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Variance.evt', expr='com.industry.analytics\.Data', condition='==12', timeout=5)

		
	def validate(self):
		self.assertDiff('Variance.evt', 'Variance.evt')
		self.assertDiff('StandardDeviation.evt', 'StandardDeviation.evt')
		self.assertDiff('MovingAverage.evt', 'MovingAverage.evt')
		self.assertDiff('correlator.out', 'correlator.log',
						sort=True,
						includes=['VolatilityService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	
