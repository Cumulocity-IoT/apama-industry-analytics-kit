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
		correlator.receive(filename='Output1.evt', channels=['Output1'])
		correlator.receive(filename='Output3.evt', channels=['Output3'])
		correlator.receive(filename='Output5.evt', channels=['Output5'])
		correlator.receive(filename='Output6.evt', channels=['Output6'])
		correlator.receive(filename='Output7.evt', channels=['Output7'])
		correlator.receive(filename='Output8.evt', channels=['Output8'])
		correlator.receive(filename='Output10.evt', channels=['Output10'])
		correlator.receive(filename='Output11.evt', channels=['Output11'])
		correlator.receive(filename='Output13.evt', channels=['Output13'])
		correlator.receive(filename='Output15.evt', channels=['Output15'])
		correlator.receive(filename='Output16.evt', channels=['Output16'])
		correlator.receive(filename='Output17.evt', channels=['Output17'])
		correlator.receive(filename='Output18.evt', channels=['Output18'])
		correlator.receive(filename='Output20.evt', channels=['Output20'])

		correlator.send('Config.evt')
		correlator.send('Events.evt')

		self.waitForSignal('correlator.out',
						   expr='Analytic Expression started for inputDataNames',
						   condition='==14',
						   timeout=5)

		
	def validate(self):
		# Basic sanity checks
		self.checkSanity()
		
		# Make sure that the test output was correct
		self.assertDiff('Output1.evt', 'Output1.evt')
		self.assertDiff('Output3.evt', 'Output3.evt')
		self.assertDiff('Output5.evt', 'Output5.evt')
		self.assertDiff('Output6.evt', 'Output6.evt')
		self.assertDiff('Output7.evt', 'Output7.evt')
		self.assertDiff('Output8.evt', 'Output8.evt')
		self.assertDiff('Output10.evt', 'Output10.evt')
		self.assertDiff('Output11.evt', 'Output11.evt')
		self.assertDiff('Output13.evt', 'Output13.evt')
		self.assertDiff('Output15.evt', 'Output15.evt')
		self.assertDiff('Output16.evt', 'Output16.evt')
		self.assertDiff('Output17.evt', 'Output17.evt')
		self.assertDiff('Output18.evt', 'Output18.evt')
		self.assertDiff('Output20.evt', 'Output20.evt')
		
		# Make sure that the we got the right number of passes/fails
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic\("Expression",.*\)', condition='==20')
		self.assertLineCount('correlator.out', expr='Error spawning Expression instance.', condition='==6')
		self.assertLineCount('correlator.out', expr='Analytic Expression started for inputDataNames', condition='==14')

		
