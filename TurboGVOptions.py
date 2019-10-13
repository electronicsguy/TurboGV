# TurboGV Charts Serializer
# Sujay Phadke, (C) 2021
#

class Generic:
    def Serialize(self):
        return self.Options
        
    def __init__(self) -> None:
        self.Options = {
            'titleTextStyle': {
                'color': 'red', 'fontSize': '16'
            },
            'fontColor': 'black',
            'legend': { 'position': 'none', 'alignment': 'center' },
            'theme': 'material'
	    }

class Column(Generic):
    def __init__(self) -> None:
        self.Options = {
            'titleTextStyle': {
                'color': 'red', 'fontSize': '16'
            },
            'tooltip': {
                'textStyle': {'fontName': 'Arial', 'fontSize': 10, 'color': 'black'}, 'showColorCode': 'true',
            },
            'headerHeight': 25,
            'headerColor': '#d1f9f8',
            'fontColor': 'black',
            'legend': { 'position': 'none', 'alignment': 'center', 'textStyle': {'fontSize': '10'}},
            'theme': 'material'
        }

if __name__ == "main":
    pass
