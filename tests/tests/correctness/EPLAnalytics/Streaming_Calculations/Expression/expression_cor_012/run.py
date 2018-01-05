# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectExpression(correlator)
		self.ready(correlator)
		correlator.receive(filename='F2C.evt', channels=['F2C'])
		correlator.receive(filename='C2F.evt', channels=['C2F'])

		correlator.send('Config.evt')
		correlator.send('Events.evt')

		self.waitForSignal('correlator.out',
						   expr='Analytic Expression started for inputDataNames',
						   condition='==2',
						   timeout=5)

		
	def validate(self):
		# Basic sanity checks
		self.checkSanity()
		
		# Make sure that the test output was correct
		self.assertDiff('F2C.evt', 'F2C.evt')
		self.assertDiff('C2F.evt', 'C2F.evt')
		
		# Make sure that the we got the right number of passes/fails
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic\("Expression",.*\)', condition='==2')
		self.assertLineCount('correlator.out', expr='Error spawning Expression instance.', condition='==0')
		self.assertLineCount('correlator.out', expr='Analytic Expression started for inputDataNames', condition='==2')

		
