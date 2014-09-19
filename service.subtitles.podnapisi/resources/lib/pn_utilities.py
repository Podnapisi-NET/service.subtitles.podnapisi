# -*- coding: utf-8 -*- 

import sys
import os
import xmlrpclib
import unicodedata
import struct
from xml.dom import minidom
import urllib
import xbmc, xbmcvfs

try:
  # Python 2.6 +
  from hashlib import md5 as md5
  from hashlib import sha256
except ImportError:
  # Python 2.5 and earlier
  from md5 import md5
  from sha256 import sha256
  
__addon__      = sys.modules[ "__main__" ].__addon__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__    = sys.modules[ "__main__" ].__version__
__cwd__        = sys.modules[ "__main__" ].__cwd__
__language__   = sys.modules[ "__main__" ].__language__
__scriptid__   = sys.modules[ "__main__" ].__scriptid__

USER_AGENT = "%s_v%s" % (__scriptname__.replace(" ","_"),__version__ )

LANGUAGES      = (

    # Full Language name[0]     podnapisi[1]  ISO 639-1[2]   ISO 639-1 Code[3]   Script Setting Language[4]   localized name id number[5]

    ("Albanian"                   , "29",       "sq",            "alb",                 "0",                     30201  ),
    ("Arabic"                     , "12",       "ar",            "ara",                 "1",                     30202  ),
    ("Belarusian"                 , "0" ,       "hy",            "arm",                 "2",                     30203  ),
    ("Bosnian"                    , "10",       "bs",            "bos",                 "3",                     30204  ),
    ("Bulgarian"                  , "33",       "bg",            "bul",                 "4",                     30205  ),
    ("Catalan"                    , "53",       "ca",            "cat",                 "5",                     30206  ),
    ("Chinese"                    , "17",       "zh",            "chi",                 "6",                     30207  ),
    ("Croatian"                   , "38",       "hr",            "hrv",                 "7",                     30208  ),
    ("Czech"                      , "7",        "cs",            "cze",                 "8",                     30209  ),
    ("Danish"                     , "24",       "da",            "dan",                 "9",                     30210  ),
    ("Dutch"                      , "23",       "nl",            "dut",                 "10",                    30211  ),
    ("English"                    , "2",        "en",            "eng",                 "11",                    30212  ),
    ("Estonian"                   , "20",       "et",            "est",                 "12",                    30213  ),
    ("Persian"                    , "52",       "fa",            "per",                 "13",                    30247  ),
    ("Finnish"                    , "31",       "fi",            "fin",                 "14",                    30214  ),
    ("French"                     , "8",        "fr",            "fre",                 "15",                    30215  ),
    ("German"                     , "5",        "de",            "ger",                 "16",                    30216  ),
    ("Greek"                      , "16",       "el",            "ell",                 "17",                    30217  ),
    ("Hebrew"                     , "22",       "he",            "heb",                 "18",                    30218  ),
    ("Hindi"                      , "42",       "hi",            "hin",                 "19",                    30219  ),
    ("Hungarian"                  , "15",       "hu",            "hun",                 "20",                    30220  ),
    ("Icelandic"                  , "6",        "is",            "ice",                 "21",                    30221  ),
    ("Indonesian"                 , "0",        "id",            "ind",                 "22",                    30222  ),
    ("Italian"                    , "9",        "it",            "ita",                 "23",                    30224  ),
    ("Japanese"                   , "11",       "ja",            "jpn",                 "24",                    30225  ),
    ("Korean"                     , "4",        "ko",            "kor",                 "25",                    30226  ),
    ("Latvian"                    , "21",       "lv",            "lav",                 "26",                    30227  ),
    ("Lithuanian"                 , "0",        "lt",            "lit",                 "27",                    30228  ),
    ("Macedonian"                 , "35",       "mk",            "mac",                 "28",                    30229  ),
    ("Malay"                      , "0",        "ms",            "may",                 "29",                    30248  ),    
    ("Norwegian"                  , "3",        "no",            "nor",                 "30",                    30230  ),
    ("Polish"                     , "26",       "pl",            "pol",                 "31",                    30232  ),
    ("Portuguese"                 , "32",       "pt",            "por",                 "32",                    30233  ),
    ("PortugueseBrazil"           , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Romanian"                   , "13",       "ro",            "rum",                 "34",                    30235  ),
    ("Russian"                    , "27",       "ru",            "rus",                 "35",                    30236  ),
    ("Serbian"                    , "36",       "sr",            "scc",                 "36",                    30237  ),
    ("Slovak"                     , "37",       "sk",            "slo",                 "37",                    30238  ),
    ("Slovenian"                  , "1",        "sl",            "slv",                 "38",                    30239  ),
    ("Spanish"                    , "28",       "es",            "spa",                 "39",                    30240  ),
    ("Swedish"                    , "25",       "sv",            "swe",                 "40",                    30242  ),
    ("Thai"                       , "0",        "th",            "tha",                 "41",                    30243  ),
    ("Turkish"                    , "30",       "tr",            "tur",                 "42",                    30244  ),
    ("Ukrainian"                  , "46",       "uk",            "ukr",                 "43",                    30245  ),
    ("Vietnamese"                 , "51",       "vi",            "vie",                 "44",                    30246  ),
    ("BosnianLatin"               , "10",       "bs",            "bos",                 "100",                   30204  ),
    ("Farsi"                      , "52",       "fa",            "per",                 "13",                    30247  ),
    ("English (US)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("English (UK)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("Portuguese (Brazilian)"     , "48",       "pt-br",         "pob",                 "100",                   30234  ),
    ("Portuguese (Brazil)"        , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Portuguese-BR"              , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Brazilian"                  , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Español (Latinoamérica)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español (España)"           , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Spanish (Latin America)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español"                    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("SerbianLatin"               , "36",       "sr",            "scc",                 "100",                   30237  ),
    ("Spanish (Spain)"            , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Chinese (Traditional)"      , "17",       "zh",            "chi",                 "100",                   30207  ),
    ("Chinese (Simplified)"       , "17",       "zh",            "chi",                 "100",                   30207  ) )


def languageTranslate(lang, lang_from, lang_to):
  for x in LANGUAGES:
    if lang == x[lang_from] :
      return x[lang_to]

def log(module, msg):
  xbmc.log((u"### [%s] - %s" % (module,msg,)).encode('utf-8'),level=xbmc.LOGDEBUG ) 

def compare_columns(b,a):
  return cmp( b["language_name"], a["language_name"] )  or cmp( a["sync"], b["sync"] ) 

def normalizeString(str):
  return unicodedata.normalize(
         'NFKD', unicode(unicode(str, 'utf-8'))
         ).encode('ascii','ignore')

def OpensubtitlesHash(file_path, rar=False):
    if rar:
      return OpensubtitlesHashRar(file_path)
      
    log( __scriptid__,"Hash Standard file")  
    longlongformat = 'q'  # long long
    bytesize = struct.calcsize(longlongformat)
    
    f = xbmcvfs.File(file_path)
    filesize = f.size()
    hash = filesize
    
    if filesize < 65536 * 2:
        return "SizeError"
    
    buffer = f.read(65536)
    f.seek(max(0,filesize-65536),0)
    buffer += f.read(65536)
    f.close()
    for x in range((65536/bytesize)*2):
        size = x*bytesize
        (l_value,)= struct.unpack(longlongformat, buffer[size:size+bytesize])
        hash += l_value
        hash = hash & 0xFFFFFFFFFFFFFFFF
    
    returnHash = "%016x" % hash
    return returnHash

def OpensubtitlesHashRar(firsrarfile):
    log( __name__,"Hash Rar file")
    f = xbmcvfs.File(firsrarfile)
    a=f.read(4)
    if a!='Rar!':
        raise Exception('ERROR: This is not rar file.')
    seek=0
    for i in range(4):
        f.seek(max(0,seek),0)
        a=f.read(100)        
        type,flag,size=struct.unpack( '<BHH', a[2:2+5]) 
        if 0x74==type:
            if 0x30!=struct.unpack( '<B', a[25:25+1])[0]:
                raise Exception('Bad compression method! Work only for "store".')            
            s_partiizebodystart=seek+size
            s_partiizebody,s_unpacksize=struct.unpack( '<II', a[7:7+2*4])
            if (flag & 0x0100):
                s_unpacksize=(struct.unpack( '<I', a[36:36+4])[0] <<32 )+s_unpacksize
                log( __name__ , 'Hash untested for files biger that 2gb. May work or may generate bad hash.')
            lastrarfile=getlastsplit(firsrarfile,(s_unpacksize-1)/s_partiizebody)
            hash=addfilehash(firsrarfile,s_unpacksize,s_partiizebodystart)
            hash=addfilehash(lastrarfile,hash,(s_unpacksize%s_partiizebody)+s_partiizebodystart-65536)
            f.close()
            return (s_unpacksize,"%016x" % hash )
        seek+=size
    raise Exception('ERROR: Not Body part in rar file.')


class OSDBServer:
  
  def create(self):
    self.subtitles_list = []
    self.connected = False
    self.pod_session = None
    self.podserver   = xmlrpclib.Server('http://ssp.podnapisi.net:8000')      
    init        = self.podserver.initiate(USER_AGENT)
    hash        = md5()
    hash.update(__addon__.getSetting( "PNpass" ))
    self.password = sha256(str(hash.hexdigest()) + str(init['nonce'])).hexdigest()
    self.user     = __addon__.getSetting( "PNuser" )
    if init['status'] == 200:
      self.pod_session = init['session']
      self.connected   = self.login()
      if (self.connected):
        log( __scriptid__ ,"Connected to Podnapisi server")


  def mergesubtitles( self, stack ):
    if( len ( self.subtitles_list ) > 0 ):
      self.subtitles_list = sorted(self.subtitles_list, compare_columns)

  def searchsubtitles_pod( self, movie_hash, lang , stack):
    # movie_hash = "e1b45885346cfa0b" # Matrix Hash, Debug only
    try:
      if (self.connected):
        self.podserver.setFilters(self.pod_session, True, lang , False)
        search = self.podserver.search(self.pod_session , [str(movie_hash)])
        if search['status'] == 200 and len(search['results']) > 0 :
          search_item = search["results"][movie_hash]
          for item in search_item["subtitles"]:
            if item["lang"]:
              flag_image = item["lang"]
            else:                                                           
              flag_image = "-"
            if item['release'] == "":
              episode = search_item["tvEpisode"]
              if str(episode) == "0":
                name = "%s (%s)" % (str(search_item["movieTitle"]),str(search_item["movieYear"]),)
              else:
                name = "%s S(%s)E(%s)" % (str(search_item["movieTitle"]),str(search_item["tvSeason"]), str(episode), )
            else:
              name = item['release']

            details = search['results'][movie_hash]
            self.subtitles_list.append({'filename'      : name,
                                        'link'          : str(item["id"]),
                                        'movie_id'      : str(details["movieId"]),
                                        'season'        : str(details["tvSeason"]),
                                        'episode'       : str(details["tvEpisode"]),     
                                        'language_name' : languageTranslate((item["lang"]),2,0),
                                        'language_flag' : flag_image,
                                        'rating'        : str(int(item['rating'])*2),
                                        'sync'          : not item["inexact"],
                                        'hearing_imp'   : "n" in item['flags']
                                        })

          self.mergesubtitles(stack)
      return self.subtitles_list
    except :
      return self.subtitles_list

  def searchsubtitlesbyname_pod( self, name, tvshow, season, episode, lang, year, stack ):
    if len(tvshow) > 1:
      name = tvshow
    
    url = "http://www.podnapisi.net/ppodnapisi/search?tbsl=1&sK=%s&sJ=%s&sY=%s&sTS=%s&sTE=%s&sXML=1&lang=0" % (name.replace(" ","+"), ','.join(lang), str(year), str(season), str(episode))
    log( __scriptid__ ,"Search URL - %s" % (url))
    
    subtitles = self.fetch(url)
         
    try:
      if subtitles:
        for subtitle in subtitles:
          filename    = self.get_element(subtitle, "release")

          if filename == "":
            filename = self.get_element(subtitle, "title")

          self.subtitles_list.append({'filename'      : filename,
                                      'link'          : self.get_element(subtitle, "id"),
                                      'movie_id'      : self.get_element(subtitle, "movieId"),
                                      'season'        : self.get_element(subtitle, "tvSeason"),
                                      'episode'       : self.get_element(subtitle, "tvEpisode"),
                                      'language_name' : languageTranslate(self.get_element(subtitle, "languageId"),1,0),
                                      'language_flag' : languageTranslate(self.get_element(subtitle, "languageId"),1,2),
                                      'rating'        : str(int(self.get_element(subtitle, "rating"))*2),
                                      'sync'          : False,
                                      'hearing_imp'   : "n" in self.get_element(subtitle, "flags")
                                      })
        self.mergesubtitles(stack)
      return self.subtitles_list
    except :
      return self.subtitles_list
  
  def download(self,id,movie_id, season, episode, hash):
    if (self.connected):
      id_pod =[]
      id_pod.append(str(id))
      if (__addon__.getSetting("PNmatch") == 'true'):
        log( __scriptid__ ,"Sending match to Podnapisi server")
        result = self.podserver.match(self.pod_session, hash, int(movie_id), int(season), int(episode), "")
        if result['status'] == 200:
          log( __scriptid__ ,"Match successfuly sent")

      download = self.podserver.download(self.pod_session , id_pod)
      if str(download['status']) == "200" and len(download['names']) > 0 :
        download_item = download["names"][0]
        if str(download["names"][0]['id']) == str(id):
          return "http://www.podnapisi.net/static/podnapisi/%s" % download["names"][0]['filename']
          
    return None  
 
  def login(self):
    auth = self.podserver.authenticate(self.pod_session, self.user, self.password)
    if auth['status'] == 300: 
      log( __scriptid__ ,__language__(32005))
      xbmc.executebuiltin(u'Notification(%s,%s,5000,%s)' %(__scriptname__,
                                                           __language__(32005),
                                                           os.path.join(__cwd__,"icon.png")
                                                          )
                          )
      return False  
    return True

  def get_element(self, element, tag):
    if element.getElementsByTagName(tag)[0].firstChild:
      return element.getElementsByTagName(tag)[0].firstChild.data
    else:
      return ""  

  def fetch(self,url):
    socket = urllib.urlopen( url )
    result = socket.read()
    socket.close()
    xmldoc = minidom.parseString(result)
    return xmldoc.getElementsByTagName("subtitle")    
