# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectDataSourceService(correlator)
		self.injectAnalytic(correlator)
		self.injectMapper(correlator)
		self.ready(correlator)
		correlator.receive(filename='DVAL.evt', channels=['DVAL'])
		correlator.receive(filename='SVAL.evt', channels=['SVAL'])
		correlator.receive(filename='XVAL.evt', channels=['XVAL'])
		correlator.receive(filename='YVAL.evt', channels=['YVAL'])
		correlator.receive(filename='ZVAL.evt', channels=['ZVAL'])
		correlator.receive(filename='TYPE.evt', channels=['TYPE'])
		correlator.receive(filename='PARAM.evt', channels=['PARAM'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out', expr='Analytic Mapper started for inputDataNames', condition='==7', timeout=5)

		correlator.send('Events.evt')
		self.waitForSignal('PARAM.evt', expr='com\.industry\.analytics\.Data', condition='==4', timeout=5)

		
	def validate(self):
		self.assertDiff('DVAL.evt', 'DVAL.evt')
		self.assertDiff('SVAL.evt', 'SVAL.evt')
		self.assertDiff('XVAL.evt', 'XVAL.evt')
		self.assertDiff('YVAL.evt', 'YVAL.evt')
		self.assertDiff('ZVAL.evt', 'ZVAL.evt')
		self.assertDiff('TYPE.evt', 'TYPE.evt')
		self.assertDiff('PARAM.evt', 'PARAM.evt')
		self.checkSanity()	
