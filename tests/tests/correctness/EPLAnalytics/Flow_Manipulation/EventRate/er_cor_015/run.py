# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(Xclock=FALSE)
		self.injectAnalytic(correlator)
		self.injectEventRate(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output.evt', channels=['Output'])
		correlator.injectMonitorscript(['test.mon'], self.input)

		# Wait until we get the last Data events
		self.waitForSignal('Output.evt', expr='com.industry.analytics\.Data', condition='>=10', timeout=15)
		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		self.assertOrderedGrep("Output.evt", exprList=exprList)


		# Ensure the Correlator log was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("EventRate",\["Input"\],\["Output"\],{"bySourceId":"false","useCorrelatorTime":"true"}\)')
		exprList.append('Analytic EventRate started for inputDataNames \["Input"\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		self.checkSanity()	
