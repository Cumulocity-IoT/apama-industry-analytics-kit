# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(logfile='correlator.log',
									inputLog='correlator_input.log',
									enableJava=True)
		self.injectAnalytic(correlator)
		self.injectPrediction(correlator)
		self.ready(correlator)
		correlator.receive(filename="Output.evt", channels=["Output"])

		# Drop Cluster ID from output in this case.
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"Temperature":"Input.XVALUE", "Pressure":"Input.YVALUE", "RPM":"Input.ZVALUE", "svm_predict_function":"Output.DVALUE", "modelName":"PredictedEngineStatus", "pmmlFileName":"Engine.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.log', expr='Analytic Prediction started for inputDataNames', condition='==1', timeout=30)

		dataFile = open(os.path.join(self.input, 'engine_sample.csv'), 'r')
		for line in dataFile:
			tokens = line.strip('\n').split(',')
			correlator.sendEventStrings('com.industry.analytics.Data("Input", "r", "engine1", ' + tokens[0] +
									    ', 0, "", ' + tokens[1] + ', ' + tokens[2] + ', ' + tokens[3] + ', {})', channel='Input')

		self.waitForSignal('Output.evt', expr='\.Data\(', condition='==777', timeout=30)		

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"Pressure":"Input.YVALUE","RPM":"Input.ZVALUE","Temperature":"Input.XVALUE","modelName":"PredictedEngineStatus","pmmlFileDirectory":".*/tests/tools/models","pmmlFileName":"Engine.pmml","svm_predict_function":"Output.DVALUE"}\)')
		exprList.append('Loaded models: \["PredictedEngineStatus"\]')
		exprList.append('Prediction Analytic using model PredictedEngineStatus from Engine.pmml')
		exprList.append('Input fields : \["Temperature","Pressure","RPM"\]')
		exprList.append('Output fields: \["predictedValue","svm_predict_function"\]')
		exprList.append('No map found for model output parameter: predictedValue')
		exprList.append('Analytic Prediction started for inputDataNames \["Input"\]')
		self.assertOrderedGrep("correlator.log", exprList=exprList)

		self.assertDiff('Output.evt', 'Output.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
