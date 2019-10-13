# TurboGV Charts Serializer
# Sujay Phadke, (C) 2021
#

import sys
import json
import copy
import random
import TurboGVCharts as GVCharts
from TurboGVUtils import TurboGVUtils
from TurboGVHTMLCreator import TurboGVHTMLCreator

class TurboGVSerializer:
	title = ''
	desc = ''
	prefix = ''
	chartNames = {}
	
	def __init__(self, title='', desc=''):
		self.charts = []
		self.Setup(title, desc)
		self.SetIndent(2)
		GVCharts.Generic.SetIndent(2)
		# Add chart specific handlers
		self.chartNames.update(dict.fromkeys(['treemap', 'tree'], GVCharts.Treemap))
		self.chartNames.update(dict.fromkeys(['columnchart', 'column'], GVCharts.Column))
		self.chartNames.update(dict.fromkeys(['scatterchart', 'scatter'], GVCharts.Scatter))
		self.chartNames.update(dict.fromkeys(['linechart', 'line'], GVCharts.Line))
		self.chartNames.update(dict.fromkeys(['bubblechart', 'bubble'], GVCharts.Bubble))

	def Setup(self, title, desc):
		sanitize = TurboGVHTMLCreator.HTMLSanitize
		self.title = sanitize(title)
		self.formattedTitle = "<span class='titleClass' >" + sanitize(title) + "</span>"		
		self.desc = "<span class='descClass' >" + sanitize(desc) + "</span>"
	
	def SetIndent(self, indent):
		self.prefix = '\t' * indent

	def AddChartsDataHeader(self):
		output = ''
		numCharts = len(self.charts)
		output += self.prefix + "// Charts data\n"
		output += self.prefix + "var VisualizationData = {};\n"
		output += self.prefix + 'VisualizationData.title = "' + self.title + '";\n'
		output += self.prefix + 'VisualizationData.formattedTitle = "' + self.formattedTitle + '";\n'
		output += self.prefix + 'VisualizationData.desc = "' + self.desc + '";\n'
		output += self.prefix + "VisualizationData.numCharts = " + str(numCharts) + ";\n"
		output += '\n'
		output += self.prefix + "VisualizationData.graphs = [];\n"
		output += '\n'

		return output

	def GetCharts(self):
		numCharts = len(self.charts)
		output = ''
		
		output += self.prefix + TurboGVUtils.AddGenericFunctions()
		output += self.prefix + self.AddChartsDataHeader()
		
		# Loop over all charts in list and serialize
		for i in range(numCharts):
			output += str(self.charts[i].Serialize(i))
			output += '\n\n'
			
		return output
		
	def AddChart(self, type = '', options = '', data = [], extras = {}):
		type = type.lower()
		
		if type in self.chartNames:
			chart = self.chartNames[type]()
		else:
			print('Using generic chart for type: ' + type)
			chart = GVCharts.Generic()

		chart.SetOptions(options)
		chart.SetData(data, extras)
		self.charts.append(chart)

		return len(self.charts)

if __name__ == "main":
    pass
