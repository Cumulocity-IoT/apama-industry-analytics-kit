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

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic EventRate started for inputDataNames',
						   condition='==1',
						   timeout=5)
		# Wait until we get the first Data before sending in the events
		self.waitForSignal('Output.evt', expr='com.industry.analytics\.Data', condition='==1', timeout=5)
		# Send the test events in
		correlator.send('Events.evt')
		# Wait until we get the last Data events
		self.waitForSignal('Output.evt', expr='com.industry.analytics\.Data', condition='>=7', timeout=5)

	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		
		# The first line should be 0, as we wait until we get the first Data before sending events
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,0,"",0,0,0,{}\)')
		# Next lines should be around 10 eps (rounding errors may occur due to real time)
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,(9\.9.*|10(\.0.*)?),"",0,0,0,{}\)')
		# Then line are 0 as we previously stopped sending events
		exprList.append('com.industry.analytics.Data\("Output","c","",.*,0,"",0,0,0,{}\)')
		self.assertOrderedGrep("Output.evt", exprList=exprList)
		
		# Ensure the Correlator log was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("EventRate",\["Input"\],\["Output"\],{"bySourceId":"false","useCorrelatorTime":"true"}\)')
		exprList.append('Analytic EventRate started for inputDataNames \["Input"\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		self.checkSanity()	
