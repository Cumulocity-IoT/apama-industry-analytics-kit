# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG
from industry.framework.BaseTest import IndustrySolutionsBaseTest
from pysys.basetest import BaseTest
from pysys.constants import *
from pysys.utils.filediff import trimContents
from pysys.utils.filediff import replace as diffReplace
import os

class AnalyticsBaseTest(IndustrySolutionsBaseTest):
	IGNORE = ['Injected MonitorScript',
			  'injected into a non-persistent correlator',
			  'Current Working Directory: ']
	REPLACE = [('^.*INFO  \[.*\] - ','INFO  - '),
			   ('^.*WARN  \[.*\] - ','WARN  - '),
			   ('^.*ERROR \[.*\] - ','ERROR - '),
			   (' \[[0-9]{1,2}\] ',' [__] ')]

	def __init__(self, descriptor, outsubdir, runner):
		IndustrySolutionsBaseTest.__init__(self, descriptor, outsubdir, runner)

		self.CACHE      = os.path.join(self.COMPONENT_MONITORS_DIR,'cache')
		self.COMPONENTS = os.path.join(self.COMPONENT_MONITORS_DIR,'components')
		self.INTERFACES = os.path.join(self.COMPONENT_MONITORS_DIR,'interfaces')
		self.OBJECTS    = os.path.join(self.COMPONENT_MONITORS_DIR,'objects')
		self.REFLECTORS = os.path.join(self.COMPONENT_MONITORS_DIR,'reflectors')
		self.CORE_ANALYTICS_ROOT   = os.path.join(self.COMPONENT_MONITORS_DIR,'analytics','core')
		self.ANALYTICS_DETECTORS   = os.path.join(self.CORE_ANALYTICS_ROOT,'Detectors')
		self.ANALYTICS_EXTENSIONS  = os.path.join(self.CORE_ANALYTICS_ROOT,'Extensions')
		self.ANALYTICS_FLOW        = os.path.join(self.CORE_ANALYTICS_ROOT,'Flow_Manipulation')
		self.ANALYTICS_GEOLOCATION = os.path.join(self.CORE_ANALYTICS_ROOT,'GeoLocation')
		self.ANALYTICS_STREAMING   = os.path.join(self.CORE_ANALYTICS_ROOT,'Streaming_Calculations')
		self.ANALYTICS_UTILITIES   = os.path.join(self.CORE_ANALYTICS_ROOT,'Utilities')
		self.RETAIL_ANALYTICS_ROOT         = os.path.join(self.COMPONENT_MONITORS_DIR_RETAIL,'analytics','retail')
		self.MANUFACTURING_ANALYTICS_ROOT  = os.path.join(self.COMPONENT_MONITORS_DIR_MANUFACTURING,'analytics','manufacturing')
		self.UTILITY_ANALYTICS_ROOT         = os.path.join(self.COMPONENT_MONITORS_DIR_UTILITY,'analytics','utility')
		self.PMMLMODELS = os.path.join(PROJECT.root, 'tools', 'models').replace("\\","/")  #We always want to use forward slashes as this is used in event params
	
		self.commonInjected = {}
		
	def startTest(self, Xclock=True, logfile='correlator.out', applicationEventLogging=False, 
				  inputLog=None, logLevel="INFO", host="localhost", port=None, 
				  outputLog='output.log',  enableJava=False, enableJMS=False, jmsConfigPath=None, 
				  persistence=False, persistenceStoreName=None,
				  persistenceStoreLocation=None, distMemStoreConfig=None):
		# Create a Correlator Helper    
		self.correlator = IndustrySolutionsBaseTest.startTest( self, Xclock=Xclock, logfile=logfile,
																applicationEventLogging=applicationEventLogging,
																inputLog=inputLog, logLevel=logLevel, host=host, port=port,
																outputLog=outputLog, persistence=persistence,
																persistenceStoreName=persistenceStoreName,
																persistenceStoreLocation=persistenceStoreLocation, 
																enableJava=enableJava, enableJMS=enableJMS, jmsConfigPath=jmsConfigPath, 
																distMemStoreConfig=distMemStoreConfig )
		return self.correlator

		
	#####################################################
	# Functions to inject the core of the Analytics Kit #
	#####################################################
	def injectDataSourceService(self, correlator):
		self.injectCommon(correlator)
		correlator.injectMonitorscript(['DataSource.mon'], self.COMPONENT_EVENT_DEFS_DIR)
		correlator.injectMonitorscript(['DataSourceService.mon'], self.CACHE)
	
	
	def injectCommon(self, correlator):
		if not correlator in self.commonInjected:
			self.injectMemoryStoreMonitors(correlator)
			self.injectDataViewMonitors(correlator)
			correlator.injectMonitorscript(['Constants.mon'], self.COMPONENT_EVENT_DEFS_DIR)
			correlator.injectMonitorscript(['MemStoreUtil.mon',
											'Cache.mon',
											'DataView.mon'], self.CACHE)
			self.commonInjected[correlator] = True
			
			
	def injectQueryAnalytic(self, correlator):
		self.injectCommon(correlator)
		correlator.injectMonitorscript(['Data.mon'], self.COMPONENT_EVENT_DEFS_DIR)
		
		
	def injectAnalytic(self, correlator):
		self.injectCommon(correlator)
		correlator.injectMonitorscript(['Data.mon',
										'Analytic.mon',
										'Ready.mon'], self.COMPONENT_EVENT_DEFS_DIR)
		correlator.injectMonitorscript(['AnalyticInterface.mon'], self.INTERFACES)
		correlator.injectMonitorscript(['AnalyticObject.mon'], self.OBJECTS)
		correlator.injectMonitorscript(['VersioningService.mon'], self.OBJECTS)

	########################################
	# DETECTORS group injection functions  #
	########################################
	def injectCorridor(self, correlator):
		correlator.injectMonitorscript(['Corridor.mon',
										'CorridorService.mon'], self.ANALYTICS_DETECTORS)

	def injectDrift(self, correlator):
		correlator.injectMonitorscript(['TimeWeightedMovingAverage.mon',
										'TimeWeightedVariance.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['Drift.mon',
										'DriftService.mon'], self.ANALYTICS_DETECTORS)
										
	def injectMissingData(self, correlator):
		correlator.injectMonitorscript(['MissingData.mon',
										'MissingDataService.mon'], self.ANALYTICS_DETECTORS)

	def injectPeerAnalysis(self, correlator):
		self.injectAverage( correlator )
		self.injectSpread( correlator )
		self.injectThreshold( correlator )
		correlator.injectMonitorscript(['PeerAnalysis.mon',
										'PeerAnalysisService.mon'], self.ANALYTICS_DETECTORS)

	def injectSpike(self, correlator):
		correlator.injectMonitorscript(['TimeWeightedMovingAverage.mon',
										'TimeWeightedVariance.mon',
										'TimeWeightedBollinger.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['Spike.mon',
										'SpikeService.mon'], self.ANALYTICS_DETECTORS)

	def injectThreshold(self, correlator):
		correlator.injectMonitorscript(['Threshold.mon',
										'ThresholdService.mon'], self.ANALYTICS_DETECTORS)

	########################################
	# EXTENSIONS group injection functions #
	########################################
	def injectPrediction(self, correlator):
		correlator.injectJava('Predictive-Analytics-Plugin.jar', os.path.join(self.APAMA_HOME,'adapters','lib'))
		correlator.injectCDP(['predictive_analytics_plugin_monitors.cdp'], self.APAMA_ADAPTER_MONITORS_DIR)
		correlator.injectMonitorscript(['Prediction.mon',
										'PredictionService.mon'], self.ANALYTICS_EXTENSIONS)

	###############################################
	# FLOW_MANIPULATION group injection functions #
	###############################################
	def injectCombiner(self, correlator):
		correlator.injectMonitorscript(['Combiner.mon',
										'CombinerService.mon'], self.ANALYTICS_FLOW)

	def injectDuplicator(self, correlator):
		correlator.injectMonitorscript(['Duplicator.mon',
										'DuplicatorService.mon'], self.ANALYTICS_FLOW)

	def injectEventRate(self, correlator):
		correlator.injectMonitorscript(['EventRate.mon',
										'EventRateService.mon'], self.ANALYTICS_FLOW)

	def injectFilter(self, correlator):
		correlator.injectMonitorscript(['Filter.mon',
										'FilterService.mon'], self.ANALYTICS_FLOW)

	def injectMapper(self, correlator):
		correlator.injectMonitorscript(['Mapper.mon',
										'MapperService.mon'], self.ANALYTICS_FLOW)
										
	def injectMerger(self, correlator):
		correlator.injectMonitorscript(['Merger.mon',
										'MergerService.mon'], self.ANALYTICS_FLOW)

	def injectRepeater(self, correlator):
		correlator.injectMonitorscript(['Repeater.mon',
										'RepeaterService.mon'], self.ANALYTICS_FLOW)

	def injectSorter(self, correlator):
		correlator.injectMonitorscript(['Sorter.mon',
										'SorterService.mon'], self.ANALYTICS_FLOW)

	def injectSlicer(self, correlator):
		correlator.injectMonitorscript(['Slicer.mon',
										'SlicerService.mon'], self.ANALYTICS_FLOW)

	def injectSuppressor(self, correlator):
		correlator.injectMonitorscript(['Suppressor.mon',
										'SuppressorService.mon'], self.ANALYTICS_FLOW)
										
	def injectThrottler(self, correlator):
		correlator.injectMonitorscript(['Throttler.mon',
										'ThrottlerService.mon'], self.ANALYTICS_FLOW)
	
	#########################################
	# GEOLOCATION group injection functions #
	#########################################
	def injectGeoFence(self, correlator):
		correlator.injectMonitorscript(['GeoFence.mon',
										'GeoFenceService.mon'], self.ANALYTICS_GEOLOCATION)

	def injectDistance(self, correlator):
		correlator.injectMonitorscript(['GeoUtil.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['Distance.mon',
										'DistanceService.mon'], self.ANALYTICS_GEOLOCATION)

	def injectSpeed(self, correlator):
		correlator.injectMonitorscript(['GeoUtil.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['Speed.mon',
										'SpeedService.mon'], self.ANALYTICS_GEOLOCATION)
	
	#########################################
	# MANFACTURING group injection functions #
	#########################################
	def injectCommonManufacturing(self, correlator):
		correlator.injectMonitorscript(['BucketSystem.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['ManufacturingConstants.mon'], self.MANUFACTURING_ANALYTICS_ROOT)
	
	def injectAvailability(self, correlator):
		correlator.injectMonitorscript(['Availability.mon', 'AvailabilityService.mon'], self.MANUFACTURING_ANALYTICS_ROOT)
		
	def injectPerformance(self, correlator):
		correlator.injectMonitorscript(['Performance.mon', 'PerformanceService.mon'], self.MANUFACTURING_ANALYTICS_ROOT)
		
	def injectQuality(self, correlator):
		correlator.injectMonitorscript(['Quality.mon', 'QualityService.mon'], self.MANUFACTURING_ANALYTICS_ROOT)
		
	def injectOEE(self, correlator):
		correlator.injectMonitorscript(['OEE.mon', 'OEEService.mon'], self.MANUFACTURING_ANALYTICS_ROOT)
		
	def injectResourceUsage(self, correlator):
		correlator.injectMonitorscript(['ResourceUsage.mon', 'ResourceUsageService.mon'], self.MANUFACTURING_ANALYTICS_ROOT)

	####################################################
	# STREAMING_CALCULATIONS group injection functions #
	####################################################
	def injectAverage(self, correlator):
		correlator.injectMonitorscript(['TimeWeightedMovingAverage.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['Average.mon',
										'AverageService.mon'], self.ANALYTICS_STREAMING)

	def injectDelta(self, correlator):
		correlator.injectMonitorscript(['Delta.mon',
										'DeltaService.mon'], self.ANALYTICS_STREAMING)

	def injectExpression(self, correlator):
		correlator.injectMonitorscript(['Expression.mon',
										'ExpressionService.mon'], self.ANALYTICS_STREAMING)
	
	def injectFFTAnalysis(self, correlator):
		correlator.injectMonitorscript(['ComplexNumber.mon',
										'fft.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['FFTAnalysis.mon',
										'FFTAnalysisService.mon'], self.ANALYTICS_STREAMING)
	
	def injectGradient(self, correlator):
		correlator.injectMonitorscript(['Gradient.mon',
										'GradientService.mon'], self.ANALYTICS_STREAMING)

	def injectMinMax(self, correlator):
		correlator.injectMonitorscript(['MinMax.mon',
										'MinMaxService.mon'], self.ANALYTICS_STREAMING)

	def injectMode(self, correlator):
		correlator.injectMonitorscript(['Mode.mon',
										'ModeService.mon'], self.ANALYTICS_STREAMING)

	def injectSpread(self, correlator):
		correlator.injectMonitorscript(['Spread.mon',
										'SpreadService.mon'], self.ANALYTICS_STREAMING)

	def injectSum(self, correlator):
		correlator.injectMonitorscript(['TimeWeightedMovingAverage.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['Sum.mon',
										'SumService.mon'], self.ANALYTICS_STREAMING)

	def injectVolatility(self, correlator):
		correlator.injectMonitorscript(['TimeWeightedMovingAverage.mon',
										'TimeWeightedVariance.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['Volatility.mon',
										'VolatilityService.mon'], self.ANALYTICS_STREAMING)

	#######################################
	# RETAIL group injection functions #
	#######################################	
	def injectCommonRetail(self, correlator):
		correlator.injectMonitorscript(['BucketSystem.mon'], self.COMPONENTS)
		
	def injectBasketAnalysis(self, correlator):
		correlator.injectMonitorscript(['TimeWeightedMovingAverage.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['BasketAnalysis.mon',
										'BasketAnalysisService.mon'], self.RETAIL_ANALYTICS_ROOT)
										
	def injectFootFall(self, correlator):
		self.injectGeoFence( correlator )
		self.injectMapper( correlator )
		self.injectSum( correlator )
		correlator.injectMonitorscript(['FootFall.mon',
										'FootFallService.mon'], self.RETAIL_ANALYTICS_ROOT)
	
	def injectSalesPerArea(self, correlator):
		self.injectSum( correlator )
		correlator.injectMonitorscript(['SalesPerArea.mon',
										'SalesPerAreaService.mon'], self.RETAIL_ANALYTICS_ROOT)
										
	def injectOnTimeArrival(self, correlator):
		correlator.injectMonitorscript(['OnTimeArrival.mon','OnTimeArrivalService.mon'], self.RETAIL_ANALYTICS_ROOT)
	
	def injectTimeOverdue(self, correlator):
		correlator.injectMonitorscript(['TimeOverdue.mon', 'TimeOverdueService.mon'], self.RETAIL_ANALYTICS_ROOT)
		
	def injectInventoryDays(self, correlator):
		correlator.injectMonitorscript(['TimeWeightedMovingAverage.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['InventoryDays.mon', 'InventoryDaysService.mon'], self.RETAIL_ANALYTICS_ROOT)

	def injectCategoryContribution(self, correlator):
		self.injectSum( correlator )
		correlator.injectMonitorscript(['CategoryContribution.mon',
										'CategoryContributionService.mon'], self.RETAIL_ANALYTICS_ROOT)

	def injectSalesPerVisitor(self, correlator):
		correlator.injectMonitorscript(['BucketSystem.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['SalesPerVisitor.mon',
										'SalesPerVisitorService.mon'], self.RETAIL_ANALYTICS_ROOT)
										
	def injectProjectedInventory(self, correlator):
		self.injectInventoryDays( correlator )
		correlator.injectMonitorscript(['ProjectedInventory.mon',
										'ProjectedInventoryService.mon'], self.RETAIL_ANALYTICS_ROOT)
										
	#######################################
	# UTILITY group injection functions #
	#######################################	
	def injectSAIDI(self, correlator):
		correlator.injectMonitorscript(['BucketSystem.mon'], self.COMPONENTS)
		correlator.injectMonitorscript(['SAIDI.mon',
										'SAIDIService.mon'], self.UTILITY_ANALYTICS_ROOT)
	
	#######################################
	# UTILITIES group injection functions #
	#######################################
	def injectDataViewer(self, correlator):
		correlator.injectMonitorscript(['DataViewReflector.mon'], self.REFLECTORS)
		correlator.injectMonitorscript(['DataViewer.mon',
										'DataViewerService.mon'], self.ANALYTICS_UTILITIES)

	def injectLogger(self, correlator):
		correlator.injectMonitorscript(['Logger.mon',
										'LoggerService.mon'], self.ANALYTICS_UTILITIES)

	def injectMemoryStore(self, correlator):
		correlator.injectMonitorscript(['MemoryStore.mon',
										'MemoryStoreService.mon'], self.ANALYTICS_UTILITIES)

	def injectDataSimulator(self, correlator):
		correlator.injectMonitorscript(['DataSimulator.mon',
										'DataSimulatorService.mon'], self.ANALYTICS_UTILITIES)

	#########################################
	# Utility functions to inject test code #
	#########################################
	def injectReflector(self, correlator):
		self.injectJMSSupportMonitors(correlator)
		correlator.injectMonitorscript(['JMSHandler.mon'], os.path.join(self.COMPONENT_TEST_MONITORS,'simulator'))
		correlator.injectMonitorscript(['Reflector.mon'], os.path.join(self.COMPONENT_MONITORS_DIR,'reflectors'))
		
	def injectTestSimulator(self, correlator):
		self.injectJMSSupportMonitors(correlator)
		self.injectAnalytic(correlator)
		self.injectDataSourceService(correlator)
		correlator.injectMonitorscript(['JMSHandler.mon'], os.path.join(self.COMPONENT_TEST_MONITORS,'simulator'))
		correlator.injectMonitorscript(['simulator.mon'],  os.path.join(self.COMPONENT_TEST_MONITORS,'simulator'))

	def ready(self, correlator):
		correlator.sendLiteral('com.industry.analytics.Ready()')

	#########################################
	# Utility functions for test validation #
	#########################################
	def assertDiff(self, file1, file2, filedir1=None, filedir2=None, ignores=[], sort=False, replace=[], includes=[], forceFriendlyFilesCreation=False, **xargs):
		'''Same semantic of the superclass, however in case of failure, it writes files easier to compare.
		'''
		BaseTest.assertDiff(self, file1, file2, filedir1, filedir2, ignores, sort, replace, includes);
		if (PASSED != self.outcome[-1]) or forceFriendlyFilesCreation:
			if filedir1 is None: filedir1 = self.output
			if filedir2 is None: filedir2 = self.reference
			f1 = os.path.join(filedir1, file1)
			f2 = os.path.join(filedir2, file2)
			self.log.info("Files differ: producing compare friendly files")
			self.produceCompareFriendlyFiles(f1, f2, ignores, sort, replace, includes)


	def produceCompareFriendlyFiles(self, file1, file2, ignore=[], sort=True, replacementList=[], include=[]):
		list1 = []
		list2 = []

		f = open(file1, 'r')
		for i in f.readlines(): list1.append(i.strip())
		f.close()

		f = open(file2, 'r')
		for i in f.readlines(): list2.append(i.strip())
		f.close()

		list1 = trimContents(list1, ignore, exclude=True)
		list2 = trimContents(list2, ignore, exclude=True)
		list1 = trimContents(list1, include, exclude=False)
		list2 = trimContents(list2, include, exclude=False)

		self.writeListToFile(file1 + ".0.result.selected.txt", list1)
		
		list1 = diffReplace(list1, replacementList)
		list2 = diffReplace(list2, replacementList)
		if sort:
			list1.sort()
			list2.sort()

		self.writeListToFile(file1 + ".1.result.replaced.txt", list1)
		self.writeListToFile(file1 + ".2.expected.replaced.txt", list2)


	def writeListToFile(self, filename, stringList):
		f = open(filename, 'w')
		for item in stringList:
			f.write("%s\n" % item)
		f.close()
