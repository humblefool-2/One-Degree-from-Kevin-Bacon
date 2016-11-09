# your name                                                                                                                                                                                 
# your GTID#                                                                                                                                                                                
                                                                                                                                                                                            
import urllib.request, json, time, requests, sys, re, csv, codecs                                                                                                                                             
                                                                                                                                                                                            
from bs4 import BeautifulSoup as bs
                                                                                                                                                         
                                                                                                                                                                                            
API_KEY='e307d3989f772742e4794219effaf23f'                                                                                                                                                  
                                               
def pr(s):
  try:
    print (s)
  except UnicodeEncodeError:
    for c in s:
      try:
        print(c,end='')
      except UnicodeEncodeError:
        print ('?',end='')
	                                                                                                                                             
def scrape_all_movies(url): #returns all movies' name and their urls                                                                                                                        
  page=urllib.request.urlopen(url)                                                                                                                                                          
                                                                                                                                                                                            
  soup=bs(page)                                                                                                                                                                             
  d=soup.find('div',class_='filmo-category-section')                                                                                                                                        
  b=d.find_all('b')                                                                                                                                                                         
  all_movies={}                                                                                                                                                                              
  for i in b:                                                                                                                                                                                                                                                                                                                                                                 
     all_movies[i.get_text().replace('>','')]='http://www.imdb.com'+i.a['href']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
  return all_movies                                                                                                                                                                           
                                                                                                                                                                                            
def look_actor_name_by_id(actor_id): #returns actor'name by its id                                                                                                                          
  actor_id=str(actor_id)                                                                                                                                                                    
  response = requests.get("https://api.themoviedb.org/3/person/"+actor_id+"?api_key="+API_KEY+"&language=en-US")                                                                            
  if  response.status_code!=200:                                                                                                                                                                                                                                                                                                      
    return  'None'                                                                                                                                                                            
  else:                                                                                                                                                                                     
    x=response.json()                                                                                                                                                                                                                                                                                                                                                                 
    return (x["name"])                                                                                                                                                                      
                                                                                                                                                                                            
def req_movies_for_actor(actor_id): #returns all the movies in which an actor with actor_id has been casted                                                                                                                                                                                                                                                    
  response = requests.get("https://api.themoviedb.org/3/person/"+str(actor_id)+"/movie_credits?api_key="+API_KEY+"&language=en-US")                                                                                                                                                                                                                                                                       
  x=response.json() 
  t=x.get('cast', None)
  movie_dict={}
  for i in t:                                                                                                                                                                                                                                                                                                                                                 
      movie_id=int(i['id'])                                                                                                                                                                     
      movie_dict[movie_id]={                                                                                                                                                                                                                                                                                                                                                   
          "name":   i['title'],                                                                                                                                           
          "parent": int(actor_id )                                                                                                                                                               
        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
  return movie_dict                                                                                                                                                                    
                                                                                                                                                                                            
def req_actors_for_movie(movie_id): #returns all the cast members in the movie with movie_id                                                                                                
  response=requests.get("https://api.themoviedb.org/3/movie/"+str(movie_id)+"/credits?api_key="+API_KEY+"&language=en-US")                                                                                                                                      
  #print (response.status_code)                                                                                                                                                                    
  x=response.json()                                                                                                                                                                               
  t=x.get('cast', None)    
  if t==None:
    return None
  cast_dict={}                                                                                                                                                                               
  for i in t:                                                                                                                                                                               
    cast_id=int(i['id'] )                                                                                                                                                             
    cast_dict[cast_id]= {                                                                                                                                                                      
                "name":i['name'],                                                                                                                                 
                "parent": int(movie_id)                                                                                                                                                          
            }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
  return cast_dict                                                                                                                                                                          
                                                                                                                                                                                            
def one_deg_from_actor(from_actor_id): #returns all the co-stars for an actor with from_actor_id                                                                                            
  actor_name=look_actor_name_by_id(from_actor_id)
  if actor_name=='None':
    return actor_name
  movies=req_movies_for_actor(from_actor_id)   
  for key,value in movies.items():
    if time.time() - start_time_new >= 9:
      start_time_new = time.time()
      time.sleep(0.105)
    movieid = key
    actors.update(req_actors_for_movie(movieid))
  del actors[from_actor_id]

  return (movies, actors)  
                                                                                                                                                                                            
def main(args):                                                                                                                                                                             
  if len(args)==1: #no parameter apart from script                                                                                                                                                                          
    print ("No actor chosen. Do you want to play one degree from the default chosen one, Kevin Bacon?")   
    a=input()
    if a=='yes': #user enters yes
      res=one_deg_from_actor(4724)
      print (res)
    else:  #user enters no                                                                                                                                                                                 
      print ("Bye!!")                                                                                                                                                                                                                                                                                                                                                
  elif len(args)>=2:                                                                                                                                                                        
    if args[1].isdigit()==True: #actor_id must be integer                                                                                                                                                                  
      if len(args)==3:
          try:
            name,format=args[2].split('.')
            if format!='csv': #format must be csv
              print ("ERROR: The output filename provided does not have a .csv extension. Please try again with a valid filename.")
            elif name.isalnum()==False: #filename contains special characters
              print ("ERROR: Whoa, buddy! We can't write to files like that. Try again, and please try to keep it clean.")
            else: #write to csv file
              result=one_deg_from_actor(int(args[1]))
              if result=='None':	
                print ("ERROR: We've don't recognize that id. They're obviously not connected to Kevin Bacon or anyone else for that matter. Please play again.")
              else:
                writer = csv.writer(open(args[2], 'w'),lineterminator = '\n')
                actor_name=lookup_actor_name_by_id(args[1])
                movies = result[0]
                costars = result[1]
                for movieid , value in movies.items():
                  movie_name = value['name']
                  for costarid , c_value in costars.items():
                    costar_name = c_value['name']
                    if movieid == c_value['parent']:
                      writer.writerow([actor_name,movie_name,costar_name])
             
                print ("Writing data to "+args[2]+" file... done.")
          except Exception as e:
            print(e)
            print ("ERROR: Whoa, buddy! We can't write to files like that. Try again, and please try to keep it clean.")
      else: #write to console	
        actor_name=look_actor_name_by_id(args[1])
        result=one_deg_from_actor(args[1]) 
        if result=='None':	
          print ("ERROR: We've don't recognize that id. They're obviously not connected to Kevin Bacon or anyone else for that matter. Please play again.")
        else:
          movies = result[0]
          costars = result[1]
          for movieid , value in movies.items():
            movie_name = value['name']
            for costarid , c_value in costars.items():
              costar_name = c_value['name']
              if movieid == c_value['parent']:
                print (actor_name+" > "+movie_name+" > "+costar_name)
    else:                                                                                                                                                                                   
      print ("Not an integer actor_id!! Bye!!")                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                            
print("If testing for Kevin Bacon, this should take less than 60 seconds.")                                                                                                                 
start_time = time.time()                                                                                                                                                                    
if __name__ == "__main__":                                                                                                                                                                  
    main(sys.argv)  
end_time = time.time() - start_time                                                                                                                                                         
print ("Took {:.1f} seconds".format(end_time))
           