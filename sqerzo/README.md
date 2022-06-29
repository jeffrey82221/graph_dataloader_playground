# How to install sqerzo for our environment? 
- [X] fork SQERZO to your github account
- [X] git clone from source
- [X] modify the code to fit python3.7/3.6 and neo4j community edition

# To fit python3.7:

- [X] remove all a:=b marks and make them a = b 

# To fit neo4j community edition: 
- [ ] remove `XXX` from property constraint cypher: `CREATE CONSTRAINT XXX ON ()-[p:{label}]-() ASSERT EXISTS (p.{key})` because "Property existence constraint requires Neo4j Enterprise Edition"

# To fit python3.6: 

- [X] remove `from __future__ import annotations`
- [X] replace `cls.__annotations__` by `typing.get_type_hints(cls)`
- [X] re-order the classes so that class are defined before used
- [X] replace clone return from `GraphElement` to `GraphElementMetaClass`