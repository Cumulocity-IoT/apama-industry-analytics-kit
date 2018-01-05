# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile="correlator.log", inputLog="input.log")
		self.injectAnalytic(correlator)
		self.injectDelta(correlator)
		correlator.injectMonitorscript(['LifecycleDummy.mon',
										'LifecycleDummyService.mon'], self.input)
		self.ready(correlator)
		correlator.receive(filename='Default.evt', channels=['Default'])
		correlator.receive(filename='KillMe.evt', channels=['KillMe'])
		correlator.receive(filename='KillMeSecond.evt', channels=['KillMeSecond'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.log',
						   expr='Analytic Delta started for inputDataNames',
						   condition='==3',
						   timeout=5)

		correlator.send('Management0.evt')
		self.waitForSignal('input.log', expr='com\.industry\.analytics\.AnalyticManagement\(', condition='==2', timeout=5)
		correlator.send('events.evt')
		self.waitForSignal('Default.evt', expr='com\.industry\.analytics\.Data\(', condition='==1', timeout=5)
		
		correlator.send('Management1.evt')
		self.waitForSignal('correlator.log', expr="Analytic instance using analyticId 'killMe' deleted", condition='==2', timeout=5)
		correlator.send('events.evt')
		self.waitForSignal('Default.evt', expr='com\.industry\.analytics\.Data\(', condition='==3', timeout=5)
		
		correlator.send('Management2.evt')
		self.waitForSignal('correlator.log', expr="Analytic instance using analyticId 'killMeSecond' deleted", condition='==2', timeout=5)
		correlator.send('events.evt')
		self.waitForSignal('Default.evt', expr='com\.industry\.analytics\.Data\(', condition='==5', timeout=5)
		
		# Should just be the main context and Deafult Delta monitors left.
		correlator.inspect()

		
	def validate(self):
		self.assertDiff('Default.evt', 'Default.evt')
		self.assertDiff('KillMe.evt', 'KillMe.evt')
		self.assertDiff('KillMeSecond.evt', 'KillMeSecond.evt')
		self.assertDiff('inspect.txt', 'inspect.txt',
						ignores=['engine_receive'])
		self.assertDiff('correlator.log', 'correlator.log',
						includes=['DeltaService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.assertDiff('correlator.log', 'correlator.log',
						includes=['LifecycleDummyService'],
						ignores=self.IGNORE,
						replace=self.REPLACE,
						sort=True)
		self.checkSanity()	
