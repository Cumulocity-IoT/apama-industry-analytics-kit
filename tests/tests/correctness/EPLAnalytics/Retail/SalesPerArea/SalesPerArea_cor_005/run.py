# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectSalesPerArea(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output.evt', channels=['Output'])
		correlator.receive(filename='Sum_Output.evt', channels=['__internalChannel_SALES_PER_AREA_SUM_Output'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic SalesPerArea started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Output.evt', expr='com.industry.analytics.Data.*', condition='==9', timeout=5)
		
	def validate(self):
		self.assertDiff('Output.evt', 'RefOutput.evt')
		self.assertDiff('Sum_Output.evt', 'RefSum_Output.evt')
		self.checkSanity()	
