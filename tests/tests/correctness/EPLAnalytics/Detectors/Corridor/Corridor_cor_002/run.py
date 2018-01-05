# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(inputLog="input.log")
		self.injectAnalytic(correlator)
		self.injectCorridor(correlator)
		self.ready(correlator)
		#correlator.receive(filename='OutputRising.evt', channels=['OutputRising'])
		correlator.receive(filename='OutputFalling.evt', channels=['OutputFalling'])
		#correlator.receive(filename='OutputCrossing_upper.evt', channels=['OutputCrossing_upper'])
		#correlator.receive(filename='OutputCrossing_lower.evt', channels=['OutputCrossing_lower'])
		#correlator.receive(filename='OutputCrossing_both.evt', channels=['OutputCrossing_both'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Corridor started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('input.log', expr='"Input1",com.industry.analytics\.Data', condition='==9', timeout=5)

		
	def validate(self):
		self.assertGrep('OutputFalling.evt', expr='com.industry.analytics.Data.*"OutputFalling","a","s1",25,3,"",1,2,3,{"anomalySource":"Corridor","duration":"10","zone":"outside"}')
		self.assertGrep('OutputFalling.evt', expr='com.industry.analytics.Data.*"OutputFalling","a","s1",35,4,"",1,2,3,{"anomalySource":"Corridor","duration":"20","zone":"outside"}')
		self.checkSanity()	
