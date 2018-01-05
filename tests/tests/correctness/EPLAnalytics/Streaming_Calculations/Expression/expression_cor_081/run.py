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
		correlator.receive(filename='Output2.evt', channels=['Output2'])
		correlator.receive(filename='Output3.evt', channels=['Output3'])
		correlator.receive(filename='Output4.evt', channels=['Output4'])
		correlator.receive(filename='Output5.evt', channels=['Output5'])
		correlator.receive(filename='Output6.evt', channels=['Output6'])
		correlator.receive(filename='Output7.evt', channels=['Output7'])
		correlator.receive(filename='Output8.evt', channels=['Output8'])
		correlator.receive(filename='Output9.evt', channels=['Output9'])
		correlator.receive(filename='Output10.evt', channels=['Output10'])
		correlator.receive(filename='Output11.evt', channels=['Output11'])
		correlator.receive(filename='Output12.evt', channels=['Output12'])
		correlator.receive(filename='Output13.evt', channels=['Output13'])
		correlator.receive(filename='Output14.evt', channels=['Output14'])
		correlator.receive(filename='Output15.evt', channels=['Output15'])
		correlator.receive(filename='Output16.evt', channels=['Output16'])
		correlator.receive(filename='Output17.evt', channels=['Output17'])
		correlator.receive(filename='Output18.evt', channels=['Output18'])
		correlator.receive(filename='Output19.evt', channels=['Output19'])
		correlator.receive(filename='Output20.evt', channels=['Output20'])
		correlator.receive(filename='Output21.evt', channels=['Output21'])

		correlator.send('Config.evt')
		correlator.send('Events.evt')

		self.waitForSignal('correlator.out',
						   expr='Analytic Expression started for inputDataNames',
						   condition='==24',
						   timeout=5)

		
	def validate(self):
		# Basic sanity checks
		self.checkSanity()
		
		# Make sure that the test output was correct
		self.assertDiff('Output1.evt', 'Output1.evt')
		self.assertDiff('Output2.evt', 'Output2.evt')
		self.assertDiff('Output3.evt', 'Output3.evt')
		self.assertDiff('Output4.evt', 'Output4.evt')
		self.assertDiff('Output5.evt', 'Output5.evt')
		self.assertDiff('Output6.evt', 'Output6.evt')
		self.assertDiff('Output7.evt', 'Output7.evt')
		self.assertDiff('Output8.evt', 'Output8.evt')
		self.assertDiff('Output9.evt', 'Output9.evt')
		self.assertDiff('Output10.evt', 'Output10.evt')
		self.assertDiff('Output11.evt', 'Output11.evt')
		self.assertDiff('Output12.evt', 'Output12.evt')
		self.assertDiff('Output13.evt', 'Output13.evt')
		self.assertDiff('Output14.evt', 'Output14.evt')
		self.assertDiff('Output15.evt', 'Output15.evt')
		self.assertDiff('Output16.evt', 'Output16.evt')
		self.assertDiff('Output17.evt', 'Output17.evt')
		self.assertDiff('Output18.evt', 'Output18.evt')
		self.assertDiff('Output19.evt', 'Output19.evt')
		self.assertDiff('Output20.evt', 'Output20.evt')
		self.assertDiff('Output21.evt', 'Output21.evt')
		
		# Make sure that the we got the right number of passes/fails
		self.assertLineCount('correlator.out', expr='Validating com.industry.analytics.Analytic\("Expression",.*\)', condition='==30')
		self.assertLineCount('correlator.out', expr='Error spawning Expression instance.', condition='==6')
		self.assertLineCount('correlator.out', expr='Analytic Expression started for inputDataNames', condition='==24')

		
