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
		
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", [], [], {})')
		self.waitForSignal('correlator.log', expr='Error spawning Prediction Analytic instance', condition='==1', timeout=30)
		
		# Sending the config events here, rather than from a file as the plugin instances are relatively slow
		# to respond and highly parallel when they do (the latter is good), but I want to keep the logging of each
		# trial distinct. 
		
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"modelName":"Iris_KM"})')
		# Different expression as there's a bug which means the error callback isn't called.
		# Unfortunately the plugin has a bug from 9.12 related to the new dynamic model behaviour
		# which means it no longer picks up on when a file isn't where it should be. I don't want to have
		# to use the File adapter just to check for this.
		self.waitForSignal('correlator.log', expr='Error spawning Prediction Analytic instance', condition='==2', timeout=30)
		
		# File not found as we haven't provided the correct directory and it's not in the working dir.
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"modelName":"Iris_KM", "pmmlFileName":"EnergyDataModel.pmml"})')
		self.waitForSignal('correlator.log', expr='Error spawning Prediction Analytic instance', condition='==3', timeout=30)
		
		# This will induce warnings, but not an error as we can't actually tell which fields are mandatory or not.
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.log', expr='Analytic Prediction started for inputDataNames', condition='==1', timeout=30)

		# Input fields can duplicate mapping, output fields can't.
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"SEPAL_LE":"Input.DVALUE", "SEPAL_WI":"Input.DVALUE", "Cluster ID":"Output.DVALUE", "Cluster Affinity for predicted":"Output.DVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.log', expr='Error spawning Prediction Analytic instance', condition='==4', timeout=30)

		# As above using prefixes and different cases.
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"input.SEPAL_LE":"Input.dvalue", "input.SEPAL_WI":"Input.Dvalue", "output.Cluster ID":"Output.dValue", "output.Cluster Affinity for predicted":"Output.DValue", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.log', expr='Error spawning Prediction Analytic instance', condition='==5', timeout=30)

		# Mapping channels not in provided sequence of channels
		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["Input"], ["Output"], {"SEPAL_LE":"Inputx.DVALUE", "Cluster ID":"Outputx.DVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.log', expr='Error spawning Prediction Analytic instance', condition='==6', timeout=30)

		
	def validate(self):
		# Ensure the test output was correct
		exprList=[]
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\[\],\[\],{}\)')

		exprList.append('Mandatory param modelName missing.')
		exprList.append('Error spawning Prediction Analytic instance.')
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"modelName":"Iris_KM"}\)')
		exprList.append('Loaded models: \[\]')
		exprList.append('Model Iris_KM not found in PMML file \'\'.')
		exprList.append('Error spawning Prediction Analytic instance.')
		
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"modelName":"Iris_KM","pmmlFileName":"EnergyDataModel.pmml"}\)')
		exprList.append('Loaded models: \[\]')
		exprList.append('Model Iris_KM not found in PMML file \'EnergyDataModel.pmml\'.')
		exprList.append('Error spawning Prediction Analytic instance.')
		
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"modelName":"Iris_KM","pmmlFileDirectory":".*/tests/tools/models","pmmlFileName":"Iris_KM.pmml"}\)')
		exprList.append('Loaded models: \["Iris_KM"\]')
		exprList.append('Prediction Analytic using model Iris_KM from Iris_KM.pmml')
		exprList.append('Input fields : \["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\]')
		exprList.append('Output fields: \["predictedValue_CLASS","Cluster ID","Cluster Affinity for predicted","Cluster Affinity for setosa","Cluster Affinity for versic","Cluster Affinity for virgin"\]')
		exprList.append('No map found for model input parameter: SEPAL_LE')
		exprList.append('No map found for model input parameter: SEPAL_WI')
		exprList.append('No map found for model input parameter: PETAL_LE')
		exprList.append('No map found for model input parameter: PETAL_WI')
		exprList.append('No map found for model output parameter: predictedValue_CLASS')
		exprList.append('No map found for model output parameter: Cluster ID')
		exprList.append('No map found for model output parameter: Cluster Affinity for predicted')
		exprList.append('No map found for model output parameter: Cluster Affinity for setosa')
		exprList.append('No map found for model output parameter: Cluster Affinity for versic')
		exprList.append('No map found for model output parameter: Cluster Affinity for virgin')
		exprList.append('Analytic Prediction started for inputDataNames \["Input"\]')
		
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"Cluster Affinity for predicted":"Output.DVALUE","Cluster ID":"Output.DVALUE","SEPAL_LE":"Input.DVALUE","SEPAL_WI":"Input.DVALUE","modelName":"Iris_KM","pmmlFileDirectory":".*/tests/tools/models","pmmlFileName":"Iris_KM.pmml"}\)')
		exprList.append('Loaded models: \["Iris_KM"\]')
		exprList.append('Prediction Analytic using model Iris_KM from Iris_KM.pmml')
		exprList.append('Input fields : \["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\]')
		exprList.append('Output fields: \["predictedValue_CLASS","Cluster ID","Cluster Affinity for predicted","Cluster Affinity for setosa","Cluster Affinity for versic","Cluster Affinity for virgin"\]')
		exprList.append('Duplicate mapping Input.DVALUE for PMML model input parameters.')
		exprList.append('No map found for model input parameter: PETAL_LE')
		exprList.append('No map found for model input parameter: PETAL_WI')
		exprList.append('No map found for model output parameter: predictedValue_CLASS')
		exprList.append('Duplicate mapping Output.DVALUE for PMML model output parameters.')
		exprList.append('No map found for model output parameter: Cluster Affinity for setosa')
		exprList.append('No map found for model output parameter: Cluster Affinity for versic')
		exprList.append('No map found for model output parameter: Cluster Affinity for virgin')
		exprList.append('Error spawning Prediction Analytic instance.')
		
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"input.SEPAL_LE":"Input.dvalue","input.SEPAL_WI":"Input.Dvalue","modelName":"Iris_KM","output.Cluster Affinity for predicted":"Output.DValue","output.Cluster ID":"Output.dValue","pmmlFileDirectory":".*/tests/tools/models","pmmlFileName":"Iris_KM.pmml"}\)')
		exprList.append('Loaded models: \["Iris_KM"\]')
		exprList.append('Prediction Analytic using model Iris_KM from Iris_KM.pmml')
		exprList.append('Input fields : \["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\]')
		exprList.append('Output fields: \["predictedValue_CLASS","Cluster ID","Cluster Affinity for predicted","Cluster Affinity for setosa","Cluster Affinity for versic","Cluster Affinity for virgin"\]')
		exprList.append('Duplicate mapping Input.Dvalue for PMML model input parameters.')
		exprList.append('No map found for model input parameter: PETAL_LE')
		exprList.append('No map found for model input parameter: PETAL_WI')
		exprList.append('No map found for model output parameter: predictedValue_CLASS')
		exprList.append('Duplicate mapping Output.DValue for PMML model output parameters.')
		exprList.append('No map found for model output parameter: Cluster Affinity for setosa')
		exprList.append('No map found for model output parameter: Cluster Affinity for versic')
		exprList.append('No map found for model output parameter: Cluster Affinity for virgin')
		exprList.append('Error spawning Prediction Analytic instance.')
		
		exprList.append('Validating com.industry.analytics.Analytic\("Prediction",\["Input"\],\["Output"\],{"Cluster ID":"Outputx.DVALUE","SEPAL_LE":"Inputx.DVALUE","modelName":"Iris_KM","pmmlFileDirectory":".*/tests/tools/models","pmmlFileName":"Iris_KM.pmml"}\)')
		exprList.append('Loaded models: \["Iris_KM"\]')
		exprList.append('Prediction Analytic using model Iris_KM from Iris_KM.pmml')
		exprList.append('Input fields : \["SEPAL_LE","SEPAL_WI","PETAL_LE","PETAL_WI"\]')
		exprList.append('Output fields: \["predictedValue_CLASS","Cluster ID","Cluster Affinity for predicted","Cluster Affinity for setosa","Cluster Affinity for versic","Cluster Affinity for virgin"\]')
		exprList.append('Data name Inputx not found in the list of inputDataNames: \["Input"\]')
		exprList.append('No map found for model input parameter: SEPAL_WI')
		exprList.append('No map found for model input parameter: PETAL_LE')
		exprList.append('No map found for model input parameter: PETAL_WI')
		exprList.append('No map found for model output parameter: predictedValue_CLASS')
		exprList.append('Data name Outputx not found in the list of outputDataNames: \["Output"\]')
		exprList.append('No map found for model output parameter: Cluster Affinity for predicted')
		exprList.append('No map found for model output parameter: Cluster Affinity for setosa')
		exprList.append('No map found for model output parameter: Cluster Affinity for versic')
		exprList.append('No map found for model output parameter: Cluster Affinity for virgin')
		exprList.append('Error spawning Prediction Analytic instance.')
		self.assertOrderedGrep("correlator.log", exprList=exprList)
		
		self.checkSanity()	
