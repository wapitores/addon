# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TvWin - Kodi Addon 



import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools,scrapertools
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,random  # PDF Reader
h = HTMLParser.HTMLParser()

from resources.tools.resolvers import *
from resources.tools.pelisyseries import *
from resources.tools.seriesretro import *
from resources.tools.vk import *
from framescrape import *
from resources.tools.spruto import *
from resources.tools.verpelis import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
                                     
home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/art', ''))




icon = art + 'icon.png'
fanart = 'fanart.jpg'

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
OTHER = "other"


def run():
    plugintools.log('[%s %s] Initializing... ' % (addonName, addonVersion))
    plugintools.set_view(THUMBNAIL)

    
    params = plugintools.get_params()

    if params.get("action") is None:
        main_list(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec action+"(params)"

    if not os.path.exists(playlists) :
        os.makedirs(playlists)

    plugintools.close_item_list()





def main_list(params):
    plugintools.log('[%s %s].main_list %s' % (addonName, addonVersion, repr(params)))

    
    mastermenu = xml_skin()
    plugintools.log("XML menu: "+mastermenu)
    try:
        data = plugintools.read(mastermenu)
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('TvWin', "Sin acceso a internet...", 4 , art+'icon.png'))
        mastermenu = 'http'+'://pas'+'teb'+'in.com'+'/raw'+'.php'+'?'+'i=RY'+'iw'+'aj'+'0q'
        data = plugintools.read(mastermenu)

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        plugintools.add_item( action="" , title = title + date , fanart = fanart , thumbnail=thumbnail , folder = False , isPlayable = False )

    data = plugintools.read(mastermenu)
    matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        last_update = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
        url = plugintools.find_single_match(entry,'<url>(.*?)</url>')
        date = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')

        
        pekes_no = plugintools.get_setting("pekes_no")
        if pekes_no == "true" :
            print "Control paternal en marcha"
            if title.find("Adultos") >= 0 :
                plugintools.log("Activando control paternal...")
            else:
                fixed = title
                plugintools.log("fixed= "+fixed)
                if fixed == "":
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
                elif fixed == '':
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
                elif fixed == '':
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = False , isPlayable = False )                    
                else:
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
        else:
            fixed = title
            if fixed == "":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            elif fixed == "":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            else:
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )




	
def play(params):    
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    plugintools.play_resolved_url(url)


    

def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')




def simpletv_items(params):
    plugintools.log('[%s %s].simpletv_items ' % (addonName, addonVersion))

    saving_url = 0  
    datamovie = {}  
    follower = 0

    show = "thumbnail"
    params["show"]=show
    
   
    thumbnail = params.get("thumbnail")
   
    if thumbnail == "" :
        thumbnail = art + ''

    fanart = params.get("extra")
    if fanart == " " :
        fanart = params.get("fanart")
        if fanart == " " :
            fanart = art + 'fanart.png'
        
    title = params.get("plot")
    texto= params.get("texto")
    busqueda = ""
    if title == 'search':
        title = title + '.txt'
        
    else:
        title = title + ''

    if title == 'search.txt':
        busqueda = 'search.txt'
        filename = title
        file = open(tmp + 'search.txt', "r")
        file.seek(0)
        data = file.readline()
        if data == "":
            ok = plugintools.message("TvWin", "Sin resultados")
            return ok
    else:
        title = params.get("title")
        title = parser_title(title)
        ext = params.get("ext")
        title_plot = params.get("plot")
        if title_plot == "":
            filename = title + "." + ext

        if ext is None:
            filename = title
        else:
            #plugintools.log("ext= "+ext)
            filename = title + "." + ext
            
        file = open(playlists + filename, "r")
        file.seek(0)
        data = file.readline().strip()
        
             
            
    if data == "":
        print "No es posible leer el archivo!"
        data = file.readline()
        #plugintools.log("data= "+data)
    else:
        file.seek(0)
        num_items = len(file.readlines())
        print num_items
        #plugintools.log("filename= "+filename)
        plugintools.add_item(action="" , title = ''+ filename + '' , url = playlists + title , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = False)
            
       
    plot = "."   # Control canal sin EPG (plot is null)
    file.seek(0)
    data = file.readline()
    i = -1
    while i <= num_items:
        if data.startswith("#EXTINF:-1") == True:
            title = data.replace("#EXTINF:-1", "")
            title = title.replace(",", "")
            title = title.replace("-AZBOX *", "")
            title = title.replace("-AZBOX-*", "")
            
           
                
                

            
            if busqueda == 'search.txt':
                title_search = title.split('"')
                print 'title',title
                titulo = title_search[0]
                titulo = titulo.strip()
                origen = title_search[1]
                origen = origen.strip()
                data = file.readline()
                i = i + 1      
            else:
                images = m3u_items(title)
                print 'images',images
                
                thumbnail = images[0]
                fanart = images[1]
                cat = images[2]
                title = images[3]
                
                
                
               
                
                origen = title.split(",")                
                title = title.strip()
               # plugintools.log("title= "+title)
                data = file.readline()
                i = i + 1

            if title.startswith("#") == True:  # Control para comentarios
                title = title.replace("#", "")
                #plugintools.log("desc= "+data)                
                if data.startswith("desc") == True:
                    plot = data.replace("desc=", "").replace('"',"")
                    plugintools.add_item(action="", title = title , url = "", plot = plot , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
                else:                    
                    plugintools.add_item(action="", title = title , url = "", thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
                data = file.readline()
                i = i + 1
                continue                

          
                    
                    
                        
            # Control para determinadas listas de decos sat
            if title.startswith(' $ExtFilter="') == True:
                if busqueda == 'search.txt':
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    data = file.readline()
                    i = i + 1                    
                else:
                    title = title.replace('$ExtFilter="', "")
                    category = title.split('"')
                    tipo = category[0]
                    tipo = tipo.strip()
                    title = category[1]
                    title = title.strip()
                    print title
                    data = file.readline()
                    i = i + 1
              
            if data != "":
                title = title.replace("radio=true", "")
                url = data.strip()
                if url == "#multilink":
                    # Control para info de canal o sinopsis de película
                    #data = file.readline()
                    plugintools.log("linea= "+data)
                    if data.startswith("desc") == True:                        
                        plot = data.replace("desc=", "").replace('"',"")
                        plugintools.log("sinopsis= "+data)
                    if cat == "":
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = title +  origen , show = show , page = show , url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )                            
                            plot = ""
                        else:
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = title , url = url ,  thumbnail = thumbnail, info_labels = datamovie , show = show , page = show , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_multilink(url, filename)
                                while url != "":
                                    url = file.readline().strip()
                                    plugintools.log("URL= "+url)
                                    save_multilink(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""
                    else:                        
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = cat + title + origen  , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show , fanart = fanart , folder = False , isPlayable = True )                           
                            plot = ""
                        else:
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = '[COLOR red][I]' + cat + title  , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                save_multilink(url, filename)
                                while url != "":
                                    url = file.readline().strip()
                                    save_multilink(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""

                elif url == "#multiparser":
                    # Control para info de canal o sinopsis de película
                    data = file.readline()
                    plugintools.log("linea= "+data)
                    if data.startswith("desc") == True:                        
                        plot = data.replace("desc=", "").replace('"',"")
                        plugintools.log("sinopsis= "+data)
                    if cat == "":
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multiparser][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', show = show , page = show , url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            plot = ""
                        else:
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multiparser][/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie , show = show , page = show , fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                while url != "":
                                    url = file.readline().strip()
                                    save_url(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""
                    else:                        
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multiparser][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]' , url = url , info_labels = datamovie , page = show , thumbnail = thumbnail, show = show, fanart = fanart , folder = True , isPlayable = False )                           
                            plot = ""
                        else:
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multiparser][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show, fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                save_url(url, filename)
                                saving_url = 0                            
                            plot = ""

                elif url.startswith("img") == True:
                    url = data.strip()
                    plugintools.add_item( action = "show_image" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white] ' + title + ' [COLOR lightyellow][IMG][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show, fanart = fanart , folder = False , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue                                       
                            
                elif url.startswith("serie") == True:
                    url = data.strip()
                    if cat == "":
                        if busqueda == 'search.txt':                            
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            if url.find("") >= 0:
                                plugintools.add_item( action = "" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]adicto][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("") >= 0:
                                plugintools.add_item( action = "" , title =  + title +  origen , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("") >= 0:
                                plugintools.add_item( action = "" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Yonkis][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("pastebin.com") >= 0:
                                plugintools.add_item( action = "" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Blanco][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("") >= 0:
                                plugintools.add_item( action = "" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B].Mu][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                              
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            if url.find("http://youanimehd.com") >= 0:
                                plugintools.add_item( action = "pelisya" , title = title , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("") >= 0:
                                plugintools.add_item( action = "" , title =  title  , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("") >= 0:
                                plugintools.add_item( action = "url_play12" , title =  title , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("pastebin.com") >= 0:
                                plugintools.add_item( action = "seriesblanco0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Blanco][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("") >= 0:
                                plugintools.add_item( action = "url_play13" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B].Mu][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                               
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + title + ' [COLOR purple][Serie online][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = cat , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                

                                     

                elif url.startswith("short") == True:
                    if busqueda == 'search.txt':
                        url = url.replace("short:", "").strip()
                        plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = url.replace("short:", "").strip()
                        plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue

                elif data.startswith("http") == True:
                    url = data.strip()
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                         

                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                plugintools.log("linea titulo= "+title_search)
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
                                url = url.strip()
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [[COLOR red]You[COLOR white]tube Video][I] (' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , fanart=fanart, show = show, thumbnail=thumbnail, url=url , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , show = show, fanart = fanart, isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue        

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "play" , title = title + '[COLOR purple][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("torrent") == True:  # Archivos torrents
                                # plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title   
                                title_fixed = title.replace(" ", "+").strip()
                                url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed                                
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR gold] [Torrent][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue   
                            
                            else:
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "play" , title = title , info_labels = datamovie , plot = datamovie["Plot"], url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            


                            elif url.find("movshare") >= 0:                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Movshare][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Movreel][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Videobam][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue                               
   
                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                title = title.split('"')
                                title = title[0]
                                title =title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")                                
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [[COLOR red]You[COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                                
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title='[COLOR red][I]'+cat+' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]', url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title='[COLOR red][I]' + cat + ' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]', url=url , thumbnail = thumbnail , show = show, fanart= fanart , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue  

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = title , url = url , plot = plot , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR gold] [CBZ][/COLOR]', url = url , plot = datamovie["Plot"] , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR gold] [CBR][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue 

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR green] [shortlink][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue
		

                            elif url.endswith("http://xtv-arxk.rhcloud.com/live_stalker/") == True:
                                  
                                title_fixed = title.replace(" ", "+").strip()
                                url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed                                
                                plugintools.add_item( action = "nariz" , title = '[COLOR blue][I]' + cat + ' / [/I][/COLOR]' + title  , url = url , plot = "", info_labels = "" , extra = "" , show = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            #channel
                            else:
                                plugintools.add_item( action = "xtvexpant" , title = '[COLOR blue][I]' + cat + ' / [/I][/COLOR]' + title  , url = url , plot = "", info_labels = "" , extra = "" , show = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )                                
                                data = file.readline()
                                i = i + 1
                                continue
                            
                    # Sin categoría de canales   
                    else:
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.log("fanart= "+fanart)
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("goear") == True:
                                params["fanart"] = fanart
                                if show == "list":
                                    show = plugintools.get_setting("music_id")
                                    plugintools.log("show en config")
                                data = file.readline()
                                if data.startswith("desc") == True:
                                    datamovie["Plot"] = data.replace("desc=", "").replace('"',"")                                    
                                plugintools.add_item( action = "goear" , plot = plot , title = '[COLOR white]' + title + ' [COLOR blue][goear][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , info_labels = datamovie , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()                                    
                                i = i + 1
                                continue
                                                        
                            elif url.find("allmyvideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )                                                      
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + titulo + '[COLOR lightskyblue] [Streamcloud][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                        
                            
                            elif url.find("vidspot") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + '[COLOR palegreen] [Vidspot][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("played.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + '[COLOR lavender] [Played.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + '[COLOR royalblue] [Vk][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi.tv") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veehd") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR orange] [VeeHD][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [streamin.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("powvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR orange] [powvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("mail.ru") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR orange] [Mail.ru][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR orange] [Novamov][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR orange] [Moevideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                             

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.add_item( action = "youtube_videos" , title = '[COLOR white][' + title + ' [[COLOR red]You[/COLOR][COLOR white]tube Video][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'                               
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , show = show, thumbnail = thumbnail , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue                             
                            
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = title + ' [COLOR purple][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBZ][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBR][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("mediafire") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][Mediafire][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("torrent") == True:
                                # plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title   
                                title_fixed = title.replace(" ", "+").strip()
                                url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR gold] [Torrent][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue                             
                            
                            else:                      
                                title = title_search[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "play" , title = title + ' [COLOR blue][HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue

                        else:
                            if url.find("allmyvideos") >= 0:
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + ' [COLOR lightyellow][Allmyvideos][/COLOR]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + title + ' [COLOR lightskyblue][Streamcloud][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidspot") >= 0:                            
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("played.to") >= 0:                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + ' [COLOR lavender][Played.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:                            
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + ' [COLOR royalblue][Vk][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi.tv") >= 0:                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("VeeHD") >= 0:                            
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR forestgreen] [VeeHD][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR forestgreen] [streamin.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("powvideo") >= 0:                            
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR forestgreen] [powvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("mail.ru") >= 0:                            
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Mail.ru][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:                            
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Novamov][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("gamovideo") >= 0:                            
                                plugintools.add_item( action = "gamovideo" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Gamovideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:                            
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Moevideos][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movshare") >= 0:                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Movshare][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Movreel][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Videobam][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                             

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?v=", "")
                                print 'videoid',videoid
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.add_item( action = "youtube_videos" , title = '[COLOR white]' + title + ' [[COLOR red]You[/COLOR][COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    thumbnail=art+'/lnh_logo.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    #plugintools.log("url= "+url)
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    #plugintools.log("url= "+url)
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , show = show, fanart = fanart , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue
                            

                            elif url.find("http://xtv") >= 0:
                                plugintools.add_item( action = "xtvexpant" , title = title , plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("http://rtvmotel") >= 0:
                                plugintools.add_item( action = "xtvexpant" , title = title , plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("http://wcm777") >= 0:
                                plugintools.add_item( action = "xtvexpant" , title = title , plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = title , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + '[/I][/COLOR][COLOR white]' + title + '[/COLOR]' , plot = plot , url = url , extra = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue
              
                if data.startswith("rtmp") == True or data.startswith("rtsp") == True:
                    url = data
                    url = parse_url(url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)                      
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")                            
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '' + server + '' + origen + '', url = params.get("url") , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            params["server"] = server
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)                         
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            plugintools.log("fanart= "+fanart)
                            url = params.get("url")                            
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR blue][' + cat + '[/COLOR] ' + title  , plot = plot , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)                        
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '[COLOR green] [' + server + '][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)                         
                            server = params.get("server")
                            plugintools.log("fanart= "+fanart)
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")                            
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + title + ''+ server + '[/COLOR]' , plot = plot , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            print url
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("udp") == True or data.startswith("rtp") == True:
                    # print "udp"
                    url = data
                    url = parse_url(url)
                    plugintools.log("url retornada= "+url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [UDP][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [UDP][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("mms") == True or data.startswith("rtp") == True:
                    # print "udp"
                    url = data
                    url = parse_url(url)
                    plugintools.log("url retornada= "+url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [MMS][/COLOR]' , plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:                            
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [MMS][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                      

                if data.startswith("plugin") == True:
                    title = title.split('"')
                    title = title[0]
                    title = title.strip()
                    title = title.replace("#EXTINF:-1,", "")
                    url = data
                    url = url.strip()
                    if url.startswith("plugin") == True:
                        if url.find("plugin.video.f4mTester") >= 0:
                            if cat != "":
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                            else:
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue

                    elif url.startswith("plugin://plugin.video.live.streamspro/") == True :
                        if cat != "":                      
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Livestreams][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Livestreams][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [Livestreams][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [Livestreams][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                    elif url.find("plugin.video.youtube") >= 0 :
                        if cat != "":                      
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                            
                        
                    elif url.find("mode=1") >= 0 :
                        if cat != "":
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue] [Acestream][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightblue] [Acestream][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR lightblue] [Acestream][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                            
                        
                    elif url.find("mode=2") >= 0 :
                        if cat != "":
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = + cat  + title + '[COLOR darkorange] [Sopcast][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + ' [COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                elif data.startswith("magnet") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            url = urllib.quote_plus(data)
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orangered] [Torrent][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            data = data.strip()
                            url = urllib.quote_plus(data).strip()                      
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            url = urllib.quote_plus(data)
                            url = launch_torrent(url)
                            title = parser_title(title)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orangered] [Torrent][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            data = data.strip()
                            url = urllib.quote_plus(data)
                            url = launch_torrent(url)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                elif data.startswith("torrent") == True:  # Torrent file (URL)
                    url = data.replace("torrent:", "").strip()
                    if cat != "":
                        if busqueda == 'search.txt':
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orangered] [Torrent file][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            data = data.strip()
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orangered][Torrent file][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':                            
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orangered] [Torrent file][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            data = data.strip()                            
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR orangered][Torrent file][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                        
                        
                elif data.startswith("sop") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            url = url.strip()
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR darkorange][Sopcast][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR darkorange][Sopcast][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                        

                elif data.startswith("ace") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title = parser_title(title)
                            title = title.strip()
                            title_fixed = title.replace(" ", "+")
                            url = data.replace("ace:", "")
                            url = url.strip()
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name=' + title_fixed
                            plugintools.add_item(action="play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue][Acestream][/COLOR] [COLOR lightblue][I](' + origen + ')[/COLOR][/I]' , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            print 'data',data
                            url = data.replace("ace:", "")
                            url = url.strip()
                            print 'url',url
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                            plugintools.add_item(action="play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue][Acestream][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title = parser_title(title)
                            url = data.replace("ace:", "")
                            url = url.strip()
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR] [COLOR lightblue][I](' + origen + ')[/COLOR][/I]' , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            print 'data',data
                            url = data.replace("ace:", "")
                            url = url.strip()
                            print 'url',url
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='                            
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue                        
                
                # Youtube playlist & channel    
                elif data.startswith("yt") == True:
                    if data.startswith("yt_playlist") == True:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            youtube_playlist = data.replace("yt_playlist(", "")
                            youtube_playlist = youtube_playlist.replace(")", "")
                            plugintools.log("youtube_playlist= "+youtube_playlist)
                            url = 'https://www.youtube.com/playlist?list='+youtube_playlist
                            plugintools.add_item( action = "yt_playlist" , title = title , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            plugintools.log("title= "+title)
                            youtube_playlist = data.replace("yt_playlist(", "")
                            youtube_playlist = youtube_playlist.replace(")", "")
                            plugintools.log("youtube_playlist= "+youtube_playlist)                    
                            url = 'https://www.youtube.com/playlist?list='+youtube_playlist                            
                            plugintools.add_item( action = "yt_playlist" , title =  title, url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue                   

                    elif data.startswith("yt_channel") == True:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            youtube_channel = data.replace("yt_channel(", "")
                            youtube_channel = youtube_channel.replace(")", "")
                            plugintools.log("youtube_user= "+youtube_channel)
                            url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                            plugintools.add_item( action = "youtube_playlists" , title = '[[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Channel][/COLOR] [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            plugintools.log("title= "+title)
                            youtube_channel = data.replace("yt_channel(", "")
                            youtube_channel = youtube_channel.replace(")", "")
                            youtube_channel = youtube_channel.strip()                 
                            url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                            plugintools.log("url= "+url)                            
                            plugintools.add_item( action = "youtube_playlists" , title = '[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Channel][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        
                elif data.startswith("m3u") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("m3u:", "")
                        data = file.readline()
                        if data.startswith("desc=") == True:
                            plot = data.replace("desc=", "")                            
                        else:
                            plot = ""
                        plugintools.add_item( action = "getfile_http" , title = title + ' [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = data.replace("m3u:", "")
                        data = file.readline()
                        if data.startswith("desc=") == True:
                            data = data.replace("desc=", "")
                            data = data.replace('"', "")
                            datamovie = {}
                            datamovie["Plot"] = data
                            #plugintools.log("SHOW= "+show)
                            if plugintools.get_setting("nolabel") == "true":
                                plugintools.add_item( action = "getfile_http" , title = title, info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "getfile_http" , title = title , info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                           # plugintools.log("SHOW= "+show)
                            if plugintools.get_setting("nolabel") == "true":
                                plugintools.add_item( action = "getfile_http" , title = title, url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "getfile_http" , title = title , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )                                                
                            i = i + 1
                            continue


                elif data.startswith("plx") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + ' [I][/COLOR][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)                        
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + '', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue

                elif data.startswith("goear") == True:
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "goear" , title = title + ' [I][/COLOR][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, extra = show , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        data = file.readline()
                        if show == "list":
                            show = plugintools.get_setting("music_id")
                            #plugintools.log("show en config")                        
                        if data.startswith("desc") == True:
                            datamovie["Plot"] = data.replace("desc=", "").replace('"',"").strip()                            
                        plugintools.add_item( action = "goear" , plot = plot , title = title + ' [COLOR blue][goear][/COLOR]', url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , show = show, extra = show , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue                    
                    
                
            else:
                data = file.readline()
                i = i + 1
                continue

        else:
            data = file.readline()
            i = i + 1
            
    
    file.close()
    plugintools.modo_vista(show)
    if title == 'search.txt':
            os.remove(tmp + title)

    plugintools.log("follower= "+str(follower))
    if follower == 1:
        if os.path.isfile(playlists + filename):
            os.remove(playlists + filename)
            print "Borrado correcto!"
        else:
            pass              



def myplaylists_m3u(params):  # Mis listas M3U
    plugintools.log('[%s %s].myplaylists_m3u %s' % (addonName, addonVersion, repr(params)))
    thumbnail = params.get("thumbnail")
    #plugintools.add_item(action="play" , title = "[COLOR lightyellow]Cómo importar listas M3U a mi biblioteca [/COLOR][COLOR lightblue][I][Youtube][/I][/COLOR]" , thumbnail = art + "icon.png" , url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=8i0KouM-4-U" , folder = False , isPlayable = True )
    plugintools.add_item(action="my_albums" , title = "[COLOR gold][B]Mis álbumes[/B][/COLOR][COLOR lightblue][I] (CBR/CBZ)[/I][/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
    plugintools.add_item(action="search_channel" , title = "[COLOR lightyellow]Buscador[/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

    # Agregamos listas online privadas del usuario
    add_playlist(params)

    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")

    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.log("entry= "+entry)

        if pekes_no == "true" :
            print "Control paternal en marcha"
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")

            else:
                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = entry , url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

        else:

                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = entry, url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )





def playlists_m3u(params):  # Biblioteca online
    plugintools.log('[%s %s].playlists_m3u %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = ''
    params["ext"] = 'TvWin'
    plugintools.add_item( action="" , title=''+name_channel+'' , thumbnail = art + 'icon.png' , folder = False , isPlayable = False )
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    # Sustituir por una lista!!!
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Television calidad estandar xtv":
            plugintools.add_item( action="xtv" , plot = ciny , title = ciny + " " +'[COLOR green]['+ xtv_user +'][/COLOR]' , url= dixy + xtv_user + '&k=' + xtv_pwd , thumbnail = winy , fanart = art + 'x.jpeg' , folder = True , isPlayable = False )
            params["ext"] = "TvWin"
            title = ciny
            params["title"]=title
        elif ciny == "Television calidad estandar rtv":
            plugintools.add_item( action="rtv" , plot = ciny , title = ciny , url= dixy + '&AUTH=' + rtv_pwd , thumbnail = winy , fanart = art + 'r.jpg' , folder = True , isPlayable = False )
            title = ciny
        elif ciny == "Television calidad alta xtv":
            plugintools.add_item( action="xtv" , plot = ciny , title = ciny + " " +'[COLOR green]['+ xtv_user + '][/COLOR]'  , url= dixy  + xtv_user + '&k=' + xtv_pwd , thumbnail = winy , fanart = art + 'x.jpeg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television calidad alta rtv":
            plugintools.add_item( action="rtv" , plot = ciny , title = ciny , url= dixy  + '&AUTH=' + rtv_pwd , thumbnail = winy , fanart = art + 'r.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television calidad media xtv":
            plugintools.add_item( action="xtv" , plot = ciny , title = ciny + " " +'[COLOR green]['+ xtv_user + '][/COLOR]'  , url= dixy  + xtv_user + '&k=' + xtv_pwd , thumbnail = winy , fanart = art + 'x.jpeg', folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television calidad media rtv":
            plugintools.add_item( action="rtv" , plot = ciny , title = ciny , url= dixy  + '&AUTH=' + rtv_pwd , thumbnail = winy , fanart = art + 'r.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television calidad baja xtv":
            plugintools.add_item( action="xtv" , plot = ciny , title = ciny + " " +'[COLOR green]['+ xtv_user + '][/COLOR]'  , url= dixy  + xtv_user + '&k=' + xtv_pwd , thumbnail = winy , fanart = art + 'x.jpeg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television calidad baja rtv":
            plugintools.add_item( action="rtv" , plot = ciny , title = ciny , url= dixy  + '&AUTH=' + rtv_pwd , thumbnail = winy , fanart = art + 'r.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television Stalker xtv":
            plugintools.add_item( action="xtv" , plot = ciny , title = ciny + " " +'[COLOR green]['+ xtv_user + '][/COLOR]'  , url= dixy  + xtv_user + '&k=' + xtv_pwd , thumbnail = winy , fanart = art + 'x.jpeg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television stalker adultos xtv":
            plugintools.add_item( action="xtv" , plot = ciny , title = ciny + " " +'[COLOR green]['+ xtv_user + '][/COLOR]'  , url= dixy  + xtv_user + '&k=' + xtv_pwd , thumbnail = winy , fanart = art + 'x.jpeg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television Stalker rtv":
            plugintools.add_item( action="rtv" , plot = ciny , title = ciny , url = dixy  + '?AUTH=' + rtv_pwd , thumbnail = winy , fanart = art + 'r.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Television internacional en contruccion":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = ciny , url= dixy , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "":
            plugintools.add_item( action="url_play12" , plot = ciny , title = ciny , url= dixy , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Series":
            plugintools.add_item( action="seriecatcher" , plot = ciny , title =  ciny , url= dixy + id_token , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Peliculas":
            plugintools.add_item( action="url_play12" , plot = ciny , title = ciny , url= dixy + id_token , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Peliculas xxx":
            plugintools.add_item( action="url_play12" , plot = ciny , title = ciny  , url= dixy + id_token , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Series Cartoon Retro":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = ciny  , url= dixy , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Ver pelis en desarrolo":
            plugintools.add_item( action="verpelis" , plot = ciny , title = ciny  , url= dixy , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "Mi Tv online":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = ciny  , url = dixy + id_pastebin , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        else:
            plot = ciny.split("[")
            plot = plot[0]
            plugintools.add_item( action="getfile_http" , plot = plot , title = ciny , url= dixy , thumbnail = winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

    plugintools.log('[%s %s].playlists_m3u %s' % (addonName, addonVersion, repr(params)))    



def getfile_http(params):
    plugintools.log('[%s %s].getfile_http ' % (addonName, addonVersion))
    
    url = params.get("url")
    params["ext"] = "m3u"
    getfile_url(params)
    simpletv_items(params)

def xtv(params):
  xtvmaster = plugintools.get_setting("xtvmaster")
  if xtvmaster == 'false':
   xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Tvwin', "Accede Primero......", 1 , art+'b.png'))
   open_settings(params)
  if xtvmaster == 'true':
   getfile_http(params)
 
def rtv(params):
  rtvmaster = plugintools.get_setting("rtvmaster")
  if rtvmaster == 'false':
   xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Tvwin', "Sin clave de autorizacion.....", 1 , art+'b.png'))
   open_settings(params)
  if rtvmaster == 'true':
   getfile_http(params)



def getfile_url(params):
    plugintools.log('[%s %s].getfile_url ' % (addonName, addonVersion))
    ext = params.get("ext")
    title = params.get("title")

    if ext == 'plx':
        filename = parser_title(title)
        params["plot"]=filename
        filename = title + ".plx" 
    elif ext == 'm3u':
        filename = params.get("plot")
        
        filename = parser_title(title)
        filename = filename + ".m3u" 
    else:
        ext == 'p2p'
        filename = parser_title(title)
        filename = filename + ".p2p"  

    if filename.endswith("plx") == True :
        filename = parser_title(filename)

    plugintools.log("filename= "+filename)
    url = params.get("url")
    
    try:
        response = urllib2.urlopen(url)
        body = response.read()
    except:
        # Control si la lista está en el cuerpo del HTTP
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)

    #open the file for writing
    fh = open(playlists + filename, "wb")

    # read from request while writing to file
    fh.write(body)

    fh.close()

    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    data = data.strip()

    lista_items = {'linea': data}
    file.seek(0)
    lista_items = {'plot': data}
    file.seek(0)



























def parser_title(title):
    plugintools.log('[%s %s].parser_title %s' % (addonName, addonVersion, title))

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")

    cyd = cyd.replace("&quot;", '"')

    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Parser]", "")
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")
    cyd = cyd.replace(" [Multiparser]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]PLX[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]M3U[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]", "")
    cyd = cyd.replace(' [COLOR gold][CBZ][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][CBR][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][Mediafire][/COLOR]', "")
    cyd = cyd.replace(' [CBZ]', "")
    cyd = cyd.replace(' [CBR]', "")
    cyd = cyd.replace(' [Mediafire]', "")

    # Control para evitar errores al crear archivos
    cyd = cyd.replace("[", "")
    cyd = cyd.replace("]", "")
    #cyd = cyd.replace(".", "")
    
    title = cyd
    title = title.strip()
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")

    plugintools.log("title_parsed= "+title)
    return title

def xtvexpant(params):
    plugintools.log('[%s %s].xtvexpant %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    url_getlink = 'http://wheredoesthislinkgo.com'
    plugintools.log("url_getlink= "+url_getlink)
    post = 'ShortenedUri=' + url
    post = post.replace('&', "%26")
    plugintools.log("post= "+post)
    data,response_headers = plugintools.read_body_and_headers(url_getlink, post=post)
    longurl = plugintools.find_single_match(data, 'expands to <a href="(.*?)">')
    plugintools.log("longurl "+longurl)
    plugintools.play_resolved_url(longurl)
  
    


xtv_user= plugintools.get_setting("xtv_user")
xtv_pwd = plugintools.get_setting("xtv_pwd")
rtv_pwd = plugintools.get_setting("rtv_pwd")
id_pastebin = plugintools.get_setting("id_pastebin")

def m3u_items(title):
    plugintools.log('[%s %s].m3u_items %s' % (addonName, addonVersion, title))    

    thumbnail = art + 'icon.png'
    fanart = art + 'fanart.jpg'
    only_title = title

    if title.find("tvg-logo") >= 0:
        thumbnail = re.compile('tvg-logo="(.*?)"').findall(title)
        num_items = len(thumbnail)
        print 'num_items',num_items
        if num_items == 0:
            thumbnail = 'icon.png'
        else:
            thumbnail = thumbnail[0]
        
        only_title = only_title.replace('tvg-logo="', "")
        only_title = only_title.replace(thumbnail, "")

    if title.find("tvg-wall") >= 0:
        fanart = re.compile('tvg-wall="(.*?)"').findall(title)
        fanart = fanart[0]
        only_title = only_title.replace('tvg-wall="', "")
        only_title = only_title.replace(fanart, "")
        
    try:
        if title.find("imdb") >= 0:
            imdb = re.compile('imdb="(.*?)"').findall(title)
            imdb = imdb[0]
            only_title = only_title.replace('imdb="', "")
            only_title = only_title.replace(imdb, "")
        else:
            imdb = ""
    except:
        imdb = ""

    try:
        if title.find("dir") >= 0:
            dir = re.compile('dir="(.*?)"').findall(title)
            dir = dir[0]
            only_title = only_title.replace('dir="', "")
            only_title = only_title.replace(dir, "")
        else:
            dir = ""
    except:
        dir = ""

    try:
        if title.find("wri") >= 0:
            writers = re.compile('wri="(.*?)"').findall(title)
            writers = writers[0]
            only_title = only_title.replace('wri="', "")
            only_title = only_title.replace(writers, "")
        else:
            writers = ""
    except:
        writers = ""

    try:
        if title.find("votes") >= 0:
            num_votes = re.compile('votes="(.*?)"').findall(title)
            num_votes = num_votes[0]
            only_title = only_title.replace('votes="', "")
            only_title = only_title.replace(num_votes, "")
        else:
            num_votes = ""
    except:
        num_votes = ""

    try:
        if title.find("plot") >= 0:
            plot = re.compile('plot="(.*?)"').findall(title)
            plot = plot[0]
            only_title = only_title.replace('plot="', "")
            only_title = only_title.replace(plot, "")
        else:
            plot = ""
    except:
        plot = ""

    try:
        if title.find("genre") >= 0:
            genre = re.compile('genre="(.*?)"').findall(title)
            genre = genre[0]
            only_title = only_title.replace('genre="', "")
            only_title = only_title.replace(genre, "")
            print 'genre',genre
        else:
            genre = ""
    except:
        genre = ""

    try:
        if title.find("time") >= 0:
            duration = re.compile('time="(.*?)"').findall(title)
            duration = duration[0]
            only_title = only_title.replace('time="', "")
            only_title = only_title.replace(duration, "")
            print 'duration',duration
        else:
            duration = ""
    except:
        duration = ""

    try:
        if title.find("year") >= 0:
            year = re.compile('year="(.*?)"').findall(title)
            year = year[0]
            only_title = only_title.replace('year="', "")
            only_title = only_title.replace(year, "")
            print 'year',year
        else:
            year = ""
    except:
        year = ""

    if title.find("group-title") >= 0:
        cat = re.compile('group-title="(.*?)"').findall(title)
        if len(cat) == 0:
            cat = ""
        else:
            cat = cat[0]
        plugintools.log("m3u_categoria= "+cat)
        only_title = only_title.replace('group-title=', "")
        only_title = only_title.replace(cat, "")
    else:
        cat = ""

    if title.find("tvg-id") >= 0:
        title = title.replace('”', '"')
        title = title.replace('“', '"')
        tvgid = re.compile('tvg-id="(.*?)"').findall(title)
        print 'tvgid',tvgid
        tvgid = tvgid[0]
        plugintools.log("m3u_categoria= "+tvgid)
        only_title = only_title.replace('tvg-id=', "")
        only_title = only_title.replace(tvgid, "")
    else:
        tvgid = ""

    if title.find("tvg-name") >= 0:
        tvgname = re.compile('tvg-name="(.*?)').findall(title)
        tvgname = tvgname[0]
        plugintools.log("m3u_categoria= "+tvgname)
        only_title = only_title.replace('tvg-name=', "")
        only_title = only_title.replace(tvgname, "")
    else:
        tvgname = ""

    only_title = only_title.replace('"', "").strip()

    return thumbnail, fanart, cat, only_title, tvgid, tvgname, imdb, duration, year, dir, writers, genre, num_votes, plot

def parse_url(url):
    # plugintools.log("url entrante= "+url)

    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")
        return url

    else:
        plugintools.log("error en url= ") 
def server_rtmp(params):
    plugintools.log('[%s %s].server_rtmp %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    plugintools.log("URL= "+url)

    if url.find("iguide.to") >= 0:
        params["server"] = 'iguide'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("freetvcast.pw") >= 0:
        params["server"] = 'freetvcast'
        return params

    elif url.find("9stream") >= 0:
        params["server"] = '9stream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("freebroadcast") >= 0:
        params["server"] = 'freebroadcast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

    elif url.find("goodgame.ru") >= 0:
        params["server"] = 'goodgame.ru'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("hdcast") >= 0:
        params["server"] = 'hdcast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("sharecast") >= 0:
        params["server"] = 'sharecast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("cast247") >= 0:
        params["server"] = 'cast247'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("castalba") >= 0:
        params["server"] = 'castalba'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("direct2watch") >= 0:
        params["server"] = 'direct2watch'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("businessapp1") >= 0:
        params["server"] = 'businessapp'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params    

    elif url.find("vaughnlive") >= 0:
        params["server"] = 'vaughnlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("sawlive") >= 0:
        params["server"] = 'sawlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("streamingfreetv") >= 0:
        params["server"] = 'streamingfreetv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url        
        return params

    elif url.find("totalplay") >= 0:
        params["server"] = 'totalplay'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        return params

    elif url.find("everyon") >= 0:
        params["server"] = 'everyon'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("iviplanet") >= 0:
        params["server"] = 'iviplanet'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("cxnlive") >= 0:
        params["server"] = 'cxnlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("ucaster") >= 0:
        params["server"] = 'ucaster'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("mediapro") >= 0:
        params["server"] = 'mediapro'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

    elif url.find("veemi") >= 0:
        params["server"] = 'veemi'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("yukons.net") >= 0:
        params["server"] = 'yukons.net'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("janjua") >= 0:
        params["server"] = 'janjua'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("mips") >= 0:
        params["server"] = 'mips'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("zecast") >= 0:
        params["server"] = 'zecast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("vertvdirecto") >= 0:
        params["server"] = 'vertvdirecto'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("filotv") >= 0:
        params["server"] = 'filotv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("dinozap") >= 0:
        params["server"] = 'dinozap'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("ezcast") >= 0:
        params["server"] = 'ezcast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("flashstreaming") >= 0:
        params["server"] = 'flashstreaming'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("multistream") >= 0:
        params["server"] = 'multistream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("flashtv") >= 0:
        params["server"] = 'flashtv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("04stream") >= 0:
        params["server"] = '04stream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("vercosas") >= 0:
        params["server"] = 'vercosasgratis'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("") >= 0:
        params["server"] = ''
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("pvtserverz") >= 0:
        params["server"] = 'pvtserverz'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    else:
        params["server"] = ''
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    if url.startswith("rtsp") >= 0:
        params["server"] = ''
        params["url"]=url
        return params

def xml_skin():
    plugintools.log('[%s %s].xml_skin ' % (addonName, addonVersion))

    mastermenu = plugintools.get_setting("mastermenu")
    xmlmaster = plugintools.get_setting("xmlmaster")
    SelectXMLmenu = plugintools.get_setting("SelectXMLmenu")

    
    if xmlmaster == 'true':
        if SelectXMLmenu == '0':
            mastermenu = 'https://dl.dropboxusercontent.com/s/zb76dwqaj8cnxlo/menu%20standar%20tvwin.xml'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            
            ver_intro = plugintools.get_setting("")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + '')
                
        elif SelectXMLmenu == '1': 
            mastermenu = 'http'+'://pas'+'teb'+'in.com'+'/raw'+'.php'+'?'+'i=um'+'hZ'+'zM'+'9Y'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            
            ver_intro = plugintools.get_setting("")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + '')              
            
        elif SelectXMLmenu == '2': 
            mastermenu = 'http'+'://pas'+'teb'+'in.com'+'/raw'+'.php'+'?'+'i=xq'+'K6'+'Ui'+'Bn'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            
            ver_intro = plugintools.get_setting("")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + '')  
        elif SelectXMLmenu == '3':
            mastermenu = 'http'+'://pas'+'teb'+'in.com'+'/raw'+'.php'+'?'+'i=9f'+'Q8'+'aG'+'bM'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            
            ver_intro = plugintools.get_setting("")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + '')                
    else:
           
        mastermenu = 'https://dl.dropboxusercontent.com/s/zb76dwqaj8cnxlo/menu%20standar%20tvwin.xml'

        
        ver_intro = plugintools.get_setting("ver_intro")
        if ver_intro == "true":
            xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + '')
        

    return mastermenu
def launch_rtmp(params):
    plugintools.log("[TvWin-0.3.0].launch_rtmp " + repr(params))

    url = params.get("url")
    plugintools.log("URL= "+url)
    title = params.get("title")
    title = title.replace("[/COLOR]", "")
    title = title.strip()
    print title

    if title.endswith("[9stream]") == True:
        print '9stream'
        params["server"] = '9stream'
        ninestreams(params)
    
    elif title.endswith("[iguide]") == True:
        params["server"] = 'iguide'
        plugintools.play_resolved_url(url)

    elif title.endswith("[vercosasgratis]") == True:
        print 'vercosasgratis'
        params["server"] = 'vercosasgratis'
        vercosas(params)

    elif title.endswith("[freebroadcast]") == True:
        print 'freebroadcast'
        params["server"] = 'freebroadcast'
        freebroadcast(params)        

    elif title.endswith("[ucaster]") == True:
        params["server"] = 'ucaster'
        plugintools.play_resolved_url(url)

    elif title.endswith("[direct2watch]") == True:
        params["server"] = 'direct2watch'
        directwatch(params)

  

    elif title.endswith("[cast247]") == True:
        params["server"] = 'cast247'
        castdos(params)

    elif url.find("hdcast") >= 0:
        params["server"] = 'hdcast'
        plugintools.play_resolved_url(url)

    elif url.find("janjua") >= 0:
        params["server"] = 'janjua'
        plugintools.play_resolved_url(url)

    elif url.find("mips") >= 0:
        params["server"] = 'mips'
        plugintools.play_resolved_url(url)

    elif url.find("zecast") >= 0:
        params["server"] = 'zecast'
        plugintools.play_resolved_url(url)

    elif url.find("filotv") >= 0:
        params["server"] = 'filotv'
        print "filotv"
        plugintools.play_resolved_url(url)

    elif url.find("ezcast") >= 0:
        params["server"] = 'ezcast'
        plugintools.play_resolved_url(url)

    elif url.find("flashstreaming") >= 0:
        params["server"] = 'flashstreaming'
        plugintools.play_resolved_url(url)

    

    elif url.find("multistream") >= 0:
        params["server"] = 'multistream'
        print "multistream"
        plugintools.play_resolved_url(url)

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        plugintools.play_resolved_url(url)

    elif url.find("flashtv") >= 0:
        params["server"] = 'flashtv'
        print "flashtv"
        plugintools.play_resolved_url(url)

    elif url.find("freetvcast") >= 0:
        params["server"] = 'freetvcast'
        print "freetvcast"
        freetvcast(params)

    elif url.find("04stream") >= 0:
        params["server"] = '04stream'
        plugintools.play_resolved_url(url)

    elif url.find("sharecast") >= 0:
        params["server"] = 'sharecast'
        plugintools.play_resolved_url(url)

    elif url.find("vaughnlive") >= 0:
        params["server"] = 'vaughnlive'
        resolve_vaughnlive(params)

    elif url.find("goodcast") >= 0:
        params["server"] = 'goodcast'
        plugintools.play_resolved_url(url)

    elif url.find("dcast.tv") >= 0:
        params["server"] = 'dcast.tv'
        plugintools.play_resolved_url(url)

    elif url.find("castalba") >= 0:
        params["server"] = 'castalba'
        castalba(params)

    elif url.find("tutelehd.com") >= 0:
        params["server"] = 'tutelehd.com'
        plugintools.play_resolved_url(url)

    elif url.find("flexstream") >= 0:
        params["server"] = 'flexstream'
        plugintools.play_resolved_url(url)

    elif url.find("xxcast") >= 0:
        params["server"] = 'xxcast'
        plugintools.play_resolved_url(url)

    elif url.find("vipi.tv") >= 0:
        params["server"] = 'vipi.tv'
        plugintools.play_resolved_url(url)

    elif url.find("watchjsc") >= 0:
        params["server"] = 'watchjsc'
        plugintools.play_resolved_url(url)

    elif url.find("zenex.tv") >= 0:
        params["server"] = 'zenex.tv'
        plugintools.play_resolved_url(url)

    elif url.find("castto") >= 0:
        params["server"] = 'castto'
        plugintools.play_resolved_url(url)

    elif url.find("tvzune") >= 0:
        params["server"] = 'tvzune'
        plugintools.play_resolved_url(url)

    elif url.find("flashcast") >= 0:
        params["server"] = 'flashcast'
        plugintools.play_resolved_url(url)

    elif url.find("ilive.to") >= 0:
        params["server"] = 'ilive.to'
        print "iliveto"
        plugintools.play_resolved_url(url)

    elif url.find("Direct2Watch") >= 0:
        params["server"] = 'Direct2Watch'
        print "direct2watch"
        plugintools.play_resolved_url(url)
        
    else:
        params["server"] = 'TvWin'
        print "ninguno"
        plugintools.play_resolved_url(url)   

def open_settings(self):
    xbmcaddon.Addon(id=addon_id).openSettings()
    params = plugintools.get_params()
    main_list(params)


    

	
run()



