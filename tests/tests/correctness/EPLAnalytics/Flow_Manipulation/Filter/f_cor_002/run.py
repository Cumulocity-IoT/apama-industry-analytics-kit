# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectDataSourceService(correlator)
		self.injectAnalytic(correlator)
		self.injectFilter(correlator)
		self.ready(correlator)
		correlator.receive(filename='OutputAll.evt', channels=['OutputAll'])
		correlator.receive(filename='OutputType.evt', channels=['OutputType'])
		correlator.receive(filename='OutputNotType.evt', channels=['OutputNotType'])
		correlator.receive(filename='OutputSensor.evt', channels=['OutputSensor'])
		correlator.receive(filename='OutputNotSensor.evt', channels=['OutputNotSensor'])
		correlator.receive(filename='OutputParam.evt', channels=['OutputParam'])
		correlator.receive(filename='OutputNotParam.evt', channels=['OutputNotParam'])
		correlator.receive(filename='OutputStringValue.evt', channels=['OutputStringValue'])
		correlator.receive(filename='OutputNotStringValue.evt', channels=['OutputNotStringValue'])
		correlator.receive(filename='OutputSpecificStringValue.evt', channels=['OutputSpecificStringValue'])
		correlator.receive(filename='OutputNotSpecificStringValue.evt', channels=['OutputNotSpecificStringValue'])
		correlator.receive(filename='OutputComb1.evt', channels=['OutputComb1'])
		correlator.receive(filename='OutputComb2.evt', channels=['OutputComb2'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Filter started for inputDataNames',
						   condition='==13',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('OutputAll.evt', expr='com.industry.analytics\.Data', condition='==21', timeout=5)

		
	def validate(self):
		self.assertDiff('OutputAll.evt', 'OutputAll.evt')
		self.assertDiff('OutputType.evt', 'OutputType.evt')
		self.assertDiff('OutputNotType.evt', 'OutputNotType.evt')
		self.assertDiff('OutputSensor.evt', 'OutputSensor.evt')
		self.assertDiff('OutputNotSensor.evt', 'OutputNotSensor.evt')
		self.assertDiff('OutputParam.evt', 'OutputParam.evt')
		self.assertDiff('OutputNotParam.evt', 'OutputNotParam.evt')
		self.assertDiff('OutputStringValue.evt', 'OutputStringValue.evt')
		self.assertDiff('OutputNotStringValue.evt', 'OutputNotStringValue.evt')
		self.assertDiff('OutputSpecificStringValue.evt', 'OutputSpecificStringValue.evt')
		self.assertDiff('OutputNotSpecificStringValue.evt', 'OutputNotSpecificStringValue.evt')
		self.assertDiff('OutputComb1.evt', 'OutputComb1.evt')
		self.assertDiff('OutputComb2.evt', 'OutputComb2.evt')
		# Need to sort as instance spawns are non-deterministic.
		self.assertDiff('correlator.out', 'correlator.log',
						sort=True,
						includes=['FilterService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	
