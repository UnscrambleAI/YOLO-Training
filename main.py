import os
import json
from PIL import Image

dir = os.listdir('./annotations/')
imgs = os.listdir('./images/')

with open('dataset.csv', 'a') as cf:
	cf.write('name, width, height, class, xmin, ymin, xmax, ymax\n')
	for i in range(len(dir)):
		cur_i = dir[i]
		if cur_i.split('.')[1] == 'json':
			with open('./annotations/' + cur_i) as f:
				data = json.load(f)
				points = data['shapes'][0]['points']
				xmin = points[0][0]
				ymin = points[0][1]
				xmax = points[1][0]
				ymax = points[1][1]

				img = Image.open('./images/' + imgs[i])
				width = img.width
				height = img.height

				cf.write('{}, {}, {}, Damage, {}, {}, {}, {}\n'.format(cur_i.split('.')[0], width, height, xmin, ymin, xmax, ymax))