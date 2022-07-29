import os
import pandas as pd
import numpy as np
import urllib.request
from PIL import Image


df = pd.read_csv("/content/drive/MyDrive/wikiPedia_ic/wiki_fa_cap_cleaned.csv")

# Convert png, webp, jpeg to jpg
def convertToJpg(parent_dir, fname):
    """
    Convert png, webp, jpeg to .jpg
    """
    im = Image.open(parent_dir + fname)
    rgb_im = im.convert('RGB')
    postfix = fname.split('.')[-1]
    c_fname = fname.replace(postfix, 'jpg') # filename with .jpg postfix
    rgb_im.save(parent_dir + c_fname)
    os.remove(parent_dir + fname) # delete original image.
    print(f'{c_fname} ............converted to jpg.')
    return c_fname

def downloadImage(url, parent_dir, filename):
  """
  Given a url and filename, it'll download image and save it into images/{passed filename}.
  """

  opener = urllib.request.build_opener()
  opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
  urllib.request.install_opener(opener)

  try:
    postfix = url.split('.')[-1].lower()
    filename = str(filename) + '.' + postfix
    urllib.request.urlretrieve(url, parent_dir + filename)
    print(f"{filename} .............Downloaded!")
    status = True
    return status, filename
  except Exception as e:
    status = False
    print(e)
    return status, np.nan

def download(urls, path):
  for idx in range(len(urls)):
    # Dowload url and save status:(True / False)
      isDownloaded, dn_fname = downloadImage(urls[idx], parent_dir=path, filename=str(idx))
      # check if file downloaded correctly and its format isn't jpg:
      if isDownloaded and not dn_fname.endswith('.jpg'):
        filename = convertToJpg(parent_dir=path, fname=dn_fname)
        df.loc[idx, 'filename'] = filename # append filename to dataset
      elif isDownloaded and dn_fname.endswith('.jpg'):
        df.loc[idx, 'filename'] = dn_fname # append filename to dataset
      else:
        df.loc[idx, 'filename'] = dn_fname # append filename to dataset

# List of urls retrieved from dataset
urls = list(df['image_url'])
print("Number of urls : {}".format(len(urls)))

# Directory that images downloaded to.
download_here = './wikipedia_images/'

download(urls, download_here)

# save modified csv.
df.to_csv("./wikipedia_facap.csv", index=False)