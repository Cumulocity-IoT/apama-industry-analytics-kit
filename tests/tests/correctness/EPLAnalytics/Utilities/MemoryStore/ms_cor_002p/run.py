# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(persistence=True)
		self.injectAnalytic(correlator)
		self.injectMemoryStore(correlator)
		self.ready(correlator)

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic MemoryStore started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		correlator.sendLiteral('"Input", com.industry.analytics.utilities.DumpTable("Input")')
		
		# Need to ensure the cache is empty for the next test
		correlator.sendLiteral('"Input", com.industry.analytics.ClearCache("")')
		correlator.sendLiteral('"Input", com.industry.analytics.utilities.DumpTable("Input")')
		self.waitForSignal('correlator.out', expr='Table: Input', condition='==2', timeout=5)

		
	def validate(self):
		self.assertDiff('correlator.out', 'correlator.log',
						includes=['MemoryStoreService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	
