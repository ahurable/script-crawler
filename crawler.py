import re
import os
import time
import zipfile
import random
import colorama



class Crawler():

  def __init__(self, path, o_textdomain, textdomain, dirname, tfuncname):
    self.path = path
    self.otextdomain = o_textdomain
    self.textdomain = textdomain
    self.dirname = dirname
    self.tfuncname = tfuncname

  def openfile(self):
    try:
      f = open(self.path, 'r', encoding='utf-8')
    except: 
      f = open(self.path, 'r')

    return f

  def writel(self):
    x = self.openfile().readlines()
    return x

  def findInLines(self):
    lines = self.writel()
    n = 0 
    while n < len(lines):
      if f"{self.tfuncname}(" in lines[n]:
        yield n
      n+=1

  def replaceItems(self):
    list_of_finded = []
    list_of_replaced = []
    items = []
    findedLines = [x for x in self.findInLines()]
    for i in findedLines:
      items.append(self.writel()[i])
    for item in items:
      if re.search(f"{self.tfuncname}\(.+.{self.otextdomain}.+.\)", item) != None:
        list_of_finded.append(re.findall(f"{self.tfuncname}\(.+.{self.otextdomain}.+.\)", item))
      else:
        continue
    n = 0
    while n < len(list_of_finded):
      list_of_replaced.append(re.sub(f'{self.otextdomain}', self.textdomain, list_of_finded[n][0]))
      items[n] = re.sub("%s\(.+.%s.+.\)"%(self.tfuncname, self.otextdomain), list_of_replaced[n], items[n])
      n+=1
    return items, findedLines

  def replaceWithTrue(self):
    
    items, lines = self.replaceItems()
    num = 0
    rfile = self.writel()
    for i in lines:
      rfile[i] = items[num]
      num+=1
    return rfile

  # def createfolder(self):
  #   dirname = self.dirname
  #   os.popen('mkdir %s'%dirname)

  def writeOtherFile(self, replaceWithTrue):
    f = open(f'{self.path}', 'w', encoding='utf-8')
    f.writelines(replaceWithTrue)





class LaunchCrawler:
  
  def __init__(self, path, tfuncname):
    self.path = path
    self.tfuncname = tfuncname
    basename = os.path.basename(path)
    filename, ext = os.path.splitext(basename)
    if os.path.isdir(filename):
      self.dirname = f"{filename}-{random.randint(0, 999)}"
    else:
      self.dirname = filename



  def unzip_file(self):

    file = zipfile.ZipFile(self.path)
    file.extractall(self.dirname)
    
  def start(self, _textdomain, textdomain):
    path = []

    def walk():
      for roots, dirs, files in os.walk(self.dirname):
        yield roots, dirs, files

    def paths(paths=path):
      for i in paths:
        yield i.replace('\\', '/')

    for r, d, f in walk():
      for i in f:
        path.append(''.join(r+"\\"+i))
    
    for i in paths(path):
      if '.php' in i:
        if 'whats-new-pro.php' not in i:
          print(i)
          c = Crawler(i, _textdomain, textdomain, dirname=self.dirname, tfuncname=self.tfuncname)
          c.writeOtherFile(c.replaceWithTrue())

  def zip_file(self):

    dirname = self.dirname
    if os.path.isfile(f'{dirname}.zip'):
      dirname = f"{dirname}-{random.randint(0,999)}"

    def getPaths(dirname):
      for root, dirs, files in os.walk(dirname):
        for file in files:
          yield os.path.join(root, file)
    
    print(colorama.Fore.RED + "[*]" + colorama.Fore.GREEN + "Making zip file ..." + colorama.Fore.RED + "[*]" + colorama.Style.RESET_ALL)
    time.sleep(3)
    with zipfile.ZipFile(f'{dirname}.zip','w') as zipObj:
      for path in getPaths(dirname=dirname):
        zipObj.write(path)
      zipObj.close()