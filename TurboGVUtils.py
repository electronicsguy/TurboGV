# TurboGV Charts Serializer
# Sujay Phadke, (C) 2021
#

class TurboGVUtils:
    def __init__(self) -> None:
        pass
    
    # Note: Need to use '{{' or '}}' to escape meaning of {x} within str.format()
    @staticmethod
    def OnReadyHandler(index, textformat=False, svg=False):
        temp1 = TurboGVUtils.TextFormatCallback(index) if textformat else ''
        temp2 = TurboGVUtils.SVGDownload(index) if svg else ''

        str = \
        '''
        VisualizationData.graphs[{0}].OnReadyHandler = function(){{
            {1}
            {2}
        }};
        '''
        return str.format(index, temp1, temp2)
	
    @staticmethod
    def SVGDownload(index):
        str = \
        '''
            var e = document.getElementById('chart_div' + {0})
            var f = e.parentElement;
            var btn = document.createElement("BUTTON");
            btn.innerHTML = "Download SVG";
            btn.setAttribute("onclick", "CreateSVG(" + {0} + ")");
            btn.className = 'myButton';
            f.appendChild(btn);
        '''
        return str.format(index)	
    
    @staticmethod
    def TextFormatCallback(index):
        str = \
        '''
            e = document.getElementById(chartHandle[{0}]);
            labels = e.getElementsByTagName('text');
            [...labels].forEach(function(label, i) {{
                label.innerHTML = TransformSuperSub(label.innerHTML);
                label.innerHTML = TransformScientific(label.innerHTML);
            }})
        '''
        return str.format(index)

    @staticmethod
    def AddGenericFunctions():
        str = \
        '''
        // Generic Functions
        function TransformSuperSub(text){				
            // Superscript or subscript follows Latex convention with forced curly-braces
            temp1 = text.replace(/\^{(.*?)}/g, "<tspan baseline-shift='super'>$1</tspan>");
            temp2 = temp1.replace(/\_{(.*?)}/g, "<tspan baseline-shift='sub'>$1</tspan>");
            return temp2;
        }

        function TransformScientific(text){				
            // Convert 10E5 to 10*(10^5)  or 10E-5 to 10*(10^-5)
            temp1 = text.replace(/[Ee]([+-]?\d+)/g, "x10<tspan baseline-shift='super'>$1</tspan>");
            return temp1;
        }

        function LimitPrecision(f) {
            return parseFloat(f).toFixed(1);
        }
        '''
        return str
        
if __name__ == 'main':
    pass
