import os,shutil,glob

from PIL import Image

if __name__ == '__main__':
    os.chdir('small')
    for dir in os.listdir('.'):
        for file in os.listdir(dir):
            im = Image.open(dir+'/'+file)
            im.resize((180,240)).save(dir+'/'+file)


