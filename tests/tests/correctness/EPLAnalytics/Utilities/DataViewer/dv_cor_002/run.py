# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile="correlator.log", inputLog="input.log")
		self.injectAnalytic(correlator)
		self.injectDataViewer(correlator)
		self.ready(correlator)
		correlator.receive(filename='DataViewEvents.evt')

		correlator.send('Config.evt')
		self.waitForSignal('correlator.log',
						   expr='Analytic DataViewer started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('DataViewEvents.evt', expr='com\.apama\.scenario\.Update', condition='==26', timeout=5)
		
		correlator.send('Management.evt')
		self.waitForSignal('correlator.log', expr="DataView 'Input' deleted", condition='==1', timeout=5)		

		
	def validate(self):
		self.assertDiff('DataViewEvents.evt', 'DataViewEvents.evt',
					    sort=True)
		self.assertDiff('correlator.log', 'correlator.log',
						includes=['DataViewerService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	
