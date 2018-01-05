from __future__ import with_statement
from pysys.constants import *
from pysys.process.user import ProcessUser
from pysys.basetest import BaseTest
from pysys.utils.filecopy import filecopy
from apama.common import XArgsHolder
from apama.common import stringToUnicode
from apama.iaf import IAFHelper
from industry.framework.Correlator import IndustrySolutionsCorrelatorHelper
from industry.framework.GrepUtils import orderedgrep
import os, re, platform, time, shutil
import subprocess
from pysys import log

class IndustrySolutionsBaseTest(BaseTest):

	def __init__(self, descriptor, outsubdir, runner):
		BaseTest.__init__(self, descriptor, outsubdir, runner)
		
		self.APAMA_HOME = getattr(PROJECT,"APAMA_HOME")
		self.APAMA_MONITORS_DIR = os.path.join( self.APAMA_HOME, 'monitors')
		self.APAMA_ADAPTER_MONITORS_DIR = os.path.join( self.APAMA_HOME,'adapters', 'monitors')

		self.ANT_HOME = os.environ['ANT_HOME']
		
		self.COMPONENT_TEST_MONITORS  = os.path.join(PROJECT.root, 'tools', 'monitors')
		self.COMPONENT_TEST_RESOURCES = os.path.join(PROJECT.root, 'resources')
		self.COMPONENT_HOME           = os.path.join(PROJECT.root, '..')
		self.COMPONENT_SOURCE_DIR     = os.path.join(self.COMPONENT_HOME, 'src')
		self.COMPONENT_BUILD_FILE     = os.path.join(self.COMPONENT_SOURCE_DIR, 'build.xml')

		outputdir = os.path.join(self.COMPONENT_HOME, 'output', 'windows')
		outputdirfolders = [p for p in map(lambda d: os.path.join(outputdir, d),os.listdir(outputdir)) if os.path.isdir(p)]
		
		# Get the versioned directory
		version_path = (p for p in outputdirfolders if not ' for ' in os.path.basename(p)).next()
		self.COMPONENT_EPL_HOME       = os.path.join(version_path, 'Industry Analytics Kit' )
		self.COMPONENT_CONFIG_DIR     = os.path.join(self.COMPONENT_EPL_HOME, 'config')
		self.COMPONENT_EVENT_DEFS_DIR = os.path.join(self.COMPONENT_EPL_HOME, 'eventdefinitions')
		self.COMPONENT_OBJECTS_DIR    = os.path.join(self.COMPONENT_EPL_HOME, 'objects')
		self.COMPONENT_MONITORS_DIR   = os.path.join(self.COMPONENT_EPL_HOME, 'monitors')
		self.COMPONENT_QUERIES_DIR    = os.path.join(self.COMPONENT_EPL_HOME, 'queries')

		# Get the versioned directory for Retail
		version_path_retail = (p for p in outputdirfolders if ' for Retail' in os.path.basename(p)).next()
		self.COMPONENT_EPL_HOME_RETAIL = os.path.join(version_path_retail, 'Industry Analytics Kit' )
		self.COMPONENT_CONFIG_DIR_RETAIL     = os.path.join(self.COMPONENT_EPL_HOME_RETAIL, 'config')
		self.COMPONENT_EVENT_DEFS_DIR_RETAIL = os.path.join(self.COMPONENT_EPL_HOME_RETAIL, 'eventdefinitions')
		self.COMPONENT_OBJECTS_DIR_RETAIL    = os.path.join(self.COMPONENT_EPL_HOME_RETAIL, 'objects')
		self.COMPONENT_MONITORS_DIR_RETAIL   = os.path.join(self.COMPONENT_EPL_HOME_RETAIL, 'monitors')
		self.COMPONENT_QUERIES_DIR_RETAIL    = os.path.join(self.COMPONENT_EPL_HOME_RETAIL, 'queries')
		
		# Get the versioned directory for Maufacturing
		version_path_manufacturing = (p for p in outputdirfolders if ' for Manufacturing' in os.path.basename(p)).next()
		self.COMPONENT_EPL_HOME_MANUFACTURING = os.path.join(version_path_manufacturing, 'Industry Analytics Kit' )
		self.COMPONENT_CONFIG_DIR_MANUFACTURING = os.path.join(self.COMPONENT_EPL_HOME_MANUFACTURING, 'config')
		self.COMPONENT_EVENT_DEFS_DIR_MANUFACTURING = os.path.join(self.COMPONENT_EPL_HOME_MANUFACTURING, 'eventdefinitions')
		self.COMPONENT_OBJECTS_DIR_MANUFACTURING = os.path.join(self.COMPONENT_EPL_HOME_MANUFACTURING, 'objects')
		self.COMPONENT_MONITORS_DIR_MANUFACTURING = os.path.join(self.COMPONENT_EPL_HOME_MANUFACTURING, 'monitors')
		self.COMPONENT_QUERIES_DIR_MANUFACTURING = os.path.join(self.COMPONENT_EPL_HOME_MANUFACTURING, 'queries')
		
		self.OUTPUT_DIR = outsubdir
		self.currDir    = os.getcwd()

		self.environ = {} 
		for key in os.environ: self.environ[stringToUnicode(key)] = stringToUnicode(os.environ[key])
		self.environ['CLASSPATH'] = ''
		self.environ['CLASSPATH'] = os.path.join(self.ANT_HOME) + ENVSEPERATOR + self.environ['CLASSPATH']
		self.environ['CLASSPATH'] = os.path.join(self.ANT_HOME, 'lib', 'ant-launcher.jar') + ENVSEPERATOR + self.environ['CLASSPATH']
		self.environ['CLASSPATH'] = os.path.join(getattr(PROJECT,"APAMA_HOME"), 'lib', 'engine_client%s.jar' % getattr(PROJECT,"APAMA_LIBRARY_VERSION")) + ENVSEPERATOR + self.environ['CLASSPATH']
		self.environ['CLASSPATH'] = os.path.join(getattr(PROJECT,"APAMA_HOME"), 'lib', 'util%s.jar' % getattr(PROJECT,"APAMA_LIBRARY_VERSION")) + ENVSEPERATOR + self.environ['CLASSPATH']
		self.environ['CLASSPATH'] = os.path.join(PROJECT.root, 'tools', 'classes') + ENVSEPERATOR + self.environ['CLASSPATH']
		self.environ['CLASSPATH'] = os.path.join(getattr(PROJECT,"APAMA_HOME"), 'lib') + ENVSEPERATOR + self.environ['CLASSPATH']
		self.environ['CLASSPATH'] = os.path.join(getattr(PROJECT,"APAMA_HOME"), 'bin') + ENVSEPERATOR + self.environ['CLASSPATH']
		self.environ['CLASSPATH'] = stringToUnicode(self.environ['CLASSPATH'])
		
		self.buildsRun = -1

		self.scenarioServiceBundleInjected = {}
		self.statusSupportBundleInjected = {}


	def startTest(self, Xclock=TRUE, applicationEventLogging=FALSE, inputLog=None, 
				  logfile='correlator.out', logLevel="INFO", host="localhost", port=None, 
				  outputLog='output.log', enableLLVM=False,
				  enableJava=False, enableJMS=False, jmsConfigPath=None, 
				  jmsOutputFile='JMSChannel.log', 
				  jmsChannel='jms:UniversalMessaging-default-sender', 
				  persistence=False, persistenceStoreName=None,
				  persistenceStoreLocation=None, distMemStoreConfig=None,
				  startTime=0.0, extraJars=[], channels=[], 
				  startAntTargets=[], extraAntProperties={},
				  **xargs):
		
		# Create a Correlator Helper    
		self.correlator = IndustrySolutionsCorrelatorHelper(self, host=host, port=port)
		
		# If there are extra JAR files to include
		for jarPath in extraJars:
			self.correlator.addToClassPath( jarPath )
			
		# Start the Correlator
		self.correlator.start(Xclock=Xclock, logfile=logfile, verbosity=logLevel, 
							  applicationEventLogging=applicationEventLogging, 
							  inputLog=inputLog,
							  java=enableJava, enableLLVM=enableLLVM, enableJMS=enableJMS,
							  jmsConfigPath=jmsConfigPath,
							  startTime=startTime, persistence=persistence,
							  persistenceStoreName=persistenceStoreName,
							  persistenceStoreLocation=persistenceStoreLocation,
							  distMemStoreConfig=distMemStoreConfig)
		
		# Log any test output to the output log
		self.correlator.receive(outputLog, channels=['TEST_OUT'])

		# If JMS is enabled, log any messages that are sent on that channel 
		if enableJMS:
			self.correlator.receive(jmsOutputFile, channels=[jmsChannel])                        
	
		# Listen to any other channels required
		if channels:
			self.correlator.receive(outputLog, channels=channels)

		# If any of the components ANT targets were specified, call them now
		if startAntTargets:
			# Set any of the properties required for the ANT scripts
			properties = extraAntProperties
			if not properties.has_key('correlator.host'):
				properties['correlator.host'] = self.correlator.host
			if not properties.has_key('correlator.port'):
				properties['correlator.port'] = self.correlator.port

			# Launch the ANT scripts now
			self.launchAnt(self.COMPONENT_BUILD_FILE, properties, startAntTargets)

		return self.correlator

	def injectDataViewMonitors(self, correlator):
		if not correlator in self.scenarioServiceBundleInjected:
			self.injectScenarioServiceMonitors(correlator);
		correlator.injectMonitorscript(['DataViewService_interface.mon',
										'DataViewService_Impl_Dict.mon'], self.APAMA_MONITORS_DIR)

	def injectIAFStatusMonitors(self, correlator):
		correlator.injectMonitorscript('IAFStatusManager.mon', self.APAMA_ADAPTER_MONITORS_DIR)
		correlator.injectMonitorscript('StatusSupport.mon', self.APAMA_MONITORS_DIR)

	def injectMemoryStoreMonitors(self, correlator):
		if not correlator in self.scenarioServiceBundleInjected:
			self.injectScenarioServiceMonitors(correlator);
		correlator.injectMonitorscript('MemoryStore.mon', os.path.join(self.APAMA_MONITORS_DIR, 'data_storage') ) 
		correlator.injectMonitorscript('MemoryStoreScenarioImpl.mon', os.path.join(self.APAMA_MONITORS_DIR, 'data_storage') )

	def injectJMSSupportMonitors(self, correlator):
		if not correlator in self.statusSupportBundleInjected:
			self.injectStatusSupportMonitors(correlator);
		correlator.injectMonitorscript('CorrelatorJMSEvents.mon', self.APAMA_MONITORS_DIR ) 
		correlator.injectMonitorscript('CorrelatorJMSStatusManager.mon', self.APAMA_MONITORS_DIR )

	def injectScenarioServiceMonitors(self, correlator):
		self.scenarioServiceBundleInjected[correlator] = True;
		correlator.injectMonitorscript('ScenarioService.mon', self.APAMA_MONITORS_DIR ) 

	def injectStatusSupportMonitors(self, correlator):
		self.statusSupportBundleInjected[correlator] = True;
		correlator.injectMonitorscript('StatusSupport.mon', self.APAMA_MONITORS_DIR ) 
		
	def startIAF(self, port=None, mainXMLConfig=None, xmlConfigFiles=[], configDir=None, 
				 replaceDict=[], timeout=30, pathsToAdd=[] ):
		if configDir==None:
			configDir = self.COMPONENT_CONFIG_DIR

		filecopy(os.path.join(configDir, mainXMLConfig), os.path.join(self.OUTPUT_DIR, mainXMLConfig))

		# Copy the config XML files too
		for xmlConfig in xmlConfigFiles:
			filecopy(os.path.join(configDir, xmlConfig), os.path.join(self.OUTPUT_DIR, xmlConfig))
			
		iaf = IAFHelper(self, port=port)
		# Add any extra paths that are required
		for currPath in pathsToAdd:
			iaf.addToPath( currPath )
			
		return iaf.start(mainXMLConfig, configdir=configDir, replace=replaceDict, logfile='iaf.log', verbosity='INFO')

	def stopIAF(self):
		command = os.path.join(PROJECT.APAMA_DEV_HOME, 'bin', 'iaf_management') 
		displayName = "iaf_management"
		dstdout = os.path.join(self.output, 'iafclient.out')
		dstderr = os.path.join(self.output, 'iafclient.err')

		arguments = []
		arguments.extend(["-p", "%d" % self.port])
		arguments.extend(["-s", "Test shutdown"])
		
		# start the process
		self.startProcess(command, arguments, self.environ, self.output, state = BACKGROUND, stdout = dstdout, stderr = dstderr, displayName = displayName)
		self.log.info("Waiting for IAF to shutdown ...")
		self.waitForSignal('iaf.log', expr='(.*)\) shutting down', timeout=10)
		
	def launchAnt(self, buildFile, properties={}, targets=[], verbose=FALSE):
		"""Run an ant task in the supplied working directory.

		"""
		# set the command and display name
		command = os.path.join(self.environ['JAVA_HOME'], 'bin', 'java')
		displayName = 'ANT'

		# set the default stdout and stderr
		instances = self.getInstanceCount(displayName)  
		dstdout = "%s/ant.out"%self.output
		dstderr = "%s/ant.err"%self.output
		if instances: dstdout  = "%s.%d" % (dstdout, instances)
		if instances: dstderr  = "%s.%d" % (dstderr, instances)

		#make parent build file to amalgamate targets
		buildInstance = self.buildsRun = self.buildsRun + 1
		if buildInstance:
			tempFilePath = os.path.join(self.output,'build%d.xml' % buildInstance)
		else:
			tempFilePath = os.path.join(self.output,'build.xml')

		file = open(tempFilePath,'w')
		file.write('<project default="go">\n')
		file.write('\t<target name="go">\n')
		file.write('\t\t<ant inheritAll="true" antfile="%s">\n' % buildFile)
		for target in targets:
			file.write('\t\t\t<target name="%s"/>\n' % target)
		file.write('\t\t</ant>\n')
		file.write('\t</target>\n')
		file.write('</project>')
		file.flush()
		file.close()

		#setup args
		args=[]
		args.append("-classpath")
		args.append(self.environ['CLASSPATH'])
		args.append("-Dant.home=%s" % self.ANT_HOME)
		for property in properties.keys():
			args.append("-D%s=%s" % (property, properties[property]))  
		args.append("org.apache.tools.ant.launch.Launcher")
		if verbose:
			args.append("-verbose")
		args.append("-f")
		args.append(tempFilePath)
			
		self.log.info('Running ant, targets = %s' % targets) 

		# run the process and return the handle
		return self.startProcess(command, args, self.environ, self.COMPONENT_HOME, state = FOREGROUND, stdout = dstdout, stderr = dstderr, displayName = displayName)

	def assertOrderedGrep(self, file, filedir=None, exprList=[], contains=True, groupValues=None):   
		"""Perform a validation assert on a list of regular expressions occurring in specified order in a text file.

		When the C{contains} input argument is set to true, this method will append a C{PASSED} outcome 
		to the test outcome list if the supplied regular expressions in the C{exprList} are seen in the file
		in the order they appear in the list; otherwise a C{FAILED} outcome is added. Should C{contains} be set 
		to false, a C{PASSED} outcome will only be added should the regular expressions not be seen in the file in 
		the order they appear in the list.

		@param file: The basename of the file used in the ordered grep
		@param filedir: The dirname of the file (defaults to the testcase output subdirectory)
		@param exprList: A list of regular expressions which should occur in the file in the order they appear in the list
		@param contains: Boolean flag to denote if the expressions should or should not be seen in the file in the order specified

		"""
		if filedir == None: filedir = self.output
		f = os.path.join(filedir, file)

		log.debug("Performing ordered grep on file:")
		log.debug("  file:       %s" % file)
		log.debug("  filedir:    %s" % filedir)
		for expr in exprList: log.debug("  exprList:   %s" % expr)
		log.debug("  contains:   %s" % LOOKUP[contains])

		try:
			grepResult = orderedgrep(f, exprList,groupValues)
		except IOError:
			self.addOutcome(BLOCKED)
		else:
			if grepResult.failureExpr == None and contains:
				result = PASSED
			elif grepResult.failureExpr == None and not contains:
				result = FAILED
			elif grepResult.failureExpr != None and not contains:
				result = PASSED
			else:
				result = FAILED
			self.outcome.append(result)
			log.info("Ordered grep on input file %s ... %s", file, LOOKUP[result].lower())
			if result == FAILED: log.info("Ordered grep failed on expression \"%s\"", grepResult.failureExpr)
		return grepResult.groupValues

	def checkNoCrash(self, correlatorLog="correlator.out"):
		self.assertGrep(file=correlatorLog, expr='ERROR.*Error on line', contains=0)
		self.assertGrep(file=correlatorLog, expr='ERROR.*Stack dump', contains=0)

	def checkParseFail(self, correlatorLog="correlator.out"):
		self.assertGrep(file=correlatorLog, expr='Failed to parse the event', contains=0)

	def checkInjectSendFail(self):
		self.assertGrep(file='run.log', expr='Executed .* in foreground with exit status = 2', contains=0)

	def checkWaitForSignalTimeouts(self):
		self.assertGrep(file='run.log',
						expr='Wait for signal .* in .* timed',
						contains=0)

	def checkSanity(self, correlatorLog="correlator.out"):
		if correlatorLog == None:
			correlatorLog = "correlator.out";
		self.checkNoCrash(correlatorLog)
		self.checkParseFail(correlatorLog)
		self.checkInjectSendFail()
		self.checkWaitForSignalTimeouts()
