class style:
    def __init__(self) -> None:
        self.name = ''
        self.params = {
            'font.family': None,
            'font.style': None,
            'font.weight':'normal',
            'font.size':2.
        }
        self.color_dict = {}
        self.markers = []
    def __init__(self, params, color_dict, markers) -> None:
        self.params = params
        self.color_dict = color_dict
        self.markers = markers

class style_default(style):
    def __init__(self) -> None:
        params = {
            'font.family':'sans-serif',
            'font.sans-serif':'Arial',
            'font.style':'normal',
            'font.weight':'normal',
            'font.size': 0.35
        }
        color_dict = {
            'grey':'#6c6c6c',
            'red':'#c82f27',
            'yellow':'#d99f42',
            'green':'#63b84e',
            'cyan':'#58a7a2',
            'blue':'#4064af',
            'purple':'#673695',
            'violet':'#b83c7d',
            'orange':'#a2462d',
            'grass':'#8f9b47',
            'dark_green':'#446e53',
            'light_blue':'#508090',
            'mild_blue':'#3c3f8b',
            'mild_purple':'#823a7e'
        }
        markers = ['o','v','D','p','s','.','^','*','O','>']
        super().__init__(params, color_dict, markers)
        self.name = 'default'
