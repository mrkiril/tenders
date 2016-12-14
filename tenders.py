print("tenders")
import requests
import re 
import os, sys

def customers():
    r = requests.get('http://5.9.9.40/tenders/', auth=('mrkiril', '123ss456'))    
    ind = 0
    arr_folders = re.findall('''<a href=".+?">(.+?/)</a>''', r.text)
    #print(arr_folders[1])
    #_=input("Break point ..")
    for i in range(1, len(arr_folders)):       
        r1 = requests.get('http://5.9.9.40/tenders/'+arr_folders[i], auth=('mrkiril', '123ss456'))
        arr_folders1 = re.findall('''<a href="(.+?)">''', r1.text)  
        print(i, arr_folders[i], str( round(i/len(arr_folders), 4)*100)+"%" ) 
        #_=input("LALKA")
        ind += 1
        print("files: ", end=" ")
        for j in range(1, len(arr_folders1)):        
            r2 = requests.get('http://5.9.9.40/tenders/'+arr_folders[i]+arr_folders1[j], auth=('mrkiril', '123ss456'))
            print(j, end=" ")    
            
            with open('files/'+arr_folders1[j], 'w') as f1:
                f1.write(r2.text)
        print()   
    

def points():
    r = requests.get('http://5.9.9.40/files/', auth=('mrkiril', '123ss456'))    
    ind = 0
    arr_folders = re.findall('''<a href=".+?">(.+?/)</a>''', r.text)
    # http://5.9.9.40/files/2015-02-05/
    for i in range(1, len(arr_folders)): 
        print(i, arr_folders[i], str( round(i/len(arr_folders), 4)*100)+"%" )       
        # http://5.9.9.40/files/2015-02-05/67403dc828034b2eb3c12b40674da3ad/
        r1 = requests.get('http://5.9.9.40/files/'+arr_folders[i], auth=('mrkiril', '123ss456'))
        arr_folders1 = re.findall('''<a href="(.+?)">''', r1.text)        
        ind += 1
        
        for j in range(1, len(arr_folders1)):
            # http://5.9.9.40/files/2015-02-05/67403dc828034b2eb3c12b40674da3ad/blablabla.yaml.json        
            
            r2 = requests.get('http://5.9.9.40/files/'+arr_folders[i]+arr_folders1[j], auth=('mrkiril', '123ss456'))
            arr_folders2 = re.findall('''<a href=".+?">(.+?)</a>''', r2.text, re.DOTALL)
            #print(r2.text)
            #_=input()
            for k in range(1, len(arr_folders2)):
                is_yaml = arr_folders2[k].find("json")
                
                if is_yaml == -1:
                    #print("NO JSON \t"+arr_folders2[k])  
                    #_=input()                  
                    continue
                
                else:  
                    print(arr_folders2[k]+"\t JSON JSON JSON")  
                    #_=input()                           
                    r3 = requests.get('http://5.9.9.40/files/'+arr_folders[i]+arr_folders1[j]+arr_folders2[k], auth=('mrkiril', '123ss456'))
                    with open('points/'+arr_folders1[j][:-1]+".json", 'w') as f2:
                        f2.write(r3.text)

                    #_=input("BR POINT TO CHEAK JSON")

points()




























































































































