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
		correlator.receive(filename='OutputRising.evt', channels=['OutputRising'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Corridor started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('input.log', expr='"Input1",com.industry.analytics\.Data', condition='==9', timeout=5)

		
	def validate(self):
		self.assertGrep('OutputRising.evt', expr='com.industry.analytics.Data.*"OutputRising","a","s1",0,5,"",1,2,3,{"anomalySource":"Corridor","duration":"0","zone":"inside"}')
		self.assertGrep('OutputRising.evt', expr='com.industry.analytics.Data.*"OutputRising","a","s1",20,7,"",1,2,3,{"anomalySource":"Corridor","duration":"0","zone":"inside"}')
		self.assertGrep('OutputRising.evt', expr='com.industry.analytics.Data.*"OutputRising","a","s1",25,7,"",1,2,3,{"anomalySource":"Corridor","duration":"0","zone":"inside"}')
		self.assertGrep('OutputRising.evt', expr='com.industry.analytics.Data.*"OutputRising","a","s1",30,7,"",1,2,3,{"anomalySource":"Corridor","duration":"0","zone":"inside"}')
		self.checkSanity()	
