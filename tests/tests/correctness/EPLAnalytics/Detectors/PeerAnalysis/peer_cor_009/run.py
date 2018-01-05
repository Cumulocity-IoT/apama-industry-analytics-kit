# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectPeerAnalysis(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output.evt', channels=['Output'])
		correlator.receive(filename='OutputAverage.evt', channels=['__internalChannel_PEER_AVERAGE_Output'])
		correlator.receive(filename='OutputSpread.evt', channels=['__internalChannel_PEER_SPREAD_Output'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic PeerAnalysis started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')

		self.waitForSignal('Output.evt', expr='com.industry.analytics\.Data', condition='==6', timeout=5)

	def validate(self):
		# Basic sanity checks
		self.checkSanity()

		# Ensure the test output was correct
		self.assertDiff('Output.evt',        'Output.evt')
		self.assertDiff('OutputAverage.evt', 'OutputAverage.evt')
		self.assertDiff('OutputSpread.evt',  'OutputSpread.evt')
