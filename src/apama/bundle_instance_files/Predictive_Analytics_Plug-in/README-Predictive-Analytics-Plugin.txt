$Copyright (c) 2015-2016 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or its subsidiaries and/or its affiliates and/or their licensors.$
Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

Predictive Analytics Plug-in
----------------------------
Version: 9.12.0.0

DESCRIPTION
-----------
Predictive Analytics Plug-in combines Zementis ADAPA’s powerful predictive model deployment and scoring capabilities
with Apama’s comprehensive big data analytics platform to create a tightly integrated solution.
Predictive Analytics Plug-in is wrapper over ADAPA library using which user can set up a context, score data etc.

PLATFORMS SUPPORTED
-------------------

	This plugin is supported on all platforms supported by Apama 9.12.

FILES
-----

All paths are relative to the "adapters" subdirectory of the Apama installation:

/doc                                                  - This directory contains the README for Predictive Analytics Plug-in.

/doc/ADAPA/Apamadoc                                   - This directory contains the ApamaDoc reference documentation for the
                                                        Predictive Analytics Plug-in EPL.

/lib                                                  - This directory contains the Predictive Analytics Plug-in JAR file.

/config                                               - It also contains the Context XML file that is required by the Predictive Analytics Plug-in application.

/ant_macros/predictive-analytics-support-macros.xml   - A helper ant script to set the required classpath and
                                                        inject all dependencies.
                                                        Users need to define 'ADAPA_LICENSE_DIR' environment
                                                        variable to point to the adapa license dir to use this

/samples                                              - This directory contains samples of how the Predictive Analytics Plug-in should
                                                        be used within an EPL application.
                                                        Currently, there is only a single sample that demonstrates using
                                                        the Apama Plugin using an EnergyData PMML model to predict changing
                                                        temperatures. An ANT build XML file is provided that will run the
                                                        sample and perform all the necessary setup required for you.
                                                        This ant build script depends on the predictive-analytics-support-macros.xml, so
                                                        users need to define 'ADAPA_LICENSE_DIR' as described above.

/monitors                                             - This directory contains a predictive_analytics_plugin_monitors.cdp that needs to be injected.

/catalogs/bundles/PredictiveAnalyticsPlugin.bnd       - Predictive Analytics Plug-in bundle file


MONITOR INJECTION ORDER
-----------------------
1. Start the correlator with ADAPA_LICENSE_DIR (Directory where the Zementis ADAPA license is present) added to the classpath
2. Inject Predictive-Analytics-Plugin.jar located in APAMA_HOME/adapters/lib to the correlator.
3. Inject predictive_analytics_plugin_monitors.cdp CDP file located in APAMA_HOME/adapters/monitors to the correlator.

Using Predictive Analytics Plug-in
----------------------------------

- Ensure that the ADAPA license file is valid, and is located on the correlator CLASSPATH.

Starting the plugin
-------------------

- start correlator

- Inject 'Predictive-Analytics-Plugin.jar' to the correlator

- Inject 'predictive_analytics_plugin_monitors.cdp' to the correlator

- Inject User Application EPL to interact with the Predictive Analytics Plug-in

An User Application EPL script should do the following:

1. Create an instance of ServiceParams

	com.apama.pa.pmml.ServiceParams serviceParams := (new com.apama.pa.pmml.ServiceParamsHelper).create();

2. Set configuration parameters

		serviceParams.setPMMLFileDirectory("PMML_CONFIG_DIRECTORY");
		serviceParams.setPMMLFileName("PMML_CONFIG_FILE_NAME");

	Please refer to the apamadoc available in APAMA_HOME/adapters/doc/ADAPA/Apamadoc for a full list of configuration
	parameters

3. Request the ServiceHandlerFactory to create a new Service Handler and pass the ServiceParams

		(new com.apama.pa.pmml.ServiceHandlerFactory).create((new com.apama.pa.pmml.ServiceName).Zementis,
										"PREDICTIVE_ANALYTICS_INSTANCE_1",
										serviceParams,
										onServiceInitialised,
										onServiceError);

		Users need to pass in two additional callbacks to the service handler factory

			action onServiceInitialised(com.apama.pa.pmml.ServiceHandler servicehandler) {
				//Implement your application logic here
			}

			This is called when the pmml file is successfully loaded and the service is initialised. The ServiceHandler
			received in this callback can be used to retrieve the list of models available for this service

			action onServiceError(com.apama.pa.pmml.ServiceError serviceError) {
				log "Received Service Error " + serviceError.getErrorMessage() at ERROR;
			}

			This is called if an error is encountered while loading the PMML file or when there's a problem with the Input

4. Create an Input event and pass it over to the plug-in

		com.apama.pa.pmml.Input input := new com.apama.pa.pmml.Input;
		input.instanceName := "PREDICTIVE_ANALYTICS_INSTANCE_1";
		input.modelName := "SAMPLE_MODEL_NAME";
		input.requestId := integer.getUnique().toString();
		input.inputFields.add("FIELD_1", "FIELD_1_VALUE");
		input.inputFields.add("FIELD_2", "FIELD_2_VALUE");
		input.inputFields.add("FIELD_2", "FIELD_3_VALUE");
		route input;

5. Listen for the Output event which corresponds to the above input

		com.apama.pa.pmml.Output output;
		on all com.apama.pa.pmml.Output(instanceName="PREDICTIVE_ANALYTICS_INSTANCE_1") : output
		{
			log output.toString() at INFO;
			//Do additional processing
		}

	Error handling when processing an input request is achieved in the following ways

        1. If there's a significant error while processing the request user can expect to receive a callback
           on the 'onServiceError' callback registered during service initialisation
        2. Errors/Warnings reported by the Predictive Analytics Engine are also propogated to the user using the
           Output event.

             a. If any errors are found during scoring, users can search for 'ADAPA_Error' in the outputFields
                Example:
                    com.apama.pa.pmml.Output("Instance_1","206",{"ADAPA_Error":"Value [NA] is invalid for field [PreUse]."},{})
             b. Warning's reported by the the scoring engine are also forwarded in the outputFields as 'ADAPA_Warning_<N>', where
                N can be 1, 2, 3 ...
                Example:
                    com.apama.pa.pmml.Output("Instance_1","206",{"ADAPA_Warning_1":"warning message","Predicted_Usage":"19.980840445004088"},{})

Please refer to the EnergyDataSample.mon available in samples/EnergyData/monitors/ for more details on interacting with the Predictive Analytics Plugin
