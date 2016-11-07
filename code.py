import urllib.request, json, requests, re,time                                                                                                                                                   
                                                                                                                                                                                            
from bs4 import BeautifulSoup as bs                                                                                                                                                         
                                                                                                                                                                                            
def scrape_all_movies(url): #returns all movies' name and their urls                                                                                                                        
  page=urllib.request.urlopen(url)                                                                                                                                                          
                                                                                                                                                                                            
  soup=bs(page)                                                                                                                                                                             
  d=soup.find('div',class_='filmo-category-section')                                                                                                                                        
  b=d.find_all('b')                                                                                                                                                                         
  response=[]                                                                                                                                                                               
  for i in b:                                                                                                                                                                               
    dict={                                                                                                                                                                                  
     i.get_text().replace('>',''):'http://www.imdb.com'+i.a['href']                                                                                                                                         
    }                                                                                                                                                                                       
    #print (dict)                                                                                                                                                                           
    response.append(dict)                                                                                                                                                                   
  return response                                                                                                                                                                           
                                                                                                                                                                                            
def look_actor_name_by_id(actor_id): #returns actor'name by its id                                                                                                                          
  response = requests.get("https://api.themoviedb.org/3/person/"+actor_id+"?api_key=e307d3989f772742e4794219effaf23f&language=en-US")                                                       
  #print (response.status_code)                                                                                                                                                             
  x=response.json()                                                                                                                                                                         
  print (x["name"])   
  
def req_movies_for_actor(actor_id): #returns all the movies in which an actor with actor_id has been casted 
  response = requests.get("https://api.themoviedb.org/3/person/"+actor_id+"?api_key=e307d3989f772742e4794219effaf23f&language=en-US")                                                                                                                                                                                                                   
  x=response.json() 
  url='http://www.imdb.com/name/'+x["imdb_id"]+'/'
  page=urllib.request.urlopen(url)                                                                                                                                                          
  soup=bs(page)                                                                                                                                                                             
  d=soup.find('div',class_='filmo-category-section')                                                                                                                                        
  b=d.find_all('b')                                                                                                                                                                         
  response=[]                                                                                                                                                                               
  for i in b:                                                                                                                                                                               
    idc=i.a['href'][7:16]
    r=requests.get("https://api.themoviedb.org/3/movie/"+idc+"?api_key=e307d3989f772742e4794219effaf23f&language=en-US")
    x=r.json()
    if r.status_code==200:
      movie_id=x["id"]
      movie_dict={
        movie_id:{
          "name": i.get_text().replace('>',''),
          "parent": actor_id
        }
      }
      print (movie_dict)                                                                                                                                                                           
    response.append(dict) 
    time.sleep(2)
  return response 

def req_actors_for_movie(movie_id): #returns all the cast members in the movie with movie_id
  r=requests.get("https://api.themoviedb.org/3/movie/"+str(movie_id)+"?api_key=e307d3989f772742e4794219effaf23f&language=en-US")
  x=r.json()
  url='http://www.imdb.com/title/'+x["imdb_id"]+'/'
  page=urllib.request.urlopen(url)
  soup=bs(page) 
  d=soup.find('table',class_='cast_list') 
  t=d.find_all('td',class_='itemprop')
  response=[]
  for i in t:
    cast_id=i.a['href'][6:15]
    cast_dict = {
            cast_id: {
                "name":i.get_text().replace('\n','')[1:-1],
                "parent": movie_id
            }
    }
    print (cast_dict)
    response.append(cast_dict)
      
  return response 
                                                                                                                                                                                            
if __name__ == "__main__":                                                                                                                                                                  
  #look_actor_name_by_id(str(4724))                                                                                                                                                          
  #scrape_all_movies("http://www.imdb.com/name/nm0000102/")
  #req_movies_for_actor(str(4724))
  req_actors_for_movie(916)