# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile='correlator.log', inputLog='input.log')
		self.injectAnalytic(correlator)
		self.injectGeoFence(correlator)
		correlator.receive(filename='Fixed Offset.evt', channels=['Fixed Offset'])
		correlator.receive(filename='Cartesian Fixed Offset.evt', channels=['Cartesian Fixed Offset'])
		correlator.receive(filename='Fixed Radius.evt', channels=['Fixed Radius'])
		correlator.receive(filename='Cartesian Fixed Radius.evt', channels=['Cartesian Fixed Radius'])
		correlator.receive(filename='Fixed Polygon.evt', channels=['Fixed Polygon'])
		correlator.receive(filename='Relative Fixed Polygon.evt', channels=['Relative Fixed Polygon'])
		correlator.receive(filename='Cartesian Fixed Polygon.evt', channels=['Cartesian Fixed Polygon'])
		correlator.receive(filename='Cartesian Relative Fixed Polygon.evt', channels=['Cartesian Relative Fixed Polygon'])
		self.ready(correlator)

		correlator.send('Config.evt')
		self.waitForSignal('correlator.log', expr='Analytic GeoFence started for inputDataNames', condition='==8', timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Cartesian Relative Fixed Polygon.evt', expr='com\.industry\.analytics\.Data\(', condition='==15', timeout=5)

		
	def validate(self):
		self.assertDiff('Fixed Offset.evt', 'Fixed Offset.evt')
		self.assertDiff('Cartesian Fixed Offset.evt', 'Cartesian Fixed Offset.evt')
		self.assertDiff('Fixed Radius.evt', 'Fixed Radius.evt')
		self.assertDiff('Cartesian Fixed Radius.evt', 'Cartesian Fixed Radius.evt')
		self.assertDiff('Fixed Polygon.evt', 'Fixed Polygon.evt')
		self.assertDiff('Relative Fixed Polygon.evt', 'Relative Fixed Polygon.evt')
		self.assertDiff('Cartesian Fixed Polygon.evt', 'Cartesian Fixed Polygon.evt')
		self.assertDiff('Cartesian Relative Fixed Polygon.evt', 'Cartesian Relative Fixed Polygon.evt')
		self.assertDiff('correlator.log', 'correlator.log',
						includes=['GeoFence'],
						ignores=self.IGNORE,
						replace=self.REPLACE,
						sort=True)
		self.checkSanity('correlator.log')	
