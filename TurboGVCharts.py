# TurboGV Charts Serializer
# Sujay Phadke, (C) 2021
#

import random
import json
from TurboGVUtils import TurboGVUtils

class Generic:
    indent = 0

    @staticmethod	
    def isFloat(s):
        try:
            f = float(s)
            return True
        except:
            return False
    
    @classmethod
    def SetIndent(cls, indent):
        cls.indent = indent

    def Serialize(self, index=0):
        output = ''
        output += self.prefix + "VisualizationData.graphs[" + str(index) + "] = {};\n"
        output += self.prefix + "VisualizationData.graphs[" + str(index) + "]['chartType'] = '" + self.type + "';\n"
        output += self.prefix + "VisualizationData.graphs[" + str(index) + "]['options'] = " + json.dumps(self.options) + ";\n"            
        output += self.prefix + "VisualizationData.graphs[" + str(index) + "]['data'] = [\n" 
        output += '\t' + self.data
        output += "\n" + self.prefix + "];\n"

        if ('textformat' in self.extras) and (self.extras['textformat']):
            textformat = True
        else:
            textformat = False
        
        if ('svg' in self.extras) and (self.extras['svg']):
            svg = True
        else:
            svg = False

        output += TurboGVUtils.OnReadyHandler(index, textformat, svg)
        return output
        
    def GetOptions(self):
        return self.options

    def SetOptions(self, options):
        self.options.update(options)
        # Sanity checks
        if 'title' not in self.options:
            self.invalid = True
            print('No Title found for chart! Skipping data.')

    def SetData(self, data, extras={}):
        self.SetExtras(extras)
        self.data = self.SerializeDataTable(data)
        
    def SetExtras(self, extras):
        self.extras = extras

    def Row_to_JS_format(self, row):
        return self.prefix + str(row)  + ",\n"

    def SerializeDataTable(self, data_table):
        serialized_data = ''

        # Check sanity from options
        if self.invalid:
            print('Error! Required options not present for chart')
            print('Skipping data ...')
            return serialized_data

        try:
            rows = len(data_table)
        except:
            # Wrong data format passed
            print('Possible incorrect data format for chart of type: ' + self.type)
            return serialized_data

        for i in range(rows):
            serialized_data += self.Row_to_JS_format(data_table[i])

        return serialized_data

    def GetType(self):
        return self.type

    def __init__(self) -> None:
        self.type = 'Generic'
        self.data = ''
        self.extras = ''
        self.raw = False
        self.prefix = '\t' * self.indent

        self.options = {
            'titleTextStyle': {
                'color': 'red', 'fontSize': '16'
            },
            'tooltip': {
                'textStyle': {'fontName': 'Arial', 'fontSize': 10, 'color': 'black'}, 'showColorCode': 'true',
            },
            'fontColor': 'black',
            'legend': { 'position': 'none', 'alignment': 'center', 'textStyle': {'fontSize': '10'}},
            'headerHeight': 25,
            'headerColor': '#d1f9f8',
            'theme': 'material'
	    }

        self.invalid = False

class Column(Generic):
    def __init__(self) -> None:
        super().__init__()
        self.type = 'ColumnChart'

        self.options.update({
        })

class Line(Generic):
    def __init__(self) -> None:
        super().__init__()
        self.type = 'LineChart'
        
        self.options.update({
            'curveType': 'none'
        })

class Bubble(Generic):
    def __init__(self) -> None:
        super().__init__()
        self.type = 'BubbleChart'

        self.options.update({
            'bubble': {'textStyle': {'fontSize': 11}}
        })

class Scatter(Generic):
    def __init__(self) -> None:
        super().__init__()
        self.type = 'ScatterChart'

        self.options.update({
            'pointSize': 5,
            'series': {
                    '0': { 'pointShape': 'circle' },
                    '1': { 'pointShape': 'diamond' },
                    '2': { 'pointShape': 'square' },
                    '3': { 'pointShape': 'triangle' },
                    '4': { 'pointShape': 'star' },
                    '5': { 'pointShape': 'polygon' }
            }
        })

class Treemap(Generic):
    def Tooltip(self, index):
        str = self.prefix
        str += \
        '''
        function Tooltip{0}(row, size) {{
            var size_f = LimitPrecision(size);
            return '<div class="myTooltipClass">' + '<span class="mySpanClass"><b>' + data[{0}].getFormattedValue(row, 0) + ': ' + size_f + '</b>' + ' </div>';
        }}
        '''
        return str.format(index)

    def Serialize(self, index=0):
        # Special handling for treemaps
        # If options contains a value for 'generateTooltip',
        # it must map to a function

        output = super().Serialize(index)
        # "ShowFullTooltip" need to be a function and 
        # it has to appear without quotes in the output
        if 'generateTooltip' in self.options:
            output = output.replace(r'"ShowFullTooltip"', 'Tooltip' + str(index))
            output += self.Tooltip(index)

        return output

    def Array_to_GVTreemap_Format(self, array, randomize=False):
        rows = len(array)
        
        # Create a suffix with random numbers since GV Treemap datatable format
        # requires unique values for the "v" key in every row (at any depth)
        # We use 2 random suffixes to minimize chances of aliasing when
        # many rows are present
        # Example. These rows:
        # ['Brazil', 'America', 11, 10],
		# ['USA', 'America', 52, 31],
        #
        # Need to be formatted like this:
        #
		# [{'v': 'Brazil_5063_4067', 'f': 'Brazil'}, 'America', 11],
        # [{'v': 'USA_1916_8919', 'f': 'USA'}, 'America', 52],

        for i in range(rows):
            temp_dict = {}
            if randomize:
                rand_suffix = '_' + str(random.randint(1,10000)) + '_' + str(random.randint(1,10000))
            else:
                rand_suffix = ''

            temp_dict['v'] = array[i][0] + rand_suffix
            temp_dict['f'] = array[i][0]
            array[i][0] = temp_dict

        return array

    def SerializeDataTable(self, data_table):
        """
        Special serialization needed for treemap data table format
        """
        serialized_data = ''

        # For GV Treemap, the header rows and the top-level data
        # need to be passed in separately in 'extras'
        # Assumption: First 2 rows are special
        # 1st row has to be the header, describing the columns
        # 2nd row has to be the 'global' id row, with a null parent value
        # For top-level data, we cannot suffix the column value with random data
        # (They already need to be unique)
        # Example:
        # ['Location', 'Parent', 'Market trade volume (size)', 'Market increase/decrease (color)'],
		# ['Global',    'null',               0,                               0],
		# ['America',   'Global',             0,                               0],
		# ['Europe',    'Global',             0,                               0],
        #
        # Note: Only first 3 columns are used for top-level and internal data tables

        if 'top_level_data' not in self.extras:
            print('Error! Treemap requires data in a special format! Top-level data not found.')
            print('Skipping data for chart: ' + self.options['title'])
            return serialized_data

        headers_globals_array = self.Array_to_GVTreemap_Format(self.extras['top_level_data'], False)
        for i in range(len(headers_globals_array)):
            serialized_data += self.Row_to_JS_format(headers_globals_array[i][0:3])

        # The value for the 'global' row, needs to literally be null, in Javascript
        serialized_data = serialized_data.replace("'null'", "null")

        # Format the internal data table
        if ('randomize' in self.extras):
            randomize = self.extras['randomize']
        else:
            randomize = False

        internal_array = self.Array_to_GVTreemap_Format(data_table, randomize)
        for i in range(len(internal_array)):
            serialized_data += self.Row_to_JS_format(internal_array[i][0:3])

        return serialized_data

    def __init__(self) -> None:
        super().__init__()
        self.type = 'TreeMap'

        self.options.update({
            'minColor': '#009688',
            'midColor': '#f7f7f7f',
            'maxColor': '#ee8100',
            'showScale': 'true',
            'highlightOnMouseOver': 'true',
            'hintOpacity': 1,
            'maxPostDepth': 1,
            'generateTooltip': 'ShowFullTooltip',
            'useWeightedAverageForAggregation': 'true'
        })

if __name__ == "main":
    pass
