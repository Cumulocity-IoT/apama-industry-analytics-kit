# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(persistence=True)
		self.injectDataSourceService(correlator)
		self.injectAnalytic(correlator)
		self.injectFilter(correlator)
		self.ready(correlator)
		correlator.receive(filename='OutputAll.evt', channels=['OutputAll'])
		correlator.receive(filename='sourceId_OnlyLeafNodes.evt', channels=['sourceId_OnlyLeafNodes'])
		correlator.receive(filename='sourceId_AllChildren.evt', channels=['sourceId_AllChildren'])

		correlator.send('DataSources.evt')
		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Filter started for inputDataNames',
						   condition='==3',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('OutputAll.evt', expr='com.industry.analytics\.Data', condition='==14', timeout=5)

		
	def validate(self):
		self.assertDiff('OutputAll.evt', 'OutputAll.evt')
		self.assertDiff('sourceId_OnlyLeafNodes.evt', 'sourceId_OnlyLeafNodes.evt')
		self.assertDiff('sourceId_AllChildren.evt', 'sourceId_AllChildren.evt')
		# Need to sort as instance spawns are non-deterministic.
		self.assertDiff('correlator.out', 'correlator.log',
						sort=True,
						includes=['FilterService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	
