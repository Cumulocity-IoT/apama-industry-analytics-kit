# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(inputLog="correlator_input.log", logfile="correlator.log")
		self.injectAnalytic(correlator)
		
		# Analytic before relevant monitor injected: should be pended.
		correlator.sendLiteral('com.industry.analytics.Analytic("Delta", ["INPUT1"], ["OUTPUT1"], {})')
		self.waitForSignal('correlator.log',
						   expr='Analytic Delta started for inputDataNames',
						   condition='==0',
						   timeout=5)

		# Inject Analytic
		self.injectDelta(correlator);

		# Analytic after monitor but before Ready(). Should be pended.
		correlator.sendLiteral('com.industry.analytics.Analytic("Delta", ["INPUT2"], ["OUTPUT2"], {})')
		self.waitForSignal('correlator.log',
						   expr='Analytic Delta started for inputDataNames',
						   condition='==0',
						   timeout=5)
		
		# Ready()
		self.ready(correlator)
		self.waitForSignal('correlator.log',
						   expr='Analytic Delta started for inputDataNames',
						   condition='==2',
						   timeout=5)
		
		# Analytic after monitor but before Ready(). Should be processed.
		correlator.sendLiteral('com.industry.analytics.Analytic("Delta", ["INPUT3"], ["OUTPUT3"], {})')
		self.waitForSignal('correlator.log',
						   expr='Analytic Delta started for inputDataNames',
						   condition='==3',
						   timeout=5)
		
		
	def validate(self):
		self.assertDiff('correlator.log', 'correlator.log',
						includes=['DeltaService'],
						ignores=self.IGNORE,
						replace=self.REPLACE,
						sort=True)
		self.checkSanity()
