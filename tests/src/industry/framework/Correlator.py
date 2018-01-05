from apama.correlator import CorrelatorHelper
from apama.common import XArgsHolder
from pysys.constants import TRUE,FALSE,FOREGROUND,BACKGROUND,PROJECT,PLATFORM
import os, types

class IndustrySolutionsCorrelatorHelper(CorrelatorHelper):

	def __init__(self, parent, port=None, host=None):
		CorrelatorHelper.__init__(self, parent, port, host)
		self.log = self.parent.log
		self.parent = parent
		self.environ = self.parent.environ

		self.eventSender = None
		self.time = 0.0
        
	def start(self, logfile=None, verbosity=None, java=None, Xclock=TRUE, 
			  applicationEventLogging=FALSE, startTime=0.0, 
			  inputLog = None, enableLLVM=FALSE, enableJMS=False, jmsConfigPath=None,
              persistence=False, persistenceStoreName=None,
			  persistenceStoreLocation=None, distMemStoreConfig=None,
			  **xargs):
		if xargs.has_key("arguments"):
			arguments = xargs["arguments"]
			del xargs["arguments"]
		else:
			arguments = []
			
		if inputLog != None:
			arguments.extend(["--inputLog",inputLog])

		# Cache the time that was set
		self.time = startTime
 
		# Check if we are enabling LLVM
		if enableLLVM:
			# Currently this option is only available on Linux
			if PLATFORM in ['linux', 'linux64']:
				arguments.extend(["--runtime",'compiled'])
			
		# Check if we are enabling JMS support
		if enableJMS:
			# Check if we have provided a specific path to the JMS adapter settings
			# Otherwise use the default setting
			if jmsConfigPath == None:
				jmsConfigPath = os.path.join(PROJECT.root,'..','bundle_instance_files','Correlator-Integrated_JMS')
				
			arguments.extend(["--jmsConfig",jmsConfigPath])
			
		# Add Distributed Memory Store configuration if required
		if distMemStoreConfig != None:
			arguments.extend(["--distMemStoreConfig", distMemStoreConfig])
			
		displayName = "industry-test-correlator"
		self.eventSender = None
		instances = self.parent.getInstanceCount(displayName)    
		
		# Check if Correlator persistence is enabled        
		if persistence == True:
			arguments.extend(["-P"])   
			# Check if we have chosen to change the default store location
			if persistenceStoreName != None:
				arguments.extend(['-PstoreName='+persistenceStoreName])
			# Check if we have chosen to change the default store location
			if persistenceStoreLocation != None:
				arguments.extend(['-PstoreLocation='+persistenceStoreLocation])
		
		if logfile == None:
			self.logFile = 'correlator.out'
			if instances: logfile  = "%s.%d" % (logfile, instances)
		else:
			self.logFile = logfile
			
		returnVal = CorrelatorHelper.start(self, logfile, verbosity, java, Xclock, arguments=arguments, **xargs)
		if applicationEventLogging:
			self.applicationEventLogging(TRUE)
		if Xclock == TRUE:
			self.sendLiteral('&SETTIME(%f)' % startTime)
			
		return returnVal
            
	def stop(self):
		self.manage(arguments=['-s','Stopping correlator from test'])
			
	def setApplicationLogLevel(self, verbosity="INFO", node=None):
		"""Set the application log level.
		
		@param verbosity: The verbosity level of the application logging
		@param node: The node to set the loglevel for
		
		"""
		if node !=None :
			self.manage(arguments=['-r','setApplicationLogLevel %s' % verbosity])
		else:
			self.manage(arguments=['-r','setApplicationLogLevel %s %s' % (verbosity, node)])
			
	def applicationEventLogging(self, enable=TRUE):
		if enable:
			self.manage(arguments=['-r','applicationEventLogging on'])
		else:
			self.manage(arguments=['-r','applicationEventLogging off'])

	def inject(self, filenames=[], filedir=None, utf8=FALSE, **xargs):
		self.injectMonitorscript(filenames,filedir,utf8, **xargs)

	def sendLiteral(self, string, log=True):
		if self.eventSender == None:
			self.eventSender = self.send(state=BACKGROUND)
		self.eventSender.write(string)
		self.eventSender.write("BATCH 000")
		if log:
			self.log.info('Sent literal: %s' % (string))

	def incrementTime(self, inc, silent=False):
		self.time = self.time + inc
		if not silent: self.parent.log.info('time is set to: %s' % self.time)
		self.sendLiteral("&TIME(%f)" % self.time)

	def setTime(self, time):
		self.time = time
		self.sendLiteral("&TIME(%f)" % self.time)
		
	def getTime(self):
		return self.time
