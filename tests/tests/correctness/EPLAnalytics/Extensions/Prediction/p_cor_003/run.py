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
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"SEPAL_LE":"Input.DVALUE", "SEPAL_WI":"Input.XVALUE", "PETAL_LE":"Input.YVALUE", "PETAL_WI":"Input.ZVALUE", "predictedValue_CLASS":"Output.SVALUE", "Cluster Affinity for predicted":"Output.DVALUE", "Cluster Affinity for setosa":"Output.XVALUE", "Cluster Affinity for versic":"Output.YVALUE", "Cluster Affinity for virgin":"Output.ZVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.log', expr='Analytic Prediction started for inputDataNames', condition='==1', timeout=30)

		correlator.send(["Measures.evt"])
		self.waitForSignal('Output.evt', expr='\.Data\(', condition='==2', timeout=30)		

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"Cluster Affinity for predicted":"Output.DVALUE","Cluster Affinity for setosa":"Output.XVALUE","Cluster Affinity for versic":"Output.YVALUE","Cluster Affinity for virgin":"Output.ZVALUE","PETAL_LE":"Input.YVALUE","PETAL_WI":"Input.ZVALUE","SEPAL_LE":"Input.DVALUE","SEPAL_WI":"Input.XVALUE","modelName":"Iris_KM","pmmlFileDirectory":".*/tests/tools/models","pmmlFileName":"Iris_KM.pmml","predictedValue_CLASS":"Output.SVALUE"}\)')
		exprList.append('Loaded models: \["Iris_KM"\]')
		exprList.append('Prediction Analytic using model Iris_KM from Iris_KM.pmml')
		exprList.append('Input fields : \["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\]')
		exprList.append('Output fields: \["predictedValue_CLASS","Cluster ID","Cluster Affinity for predicted","Cluster Affinity for setosa","Cluster Affinity for versic","Cluster Affinity for virgin"\]')
		exprList.append('No map found for model output parameter: Cluster ID')
		exprList.append('Analytic Prediction started for inputDataNames \["Input"\]')
		self.assertOrderedGrep("correlator.log", exprList=exprList)

		self.assertDiff('Output.evt', 'Output.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
