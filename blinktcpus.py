# blinktcpus.py - per-CPU % display for Pimoroni's Blinkt! colour LEDs. Must be run sudo (!?)
# Viridis colour values from https://github.com/sjmgarnier/viridisLite/blob/master/R/zzz.R

import sys
import time
import math
import psutil
import blinkt

BRIGHTNESS_DAY = 0.25  # Day brightness
BRIGHTNESS_NIGHT = 0.1 # Night brightness. Lowest it seems to go is 0.033
RGBMAX_DAY = 64 	   # RGBMAX must be in [0,255]
RGBMAX_NIGHT = 16 	   # RGBMAX must be in [0,255]
UPDATE = 0.2 		   # Update frequency in seconds

def collect():
	"""Fetch per-CPU utilization %"""
	cpu = psutil.cpu_percent(percpu = True)
	return cpu

def ccalc_viridis(x, rgbmax):
	"""viridis colour map"""
	r = [0.26700401, 0.26851048, 0.26994384, 0.27130489, 0.27259384, 0.27380934, 0.27495242, 0.27602238, 0.2770184, 0.27794143, 0.27879067, 0.2795655, 0.28026658, 0.28089358, 0.28144581, 0.28192358, 0.28232739, 0.28265633, 0.28291049, 0.28309095, 0.28319704, 0.28322882, 0.28318684, 0.283072, 0.28288389, 0.28262297, 0.28229037, 0.28188676, 0.28141228, 0.28086773, 0.28025468, 0.27957399, 0.27882618, 0.27801236, 0.27713437, 0.27619376, 0.27519116, 0.27412802, 0.27300596, 0.27182812, 0.27059473, 0.26930756, 0.26796846, 0.26657984, 0.2651445, 0.2636632, 0.26213801, 0.26057103, 0.25896451, 0.25732244, 0.25564519, 0.25393498, 0.25219404, 0.25042462, 0.24862899, 0.2468114, 0.24497208, 0.24311324, 0.24123708, 0.23934575, 0.23744138, 0.23552606, 0.23360277, 0.2316735, 0.22973926, 0.22780192, 0.2258633, 0.22392515, 0.22198915, 0.22005691, 0.21812995, 0.21620971, 0.21429757, 0.21239477, 0.2105031, 0.20862342, 0.20675628, 0.20490257, 0.20306309, 0.20123854, 0.1994295, 0.1976365, 0.19585993, 0.19410009, 0.19235719, 0.19063135, 0.18892259, 0.18723083, 0.18555593, 0.18389763, 0.18225561, 0.18062949, 0.17901879, 0.17742298, 0.17584148, 0.17427363, 0.17271876, 0.17117615, 0.16964573, 0.16812641, 0.1666171, 0.16511703, 0.16362543, 0.16214155, 0.16066467, 0.15919413, 0.15772933, 0.15626973, 0.15481488, 0.15336445, 0.1519182, 0.15047605, 0.14903918, 0.14760731, 0.14618026, 0.14475863, 0.14334327, 0.14193527, 0.14053599, 0.13914708, 0.13777048, 0.1364085, 0.13506561, 0.13374299, 0.13244401, 0.13117249, 0.1299327, 0.12872938, 0.12756771, 0.12645338, 0.12539383, 0.12439474, 0.12346281, 0.12260562, 0.12183122, 0.12114807, 0.12056501, 0.12009154, 0.11973756, 0.11951163, 0.11942341, 0.11948255, 0.11969858, 0.12008079, 0.12063824, 0.12137972, 0.12231244, 0.12344358, 0.12477953, 0.12632581, 0.12808703, 0.13006688, 0.13226797, 0.13469183, 0.13733921, 0.14020991, 0.14330291, 0.1466164, 0.15014782, 0.15389405, 0.15785146, 0.16201598, 0.1663832, 0.1709484, 0.17570671, 0.18065314, 0.18578266, 0.19109018, 0.19657063, 0.20221902, 0.20803045, 0.21400015, 0.22012381, 0.2263969, 0.23281498, 0.2393739, 0.24606968, 0.25289851, 0.25985676, 0.26694127, 0.27414922, 0.28147681, 0.28892102, 0.29647899, 0.30414796, 0.31192534, 0.3198086, 0.3277958, 0.33588539, 0.34407411, 0.35235985, 0.36074053, 0.3692142, 0.37777892, 0.38643282, 0.39517408, 0.40400101, 0.4129135, 0.42190813, 0.43098317, 0.44013691, 0.44936763, 0.45867362, 0.46805314, 0.47750446, 0.4870258, 0.49661536, 0.5062713, 0.51599182, 0.52577622, 0.5356211, 0.5455244, 0.55548397, 0.5654976, 0.57556297, 0.58567772, 0.59583934, 0.60604528, 0.61629283, 0.62657923, 0.63690157, 0.64725685, 0.65764197, 0.66805369, 0.67848868, 0.68894351, 0.69941463, 0.70989842, 0.72039115, 0.73088902, 0.74138803, 0.75188414, 0.76237342, 0.77285183, 0.78331535, 0.79375994, 0.80418159, 0.81457634, 0.82494028, 0.83526959, 0.84556056, 0.8558096, 0.86601325, 0.87616824, 0.88627146, 0.89632002, 0.90631121, 0.91624212, 0.92610579, 0.93590444, 0.94563626, 0.95529972, 0.96489353, 0.97441665, 0.98386829, 0.99324789]
	g = [0.00487433, 0.00960483, 0.01462494, 0.01994186, 0.02556309, 0.03149748, 0.03775181, 0.04416723, 0.05034437, 0.05632444, 0.06214536, 0.06783587, 0.07341724, 0.07890703, 0.0843197, 0.08966622, 0.09495545, 0.10019576, 0.10539345, 0.11055307, 0.11567966, 0.12077701, 0.12584799, 0.13089477, 0.13592005, 0.14092556, 0.14591233, 0.15088147, 0.15583425, 0.16077132, 0.16569272, 0.17059884, 0.1754902, 0.18036684, 0.18522836, 0.19007447, 0.1949054, 0.19972086, 0.20452049, 0.20930306, 0.21406899, 0.21881782, 0.22354911, 0.2282621, 0.23295593, 0.23763078, 0.24228619, 0.2469217, 0.25153685, 0.2561304, 0.26070284, 0.26525384, 0.26978306, 0.27429024, 0.27877509, 0.28323662, 0.28767547, 0.29209154, 0.29648471, 0.30085494, 0.30520222, 0.30952657, 0.31382773, 0.3181058, 0.32236127, 0.32659432, 0.33080515, 0.334994, 0.33916114, 0.34330688, 0.34743154, 0.35153548, 0.35561907, 0.35968273, 0.36372671, 0.36775151, 0.37175775, 0.37574589, 0.37971644, 0.38366989, 0.38760678, 0.39152762, 0.39543297, 0.39932336, 0.40319934, 0.40706148, 0.41091033, 0.41474645, 0.4185704, 0.42238275, 0.42618405, 0.42997486, 0.43375572, 0.4375272, 0.44128981, 0.4450441, 0.4487906, 0.4525298, 0.45626209, 0.45998802, 0.46370813, 0.4674229, 0.47113278, 0.47483821, 0.47853961, 0.4822374, 0.48593197, 0.4896237, 0.49331293, 0.49700003, 0.50068529, 0.50436904, 0.50805136, 0.51173263, 0.51541316, 0.51909319, 0.52277292, 0.52645254, 0.53013219, 0.53381201, 0.53749213, 0.54117264, 0.54485335, 0.54853458, 0.55221637, 0.55589872, 0.55958162, 0.56326503, 0.56694891, 0.57063316, 0.57431754, 0.57800205, 0.58168661, 0.58537105, 0.58905521, 0.59273889, 0.59642187, 0.60010387, 0.60378459, 0.60746388, 0.61114146, 0.61481702, 0.61849025, 0.62216081, 0.62582833, 0.62949242, 0.63315277, 0.63680899, 0.64046069, 0.64410744, 0.64774881, 0.65138436, 0.65501363, 0.65863619, 0.66225157, 0.66585927, 0.66945881, 0.67304968, 0.67663139, 0.68020343, 0.68376525, 0.68731632, 0.69085611, 0.69438405, 0.6978996, 0.70140222, 0.70489133, 0.70836635, 0.71182668, 0.71527175, 0.71870095, 0.72211371, 0.72550945, 0.72888753, 0.73224735, 0.73558828, 0.73890972, 0.74221104, 0.74549162, 0.74875084, 0.75198807, 0.75520266, 0.75839399, 0.76156142, 0.76470433, 0.76782207, 0.77091403, 0.77397953, 0.7770179, 0.78002855, 0.78301086, 0.78596419, 0.78888793, 0.79178146, 0.79464415, 0.79747541, 0.80027461, 0.80304099, 0.80577412, 0.80847343, 0.81113836, 0.81376835, 0.81636288, 0.81892143, 0.82144351, 0.82392862, 0.82637633, 0.82878621, 0.83115784, 0.83349064, 0.83578452, 0.83803918, 0.84025437, 0.8424299, 0.84456561, 0.84666139, 0.84871722, 0.8507331, 0.85270912, 0.85464543, 0.85654226, 0.85839991, 0.86021878, 0.86199932, 0.86374211, 0.86544779, 0.86711711, 0.86875092, 0.87035015, 0.87191584, 0.87344918, 0.87495143, 0.87642392, 0.87786808, 0.87928545, 0.88067763, 0.88204632, 0.88339329, 0.88472036, 0.88602943, 0.88732243, 0.88860134, 0.88986815, 0.89112487, 0.89237353, 0.89361614, 0.89485467, 0.89609127, 0.89732977, 0.8985704, 0.899815, 0.90106534, 0.90232311, 0.90358991, 0.90486726, 0.90615657]
	b = [0.32941519, 0.33542652, 0.34137895, 0.34726862, 0.35309303, 0.35885256, 0.36454323, 0.37016418, 0.37571452, 0.38119074, 0.38659204, 0.39191723, 0.39716349, 0.40232944, 0.40741404, 0.41241521, 0.41733086, 0.42216032, 0.42690202, 0.43155375, 0.43611482, 0.44058404, 0.44496, 0.44924127, 0.45342734, 0.45751726, 0.46150995, 0.46540474, 0.46920128, 0.47289909, 0.47649762, 0.47999675, 0.48339654, 0.48669702, 0.48989831, 0.49300074, 0.49600488, 0.49891131, 0.50172076, 0.50443413, 0.50705243, 0.50957678, 0.5120084, 0.5143487, 0.5165993, 0.51876163, 0.52083736, 0.52282822, 0.52473609, 0.52656332, 0.52831152, 0.52998273, 0.53157905, 0.53310261, 0.53455561, 0.53594093, 0.53726018, 0.53851561, 0.53970946, 0.54084398, 0.5419214, 0.54294396, 0.54391424, 0.54483444, 0.54570633, 0.546532, 0.54731353, 0.54805291, 0.54875211, 0.54941304, 0.55003755, 0.55062743, 0.5511844, 0.55171011, 0.55220646, 0.55267486, 0.55311653, 0.55353282, 0.55392505, 0.55429441, 0.55464205, 0.55496905, 0.55527637, 0.55556494, 0.55583559, 0.55608907, 0.55632606, 0.55654717, 0.55675292, 0.55694377, 0.5571201, 0.55728221, 0.55743035, 0.55756466, 0.55768526, 0.55779216, 0.55788532, 0.55796464, 0.55803034, 0.55808199, 0.55811913, 0.55814141, 0.55814842, 0.55813967, 0.55811466, 0.5580728, 0.55801347, 0.557936, 0.55783967, 0.55772371, 0.55758733, 0.55742968, 0.5572505, 0.55704861, 0.55682271, 0.55657181, 0.55629491, 0.55599097, 0.55565893, 0.55529773, 0.55490625, 0.55448339, 0.55402906, 0.55354108, 0.55301828, 0.55245948, 0.55186354, 0.55122927, 0.55055551, 0.5498411, 0.54908564, 0.5482874, 0.54744498, 0.54655722, 0.54562298, 0.54464114, 0.54361058, 0.54253043, 0.54139999, 0.54021751, 0.53898192, 0.53769219, 0.53634733, 0.53494633, 0.53348834, 0.53197275, 0.53039808, 0.52876343, 0.52706792, 0.52531069, 0.52349092, 0.52160791, 0.51966086, 0.5176488, 0.51557101, 0.5134268, 0.51121549, 0.50893644, 0.5065889, 0.50417217, 0.50168574, 0.49912906, 0.49650163, 0.49380294, 0.49103252, 0.48818938, 0.48527326, 0.48228395, 0.47922108, 0.47608431, 0.4728733, 0.46958774, 0.46622638, 0.46278934, 0.45927675, 0.45568838, 0.45202405, 0.44828355, 0.44446673, 0.44057284, 0.4366009, 0.43255207, 0.42842626, 0.42422341, 0.41994346, 0.41558638, 0.41115215, 0.40664011, 0.40204917, 0.39738103, 0.39263579, 0.38781353, 0.38291438, 0.3779385, 0.37288606, 0.36775726, 0.36255223, 0.35726893, 0.35191009, 0.34647607, 0.3409673, 0.33538426, 0.32972749, 0.32399761, 0.31819529, 0.31232133, 0.30637661, 0.30036211, 0.29427888, 0.2881265, 0.28190832, 0.27562602, 0.26928147, 0.26287683, 0.25641457, 0.24989748, 0.24332878, 0.23671214, 0.23005179, 0.22335258, 0.21662012, 0.20986086, 0.20308229, 0.19629307, 0.18950326, 0.18272455, 0.17597055, 0.16925712, 0.16260273, 0.15602894, 0.14956101, 0.14322828, 0.13706449, 0.13110864, 0.12540538, 0.12000532, 0.11496505, 0.11034678, 0.10621724, 0.1026459, 0.09970219, 0.09745186, 0.09595277, 0.09525046, 0.09537439, 0.09633538, 0.09812496, 0.1007168, 0.10407067, 0.10813094, 0.11283773, 0.11812832, 0.12394051, 0.13021494, 0.13689671, 0.1439362]
	i = int(round(x * 255, 0))
	return [r[i]*rgbmax, g[i]*rgbmax, b[i]*rgbmax]

def ccalc_plasma(x, rgbmax):
	"""viridis 'plasma' colour map"""
	r = [0.05038321,0.06353636,0.07535312,0.08622180,0.09637861,0.10597970,0.11512364,0.12390290,0.13238072,0.14060308,0.14860653,0.15642065,0.16406972,0.17157392,0.17895021,0.18621296,0.19337445,0.20044526,0.20743455,0.21435030,0.22119675,0.22798297,0.23471454,0.24139625,0.24803238,0.25462669,0.26118256,0.26770299,0.27419067,0.28064797,0.28707606,0.29347769,0.29985512,0.30620982,0.31254312,0.31885618,0.32515003,0.33142555,0.33768345,0.34392459,0.35014970,0.35635921,0.36255347,0.36873276,0.37489727,0.38104712,0.38718264,0.39330401,0.39941082,0.40550291,0.41158008,0.41764206,0.42368855,0.42971919,0.43573357,0.44173212,0.44771360,0.45367739,0.45962294,0.46554963,0.47145685,0.47734393,0.48321020,0.48905495,0.49487747,0.50067769,0.50645414,0.51220603,0.51793258,0.52363299,0.52930647,0.53495224,0.54056951,0.54615749,0.55171542,0.55724254,0.56273810,0.56820137,0.57363186,0.57902868,0.58439114,0.58971861,0.59501050,0.60026628,0.60548543,0.61066747,0.61581197,0.62091856,0.62598687,0.63101661,0.63600754,0.64095944,0.64587216,0.65074557,0.65557961,0.66037427,0.66512949,0.66984539,0.67452206,0.67915966,0.68375838,0.68831844,0.69284009,0.69732361,0.70176933,0.70617759,0.71054875,0.71488319,0.71918134,0.72344360,0.72767043,0.73186223,0.73601942,0.74014256,0.74423210,0.74828853,0.75231232,0.75630394,0.76026385,0.76419252,0.76809039,0.77195792,0.77579552,0.77960361,0.78338264,0.78713298,0.79085501,0.79454910,0.79821558,0.80185476,0.80546695,0.80905242,0.81261151,0.81614438,0.81965126,0.82313231,0.82658771,0.83001758,0.83342205,0.83680124,0.84015528,0.84348410,0.84678773,0.85006613,0.85331928,0.85654710,0.85974952,0.86292656,0.86607792,0.86920344,0.87230292,0.87537615,0.87842290,0.88144292,0.88443598,0.88740168,0.89033969,0.89324965,0.89613119,0.89898393,0.90180746,0.90460129,0.90736500,0.91009809,0.91280010,0.91547052,0.91810885,0.92071438,0.92328666,0.92582515,0.92832927,0.93079847,0.93323214,0.93562968,0.93799003,0.94031294,0.94259777,0.94484389,0.94705066,0.94921743,0.95134353,0.95342772,0.95546964,0.95746877,0.95942443,0.96133593,0.96320257,0.96502366,0.96679847,0.96852564,0.97020459,0.97183501,0.97341614,0.97494726,0.97642761,0.97785642,0.97923292,0.98055634,0.98182589,0.98304074,0.98419892,0.98530076,0.98634542,0.98733207,0.98825985,0.98912789,0.98993533,0.99068126,0.99136479,0.99198499,0.99254094,0.99303169,0.99345630,0.99381380,0.99410323,0.99432360,0.99447393,0.99455326,0.99456059,0.99449496,0.99435541,0.99414099,0.99385078,0.99348219,0.99303325,0.99250521,0.99189727,0.99120868,0.99043879,0.98958707,0.98864774,0.98762056,0.98650937,0.98531420,0.98403114,0.98265282,0.98119039,0.97964364,0.97799492,0.97626498,0.97444304,0.97253001,0.97053293,0.96844348,0.96627122,0.96402106,0.96168148,0.95927565,0.95680807,0.95428681,0.95172608,0.94915053,0.94660227,0.94415174,0.94189612,0.94001510]
	g = [0.0298028976,0.0284259729,0.0272063728,0.0261253206,0.0251650976,0.0243092436,0.0235562500,0.0228781011,0.0222583774,0.0216866674,0.0211535876,0.0206507174,0.0201705326,0.0197063415,0.0192522243,0.0188029767,0.0183540593,0.0179015512,0.0174421086,0.0169729276,0.0164970484,0.0160071509,0.0155015065,0.0149791041,0.0144393586,0.0138820918,0.0133075156,0.0127162163,0.0121091423,0.0114875915,0.0108554862,0.0102128849,0.0095607955,0.0089018535,0.0082390070,0.0075755105,0.0069149173,0.0062610738,0.0056183089,0.0049905308,0.0043820256,0.0037978176,0.0032431959,0.0027237072,0.0022451490,0.0018135620,0.0014344692,0.0011138826,0.0008594208,0.0006780915,0.0005771017,0.0005638475,0.0006459028,0.0008310082,0.0011270588,0.0015398478,0.0020795474,0.0027547030,0.0035737442,0.0045451808,0.0056775876,0.0069795874,0.0084598349,0.0101269996,0.0119897486,0.0140550640,0.0163333443,0.0188332232,0.0215631918,0.0245316468,0.0277468735,0.0312170300,0.0349501310,0.0389540334,0.0431364795,0.0473307585,0.0515448092,0.0557776706,0.0600281369,0.0642955547,0.0685790261,0.0728775875,0.0771902878,0.0815161895,0.0858543713,0.0902039303,0.0945639838,0.0989336721,0.1033121600,0.1076986410,0.1120923350,0.1164924950,0.1208984050,0.1253093840,0.1297247850,0.1341439970,0.1385664280,0.1429915400,0.1474188350,0.1518478510,0.1562781630,0.1607093870,0.1651411740,0.1695732150,0.1740052360,0.1784370000,0.1828683060,0.1872989860,0.1917289060,0.1961579620,0.2005860860,0.2050131740,0.2094390710,0.2138639650,0.2182878990,0.2227109420,0.2271331870,0.2315547490,0.2359757650,0.2403963940,0.2448168130,0.2492372200,0.2536577970,0.2580783970,0.2624996620,0.2669218590,0.2713452670,0.2757701790,0.2801969010,0.2846257500,0.2890570570,0.2934911170,0.2979278650,0.3023681300,0.3068122820,0.3112607030,0.3157137820,0.3201719130,0.3246354990,0.3291048360,0.3335801060,0.3380621090,0.3425512720,0.3470480280,0.3515528150,0.3560660720,0.3605882290,0.3651194080,0.3696604460,0.3742117950,0.3787739100,0.3833472430,0.3879322490,0.3925293390,0.3971388770,0.4017615110,0.4063976940,0.4110478710,0.4157124890,0.4203919860,0.4250868070,0.4297974420,0.4345243350,0.4392679080,0.4440285740,0.4488067440,0.4536028180,0.4584174200,0.4632508280,0.4681033870,0.4729754650,0.4778674200,0.4827796030,0.4877123570,0.4926665440,0.4976420380,0.5026391470,0.5076581690,0.5126993900,0.5177630870,0.5228495220,0.5279595500,0.5330930830,0.5382501720,0.5434310380,0.5486358900,0.5538649310,0.5591183490,0.5643963270,0.5696996330,0.5750282700,0.5803820150,0.5857610120,0.5911653940,0.5965952870,0.6020508110,0.6075320770,0.6130391900,0.6185722500,0.6241313620,0.6297175160,0.6353298760,0.6409685080,0.6466334750,0.6523248320,0.6580426300,0.6637869140,0.6695577200,0.6753550820,0.6811790250,0.6870295670,0.6929067190,0.6988104840,0.7047408540,0.7106978140,0.7166813360,0.7226913790,0.7287278900,0.7347907990,0.7408800200,0.7469954480,0.7531369550,0.7593043900,0.7654985510,0.7717198330,0.7779667750,0.7842391200,0.7905365690,0.7968587750,0.8032053370,0.8095786050,0.8159779420,0.8224006200,0.8288459800,0.8353153600,0.8418117300,0.8483289020,0.8548664680,0.8614323140,0.8680159980,0.8746221940,0.8812500630,0.8878961250,0.8945639890,0.9012493650,0.9079503790,0.9146724790,0.9214065370,0.9281520650,0.9349077300,0.9416706050,0.9484349000,0.9551898600,0.9619164870,0.9685898140,0.9751583570]
	b = [0.5279749,0.5331237,0.5380070,0.5426577,0.5471035,0.5513679,0.5554677,0.5594235,0.5632501,0.5669595,0.5705617,0.5740654,0.5774781,0.5808059,0.5840542,0.5872277,0.5903300,0.5933643,0.5963333,0.5992392,0.6020833,0.6048674,0.6075924,0.6102591,0.6128677,0.6154185,0.6179114,0.6203460,0.6227219,0.6250385,0.6272950,0.6294905,0.6316239,0.6336941,0.6356998,0.6376395,0.6395120,0.6413156,0.6430489,0.6447102,0.6462977,0.6478098,0.6492446,0.6506006,0.6518758,0.6530685,0.6541768,0.6551988,0.6561328,0.6569773,0.6577304,0.6583905,0.6589560,0.6594254,0.6597971,0.6600690,0.6602404,0.6603100,0.6602767,0.6601394,0.6598972,0.6595493,0.6590950,0.6585337,0.6578649,0.6570876,0.6562023,0.6552092,0.6541085,0.6529006,0.6515860,0.6501654,0.6486397,0.6470099,0.6452773,0.6434433,0.6415094,0.6394774,0.6373488,0.6351261,0.6328116,0.6304077,0.6279170,0.6253421,0.6226857,0.6199508,0.6171404,0.6142574,0.6113052,0.6082868,0.6052055,0.6020646,0.5988674,0.5956173,0.5923175,0.5889713,0.5855823,0.5821536,0.5786882,0.5751894,0.5716602,0.5681034,0.5645220,0.5609187,0.5572961,0.5536570,0.5500036,0.5463383,0.5426633,0.5389808,0.5352926,0.5316010,0.5279084,0.5242155,0.5205238,0.5168345,0.5131490,0.5094683,0.5057935,0.5021256,0.4984653,0.4948133,0.4911705,0.4875391,0.4839177,0.4803067,0.4767063,0.4731168,0.4695383,0.4659709,0.4624146,0.4588696,0.4553376,0.4518164,0.4483059,0.4448058,0.4413159,0.4378359,0.4343656,0.4309051,0.4274548,0.4240131,0.4205793,0.4171533,0.4137344,0.4103225,0.4069170,0.4035188,0.4001260,0.3967382,0.3933549,0.3899758,0.3866005,0.3832286,0.3798602,0.3764942,0.3731302,0.3697679,0.3664069,0.3630470,0.3596878,0.3563288,0.3529698,0.3496105,0.3462507,0.3428901,0.3395288,0.3361656,0.3328008,0.3294345,0.3260666,0.3226969,0.3193254,0.3159522,0.3125754,0.3091966,0.3058158,0.3024331,0.2990486,0.2956623,0.2922745,0.2888834,0.2854904,0.2820961,0.2787010,0.2753052,0.2719092,0.2685132,0.2651178,0.2617215,0.2583254,0.2549313,0.2515396,0.2481512,0.2447668,0.2413872,0.2380134,0.2346463,0.2312872,0.2279371,0.2245950,0.2212649,0.2179485,0.2146475,0.2113641,0.2081004,0.2048589,0.2016420,0.1984529,0.1952946,0.1921705,0.1890845,0.1860405,0.1830432,0.1800972,0.1772078,0.1743807,0.1716217,0.1689375,0.1663349,0.1638212,0.1614042,0.1590920,0.1568906,0.1548076,0.1528549,0.1510416,0.1493769,0.1478698,0.1465291,0.1453573,0.1443626,0.1435567,0.1429451,0.1425284,0.1423027,0.1422786,0.1424534,0.1428082,0.1433509,0.1440612,0.1449229,0.1459187,0.1470144,0.1481796,0.1493704,0.1505203,0.1515660,0.1524095,0.1529212,0.1529254,0.1521776,0.1503279,0.1468608,0.1409556,0.1313255]
	i = int(round(x * 255, 0))
	return [r[i]*rgbmax, g[i]*rgbmax, b[i]*rgbmax]

def ccalc_turbo(x, rgbmax):
	""" viridis 'turbo' colour map"""
	r = [0.18995, 0.19483, 0.19956, 0.20415, 0.2086, 0.21291, 0.21708, 0.22111, 0.225, 0.22875, 0.23236, 0.23582, 0.23915, 0.24234, 0.24539, 0.2483, 0.25107, 0.25369, 0.25618, 0.25853, 0.26074, 0.2628, 0.26473, 0.26652, 0.26816, 0.26967, 0.27103, 0.27226, 0.27334, 0.27429, 0.27509, 0.27576, 0.27628, 0.27667, 0.27691, 0.27701, 0.27698, 0.2768, 0.27648, 0.27603, 0.27543, 0.27469, 0.27381, 0.27273, 0.27106, 0.26878, 0.26592, 0.26252, 0.25862, 0.25425, 0.24946, 0.24427, 0.23874, 0.23288, 0.22676, 0.22039, 0.21382, 0.20708, 0.20021, 0.19326, 0.18625, 0.17923, 0.17223, 0.16529, 0.15844, 0.15173, 0.14519, 0.13886, 0.13278, 0.12698, 0.12151, 0.11639, 0.11167, 0.10738, 0.10357, 0.10026, 0.0975, 0.09532, 0.09377, 0.09287, 0.09267, 0.0932, 0.09451, 0.09662, 0.09958, 0.10342, 0.10815, 0.11374, 0.12014, 0.12733, 0.13526, 0.14391, 0.15323, 0.16319, 0.17377, 0.18491, 0.19659, 0.20877, 0.22142, 0.23449, 0.24797, 0.2618, 0.27597, 0.29042, 0.30513, 0.32006, 0.33517, 0.35043, 0.36581, 0.38127, 0.39678, 0.41229, 0.42778, 0.44321, 0.45854, 0.47375, 0.48879, 0.50362, 0.51822, 0.53255, 0.54658, 0.56026, 0.57357, 0.58646, 0.59891, 0.61088, 0.62233, 0.63323, 0.64362, 0.65394, 0.66428, 0.67462, 0.68494, 0.69525, 0.70553, 0.71577, 0.72596, 0.7361, 0.74617, 0.75617, 0.76608, 0.77591, 0.78563, 0.79524, 0.80473, 0.8141, 0.82333, 0.83241, 0.84133, 0.8501, 0.85868, 0.86709, 0.8753, 0.88331, 0.89112, 0.8987, 0.90605, 0.91317, 0.92004, 0.92666, 0.93301, 0.93909, 0.94489, 0.95039, 0.9556, 0.96049, 0.96507, 0.96931, 0.97323, 0.97679, 0.98, 0.98289, 0.98549, 0.98781, 0.98986, 0.99163, 0.99314, 0.99438, 0.99535, 0.99607, 0.99654, 0.99675, 0.99672, 0.99644, 0.99593, 0.99517, 0.99419, 0.99297, 0.99153, 0.98987, 0.98799, 0.9859, 0.9836, 0.98108, 0.97837, 0.97545, 0.97234, 0.96904, 0.96555, 0.96187, 0.95801, 0.95398, 0.94977, 0.94538, 0.94084, 0.93612, 0.93125, 0.92623, 0.92105, 0.91572, 0.91024, 0.90463, 0.89888, 0.89298, 0.88691, 0.88066, 0.87422, 0.8676, 0.86079, 0.8538, 0.84662, 0.83926, 0.83172, 0.82399, 0.81608, 0.80799, 0.79971, 0.79125, 0.7826, 0.77377, 0.76476, 0.75556, 0.74617, 0.73661, 0.72686, 0.71692, 0.7068, 0.6965, 0.68602, 0.67535, 0.66449, 0.65345, 0.64223, 0.63082, 0.61923, 0.60746, 0.5955, 0.58336, 0.57103, 0.55852, 0.54583, 0.53295, 0.51989, 0.50664, 0.49321, 0.4796]
	g = [0.07176, 0.08339, 0.09498, 0.10652, 0.11802, 0.12947, 0.14087, 0.15223, 0.16354, 0.17481, 0.18603, 0.1972, 0.20833, 0.21941, 0.23044, 0.24143, 0.25237, 0.26327, 0.27412, 0.28492, 0.29568, 0.30639, 0.31706, 0.32768, 0.33825, 0.34878, 0.35926, 0.3697, 0.38008, 0.39043, 0.40072, 0.41097, 0.42118, 0.43134, 0.44145, 0.45152, 0.46153, 0.47151, 0.48144, 0.49132, 0.50115, 0.51094, 0.52069, 0.5304, 0.54015, 0.54995, 0.55979, 0.56967, 0.57958, 0.5895, 0.59943, 0.60937, 0.61931, 0.62923, 0.63913, 0.64901, 0.65886, 0.66866, 0.67842, 0.68812, 0.69775, 0.70732, 0.7168, 0.7262, 0.73551, 0.74472, 0.75381, 0.76279, 0.77165, 0.78037, 0.78896, 0.7974, 0.80569, 0.81381, 0.82177, 0.82955, 0.83714, 0.84455, 0.85175, 0.85875, 0.86554, 0.87211, 0.87844, 0.88454, 0.8904, 0.896, 0.90142, 0.90673, 0.91193, 0.91701, 0.92197, 0.9268, 0.93151, 0.93609, 0.94053, 0.94484, 0.94901, 0.95304, 0.95692, 0.96065, 0.96423, 0.96765, 0.97092, 0.97403, 0.97697, 0.97974, 0.98234, 0.98477, 0.98702, 0.98909, 0.99098, 0.99268, 0.99419, 0.99551, 0.99663, 0.99755, 0.99828, 0.99879, 0.9991, 0.99919, 0.99907, 0.99873, 0.99817, 0.99739, 0.99638, 0.99514, 0.99366, 0.99195, 0.98999, 0.98775, 0.98524, 0.98246, 0.97941, 0.9761, 0.97255, 0.96875, 0.9647, 0.96043, 0.95593, 0.95121, 0.94627, 0.94113, 0.93579, 0.93025, 0.92452, 0.91861, 0.91253, 0.90627, 0.89986, 0.89328, 0.88655, 0.87968, 0.87267, 0.86553, 0.85826, 0.85087, 0.84337, 0.83576, 0.82806, 0.82025, 0.81236, 0.80439, 0.79634, 0.78823, 0.78005, 0.77181, 0.76352, 0.75519, 0.74682, 0.73842, 0.73, 0.7214, 0.7125, 0.7033, 0.69382, 0.68408, 0.67408, 0.66386, 0.65341, 0.64277, 0.63193, 0.62093, 0.60977, 0.59846, 0.58703, 0.57549, 0.56386, 0.55214, 0.54036, 0.52854, 0.51667, 0.50479, 0.49291, 0.48104, 0.4692, 0.4574, 0.44565, 0.43399, 0.42241, 0.41093, 0.39958, 0.38836, 0.37729, 0.36638, 0.35566, 0.34513, 0.33482, 0.32473, 0.31489, 0.3053, 0.29599, 0.28696, 0.27824, 0.26981, 0.26152, 0.25334, 0.24526, 0.2373, 0.22945, 0.2217, 0.21407, 0.20654, 0.19912, 0.19182, 0.18462, 0.17753, 0.17055, 0.16368, 0.15693, 0.15028, 0.14374, 0.13731, 0.13098, 0.12477, 0.11867, 0.11268, 0.1068, 0.10102, 0.09536, 0.0898, 0.08436, 0.07902, 0.0738, 0.06868, 0.06367, 0.05878, 0.05399, 0.04931, 0.04474, 0.04028, 0.03593, 0.03169, 0.02756, 0.02354, 0.01963, 0.01583]
	b = [0.23217, 0.26149, 0.29024, 0.31844, 0.34607, 0.37314, 0.39964, 0.42558, 0.45096, 0.47578, 0.50004, 0.52373, 0.54686, 0.56942, 0.59142, 0.61286, 0.63374, 0.65406, 0.67381, 0.693, 0.71162, 0.72968, 0.74718, 0.76412, 0.7805, 0.79631, 0.81156, 0.82624, 0.84037, 0.85393, 0.86692, 0.87936, 0.89123, 0.90254, 0.91328, 0.92347, 0.93309, 0.94214, 0.95064, 0.95857, 0.96594, 0.97275, 0.97899, 0.98461, 0.9893, 0.99303, 0.99583, 0.99773, 0.99876, 0.99896, 0.99835, 0.99697, 0.99485, 0.99202, 0.98851, 0.98436, 0.97959, 0.97423, 0.96833, 0.9619, 0.95498, 0.94761, 0.93981, 0.93161, 0.92305, 0.91416, 0.90496, 0.8955, 0.8858, 0.8759, 0.86581, 0.85559, 0.84525, 0.83484, 0.82437, 0.81389, 0.80342, 0.79299, 0.78264, 0.7724, 0.7623, 0.75237, 0.74265, 0.73316, 0.72393, 0.715, 0.70599, 0.69651, 0.6866, 0.67627, 0.66556, 0.65448, 0.64308, 0.63137, 0.61938, 0.60713, 0.59466, 0.58199, 0.56914, 0.55614, 0.54303, 0.52981, 0.51653, 0.50321, 0.48987, 0.47654, 0.46325, 0.45002, 0.43688, 0.42386, 0.41098, 0.39826, 0.38575, 0.37345, 0.3614, 0.34963, 0.33816, 0.32701, 0.31622, 0.30581, 0.29581, 0.28623, 0.27712, 0.26849, 0.26038, 0.2528, 0.24579, 0.23937, 0.23356, 0.22835, 0.2237, 0.2196, 0.21602, 0.21294, 0.21032, 0.20815, 0.2064, 0.20504, 0.20406, 0.20343, 0.20311, 0.2031, 0.20336, 0.20386, 0.20459, 0.20552, 0.20663, 0.20788, 0.20926, 0.21074, 0.2123, 0.21391, 0.21555, 0.21719, 0.2188, 0.22038, 0.22188, 0.22328, 0.22456, 0.2257, 0.22667, 0.22744, 0.228, 0.22831, 0.22836, 0.22811, 0.22754, 0.22663, 0.22536, 0.22369, 0.22161, 0.21918, 0.2165, 0.21358, 0.21043, 0.20706, 0.20348, 0.19971, 0.19577, 0.19165, 0.18738, 0.18297, 0.17842, 0.17376, 0.16899, 0.16412, 0.15918, 0.15417, 0.1491, 0.14398, 0.13883, 0.13367, 0.12849, 0.12332, 0.11817, 0.11305, 0.10797, 0.10294, 0.09798, 0.0931, 0.08831, 0.08362, 0.07905, 0.07461, 0.07031, 0.06616, 0.06218, 0.05837, 0.05475, 0.05134, 0.04814, 0.04516, 0.04243, 0.03993, 0.03753, 0.03521, 0.03297, 0.03082, 0.02875, 0.02677, 0.02487, 0.02305, 0.02131, 0.01966, 0.01809, 0.0166, 0.0152, 0.01387, 0.01264, 0.01148, 0.01041, 0.00942, 0.00851, 0.00769, 0.00695, 0.00629, 0.00571, 0.00522, 0.00481, 0.00449, 0.00424, 0.00408, 0.00401, 0.00401, 0.0041, 0.00427, 0.00453, 0.00486, 0.00529, 0.00579, 0.00638, 0.00705, 0.0078, 0.00863, 0.00955, 0.01055]
	i = int(round(x * 255, 0))
	return [r[i]*rgbmax, g[i]*rgbmax, b[i]*rgbmax]

def update_pixels(rgbarr):
	"""Colour the Blinkt! pixels"""
	chunks = blinkt.NUM_PIXELS / len(rgbarr)
	for i in range(blinkt.NUM_PIXELS):
		r, g, b = rgbarr[math.floor(i/chunks)]
		blinkt.set_pixel(i, r, g, b)
	blinkt.show()

if __name__ == '__main__':

	ccalcdict = {'viridis':ccalc_viridis, 'plasma':ccalc_plasma, 'turbo':ccalc_turbo}
	ccalc = ccalc_turbo      # Default colour calc
	if (len(sys.argv) >= 2): # Check if a colour scheme is specified
		if (sys.argv[1] in ccalcdict):
			ccalc = ccalcdict[sys.argv[1]]
		else:
			print("Usage: python3 blinktcpus.py [viridis|plasma|turbo]")
			quit()

	while True:
		# Adjust brightness according to time
		hour = time.localtime().tm_hour
		if (hour >= 6 and hour < 18): # Daytime
			blinkt.set_brightness(BRIGHTNESS_DAY)
			rgbmax = RGBMAX_DAY
		else: # Nighttime
			blinkt.set_brightness(BRIGHTNESS_NIGHT)
			rgbmax = RGBMAX_NIGHT

		# Collect CPU usage and update pixels
		sample = collect()
		scaled = [max(min(x/100,1),0) for x in sample] # Scale [0,100] to [0,1]
		rgbarr = [ccalc(x, rgbmax) for x in scaled]
		# print("CPU %s: " + str([str(int(x*100)) + "%" for x in sample]))
		update_pixels(rgbarr)
		time.sleep(UPDATE)