# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectSuppressor(correlator)
		self.ready(correlator)
		correlator.receive(filename='OutputTEfABAf.evt', channels=['OutputTEfABAf'])
		correlator.receive(filename='OutputTEtABAf.evt', channels=['OutputTEtABAf'])
		correlator.receive(filename='OutputTEfABAt.evt', channels=['OutputTEfABAt'])
		correlator.receive(filename='OutputTEtABAt.evt', channels=['OutputTEtABAt'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Suppressor started for inputDataNames',
						   condition='==4',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('OutputTEtABAt.evt', expr='com.industry.analytics\.Data', condition='==23', timeout=5)

		
	def validate(self):
		self.assertDiff('OutputTEfABAf.evt', 'OutputTEfABAf.evt')
		self.assertDiff('OutputTEtABAf.evt', 'OutputTEtABAf.evt')
		self.assertDiff('OutputTEfABAt.evt', 'OutputTEfABAt.evt')
		self.assertDiff('OutputTEtABAt.evt', 'OutputTEtABAt.evt')
		self.assertDiff('correlator.out', 'correlator.log',
						sort=True,
						includes=['SuppressorService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	
