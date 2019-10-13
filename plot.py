# TurboGV Plot Example Script
# Sujay Phadke, (C) 2021
#

from TurboGVSerializer import TurboGVSerializer
from TurboGVHTMLCreator import TurboGVHTMLCreator as HTML

def ArrayAddHeader(a, h):
	a.insert(0, h)
	return a

def _1DMap2Array(m):
	temp_array = []
	temp_list = []
	
	# v, below, could be a single value or array. deal with both
	for k,v in m.items():
		if isList(v):
			temp_list = [k]
			temp_list.extend(v)
		else:
			temp_list = [k, v]
			
		temp_array.append(temp_list)	
	
	return temp_array
	
	
def _2DMap2Array(d, h = []):
	temp_array = []
	temp_list = []
	
	first_key = list(d)[0]	
	temp_header = list(d[first_key].keys())
	h.extend(temp_header)
	
	for k,v in d.items():
		temp_list = [k]
		
		for k2,v2 in d[k].items():
			temp_list.append(v2)
			
		temp_array.append(temp_list)	
	
	return temp_array

def isList(x):
	try:
		t = float(x)
		return False
	except:
		return True
	
def main():	
	gv = TurboGVSerializer('TurboGV Example Script', "Create Google Visualization Charts from raw data in Python\nView in a web browser. Supports downloading the charts in SVG format.\n\
			Note: The data for these charts is taken from: https://developers.google.com/chart/interactive/docs")
	gv.SetIndent(7)
	
	data1 = [
		['Element', 'Density', { 'role': 'style' }],
		['Copper', 8.94, '#b87333'],
		['Silver', 10.49, 'silver'],
		['Gold', 19.30, 'gold'],
		['Platinum', 21.45, 'color: #e5e4e2' ],
	]
	
	#ArrayAddHeader(data1, ['Time', 'Buy', 'Sell'])
	gv.AddChart('ColumnChart', \
				{'title': 'Density of Precious Metals, in g/cm^{3}. (This title contains ^{superscript} and _{subscript})', \
				 'hAxis': {'title': 'Metal'}, \
				 'vAxis': {'title': 'Density (g/cm^{3})'} 
				}, \
				data1, \
				extras = {'raw': True, 'textformat': True, 'svg': True})
	
	internal_data = [
		['Brazil',    'America',            11,                              10],
		['USA',       'America',            52,                              31],
		['Mexico',    'America',            24,                              12],
		['Canada',    'America',            16,                              -23],
		['France',    'Europe',             42,                              -11],
		['Germany',   'Europe',             31,                              -2],
		['Sweden',    'Europe',             22,                              -13],
		['Italy',     'Europe',             17,                              4],
		['UK',        'Europe',             21,                              -5],
		['China',     'Asia',               36,                              4],
		['Japan',     'Asia',               20,                              -12],
		['India',     'Asia',               40,                              63],
		['Laos',      'Asia',               4,                               34],
		['Mongolia',  'Asia',               1,                               -5],
		['Israel',    'Asia',               12,                              24],
		['Iran',      'Asia',               18,                              13],
		['Pakistan',  'Asia',               11,                              -52],
		['Egypt',     'Africa',             21,                              0],
		['S. Africa', 'Africa',             30,                              43],
		['Sudan',     'Africa',             12,                              2],
		['Congo',     'Africa',             10,                              12],
		['Zaire',     'Africa',             8,                               10],
	]

	top_level_data = [
		['Location', 'Parent', 'Market trade volume (size)', 'Market increase/decrease (color)'],
		['Global',    'null',               0,                               0],
		['America',   'Global',             0,                               0],
		['Europe',    'Global',             0,                               0],
		['Asia',      'Global',             0,                               0],
		['Australia', 'Global',             0,                               0],
		['Africa',    'Global',             0,                               0]
	]

	gv.AddChart('TreeMap', {'title': 'Treemap'}, data=internal_data, 
				extras={'top_level_data': top_level_data, 'randomize': True}
			   )
	
	data3 = [
		[ 8,      12],
		[ 4,      5.5],
		[ 11,     14],
		[ 4,      5],
		[ 3,      3.5],
		[ 6.5,    7]
		]

	ArrayAddHeader(data3, ['Age', 'Weight'])
	gv.AddChart('ScatterChart', {'title': 'Age vs. Weight comparison', 'hAxis': {'title': 'Age'}, 'vAxis': {'title': 'Weight'}}, data3)
		
	
	data4 = [
		[{'v': [8, 0, 0],  'f': '8 am'}, 1, .25],
		[{'v': [9, 0, 0],  'f': '9 am'}, 2, .5],
		[{'v': [10, 0, 0], 'f':'10 am'}, 3, 1],
		[{'v': [11, 0, 0], 'f': '11 am'}, 4, 2.25],
		[{'v': [12, 0, 0], 'f': '12 pm'}, 5, 2.25],
		[{'v': [13, 0, 0], 'f': '1 pm'}, 6, 3],
		[{'v': [14, 0, 0], 'f': '2 pm'}, 7, 4],
		[{'v': [15, 0, 0], 'f': '3 pm'}, 8, 5.25],
		[{'v': [16, 0, 0], 'f': '4 pm'}, 9, 7.5],
		[{'v': [17, 0, 0], 'f': '5 pm'}, 10, 10],
	]
	ArrayAddHeader(data4, ['Time of Day', 'Motivation Level', 'Energy Level'])
	gv.AddChart('ColumnChart', {'isStacked': 'true', 'title': 'Motivation and Energy Level Throughout the Day', 'hAxis': {'title': 'Time of Day'}, 'vAxis': {'title': 'Rating (scale of 1-10)'}, 'legend': {'position': 'top', 'alignment': 'center'} }, data4, extras = {'raw': True})

	data5 = [
		['Year', 'Sales', 'Expenses'],
		['2004',  1000,      400],
		['2005',  1170,      460],
		['2006',   660,     1120],
		['2007',  1030,      540]
	]
	gv.AddChart('LineChart', {'title': 'Company Performance. (Y-axis labels have been modified to display exponent as a superscript)', 'hAxis': {'title': 'Year'}, 'vAxis': {'title': 'Performance', 'format': 'scientific'}, 'legend': {'position': 'bottom', 'alignment': 'center'}, 'curveType': 'function' }, data5, extras = {'textformat': True})
	
	data6 = [
		['ID', 'Life Expectancy', 'Fertility Rate', 'Region',     'Population'],
		['CAN',    80.66,              1.67,      'North America',  33739900],
		['DEU',    79.84,              1.36,      'Europe',         81902307],
		['DNK',    78.6,               1.84,      'Europe',         5523095],
		['EGY',    72.73,              2.78,      'Middle East',    79716203],
		['GBR',    80.05,              2,         'Europe',         61801570],
		['IRN',    72.49,              1.7,       'Middle East',    73137148],
		['IRQ',    68.09,              4.77,      'Middle East',    31090763],
		['ISR',    81.55,              2.96,      'Middle East',    7485600],
		['RUS',    68.6,               1.54,      'Europe',         141850000],
		['USA',    78.09,              2.05,      'North America',  307007000]
	]
	
	gv.AddChart('BubbleChart', {'title': 'Correlation between life expectancy, fertility rate ' +
               'and population of some world countries (2010)', 'hAxis': {'title': 'Life Expectancy'}, 'vAxis': {'title': 'Fertility Rate'}, 'legend': {'position': 'right', 'alignment': 'top'} }, data6, extras = {'raw': True})

	serialized_charts = gv.GetCharts()
	# Generate HTML output
	
	HTML.Generate(serialized_charts)
	
if __name__ == "__main__":
	main()
	
