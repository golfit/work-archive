from numpy import *
from scipy import *

fsdS1=[37424.5996476, 41653.5595834, 44227.5263150, 46131.0556774, 49182.1682894, 50653.2950739, 53606.1748703, 55780.1390832, 57089.1133718, 59985.6457535, 62107.8610625, 63587.5513792, 66341.8088564, 68092.5511813, 72247.5476337, 76712.7851415, 80658.8429454, 85017.1129488, 89356.3968951, 93594.0489333, 97618.9823264, 101981.4708949, 106214.5114575, 110216.4585374, 114905.6925208, 118811.4579622, 123044.2552899, 127534.0780242, 131430.0200858, 135934.5997732, 140156.0737681, 144331.1893368, 148525.0469170, 152760.9304824, 156941.8488254, 161419.7132036, 165665.5066499, 169585.6757436, 174018.4621135, 178282.8769970, 182210.7172861, 186363.4646203, 189397.8241460, 190610.0620549, 192888.9157879, 195703.7345092, 196911.8206453, 199199.9926560, 202010.4013603, 203216.1321761, 205529.6446799, 208522.5978787, 210151.8740108, 211854.3228970, 214813.9191489, 216735.7611092, 218191.1551739, 221125.9724840, 223036.1525139, 224513.5490365, 227439.7441895, 229328.6753949, 230838.7373929, 233757.8880172, 235600.1324580, 237403.7660717, 240189.5206042, 241874.3935235, 243703.6902578, 246510.9192798, 248176.9515318, 250004.1428072, 252829.8252008, 254483.5682235, 256307.7576349, 259129.6242293, 261355.1974513, 262616.0436537, 265437.7732735, 267656.0504605, 268929.2057121, 271759.1764223, 273958.6792342, 275239.0767348, 278084.8413393, 280215.5909803, 281787.8815468, 284438.4985998, 286533.0096677, 288269.3083714, 290768.9270019, 292476.0027460, 294314.4896480, 297087.8179945, 299011.2694920, 300795.1439464]

Hreal=[199.05837, 199.79194, 199.09048, 197.58215, 197.07984, 196.98346, 196.74508, 196.55577, 196.45237, 196.58390, 197.09146, 197.62422, 198.15029, 198.64785, 199.12736, 199.59044, 200.02534, 200.43851, 200.85210, 201.22315, 201.55419, 201.84666, 202.11577, 202.35132, 202.56785, 202.76578, 202.94892, 203.11071, 203.26541, 203.41517, 203.55713, 203.69295, 203.80766, 203.92983, 204.03262, 204.13144, 204.22284, 204.31694, 204.39592, 204.46153, 204.51805, 204.57406, 204.62548, 204.66010, 204.69856, 204.72940, 204.75556, 204.77954, 204.81091, 204.83858, 204.86068, 204.88717, 204.91028, 204.93041, 204.95372, 204.97891, 205.00893, 205.03144, 205.05018, 205.06241, 205.08955, 205.11090, 205.13244, 205.16095, 205.18529, 205.20489, 205.21826, 205.23180, 205.24835, 205.27129, 205.28638, 205.29426, 205.30863, 205.32259, 205.33166, 205.34771, 205.36792, 205.39145, 205.40305, 205.42731, 205.44927, 205.47474, 205.49399, 205.51264, 205.53373, 205.55352, 205.57558, 205.59069, 205.61153, 205.61142, 205.63191, 205.61762, 205.62793, 205.62708, 205.60543, 205.61053]

Himag=[-7.43645, -6.39943, -6.55689, -6.34487, -6.04337, -5.73344, -5.44799, -5.21252, -4.90764, -4.59269, -4.30699, -4.02726, -3.77049, -3.53250, -3.31251, -3.11950, -2.97711, -2.80988, -2.64540, -2.49958, -2.38517, -2.29105, -2.21999, -2.16245, -2.11519, -2.08275, -2.06176, -2.05005, -2.04254, -2.03133, -2.02611, -2.02941, -2.04326, -2.06599, -2.09051, -2.11340, -2.13731, -2.15911, -2.18845, -2.22549, -2.26033, -2.29902, -2.32294, -2.34754, -2.37538, -2.39570, -2.41618, -2.44008, -2.46319, -2.48732, -2.51009, -2.53353, -2.55497, -2.57187, -2.58517, -2.60898, -2.63523, -2.65256, -2.67976, -2.70542, -2.72567, -2.74906, -2.76994, -2.78470, -2.80841, -2.82567, -2.84175, -2.86575, -2.87676, -2.87851, -2.89777, -2.90922, -2.92317, -2.95224, -2.96450, -2.97822, -2.98625, -2.99039, -3.00933, -3.03810, -3.05554, -3.08144, -3.10787, -3.12112, -3.15091, -3.26453, -3.30104, -3.33641, -3.36786, -3.39934, -3.47601, -3.50349, -3.57367, -3.52047, -3.60066, -3.75463]

HsdS1=double(Hreal)+1j*double(Himag)