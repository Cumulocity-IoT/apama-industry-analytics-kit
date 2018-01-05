# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(inputLog="input.log")
		self.injectAnalytic(correlator)
		self.injectSlicer(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output.evt', channels=['Output'])
		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Slicer started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('input.log', expr='"Input",com.industry.analytics\.Data', condition='==2', timeout=15)
		self.waitForSignal('Output.evt', expr='com.industry.analytics.Data.*', condition='==20', timeout=15)

		
	def validate(self):
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",2,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",3,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",4,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",5,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",5,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",6,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",6,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",7,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",7,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",8,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",8,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",9,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",9,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",10,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",10,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s1",11,1.5,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",11,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",12,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",13,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.assertGrep('Output.evt', expr='com.industry.analytics.Data.*"Output","c","s2",14,2.55,"",1,2,3,{"sliceType":"slicecount","sliceValue":"10","timeInterval":"1"}')
		self.checkSanity()	
