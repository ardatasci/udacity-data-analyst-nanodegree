# encoding=utf8
import xml.etree.cElementTree as ET
import pprint
import re
import csv
import sqlite3
import pandas


OSMFILE = "ankara_turkey.osm"


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

'''
Creates csv files by giving arrays, headers and the csv file location to be saved.
'''
def create_csv(arr, headers, path):
    with open(path, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers, delimiter = ',')
        writer.writeheader()
        for el in arr:
            writer.writerow()


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

'''
Creating the database tables in SQL.
'''
def create_tables():
    global OSMFILE

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
    create_node_csv_files(OSMFILE)
    create_way_csv_files(OSMFILE)

'''
CSV files are read into dataframe and seeded into database.
'''
def seed_csv_to_db():

    con = sqlite3.connect("ankara_turkey_osm.db")
    con.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

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


if __name__ == "__main__":
    create_node_csv_files(OSMFILE)
    create_way_csv_files(OSMFILE)
    create_tables()
    seed_csv_to_db()
