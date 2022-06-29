wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
apt update
apt install neo4j
# NOTE: 
# Community Edition May Cause Error: Property existence constraint requires Neo4j Enterprise Edition
# - CREATE CONSTRAINT constraint_edge IF NOT EXISTS ON ()-[p:Label]-() ASSERT EXISTS (p.Key); 
# -> Unable to create Constraint( type='RELATIONSHIP PROPERTY EXISTENCE', schema=-[:Label {Key}]- ):
