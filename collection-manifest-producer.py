from __future__ import print_function
import dateutil.parser
import datetime
import json
import uuid
import urllib2
import sys
import argparse
import time

#  This code takes a CONTENTdm Host ID and Collection ID and produces a IIIF Collection Manifest file
#
#  Script pattern:
#  python -host_id <CDM Host ID> -collection_id <CDM Collection ID> 
#
#  Example:
#  python collection-manifest-producer.py -host_id 'cdm15890' -collection_id 'p15890coll3'

def main():
    
    global f
    global collection_blob
    
    # open file for Collection Manifest to be written to
    # TODO: make the file related to the CDM Host and Collection ID
    f = open('manifest/collectionManifest.json', 'w+')
    
    # set the arguments for the script
    parser = argparse.ArgumentParser()
    parser.add_argument('-host_id', help='The ID for the CDM host', required=True)
    parser.add_argument('-collection_id', help='The ID for the CDM collection', required=True)
    args = parser.parse_args()
    # convert args to variables
    host_id = args.host_id
    collection_id = args.collection_id

    # initialize the collection
    collection_blob = {}
    # Since CDM IIIF Collection Manifest have no permanent URIs use a UUID as the URI
    # THIS SHOULD BE FIXED FOR A PRODUCTION INSTALL SO THE COLLECTIOM MANIFEST URI IS A PERSISTANT LINKED DATA URI
    collection_uri = 'http://example.com/' + str(uuid.uuid4())
    collection_blob['@context'] = 'http://iiif.io/api/presentation/2/context.json'
    collection_blob['@type'] = 'sc:Collection'
    collection_blob['@id'] = collection_uri
    collection_blob['label'] = 'IIIF collection of manifests for all compound objects within CONTENTdm collection '+collection_id
    collection_blob['manifests'] = []

    number_of_results = 200
    #set starting loop variables
    starting_record = 1
    parse_collection(host_id, collection_id, starting_record, number_of_results)
    


def parse_collection(host_id, collection_id, starting_record, number_of_results):
    # convert the parameters into a CDM Collection API call and retrieve the collection data (title and item IDs)
    collection_url = 'https://' + host_id + '.contentdm.oclc.org/digital/bl/dmwebservices/index.php?q=dmQuery/' + collection_id + '/0/title/title/' + str(number_of_results) + '/' + str(starting_record) + '/1/0/0/0/0/0/json'
    collection_response = urllib2.urlopen(collection_url)
    collection_data = json.loads(collection_response.read())
    create_collection(collection_data, host_id, collection_id, starting_record, number_of_results)
    
def create_collection(collection_data, host_id, collection_id, starting_record, number_of_results):
    # Loop through all of the items in the collection and append them to the Manifest list
    for rec in collection_data['records']:
        manifest = {}
        item_id = rec['pointer']
        # TODO: Test the resulting Manifest URI to make sure it exists
        manifest['@id'] = 'https://' + host_id + '.contentdm.oclc.org/digital/iiif-info/' + collection_id + '/' + str(item_id) + '/manifest.json'
        manifest['label'] = rec['title']
        manifest['@type'] = 'sc:Manifest'
        collection_blob['manifests'].append(manifest)
    
    # If the length of the record response is 200 then there are more records to in the collection
    if len(collection_data['records']) == 200:
        starting_record = starting_record + 200
        # Be a good citizen and pause 3 second before another request
        time.sleep(3)
        parse_collection(host_id, collection_id, starting_record, number_of_results)
    # If the length of the record response is less than 200 than there are no more records to grab and the data can be written to disk
    else:
        collection_json = json.dumps(collection_blob)
        write_collection_manifest(collection_json)


def write_collection_manifest(collection_json):
    # writes data to disk
    data = (collection_json)
    f.write(data)
    
if __name__ == "__main__":
        main()
