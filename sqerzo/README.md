# How to install sqerzo for python3.7? 

- [ ] git clone from source
- [ ] modify the code to fit python3.7 and neo4j community edition

# To fit python3.7:

- [ ] remove all a:=b marks and make them a = b 

# To fit neo4j community edition: 

- [ ] remove `XXX` from cypher: `CREATE CONSTRAINT XXX ON ()-[p:{label}]-() ASSERT EXISTS (p.{key})`
- [ ] remove `XXX` from cypher: `CREATE CONSTRAINT {constrain_name}_unique_{key} IF NOT EXISTS ON (p:{label}) ASSERT p.{key} IS UNIQUE`
- [ ] remove the `CREATE INDEX` cypher

# To fit python3.6: 

- [ ] remove `from __future__ import annotations`
- [ ] replace __annotations__ by get_type_hints(cls) of typing
- [ ] re-order the classes so that class are defined before used
