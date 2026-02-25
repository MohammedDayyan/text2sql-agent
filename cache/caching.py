import json
import os 

CACHE_PATH = 'cache/sql_cache.json'

def load_cache():
    if not os.path.exists(CACHE_PATH):
        with open(CACHE_PATH,'w') as f:
            json.dump({},f)
        return {}
    if os.path.getsize(CACHE_PATH) == 0:
        return {}
    
    with open(CACHE_PATH,'r') as f:
        data=json.load(f)
        if isinstance(data,dict):
            return data
        else:
            return {}
        
def save_cache(cache):
    with open(CACHE_PATH,'w') as f:
        json.dump(cache,f,indent=4)
        
def get_cached_sql(question):
    cache = load_cache()
    return cache.get(question)

def store_sql(question,query):
    cache=load_cache()
    cache[question] = query 
    save_cache(cache)