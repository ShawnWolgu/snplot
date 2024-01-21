from cmcrameri import cm
from matplotlib import cm as mcm

cm_pure = {
    'black': '#000000',
    'red' : '#ff0000',
    'blue' : '#0000ff',
    'green' : '#00ff00',
    'cyan' : '#00ffff',
    'violet' : '#ff00ff',
    'grass' : '#008000',
    'orange' : '#ff8000',
    'purple' : '#8000ff',
    'navy' : '#000080',
    'rose' : '#ff0080',
    'yellow' : '#ffff00',
    'spring' : '#00ff80',
    'sky' : '#0080ff',
}

cm_pure2 = {
    'red' : '#ff0000',
    'blue' : '#0000ff',
    'grass' : '#008000',
    'cyan' : '#00bfbf',
    'yellow' : '#bfbf00',
    'orange' : '#ff7f0e',
    'violet' : '#bf00bf',
    'black': '#000000',
    'navy' : '#0000bf',
    'green': '#00ff00',
    'rose' : '#ff00bf',
    'purple' : '#7f00ff',
    "earth": "#E4B363",
    "wine": "#6B2737"
}

cm_snplot = {
    'grey':'#6c6c6c',
    'red':'#c82f27',
    'yellow':'#d99f42',
    'green':'#63b84e',
    'cyan':'#58a7a2',
    'blue':'#4064af',
    'purple':'#673695',
    'violet':'#b83c7d',
    'orange':'#a2462d',
    'mild_blue':'#3c3f8b',
    'grass':'#8f9b47',
    'mild_purple':'#823a7e',
    'dark_green':'#446e53',
    'light_blue':'#508090',
    "pink": "#FF9FE5",
    "lemon": "#F4F1BB"
}

cm_zepeda = {
    'blue':'#332288',
    'cyan':'#88ccee',
    'grass':'#0f7733',
    'red':'#cc6677',
    'yellow':'#ddcc77',
    'purple':'#aa4499',
    'orange':'#42a998',
    'grey':'#6c6c6c',
    'willow':'#6d7559',
    'skin':'#e0b9bf',
    'navy':'#2c5052',
    'black':'#000000',
    "sunset": "#E6C79C",
    "garnet": "#6A3937"
}

cm_dislocation = {
    'black':'#000000',
    'red':'#ff0000',
    'blue':'#0700ff',
    'grass':'#005700',
    'violet':'#ff19b9',
    'mint':'#00ffc1',
    'cheese':'#ffd300',
    'navy':'#00007b',
    'blueberry':'#8484ff',
    'cyan':'#008495',
    'brown':'#a0534a',
    'green':'#00ff00',
    "pink": "#FF9FE5",
    "lemon": "#F4F1BB"
}

contour_colormap = {
    'batlow': cm.batlow,
    'viridis': mcm.get_cmap('viridis'),
    'jet': mcm.get_cmap('jet'),
    'rainbow': mcm.get_cmap('rainbow')
}
