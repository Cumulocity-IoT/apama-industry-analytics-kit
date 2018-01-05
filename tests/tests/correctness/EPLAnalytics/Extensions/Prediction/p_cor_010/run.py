# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(enableJava=True)
		self.injectAnalytic(correlator)
		self.injectPrediction(correlator)
		self.ready(correlator)

		correlator.sendEventStrings('com.industry.analytics.Analytic("prediction", ["SEPAL_LE", "SEPAL_WI", "PETAL_LE", "PETAL_WI"], ["predictedValue_CLASS", "Cluster ID", "Cluster Affinity for predicted", "Cluster Affinity for setosa", "Cluster Affinity for versic", "Cluster Affinity for virgin"], {"SEPAL_LE":"SEPAL_LE.DVALUE", "SEPAL_WI":"SEPAL_WI.DVALUE", "PETAL_LE":"PETAL_LE.DVALUE", "PETAL_WI":"PETAL_WI.DVALUE", "predictedValue_CLASS":"predictedValue_CLASS.SVALUE", "Cluster ID":"Cluster ID.SVALUE", "Cluster Affinity for predicted":"Cluster Affinity for predicted.DVALUE", "Cluster Affinity for setosa":"Cluster Affinity for setosa.DVALUE", "Cluster Affinity for versic":"Cluster Affinity for versic.DVALUE", "Cluster Affinity for virgin":"Cluster Affinity for virgin.DVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.out', expr='Analytic [p|P]rediction started for inputDataNames', condition='==1', timeout=20)

		correlator.sendEventStrings('com.industry.analytics.Analytic("PREDICTION", ["SEPAL_LE", "SEPAL_WI", "PETAL_LE", "PETAL_WI"], ["predictedValue_CLASS", "Cluster ID", "Cluster Affinity for predicted", "Cluster Affinity for setosa", "Cluster Affinity for versic", "Cluster Affinity for virgin"], {"SEPAL_LE":"SEPAL_LE.DVALUE", "SEPAL_WI":"SEPAL_WI.DVALUE", "PETAL_LE":"PETAL_LE.DVALUE", "PETAL_WI":"PETAL_WI.DVALUE", "predictedValue_CLASS":"predictedValue_CLASS.SVALUE", "Cluster ID":"Cluster ID.SVALUE", "Cluster Affinity for predicted":"Cluster Affinity for predicted.DVALUE", "Cluster Affinity for setosa":"Cluster Affinity for setosa.DVALUE", "Cluster Affinity for versic":"Cluster Affinity for versic.DVALUE", "Cluster Affinity for virgin":"Cluster Affinity for virgin.DVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.out', expr='Analytic [p|P]rediction started for inputDataNames', condition='==2', timeout=20)

		correlator.sendEventStrings('com.industry.analytics.Analytic("PrEdIcTiOn", ["SEPAL_LE", "SEPAL_WI", "PETAL_LE", "PETAL_WI"], ["predictedValue_CLASS", "Cluster ID", "Cluster Affinity for predicted", "Cluster Affinity for setosa", "Cluster Affinity for versic", "Cluster Affinity for virgin"], {"SEPAL_LE":"SEPAL_LE.DVALUE", "SEPAL_WI":"SEPAL_WI.DVALUE", "PETAL_LE":"PETAL_LE.DVALUE", "PETAL_WI":"PETAL_WI.DVALUE", "predictedValue_CLASS":"predictedValue_CLASS.SVALUE", "Cluster ID":"Cluster ID.SVALUE", "Cluster Affinity for predicted":"Cluster Affinity for predicted.DVALUE", "Cluster Affinity for setosa":"Cluster Affinity for setosa.DVALUE", "Cluster Affinity for versic":"Cluster Affinity for versic.DVALUE", "Cluster Affinity for virgin":"Cluster Affinity for virgin.DVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.out', expr='Analytic [p|P]rediction started for inputDataNames', condition='==3', timeout=20)

		correlator.sendEventStrings('com.industry.analytics.Analytic("Prediction", ["SEPAL_LE", "SEPAL_WI", "PETAL_LE", "PETAL_WI"], ["predictedValue_CLASS", "Cluster ID", "Cluster Affinity for predicted", "Cluster Affinity for setosa", "Cluster Affinity for versic", "Cluster Affinity for virgin"], {"SEPAL_LE":"SEPAL_LE.DVALUE", "SEPAL_WI":"SEPAL_WI.DVALUE", "PETAL_LE":"PETAL_LE.DVALUE", "PETAL_WI":"PETAL_WI.DVALUE", "predictedValue_CLASS":"predictedValue_CLASS.SVALUE", "Cluster ID":"Cluster ID.SVALUE", "Cluster Affinity for predicted":"Cluster Affinity for predicted.DVALUE", "Cluster Affinity for setosa":"Cluster Affinity for setosa.DVALUE", "Cluster Affinity for versic":"Cluster Affinity for versic.DVALUE", "Cluster Affinity for virgin":"Cluster Affinity for virgin.DVALUE", "modelName":"Iris_KM", "pmmlFileName":"Iris_KM.pmml", "pmmlFileDirectory":"'+self.PMMLMODELS+'"})')
		self.waitForSignal('correlator.out', expr='Analytic [p|P]rediction started for inputDataNames', condition='==4', timeout=20)

	def validate(self):
		self.checkSanity()
		self.assertLineCount('correlator.out', expr='Analytic [p|P]rediction started for inputDataNames', condition='==4')
