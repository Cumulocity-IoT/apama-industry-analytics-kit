# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile='correlator.log')
		self.injectAnalytic(correlator)
		self.injectAverage(correlator)
		self.ready(correlator)
		correlator.receive(filename='InOrderMA.evt', channels=['InOrderMA'])
		correlator.receive(filename='6thItemAfter10thItemMA.evt', channels=['6thItemAfter10thItemMA'])
		correlator.receive(filename='3rdItemAfter7thItemMA.evt', channels=['3rdItemAfter7thItemMA'])
		correlator.receive(filename='3rdItemAfter10thItemMA.evt', channels=['3rdItemAfter10thItemMA'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.log',
						   expr='Analytic Average started for inputDataNames',
						   condition='==4',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('InOrderMA.evt', expr='com.industry.analytics\.Data', condition='==10', timeout=5)
		self.waitForSignal('6thItemAfter10thItemMA.evt', expr='com.industry.analytics\.Data', condition='==10', timeout=5)
		self.waitForSignal('3rdItemAfter7thItemMA.evt', expr='com.industry.analytics\.Data', condition='==10', timeout=5)
		self.waitForSignal('3rdItemAfter10thItemMA.evt', expr='com.industry.analytics\.Data', condition='==10', timeout=5)

		
	def validate(self):
		self.assertDiff('InOrderMA.evt', 'InOrderMA.evt')
		self.assertDiff('correlator.log', 'correlator.log',
						includes=['AverageService'],
						ignores=self.IGNORE,
						replace=self.REPLACE,
						sort=True)
		self.assertDiff('InOrderMA.evt', 'InOrderMA.evt')
		self.assertDiff('6thItemAfter10thItemMA.evt', '6thItemAfter10thItemMA.evt')
		self.assertDiff('3rdItemAfter7thItemMA.evt', '3rdItemAfter7thItemMA.evt')
		self.assertDiff('3rdItemAfter10thItemMA.evt', '3rdItemAfter10thItemMA.evt')
		self.checkSanity()	
