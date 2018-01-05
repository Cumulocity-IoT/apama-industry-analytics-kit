package com.industry.analytics

import groovy.io.FileType
import groovy.json.*

def cli = new CliBuilder(usage: 'buildMetadata [options]')
cli.with {
    s longOpt: 'srcDir', args: 1, 'The Apama source folder'
    d longOpt: 'docDir', args: 1, 'The ApamaDoc folder'
    o longOpt: 'outputDir', args: 1, 'The Build output folder'
    v longOpt: 'version', args: 1, 'The Version being built'
    t longOpt: 'templateFile', args: 1, 'The output template to use'
    x longOpt: 'samplesDir', args: 1, 'The directory of any samples to include'
    h longOpt: 'help', 'print the usage'
}
def options = cli.parse(args)

if (!options || options.h || !options.s || !options.o || !options.d || !options.v || !options.t || !options.x) {
    cli.usage()
    return
}

def srcDir = options.s
def docDir = options.d
def outputDir = options.o
def version = options.v
def templateFile = options.t
def samplesDir = options.x
def jsonSlurper = new JsonSlurper()

println "sourceDir: ${srcDir}"
println "docDir: ${docDir}"
println "outputDir: ${outputDir}"
println "version: ${version}"
println "template: ${templateFile}"
println "samplesDir: ${samplesDir}"

def analyticFiles = []

// Find all of the .mon files
new File("${srcDir}").eachFileRecurse(FileType.FILES) { file ->
    if (file.name.endsWith(".mon")) {
        analyticFiles << file
    }
}

def samples = []

// Find all of the .evt files
new File(samplesDir).eachFile(FileType.FILES) { file ->
    if (file.name.endsWith(".evt")) {
        samples << file.text
    }
}

def getDocumentation = { String docFile ->
    def file = new File("${docDir}/${docFile}")
    def text = (file.text =~ /(?si)<body[^>]*>.*?<table.*?<table.*?<\/table>.*?<\/table>\s*<hr>(.*)\s*<hr>\s*<hr>\s*<table.*?<table.*?<\/table>.*?<\/table>\s*<hr>\s*<\/body>/)[0][1]

    text = text.replaceAll(/(?i)href=".*?"/, "")
    text = text.replaceAll(/(?i)target=".*?"/, "")
    text = text.replaceAll(/(?si)<script.*?<\/script>/, "")
    text = text.replaceAll(/(?si)<noscript.*?<\/noscript>/, "")
    text = text.replaceAll(/[\r\n]/, "")
    text = text.replaceFirst(/Event /, "")
    return text
}

def enrichAnalytic = { String analytic ->
    jsonAnalytic = jsonSlurper.parseText(analytic)
    if (jsonAnalytic.containsKey('documentation')) {
        try {
            jsonAnalytic.documentation = getDocumentation(jsonAnalytic.documentation as String)
        } catch (e) {
            println "Unable to get docs at: ${jsonAnalytic.documentation}"
            e.printStackTrace()
        }
    }
    return jsonAnalytic
}

// Grab all of the "@AnalyticDefinition"s
def analytics = analyticFiles.collectMany { file ->
    (file.text =~ /(?s)(\/\*\s*@AnalyticDefinition\s*(\{.*?\})\s*\*\/)/).collect { match ->
        // Validate the analytic
        try {
            jsonSlurper.parseText(match[2] as String)
        } catch(e) {
            throw new Error("Unable to parse Analytic in file: ${file}", e)
        }
        enrichAnalytic(match[2] as String)
    }
}

def templateText = new File(templateFile as String).text
def templateJson
// Parse the template
try {
    templateJson = jsonSlurper.parseText(templateText)
} catch (e) {
    throw new Error("Unable to Build output file, invalid template. ${templateFile}", e)
}

if (!templateJson.containsKey('version')) {
    throw new Error("Template must have a version placeholder. ${templateFile}")
}
templateJson.version = version

if (!templateJson.containsKey('analytics')) {
    throw new Error("Template must have a analytics placeholder. ${templateFile}")
}
templateJson.analytics = analytics

if (!templateJson.containsKey('samples')) {
    throw new Error("Template must have a samples placeholder. ${templateFile}")
}
templateJson.samples = samples

// Output
new File("${outputDir}/metadata.json").write JsonOutput.prettyPrint(JsonOutput.toJson(templateJson))