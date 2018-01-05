# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectDataSourceService(correlator)
		self.waitForSignal('correlator.out', expr='DataSource cache ready', condition='>=1', timeout=5)
		correlator.send('DataSources.evt')
		# Wait for the last event to be sent (the name is then interned)
		self.waitForSignal('correlator.out', expr='Interning S9', condition='==1', timeout=5)
	
		correlator.injectMonitorscript(['DataSourceServiceTest002.mon'], self.input)
		self.waitForSignal('correlator.out', expr='SourceIds Response \(just leaf nodes\):', condition='==4', timeout=5)

		
	def validate(self):
		self.assertDiff('correlator.out', 'correlator.log',
						includes=['com.industry.analytics\.DataSourceService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()
