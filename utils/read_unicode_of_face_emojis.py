import re
import os

def read_unicode_of_face_emojis(f_face):
	'''
	f_face: the face emoji file name
	return: dict_face with key: face type, value: a list of the unicodes of faces
	'''
	dict_face = {} # key: face type, value: a list of the unicodes of faces
	for face in f_face:
		dict_face[face] = []

	for face in f_face:
		with open(os.getcwd() + '/data/face_list/' + face + '.txt', 'rb') as f:
			for line in f:
				line = str(line).lower()
				face_unicode = re.findall(r'u\+[a-f0-9]+', line)
				if (face_unicode != []):
					if (len(face_unicode) != 1):
						print ('Error occurs')
					else:
						pure_face_unicode = face_unicode[0].split('u+')[1]
						dict_face[face].append(pure_face_unicode)
	return dict_face