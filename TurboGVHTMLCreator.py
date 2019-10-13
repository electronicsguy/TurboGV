# TurboGV HTML Creator
# Sujay Phadke, (C) 2021
#

class TurboGVHTMLCreator:
	@classmethod
	def PrintHTMLHead(cls, fp):

		mystr = '''\
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<meta name="author" content="Sujay S. Phadke">
	<meta name="copyright" content="">
	<meta name="url" content="https://github.com/electronicsguy">
	<meta name="description" content="TurboGV: Google Visualization HTML Creator">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title></title>
	
	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	<style>
		rect {
			stroke: white;
			stroke-width: 1;
		}
		.myTooltipClass {
			background: #fd9;
			padding: 10px;
			border-style: solid;
			border-width: 2px;
			border-color: red;
			border-radius: 5px;
		}
		.mySpanClass {
			font-family: Courier;
			color: blue
		}
		.preloaderClass {
						background: #fd9;
						border-width: 2px;
						border-color: red;
			font-size: 50px;
			text-align: center;
			vertical-align: middle;
		}
		.selectClass {
			font-weight: bold;
			padding: 5px;
			/* color: red; */
		}
		.headerClass {
			position: top;
		}
		.titleClass { 
            font-family: Arial;
			font-weight: bold;
            color: #E42D05;
            margin-left: 20px;
			text-align: left;
			display: inline-block;
			margin-bottom: 5px;
        }
		.descClass { 
            font-family: Arial;
			font-weight: normal;
            color: #009900;
            margin-left: 20px;
			text-align: left;
			display: inline-block;
			margin-bottom: 20px;
        }
		.myButton {
			background-color: #4CAF50; /* Green */
			border: none;
			color: white;
			padding: 5px;
			text-align: center;
			text-decoration: none;
			display: inline-block;
			font-size: 15px;
			margin: 4px 2px;
			cursor: pointer;
			border-radius: 12px;
		}
	</style>
</head>    
'''
					
		print (mystr, file = fp)

	@classmethod
	def PrintHTMLBody(cls, fp):
		mystr = '''\
<body>		
	<script type='text/javascript'>
		google.charts.load('current', {'packages': ['treemap', 'corechart'], callback: Main});
		
		var numCharts;
		var chartTypes = [];
		var chartHandle = [];
		var dataArr = [];
		
		var data = [];
		var columnOptions;
		var options = [];
		var chart = [];
		
		
		function Main() {
			Init();
			CreateChartDivs();				
			DrawChart();
			CustomizeCharts();
		}
		
		function Init() {
			SetRawData();
		}
		
		function CreateChartDivs() {
			
			var main_title = document.createElement('div');
			main_title.id = 'main_title';
			main_title.class = 'headerClass';
			main_title.style.paddingBottom = '2px';
			main_title.innerHTML = VisualizationData.formattedTitle;
			document.body.appendChild(main_title);
			
			var main_desc = document.createElement('div');
			main_desc.id = 'main_desc';
			main_desc.style.paddingBottom = '50px';
			main_desc.innerHTML = VisualizationData.desc;
			document.body.appendChild(main_desc);
			
			for (i=0; i<numCharts; i++) {
				var div_outer = document.createElement('div');
				div_outer.id = 'chart_div_outer' + i;
				
				var div1 = document.createElement('div');
				div1.id = 'chart_div' + i;
				div1.style.width = '900px';
				div1.style.height = '500px';
				
				var div2 = document.createElement('div');
				div2.className = 'preloaderClass';
				div2.innerHTML = 'Loading Chart...';
				div2.id = 'inner_div' + i;
				
				div1.appendChild(div2);
				div_outer.appendChild(div1);
				
				document.body.appendChild(div_outer);
				
				chartHandle[i] = div1.id;
				
				// Draw horizontal line
				var hr = document.createElement('hr');
				document.body.appendChild(hr); 
				
			}
		}
		
		
		function SetOptions() {
			for (i=0; i<numCharts; i++) {
				options[i] = VisualizationData.graphs[i]['options'];				
			}
		}
		
		function SetRawData() {
		
			if ((typeof VisualizationData === 'undefined') || (VisualizationData === null)) {
				alert('No Charts found!');
				numCharts = 0;
				VisualizationData = { 'title': 'No charts found!' };
				return;
			}
			
			document.title = VisualizationData.title;
			numCharts = VisualizationData.numCharts;
			
			for (i=0; i<numCharts; i++) {
				try{
					chartTypes[i] = VisualizationData.graphs[i].chartType;
					dataArr[i] = VisualizationData.graphs[i].data;
				}
				catch(err){
					console.log('Error while setting chart properties. Perhaps wrong chart index: ' + i)
					console.log(err.message)
				}
			}
		}
		
		function DrawChart() {				
			// Create and populate the data table
			for (i=0; i<numCharts; i++) {
				try{
					data[i] = google.visualization.arrayToDataTable(dataArr[i]);
				}
				catch(err){
					console.log('Error in converting datatable for chart: ' + String(i))
					console.log('Chart title: ' + String(VisualizationData.graphs[i]['options']['title']))
					console.log('Check input data format')
					console.log(err.str)
				}
			}
			
			SetOptions();
			
			// Create and draw the visualization
			for (i=0; i<numCharts; i++) {
				try{
					chart[i] = new google.visualization[chartTypes[i]](document.getElementById(chartHandle[i]));
					chart[i].draw(data[i], options[i]);
				}
				catch(err){
					h = document.getElementById(chartHandle[i])
					h.innerHTML='Error creating Google Visualization. Could be incorrect chart type: ' + chartTypes[i] + '<br />' + 'Error message: ' + err.message
				}
			}
		}
		
		function CustomizeCharts() {
			for (i=0; i<numCharts; i++) {
				if (VisualizationData.graphs[i].OnReadyHandler) {
					console.log('On ready, calling customize on graph: ' + i);
					google.visualization.events.addListener(chart[i], 'ready', VisualizationData.graphs[i].OnReadyHandler);
				}
			}
			
			/*for (i=0; i<numCharts; i++) {
				var e = document.getElementById('chart_div_outer' + i)
				var btn = document.createElement("BUTTON");
				btn.innerHTML = "Download SVG";
				btn.setAttribute("onclick", "CreateSVG(" + i + ")");
				btn.className = 'myButton';
				e.appendChild(btn);
			}*/
			
		}
		
		
		function CreateSVG(id){
			var e = document.getElementById('chart_div' + id);
			var s = e.getElementsByTagName('svg')[0].outerHTML;
			var s_svg = s.replace(/svg width/, 'svg xmlns="http://www.w3.org/2000/svg" width');
			
			var element = document.createElement('a');
			element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(s_svg));
			element.setAttribute('download', 'chart' + id + '.svg');

			element.style.display = 'none';
			document.body.appendChild(element);

			element.click();
			document.body.removeChild(element);			
		}

		
	</script>	
'''
					
		print (mystr, file = fp)
	
	@classmethod
	def PrintHTMLBody2(cls, fp, data = ''):
		mystr = '''\
	<script type='text/javascript'>				  	
		{0}
	</script>
</body>
</html>
		'''
		print (mystr.format(data), file = fp);
	
	@classmethod
	def Generate(cls, serialized_charts = '', filename='results.html'):
		fp = open(filename, 'w')
		cls.PrintHTMLHead(fp)
		cls.PrintHTMLBody(fp)
		cls.PrintHTMLBody2(fp, serialized_charts)
		fp.close()

	@staticmethod
	def HTMLSanitize(s):
		s = s.replace('\n', '<br />')
		s = s.replace('\r', '<br />')
		s = s.replace('"', '\\"')
		return s

if __name__ == "main":
    pass
