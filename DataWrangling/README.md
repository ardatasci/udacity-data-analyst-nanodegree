
# Open Street Map Data Analysis

In this project, the ATMs and branches of the banks in Ankara, capital of Turkey are analyzed and inserted into SQL database.
 

In order to analyze the branches and atms in Ankara, nodes, ways and the related tags will be converted into csv files and inserted into database. While creating the csv files, the names of banks will be preprocessed for better analysis.

The schema of the SQL database is shown below : 

```
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);
```

## Map Area

The map is my hometown, so I am more interested in finding ATMs and Banks in the city.

The osm file size is 281.3 MB which can be downloaded here : https://s3.amazonaws.com/metro-extracts.mapzen.com/ankara_turkey.osm.bz2


## Problems Encountered in the Dataset

According to the documantation in openstreetmap.org, the banks and atms exist in the data as amenities. The names of the banks can be different so that first of all the names of the banks are analyzed. 

The brances of banks are represented as amenity=bank in the dataset and ATMs are represented as amenity=atm.

In order to analyze the problems in the dataset, I checked the distinct bank names.




```python
# encoding=utf8
import xml.etree.cElementTree as ET
import pprint
import re  


OSMFILE = "ankara_turkey.osm"


```


```python
# encoding=utf8
'''
Checks if the node is an bank or not.
returns True if node is a bank
'''
def is_bank_node(node):
    for tag in node.iter("tag"):
        if tag.attrib['k'] == "amenity" and (tag.attrib['v'] == "bank" or tag.attrib['v'] == "atm"):
            return True 
    return False

'''
Fills the set with the distinct names of banks in the dataset.
'''
bank_names = set()
def distinct_bank_names(osm_file):
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" and is_bank_node(elem):
            name = ""
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "name":
                    name = tag.attrib['v']
                    bank_names.add(name.lower())
    


distinct_bank_names(OSMFILE)
print ', '.join(bank_names)
```

    deniz bank, ingbank atm, ziraat bankasi, vakıfbank (atm), finansbank pursaklar, ptt, akbank atm, akbank, bank asya, vakıf bank, vakıfbank söğütözü şubesi, tekstilbank, finansbank atm, halkbank, türkiye iş bankası atm, qnb finansbank, şekerbank, albaraka türk, kuveyt türk, turkiye is bankasi, işbankası atm, tc ziraat bankasi, teb atm, odeabank, vakıfbank, halkbankası atm, albaraka, işbankası (atm), abank, halk banksı, halkbank hüseyingazi şubesi, teb, cüzdanmatik, emniyet md. ek bina, akbank, tr-ankara, yapı kredi leasing, türkiye finans katılım bankası, ziraat bankası güneşevler şubesi, ykb atm, garanti bankası atm, yapıkredi atm, iş b., garanti bankası, yapı kredi bankası atm, t.c. ziraat bankası a.ş., fibabanka, garanti, türkiye finans katılım, burgan bank, finans bank, vakıfbank atm, ing bank atm, a bank, ziraat b., yapı kredi bankası, finansbank, halkbankası (atm), yapi kredi, yapı kredi bankası çukurambar şubesi, ing bankası, hsbc atm, yapı kredi, hsbc pursaklar, t-bank, garanti bankası (atm), ziraat bankası atm, nakit yükleme noktası, vakıfbank tpao şubesi, akbank - yaşamkent şubesi, yapıkredi bankası, garanti atm, kuveyt türk atm, hsbc, anadolubank, ing atm, finansbank (atm), ing bank, akbank (atm), iş bankası, garanti bank, denizbank atm, vakifbank, yapıkredi, qnb finansbank atm, ziraat atm, garanti bankası - yaşmkent şubesi, ak bank atm, ziraat bankası pursaklar, halkbank atm, garanti kavaklıdere şubesi, ziraat bankası, ziraatbank atm, iş bankası atm, garanti bankasi, türkiye iş bankası, asya bank, denizbank, türkiye iş bankası bankamatik


<b>Problems : </b>
When the names of the banks were analyzed, some problems are clearly seen in the dataset.

- Some bank names are written in different formats. For example, Akbank is written in the forms of "AKBANK","Ak Bank", "Akbank", "Akbank - Yaşamkent Şubesi". Those strings needed to be fixed to create a banks table in SQL which includes unique banks.

- ATMs of banks are stated using "ATM" or "(ATM)" strings at the end of the bank names.  

- Some of the banks changed their name over time, for example "Finansbank" is now "QNB Finansbank". Those changes need to be considered.

- There are some names that do not represent a bank name, for example "PTT" which is national post and telegraph directorate in Turkey. Those need to be exclueded.

- Abbreviated names are another problem, for example YKB for Yapi Kredi Bankasi.

- Since the names of banks are in Turkish, some encoding problems occur.

- There are None and empty values in the names.

In order to solve those problems, I have created a expected bank names list which are all unicode and lower case. The names which are not included in the expected bank names list are updated using a dictionary which converts the problematic bank names to expected names.




```python
#RegEx for getting the first part of the string
# encoding=utf-8

'''
Expected bank names list
'''
expected_bank_names = ["denizbank", "ingbank", "ziraat bankası", "vakıfbank", "qnb finansbank", 
                       "akbank", "bank asya", "tekstilbank", "halkbank", "iş bankası", "şekerbank",
                       "albaraka türk", "kuveyt türk", "teb", "odeabank", "abank", "türkiye finans katılım bankası",
                       "garanti bankası", "yapı kredi", "fibabanka", "burgan bank", "hsbc", "t-bank", "anadolubank"]

'''
Bank names mapping
'''
bank_name_mapping = {
    "deniz bank" : "denizbank",
    "ingbank atm" : "ingbank",
    "ziraat bankasi" : "ziraat bankasi",
    "vakıfbank (atm)" : "vakifbank",
    "finansbank pursaklar" : "qnb finansbank",
    "akbank atm" : "akbank",
    "vakıf bank" : "vakıfbank",
    "vakıfbank söğütözü şubesi": "vakıfbank",
    "finansbank atm" : "qnb finansbank",
    "türkiye iş bankası atm" : "iş bankası",
    "turkiye is bankasi" : "iş bankası",
    "işbankası atm" : "iş bankası",
    "tc ziraat bankasi" : "ziraat bankası",
    "teb atm" : "teb",
    "halkbankası atm" : "halkbank",
    "albaraka" : "albaraka türk",
    "işbankası (atm)" : "iş bankası",
    "halk banksı" : "halkbank",
    "halkbank hüseyingazi şubesi" : "halkbank",
    "akbank, tr-ankara" : "akbank",
    "yapı kredi leasing" : "yapı kredi",
    "türkiye finans katılım bankası" : "qnb finansbank",
    "ziraat bankası güneşevler şubesi" : "ziraat bankası",
    "ykb atm" : "yapı kredi",
    "garanti bankası atm" : "garanti bankası",
    "yapıkredi atm" : "yapı kredi",
    "iş b." : "iş bankası",
    "yapı kredi bankası atm" :"yapı kredi",
    "t.c. ziraat bankası a.ş." : "ziraat bankası",
    "garanti" : "garanti bankası",
    "türkiye finans katılım" : "qnb finansbank",
    "finans bank" : "qnb finansbank",
    "vakıfbank atm": "vakıfbank",
    "ing bank atm" : "ingbank",
    "a bank" : "abank",
    "ziraat b." : "ziraat bankası",
    "yapı kredi bankası" : "yapı kredi",
    "finansbank" : "qnb finansbank",
    "halkbankası (atm)" : "halkbank",
    "yapı kredi bankası çukurambar şubesi" : "yapı kredi",
    "ing bankası" : "ingbank",
    "hsbc atm" : "hsbc",
    "hsbc pursaklar": "hsbc",
    "garanti bankası (atm)" : "garanti bankası",
    "ziraat bankası atm" : "ziraat bankası",
    "vakıfbank tpao şubesi": "vakıfbank",
    "akbank - yaşamkent şubesi" :  "akbank",
    "yapıkredi bankası" : "yapı kredi",
    "garanti atm" : "garanti bankası",
    "kuveyt türk atm" : "kuveyt türk",
    "ing atm" : "ingbank",
    "finansbank (atm)" : "qnb finansbank",
    "ing bank" : "ingbank",
    "akbank (atm)" :  "akbank",
    "iş bankası" : "iş bankası",
    "garanti bank" : "garanti bankası",
    "denizbank atm" : "denizbank",
    "vakifbank": "vakıfbank",
    "yapıkredi" : "yapı kredi",
    "ziraat atm" : "ziraat bankası",
    "garanti bankası - yaşmkent şubesi" : "garanti bankası",
    "ak bank atm" :  "akbank",
    "ziraat bankası pursaklar" : "ziraat bankası",
    "halkbank atm" : "halkbank",
    "ziraatbank atm" : "ziraat bankası",
    "iş bankası atm" : "iş bankası",
    "garanti bankasi" : "garanti bankası",
    "türkiye iş bankası" : "iş bankası",
    "asya bank" : "bank asya",
    "denizbank": "denizbank",
    "yapi kredi" : "yapı kredi",
    "garanti":"garanti bankası"

}

'''
Converts non unicode strings to unicode strings
'''
def convert_unicode_if_not(strn):
    if strn == None:
        return None
    elif isinstance(strn, unicode):
        return strn
    else:
        return unicode(strn, 'utf-8')

'''
Updates the bank name using the bank name mapping, fixes the encoding
'''
def update_bank_name(name):
    converted_name = convert_unicode_if_not(name).lower()
    if converted_name in [convert_unicode_if_not(x).lower() for x in expected_bank_names]:
        return converted_name.encode("utf-8")
    elif converted_name in [x.decode('utf-8') for x in bank_name_mapping.keys()]:
        return bank_name_mapping[converted_name.encode('utf-8')]


```

## Creating csv files


After developing converting mechanism, the csv files are generated to seed the data into SQL database. First of all, a function which converts list of hashes to csv  format and persist to filesystem is implemented as below.



```python
# encoding=utf-8
import csv

'''
Creates csv files by giving arrays, headers and the csv file location to be saved.
'''
def create_csv(arr, headers, path):
    with open(path, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers, delimiter = ',')
        writer.writeheader()
        for el in arr:
            writer.writerow()
```

For nodes, ways and the tags of them the csv files are created. For creating CSV files and insterting them into the SQL database, the initals of paths and fields are creted.


```python
# encoding=utf-8
'''
Paths of CSV files to be saved.
'''

NODES_PATH = "nodes.csv"  
WAYS_PATH = "ways.csv"
NODES_TAGS_PATH = "node_tags.csv"
WAYS_TAGS_PATH = "way_tags.csv"
WAYS_NODES_PATH = "ways_nodes.csv"


'''
Fields of elements to be saved.
'''
NODES_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAYS_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODES_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAYS_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAYS_NODES_FIELDS = ['id', 'node_id', 'position']


```


```python
# encoding=utf-8

'''
Creates nodes and node tags CSV files by iterating through OSM file
'''
def create_node_csv_files(osm_file):
    with open(NODES_PATH, 'wb') as nodes_file, open(NODES_TAGS_PATH, 'wb') as nodes_tags_file :
        
        node_writer = csv.DictWriter(nodes_file, fieldnames = NODES_FIELDS, delimiter = ',')
        node_writer.writeheader()
        
        nodes_tags_writer = csv.DictWriter(nodes_tags_file, fieldnames = NODES_TAGS_FIELDS, delimiter = ',')
        nodes_tags_writer.writeheader()
        
        for event, elem in ET.iterparse(osm_file, events=("start",)):
            if elem.tag == "node":
                node = {}
                node['id'] = elem.attrib['id']
                node['lat'] = elem.attrib['lat']
                node['lon'] = elem.attrib['lon']
                node['version'] = elem.attrib['version']
                node['timestamp'] = elem.attrib['timestamp']
                node['changeset'] = elem.attrib['changeset']
                node['uid'] = elem.attrib['uid']
                node['user'] = elem.attrib['user'].encode("utf-8")
                node_writer.writerow(node)
                is_bank = is_bank_node(elem)
                for tag in elem.iter("tag"):
                    node_tag = {}
                    node_tag['id'] = elem.attrib['id']
                    node_tag['type'] = tag.attrib['k'].split(":")[0].encode("utf-8")
                    node_tag['key'] = tag.attrib['k'].split(":")[-1].encode("utf-8")
                    if tag.attrib['k'].split(":")[0].encode("utf-8") == "name" and is_bank:
                        node_tag['value'] = update_bank_name(tag.attrib['v'])
                    else:
                        node_tag['value'] = tag.attrib['v'].encode("utf-8")
                    nodes_tags_writer.writerow(node_tag)
                    
            
'''
Creates ways, way tags and ways_nodes CSV files by iterating through OSM file
'''                
def create_way_csv_files(osm_file):
    with open(WAYS_PATH, 'wb') as ways_file, open(WAYS_TAGS_PATH, 'wb') as ways_tags_file,  open(WAYS_NODES_PATH, 'wb') as ways_nodes_file:
        
        way_writer = csv.DictWriter(ways_file, fieldnames = WAYS_FIELDS, delimiter = ',')
        way_writer.writeheader()
        
        ways_tags_writer = csv.DictWriter(ways_tags_file, fieldnames = WAYS_TAGS_FIELDS, delimiter = ',')
        ways_tags_writer.writeheader()
        
        ways_nodes_writer = csv.DictWriter(ways_nodes_file, fieldnames = WAYS_NODES_FIELDS, delimiter = ',')
        ways_nodes_writer.writeheader()
        
        for event, elem in ET.iterparse(osm_file, events=("start",)):
            if elem.tag == "way":
                way = {}
                way['id'] = elem.attrib['id']
                way['version'] = elem.attrib['version']
                way['timestamp'] = elem.attrib['timestamp']
                way['changeset'] = elem.attrib['changeset']
                way['uid'] = elem.attrib['uid']
                way['user'] = elem.attrib['user'].encode("utf-8")
                way_writer.writerow(way)
                for tag in elem.iter("tag"):
                    way_tag = {}
                    way_tag['id'] = elem.attrib['id']
                    way_tag['type'] = tag.attrib['k'].split(":")[0].encode("utf-8")
                    way_tag['key'] = tag.attrib['k'].split(":")[-1].encode("utf-8")
                    way_tag['value'] = tag.attrib['v'].encode("utf-8")
                    ways_tags_writer.writerow(way_tag)
                idx = 0
                for tag in elem.iter("nd"):
                    way_node = {}
                    way_node['id'] = elem.attrib['id']
                    way_node['node_id'] = tag.attrib['ref']
                    way_node['position'] = idx
                    ways_nodes_writer.writerow(way_node)
                    idx += 1
                    
create_node_csv_files(OSMFILE)                    
create_way_csv_files(OSMFILE)
```

## Seeding to SQL

### Creating tables



```python
import sqlite3

'''
Creating the database tables in SQL.
'''

nodes_table_create_q = "CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL,lat REAL,lon REAL,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT);"
nodes_tags_table_create_q = "CREATE TABLE nodes_tags (id INTEGER,key TEXT,value TEXT,type TEXT,FOREIGN KEY (id) REFERENCES nodes(id));"
ways_table_create_q = "CREATE TABLE ways (id INTEGER PRIMARY KEY NOT NULL,user TEXT,uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT);"
ways_tags_table_create_q = "CREATE TABLE ways_tags (id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,type TEXT,FOREIGN KEY (id) REFERENCES ways(id));"
ways_nodes_table_create_q = "CREATE TABLE ways_nodes (id INTEGER NOT NULL,node_id INTEGER NOT NULL,position INTEGER NOT NULL,FOREIGN KEY (id) REFERENCES ways(id),FOREIGN KEY (node_id) REFERENCES nodes(id));"

con = sqlite3.connect("ankara_turkey_osm.db")
cur = con.cursor()
cur.execute(nodes_table_create_q) 
cur.execute(nodes_tags_table_create_q) 
cur.execute(ways_table_create_q)
cur.execute(ways_tags_table_create_q) 
cur.execute(ways_nodes_table_create_q)
```




    <sqlite3.Cursor at 0x7f3e19a76ce0>



### Seeding the CSVs to DB



```python
import pandas

con.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

'''
CSV files are read into dataframe and seeded into database.
'''

df = pandas.read_csv(NODES_PATH)
df.to_sql("nodes", con, if_exists='append', index=False)

df = pandas.read_csv(WAYS_PATH)
df.to_sql("ways", con, if_exists='append', index=False)

df = pandas.read_csv(NODES_TAGS_PATH)
df.to_sql("nodes_tags", con, if_exists='append', index=False)

df = pandas.read_csv(WAYS_TAGS_PATH)
df.to_sql("ways_tags", con, if_exists='append', index=False)

df = pandas.read_csv(WAYS_NODES_PATH)
df.to_sql("ways_nodes", con, if_exists='append', index=False)

```

## Queries to SQL db


### Banks, ATMs and Branches

Top five banks based on occurances are listed using the query below.

```
Select nodes_tags.value, count(*) as c  FROM nodes_tags WHERE nodes_tags.key == 'name' AND nodes_tags.id IN  (     Select nodes_tags.id FROM nodes_tags WHERE nodes_tags.key='amenity' AND (nodes_tags.value = 'atm' OR nodes_tags.value = 'bank') ) GROUP BY nodes_tags.value ORDER BY c DESC LIMIT 5
```

        iş bankası : 65
        ziraat bankası : 62
        akbank : 49
        garanti bankası : 40
        qnb finansbank : 39


Top five banks having the most number of ATMS are listed using below query.

```
Select nodes_tags.value, count(*) as c  FROM nodes_tags WHERE nodes_tags.key == 'name' AND nodes_tags.id IN  (     Select nodes_tags.id FROM nodes_tags WHERE nodes_tags.key='amenity' AND nodes_tags.value = 'atm' ) GROUP BY nodes_tags.value ORDER BY c DESC LIMIT 5
```

        iş bankası : 24
        akbank : 16
        halkbank : 13
        ziraat bankası : 13
        garanti bankası : 11
        
        
        
İş Bankası (first bank of Turkey) has more accurances than the other banks. Although Ziraat Bankası placed top in branches list, other banks like Akbank has more ATMs based on OSM.


## Data Overview and Additional Ideas

This section includes basic statistics about the dataset, and some additional ideas about data in context.

### Data Overview

The sizes of files are :

|   File Name   	|  Size 	|
|:-------------:	|:-----:	|
|   Nodes.csv   	| 102MB 	|
|    Ways.csv   	|  11MB 	|
| Node_tags.csv 	|  1MB  	|
| Way_tags.csv  	| 10MB  	|
| Way_nodes.csv 	| 36MB  	|



#### Number of Nodes
```
SELECT COUNT(*) FROM nodes;
```

1314728

#### Number of Ways

```
SELECT COUNT(*) FROM ways;
```

203780

#### Number of Tags
```
SELECT COUNT(*) FROM nodes_tags;
```
41524


```
SELECT COUNT(*) FROM ways_tags;
```
337673 
 
#### Top 10 Contributing users
```
SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
```

|     User     	| Number of Contributions 	|
|:------------:	|:-----------------------:	|
| Nesim        	| 434963                  	|
| penom        	| 262943                  	|
| turankaya74  	| 199755                  	|
| katpatuka    	| 138256                  	|
| summerson    	| 126924                  	|
| nawt12       	| 24027                   	|
| VinothS      	| 22414                   	|
| dogukann     	| 21259                   	|
| gezginrocker 	| 16865                   	|
| İşfatay      	| 13044                   	|

> It is seen that there need to be more contributers to make the Ankara region data more complete. Combined top five users have the most contributions, almost 80%.  


#### Number of Distinct Users

```
SELECT count(distinct(e.user))
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e;
```

863


### Additional Data Exploration

#### Top 10 appering amenities in Ankara

```
SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```

|   Amenity  	|   #  	|
|:----------:	|:----:	|
| pharmacy   	| 1055 	|
| shelter    	| 738  	|
| restaurant 	| 405  	|
| bank       	| 353  	|
| cafe       	| 250  	|
| fuel       	| 229  	|
| atm        	| 176  	|
| fast_food  	| 172  	|
| taxi       	| 159  	|
| parking    	| 148  	|


#### Touristic Attractions

```
SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='tourism'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```

|   Tourism   	|  # 	|
|:-----------:	|:--:	|
| hotel       	| 30 	|
| artwork     	| 17 	|
| museum      	| 9  	|
| guest_house 	| 7  	|
| picnic_site 	| 7  	|
| attraction  	| 6  	|
| camp_site   	| 2  	|
| hostel      	| 2  	|
| information 	| 2  	|
| viewpoint   	| 1  	|

> Touristic attractions are not complete in Ankara. Although hotels are seem to be more complete this is beacuse those places are privately held, other attractions like artwork, museums and information are not complete enough. Turkish State shall contribute more in order to attract more tourists since many applications use this data. <br>
> This improvement has <b>benefits</b> for the touristic attractions to be easy to find for tourists. Of course there would be some problems while improving the completeness of the data. Turkish state itself may not be capable of filling such information. This problem may be solved by crowdsourcing instruments. Tourists may check-in those places or create new places in a platform for the State.   



#### Artwork Types

```
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE key='tourism' and value='artwork') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='artwork_type'
GROUP BY nodes_tags.value
ORDER BY num DESC;
```

| Artwork Type 	| # 	|
|:------------:	|:-:	|
| statue       	| 6 	|
| relief       	| 4 	|
| sculpture    	| 3 	|
| bust         	| 1 	|
| mural        	| 1 	|
| stone        	| 1 	|




## Conclusion



This review of the data shows that the openmaps dataset for Ankara is inclomplete since there are a few records of branches and ATMs. This might caused by the limited set of contributers in this context. 

Moreover, dataset is also incomplete in terms of touristic attractions. The state shall contribute more to openstreetmap.org.


