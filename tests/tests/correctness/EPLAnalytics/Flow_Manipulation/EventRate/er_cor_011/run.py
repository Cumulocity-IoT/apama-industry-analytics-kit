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
		correlator.send('Events.evt')
		self.waitForSignal('Output.evt', expr='com.industry.analytics\.Data', condition='>=21', timeout=5)

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		# First set should be around 1 eps (rounding errors may occur due to real time)
		exprList.append('com.industry.analytics.Data\("Output","c","s1",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s2",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s3",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		# 2nd set should be around 2 eps( rounding errors may occur due to real time)
		exprList.append('com.industry.analytics.Data\("Output","c","s1",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s2",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s3",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		## 3rd set should be around 2 eps( rounding errors may occur due to real time)
		exprList.append('com.industry.analytics.Data\("Output","c","s1",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s2",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s3",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		## 4th set should be around 2 eps( rounding errors may occur due to real time)
		exprList.append('com.industry.analytics.Data\("Output","c","s1",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s2",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s3",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		# 5th set should be around 2 eps (rounding errors may occur due to real time), as we have stopped sending events, but still have data
		exprList.append('com.industry.analytics.Data\("Output","c","s1",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s2",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s3",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		# 6th set should be around 2 eps (rounding errors may occur due to real time), as we have stopped sending events, but still have data
		exprList.append('com.industry.analytics.Data\("Output","c","s1",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s2",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s3",.*,(1\.9.*|2(\.0.*)?),"",0,0,0,{}\)')
		# 7th set should be 0eps as we have stopped sending events
		exprList.append('com.industry.analytics.Data\("Output","c","s1",.*,0,"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s2",.*,0,"",0,0,0,{}\)')
		exprList.append('com.industry.analytics.Data\("Output","c","s3",.*,0,"",0,0,0,{}\)')
		self.assertOrderedGrep("Output.evt", exprList=exprList)

		# Ensure the Correlator log was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("EventRate",\["Input"\],\["Output"\],{"bySourceId":"true","useCorrelatorTime":"true"}\)')
		exprList.append('Analytic EventRate started for inputDataNames \["Input"\]')
		self.assertOrderedGrep("correlator.out", exprList=exprList)
		
		self.checkSanity()	
