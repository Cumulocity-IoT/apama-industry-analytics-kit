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
		correlator.receive(filename="predictedValue_CLASS.evt", channels=["predictedValue_CLASS"])
		correlator.receive(filename="Cluster ID.evt", channels=["Cluster ID"])
		correlator.receive(filename="Cluster Affinity for predicted.evt", channels=["Cluster Affinity for predicted"])
		correlator.receive(filename="Cluster Affinity for setosa.evt", channels=["Cluster Affinity for setosa"])
		correlator.receive(filename="Cluster Affinity for versic.evt", channels=["Cluster Affinity for versic"])
		correlator.receive(filename="Cluster Affinity for virgin.evt", channels=["Cluster Affinity for virgin"])

		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["SEPAL_LE", "SEPAL_WI", "PETAL_LE", "PETAL_WI"], ["predictedValue_CLASS", "Cluster ID", "Cluster Affinity for predicted", "Cluster Affinity for setosa", "Cluster Affinity for versic", "Cluster Affinity for virgin"], {"SEPAL_LE":"SEPAL_LE.PVALUE.currValue", "SEPAL_WI":"SEPAL_WI.PVALUE.currValue", "PETAL_LE":"PETAL_LE.PVALUE.currValue", "PETAL_WI":"PETAL_WI.PVALUE.currValue", "predictedValue_CLASS":"predictedValue_CLASS.SVALUE", "Cluster ID":"Cluster ID.SVALUE", "Cluster Affinity for predicted":"Cluster Affinity for predicted.DVALUE", "Cluster Affinity for setosa":"Cluster Affinity for setosa.DVALUE", "Cluster Affinity for versic":"Cluster Affinity for versic.DVALUE", "Cluster Affinity for virgin":"Cluster Affinity for virgin.DVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.log', expr='Analytic Prediction started for inputDataNames', condition='==1', timeout=30)

		correlator.send(["Measures.evt"])
		self.waitForSignal('Cluster ID.evt', expr='\.Data\(', condition='==2', timeout=30)		

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\],\["predictedValue_CLASS","Cluster ID","Cluster Affinity for predicted","Cluster Affinity for setosa","Cluster Affinity for versic","Cluster Affinity for virgin"\],{"Cluster Affinity for predicted":"Cluster Affinity for predicted.DVALUE","Cluster Affinity for setosa":"Cluster Affinity for setosa.DVALUE","Cluster Affinity for versic":"Cluster Affinity for versic.DVALUE","Cluster Affinity for virgin":"Cluster Affinity for virgin.DVALUE","Cluster ID":"Cluster ID.SVALUE","PETAL_LE":"PETAL_LE.PVALUE.currValue","PETAL_WI":"PETAL_WI.PVALUE.currValue","SEPAL_LE":"SEPAL_LE.PVALUE.currValue","SEPAL_WI":"SEPAL_WI.PVALUE.currValue","modelName":"Iris_KM","pmmlFileDirectory":".*/tests/tools/models","pmmlFileName":"Iris_KM.pmml","predictedValue_CLASS":"predictedValue_CLASS.SVALUE"}\)')
		exprList.append('Loaded models: \["Iris_KM"\]')
		exprList.append('Prediction Analytic using model Iris_KM from Iris_KM.pmml')
		exprList.append('Input fields : \["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\]')
		exprList.append('Output fields: \["predictedValue_CLASS","Cluster ID","Cluster Affinity for predicted","Cluster Affinity for setosa","Cluster Affinity for versic","Cluster Affinity for virgin"\]')
		exprList.append('Analytic Prediction started for inputDataNames \["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\]')
		self.assertOrderedGrep("correlator.log", exprList=exprList)
						
		self.assertDiff('predictedValue_CLASS.evt', 'predictedValue_CLASS.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
		self.assertDiff('Cluster ID.evt', 'Cluster ID.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
		self.assertDiff('Cluster Affinity for predicted.evt', 'Cluster Affinity for predicted.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
		self.assertDiff('Cluster Affinity for setosa.evt', 'Cluster Affinity for setosa.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
		self.assertDiff('Cluster Affinity for versic.evt', 'Cluster Affinity for versic.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
		self.assertDiff('Cluster Affinity for virgin.evt', 'Cluster Affinity for virgin.evt', replace=[('\",[0-9]{10}\.*[0-9]*,','",<TIMESTAMP>,')])
		self.checkSanity()	
