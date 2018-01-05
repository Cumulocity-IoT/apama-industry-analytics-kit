# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectDataSourceService(correlator)
		self.injectAnalytic(correlator)
		self.injectFilter(correlator)
		self.ready(correlator)
		correlator.receive(filename='LT.evt', channels=['LT'])
		correlator.receive(filename='LTEQ.evt', channels=['LTEQ'])
		correlator.receive(filename='EQ.evt', channels=['EQ'])
		correlator.receive(filename='GTEQ.evt', channels=['GTEQ'])
		correlator.receive(filename='GT.evt', channels=['GT'])
		correlator.receive(filename='BT.evt', channels=['BT'])
		correlator.receive(filename='BTEQ.evt', channels=['BTEQ'])
		correlator.receive(filename='WO.evt', channels=['WO'])
		correlator.receive(filename='WOEQ.evt', channels=['WOEQ'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out', expr='Analytic Filter started for inputDataNames', condition='==9', timeout=5)

		correlator.send('Events.evt')
		self.waitForSignal('WO.evt', expr='com\.industry\.analytics\.Data\("WO","c","s1",0,0,"",0,0,11,\{\}\)', condition='==1', timeout=5)

		
	def validate(self):
		self.assertDiff('correlator.out', 'correlator.log',
						includes=['FilterService'],
						ignores=self.IGNORE,
						replace=self.REPLACE,
						sort=True)
		self.assertDiff('LT.evt', 'LT.evt')
		self.assertDiff('LTEQ.evt', 'LTEQ.evt')
		self.assertDiff('EQ.evt', 'EQ.evt')
		self.assertDiff('GTEQ.evt', 'GTEQ.evt')
		self.assertDiff('GT.evt', 'GT.evt')
		self.assertDiff('BT.evt', 'BT.evt')
		self.assertDiff('BTEQ.evt', 'BTEQ.evt')
		self.assertDiff('WO.evt', 'WO.evt')
		self.assertDiff('WOEQ.evt', 'WOEQ.evt')
		self.checkSanity()	
