# Aminer Data 2 Knowledge Graph Triples and Embedding

You should download academic social network data from [Aminer](https://www.aminer.cn/aminernetwork) and replace variable 'f' in each .py file accordingly.


## Triples
- author2csv.py includes
  - e_author.csv: author entity
  - e_affiliation: affiliation entity
  - e_concept.csv: concept entity
  - r_author2affiliation.csv: relation between author and affiliation
  - r_author2concept.csv: relation between author and concept
- author2paper2csv.py includes
  - r_author2paper.csv: relation between author and paper
- paper2csv.py includes
  - e_paper.csv: paper entity
  - e_venue.csv: venue entity
  - r_paper2venue.csv: relation between paper and venue
  - r_citation.csv: relation between papers
  - r_coauthor.csv: relation between authors
  
Then Neo4j is used to visualize these csv files.

## Import to Neo4j

```CYPHER
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///e_author.csv" AS line
CREATE (author:AUTHOR{authorID:line.authorID, authorName:line.authorName, pc:line.pc, cn:line.cn, hi:line.hi, pi:line.pi, upi:line.upi})

USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///e_affiliation.csv" AS line
CREATE (affiliation:AFFILIATION{affiliationID:line.affiliationID, affiliationName:line.affiliationName})

USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///e_concept.csv" AS line
CREATE (concept:CONCEPT{conceptID:line.conceptID, conceptName:line.conceptName})

USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///e_paper.csv" AS line
CREATE (paper:PAPER{paperID:line.paperID, paperTitle:line.title, paperYear:line.year, paperAbstract:line.abstract})

USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///e_venue.csv" AS line
CREATE (venue:VENUE{venueID:line.venueID, venueName:line.name})

CREATE INDEX ON: AUTHOR(authorID)

CREATE INDEX ON: AFFILIATION(affiliationID)

CREATE INDEX ON: CONCEPT(conceptID)

CREATE INDEX ON: PAPER(paperID)

CREATE INDEX ON: VENUE(venueID)



USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///r_author2affiliation.csv" AS line
MATCH (FROM:AUTHOR{authorID:line.START_ID}), (TO:AFFILIATION{affiliationID:line.END_ID})
MERGE (FROM)-[AUTHOR2AFFILIATION: AUTHOR2AFFILIATION{type:line.TYPE}]->(TO)


USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///r_author2concept.csv" AS line
MATCH (FROM:AUTHOR{authorID:line.START_ID}), (TO:CONCEPT{conceptID:line.END_ID})
MERGE (FROM)-[AUTHOR2CONCEPT: AUTHOR2CONCEPT{type:line.TYPE}]->(TO)

USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///r_author2paper.csv" AS line
MATCH (FROM:AUTHOR{authorID:line.START_ID}), (TO:PAPER{paperID:line.END_ID})
MERGE (FROM)-[AUTHOR2PAPER: AUTHOR2PAPER{type:line.TYPE, author_pos:line.author_position}]->(TO)


USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///r_citation.csv" AS line
MATCH (FROM:PAPER{paperID:line.START_ID}), (TO:PAPER{paperID:line.END_ID})
MERGE (FROM)-[CITATION: CITATION{type:line.TYPE}]->(TO)


USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///r_coauthor.csv" AS line
MATCH (FROM:AUTHOR{authorID:line.START_ID}), (TO:AUTHOR{authorID:line.END_ID})
MERGE (FROM)<-[COAUTHOR: COAUTHOR{type:line.TYPE, n_cooperation:line.n_cooperation}]->(TO)

USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM "file:///r_paper2venue.csv" AS line
MATCH (FROM:PAPER{paperID:line.START_ID}), (TO:VENUE{venueID:line.END_ID})
MERGE (FROM)-[PAPER2VENUE: PAPER2VENUE{type:line.TYPE}]->(TO)


--- 

CREATE INDEX ON: AUTHOR(authorName)

CREATE INDEX ON: AFFILIATION(affiliationName)

CREATE INDEX ON: CONCEPT(conceptName)

CREATE INDEX ON: PAPER(paperTitle)

CREATE INDEX ON: VENUE(venueName)

```
  
## Embedding
After generating csv files, you can execute data4embedding.py to divide relations into train, valid and test sets(98:1:1) which will be fed to [PyTorch BigGraph](https://github.com/facebookresearch/PyTorch-BigGraph).

Training:

```bash
torchbiggraph_import_from_tsv --lhs-col=0 --rel-col=1 --rhs-col=2 new_config.py rel9811/train.txt rel9811/valid.txt rel9811/test.txt

torchbiggraph_train new_config.py -p edge_paths=rel9811/train_p

torchbiggraph_eval new_config.py -p edge_paths=rel9811/test_p -p relations.0.all_negs=true -p num_uniform_negs=0

torchbiggraph_export_to_tsv new_config.py --entities-output entity_embeddings.tsv --relation-types-output relation_types_parameters.tsv

```
