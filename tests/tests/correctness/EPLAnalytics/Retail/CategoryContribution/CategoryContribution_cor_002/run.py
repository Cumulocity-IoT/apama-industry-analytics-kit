# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectCategoryContribution(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output.evt', channels=['Output'])
		correlator.receive(filename='Sum_input.evt', channels=['__internalChannel_CATEGORY_CONTRIBUTION_SUM_Input'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic CategoryContribution started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Output.evt', expr='com.industry.analytics.Data.*', condition='==18', timeout=5)
		
	def validate(self):
		self.assertDiff('Output.evt', 'RefOutput.evt')
		self.assertDiff('Sum_input.evt', 'RefSum_input.evt')
		self.checkSanity()	
