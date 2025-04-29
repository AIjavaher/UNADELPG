import pandas as pd
from neo4j import GraphDatabase

csv_file = '/Users/ensiyehj/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/dbms-3e4f38bb-4558-4369-be00-0f72222925c2/import/water_startend_3D_linegeo_size_v01_interexter.csv'
data = pd.read_csv(csv_file)
xx = 5
uri = "bolt://localhost:7687"  # Update with your Neo4j connection details
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))


def create_nodes(tx, row):
    start = row['start_point3D']
    end = row['end_point3D']
    curve = row['wkt_geom']
    objectid = row['OBJECTID']
    segment_id = row['segment_id']
    type_start = row['type_start']
    type_end = row['type_end']
    state = row['STATE']
    owner = row['ASSET_OWNE']
    g3e_cid = row['G3E_CID']
    g3e_cno = row['G3E_CNO']
    g3e_fno = row['G3E_FNO']
    featuretype = row['FEATURE_TY']

    tx.run("""
        MERGE (ns:Node {geometry: $start, type: $type_start})
        MERGE (ne:Node {geometry: $end, type: $type_end})
        MERGE (ngs:Geo {geometry: $start})
        MERGE (nge:Geo {geometry: $end})
        MERGE (nga:Geo {geometry: $curve})
        MERGE (abs:AbstractLink {geometry: $curve, Direction:'Gravity'})
        MERGE (inter:InteriorFeatureLink {id: $segment_id, geometry: $curve})
        MERGE (fg:FeatureGraph {id: $objectid})
        MERGE (ng:NetworkGraph {representation: '3DSolid'})
        MERGE (anf:AbstractNetworkFeature {cid: $g3e_cid, cno: $g3e_cno, fno: $g3e_fno, state: $state, owner: $owner})
        MERGE (n:Network {featuretype: $featuretype, state: $state, owner: $owner})
        MERGE (ns)-[:STARTNODE]->(ngs)
        MERGE (ne)-[:STARTNODE]->(nge)
        MERGE (abs)-[:STARTNODE]->(nga)
        MERGE (abs)-[:STARTNODE]->(ns)
        MERGE (abs)-[:ENDNODE]->(ne)
        MERGE (inter)-[:ENDNODE]->(abs)
        MERGE (fg)-[:INTERIORFEATURELINK]->(inter)
        MERGE (ng)-[:FEATUREGRAPH_NG]->(fg)
        MERGE (anf)-[:FEATUREGRAPH_ANF]->(fg)
        MERGE (n)-[:NETWORKGRAPH]->(anf)
    """, start=start, type_start=type_start, type_end=type_end, end=end, curve=curve, segment_id=segment_id,
           objectid=objectid, g3e_cid=g3e_cid, g3e_cno=g3e_cno, g3e_fno=g3e_fno, state=state, owner=owner,
           featuretype=featuretype)


with driver.session(database="waterpipes") as session:
    for _, row in data.iterrows():
        session.write_transaction(create_nodes, row)

# Close the driver after use
driver.close()


