# your name                                                                                                                                                                                 
# your GTID#                                                                                                                                                                                
                                                                                                                                                                                            
import urllib.request, json, time, requests, sys, re, csv                                                                                                                                             
                                                                                                                                                                                            
from bs4 import BeautifulSoup as bs                                                                                                                                                         
                                                                                                                                                                                            
API_KEY='e307d3989f772742e4794219effaf23f'                                                                                                                                                  
                                                                                                                                                                                            
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
  actor_id=str(actor_id)                                                                                                                                                                    
  response = requests.get("https://api.themoviedb.org/3/person/"+actor_id+"?api_key="+API_KEY+"&language=en-US")                                                                            
  if  response.status_code!=200:                                                                                                                                                                                                                                                                                                      
    return  'None'                                                                                                                                                                            
  else:                                                                                                                                                                                     
    x=response.json()                                                                                                                                                                                                                                                                                                                                                                 
    return (x["name"])                                                                                                                                                                      
                                                                                                                                                                                            
def req_movies_for_actor(actor_id): #returns all the movies in which an actor with actor_id has been casted                                                                                 
  actor_id=str(actor_id)                                                                                                                                                                    
  response = requests.get("https://api.themoviedb.org/3/person/"+actor_id+"/movie_credits?api_key="+API_KEY+"&language=en-US")                                                                                                                                                                                                                                                                       
  x=response.json() 
  t=x.get('cast', None)
  result=[]
  for i in t:                                                                                                                                                                                                                                                                                                                                                 
      movie_id=i['id']                                                                                                                                                                     
      movie_dict={                                                                                                                                                                          
        movie_id:{                                                                                                                                                                          
          "name":   i['title'],                                                                                                                                           
          "parent": actor_id                                                                                                                                                                
        }                                                                                                                                                                                   
      }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
      result.append(movie_dict)                                                                                                                                                                                                                                                                                                                                     
  return result                                                                                                                                                                           
                                                                                                                                                                                            
def req_actors_for_movie(movie_id): #returns all the cast members in the movie with movie_id                                                                                                
  response=requests.get("https://api.themoviedb.org/3/movie/"+str(movie_id)+"/credits?api_key="+API_KEY+"&language=en-US")                                                                                                                                      
  #print (r.status_code)                                                                                                                                                                    
  x=response.json()                                                                                                                                                                                
  t=x.get('cast', None)      
  #print (t)
  result=[]                                                                                                                                                                               
  for i in t:                                                                                                                                                                               
    cast_id=i['id']                                                                                                                                                              
    cast_dict = {                                                                                                                                                                           
            cast_id: {                                                                                                                                                                      
                "name":i['name'],                                                                                                                                 
                "parent": movie_id                                                                                                                                                          
            }                                                                                                                                                                               
    }                                                                                                                                                                                       
    #print (cast_dict)                                                                                                                                                                      
    result.append(cast_dict)                                                                                                                                                                                                                                                                                                                                                      
  return result                                                                                                                                                                          
                                                                                                                                                                                            
def one_deg_from_actor(from_actor_id): #returns all the co-stars for an actor with from_actor_id                                                                                            
  result=[]  
  actor_name=look_actor_name_by_id(from_actor_id)
  if actor_name=='None':
    return actor_name
  res1=req_movies_for_actor(from_actor_id)                                                                                                                                                                                                                                                                                                                                                               
  for i in res1:                                                                                                                                                                            
    for k in i: 
      time.sleep(0.5)
      response=req_actors_for_movie(k)                                                                                                                                                      
      for j in response:                                                                                                                                                                    
        for v in j.values():                                                                                                                                                                
          if actor_name!=v['name']:
            res2=[]
            res2.append(i) #append movies info
            res2.append(j) #append costars info
            result.append(res2)
            
  return result                                                                                                                                                                             
                                                                                                                                                                                            
def main(args):                                                                                                                                                                             
  if len(args)==1: #no parameter apart from script                                                                                                                                                                          
    print ("No actor chosen. Do you want to play one degree from the default chosen one, Kevin Bacon?")   
    a=input()
    if a=='yes': #user enters yes
      print (one_deg_from_actor(4724))
    else:  #user enters no                                                                                                                                                                                 
      print ("Bye!!")                                                                                                                                                                                                                                                                                                                                                
  elif len(args)>=2:                                                                                                                                                                        
    if args[1].isdigit()==True: #actor_id must be integer                                                                                                                                                                  
      if len(args)==3:
          name,format=args[2].split('.')
          if format!='csv': #format must be csv
            print ("ERROR: The output filename provided does not have a .csv extension. Please try again with a valid filename.")
          elif name.isalnum()==False: #filename contains special characters
            print ("ERROR: Whoa, buddy! We can't write to files like that. Try again, and please try to keep it clean.")
          else: #write to csv file
            result=one_deg_from_actor(args[1]) 
            if result=='None':	
              print ("ERROR: We've don't recognize that id. They're obviously not connected to Kevin Bacon or anyone else for that matter. Please play again.")
            else:
              writer = csv.writer(open(args[2], 'w'))
              actor_name=look_actor_name_by_id(args[1])
              movie_name=''
              costar_name=''
              for i in result:
                for x in i[0].values():
	                movie_name=x['name']
                for x in i[1].values():
	                costar_name=x['name']
                writer.writerow(','.join((actor_name,movie_name,costar_name)))
           
              print ("Writing data to "+args[2]+" file... done.")
      else: #write to console	
        actor_name=look_actor_name_by_id(args[1])
        result=one_deg_from_actor(args[1]) 
        if result=='None':	
          print ("ERROR: We've don't recognize that id. They're obviously not connected to Kevin Bacon or anyone else for that matter. Please play again.")
        else:
          movie_name=''
          costar_name=''
          for i in result:
            for x in i[0].values():
	              movie_name=x['name']
            for x in i[1].values():
	              costar_name=x['name']
            print (actor_name+" > "+movie_name+" > "+costar_name)
    else:                                                                                                                                                                                   
      print ("Not an integer actor_id!! Bye!!")                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                            
print("If testing for Kevin Bacon, this should take less than 60 seconds.")                                                                                                                 
start_time = time.time()                                                                                                                                                                    
if __name__ == "__main__":                                                                                                                                                                  
    main(sys.argv)  
end_time = time.time() - start_time                                                                                                                                                         
print("Took {:.1f} seconds".format(end_time))
           