# CONTENTdm IIIF Collectiom Manifest Creator
This code is experimental and offered as-is. 

Currently there is not logic to:
* genreate Paged Manifest lists - this is due to the lack of persistant URIs for the individual pages. Needs to be solved within the context of the deployment strategy
* test if the generated Item Manifests exist - the code simply generated Item Manifest URIs based on the Collection record IDs 

## Requirements
* Python 2.7
* CONTENTdm Host ID
* CONTENTdm Collection ID

## Instructions
* Clone the GitHub Repo
* Run the python code providing a -host_id and -collection_id parameter values

## Example Python run command
`python collection-manifest-producer.py -host_id 'cdm15890' -collection_id 'p15890coll3'`
