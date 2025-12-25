---
layout: post
title: Neo4j for Beginners (Part 2)- Cypher Fundamentals
---

In [Part 1](https://sponug.github.io/Thinking-In-graphs/), we learned what makes graph databases different: data is stored as nodes (things) and relationships (connections), and those connections are first-class citizens in the database. We also wrote your first Cypher query to find patterns in banking data.
Now it's time to go deeper. In this article, lets learn how to create your own graph data, master essential Cypher clauses, and write the queries that make graphs truly powerful.


# Table of contents
1. [Graph Database Fundamentals: The Building Blocks](#fundamentals)
2. [Setting Up Your Practice Environment](#environment)
3. [Creating Your Banking Graph](#bankgraph)
4. [Essential Cypher Clauses](#essential)
5. [Your First Multi-Hop Query](#hop)

## Graph Database Fundamentals: The Building Blocks <a name="fundamentals"></a>
Before we start creating data and writing queries, let's establish a solid foundation by understanding the core concepts that make up Neo4j's property graph model. These fundamentals will guide everything you do with graph databases.

### The Property Graph Model
Neo4j uses a property graph database model. At its core, a graph data structure consists of nodes (discrete objects) that can be connected by relationships. Think of it like a network or mind map where circles represent things and arrows represent connections between those things.
Here's the simplest possible visualization:

```Cypher
(Node A) --[RELATIONSHIP]--> (Node B)
```

The Neo4j property graph model consists of ***five fundamental*** building blocks:
- **Nodes** - Represent entities or discrete objects in your domain
- **Labels** - Classify and group nodes into sets
- **Relationships** - Connect nodes and describe how they're related
- **Relationship Types** - Classify relationships
- **Properties** - Store data as key-value pairs on both nodes and relationships

Let's explore each of these in detail.

#### Nodes: The Things in Your Graph
Nodes are used to represent entities — the discrete objects in your domain. In our banking context, customers, products, accounts, and transactions would all be nodes.Key characteristics of nodes:

- A node can have zero or more labels
- A node can have zero or more properties
- Nodes can exist independently (a node doesn't need relationships)
- The simplest possible graph is a single node with no relationships:

```Cypher
(Customer)
```
***Nodes represent the "nouns" of your domain — the people, places, things, or concepts that matter to your application.***

### Labels: Classifying Your Nodes

Labels shape your domain by grouping nodes into sets. All nodes with a certain label belong to the same set, which allows you to perform operations on specific types of nodes. Key characteristics of labels:

- A node can have zero to many labels
- Labels can be added or removed at runtime
- Labels are case-sensitive (:Person is different from :person)
  
Examples:
- All customer nodes could be labeled :Customer
- A person who is both a customer and an actor could have labels ``` Cypher :Person:Customer:Actor ```
- You can use labels for temporary states: :Suspended for suspended accounts, :Active for active products
- In the example below, a single node has multiple labels to describe different dimensions: (tom:Person:Actor:Customer)
- This flexibility lets you query nodes from different perspectives. You might ask for "all Persons" in one query and "all Actors" in another, even if some nodes satisfy both criteria

### Relationships: The Connections Between Things
A relationship describes a connection between a source node and a target node. This is where graphs truly differ from relational databases—relationships are not inferred or calculated; they're stored directly as first-class data structures.Key characteristics of relationships:

- Connects exactly one source node to one target node
- Always has a direction (though you can ignore direction in queries when appropriate)
- Must have exactly one relationship type
- Can have properties (key-value pairs)
- A node can have a relationship to itself
Example relationship:
```Cypher
(alice:Customer)-[:USES {since: date('2020-01-15'), status: 'active'}]->(savings:Product)
```
This shows:
- Source node: alice (a Customer)
- Relationship type: USES
- Direction: From alice to savings (indicated by ->)
- Properties: since and status stored on the relationship itself
- Target node: savings (a Product)
- Relationships always have a direction, but you can traverse them in either direction or ignore direction entirely when querying. **The direction is part of the data model and can carry semantic meaning—"Alice USES Product" is different from "Product USED_BY Alice," even though they describe the same connection from different perspectives.**
- Important: A node can have a relationship to itself. For example, if Tom Hanks knows himself:
```Cypher
(tom:Person)-[:KNOWS]->(tom)
```

### Relationship Types: Classifying Connections
Just as labels classify nodes, relationship types classify relationships. Every relationship must have exactly one type.
Key characteristics:
- A relationship has exactly one type (unlike labels, you can't have multiple)
- Types define the semantic meaning of the connection
- Types are case-sensitive
- Common relationship types in banking:
  - :USES - Customer uses Product
  - :OWNS - Customer owns Account
  - :ISSUED_BY - Card issued by Bank
  - :TRANSFERS_TO - Account transfers to Account
- The relationship type tells you how two nodes are connected. This is crucial for traversals—when you follow relationships, you often want to follow only specific types. You might want to find "all products a customer USES" without including "all accounts they OWN."

### Properties: Storing Data
Properties are key-value pairs that store data on both nodes and relationships. They're where you put the actual information about your entities and connections.
Key characteristics:
- Properties are stored as key-value pairs
- Both nodes and relationships can have properties
- Values can be primitives (numbers, strings, booleans) or homogeneous arrays
- Properties are case-sensitive
- Naming convention: Use camelCase for properties (firstName rather than first_name)
- Supported data types:
```Cypher
Numbers:
CREATE (:Example {count: 42, price: 19.99})

Strings and booleans:
CREATE (:Example {name: 'Alice', active: true})

Dates and temporal types:
CREATE (:Customer {since: date('2020-01-15'), lastLogin: datetime()})

Arrays (homogeneous lists):
CREATE (:Example {
  tags: ['premium', 'verified'],
  scores: [95, 87, 92],
  active: [true, false, true]
})
```
Important: Properties are only stored when they have values. There's no concept of null values being stored—if a property isn't set, it simply doesn't exist on that node or relationship.

## Setting Up Your Practice Environment <a name="environment"></a>
Neo4j Sandbox runs entirely in your browser—no installation required. Visit [sandbox.neo4j.com](sandbox.neo4j.com), create a free account, and launch a blank sandbox. Within seconds, you'll have a working Neo4j instance with the Browser interface ready to go. This is perfect if you want to start immediately without worrying about setup. If you're using a sandbox that has sample data, or if you want to start fresh at any point, you can clear everything with:

```Cypher
MATCH (n) DETACH DELETE n
```
This finds all nodes (MATCH (n)), detaches them from their relationships, and deletes everything. This was very useful for the exercise below .

## Creating Your Banking Graph <a name="bankgraph"></a>

In [Part 1](https://sponug.github.io/Thinking-In-graphs/), you queried existing data. Now you'll learn how to create it yourself. Neo4j uses the CREATE clause to add nodes and relationships to your graph.

### Creating Nodes

Let's start by creating some customers. Each customer is a node with properties that describe them:
```Cypher
CREATE (alice:Customer {id: 'C001', name: 'Alice', since: date('2020-01-15')})
```

Let's break down what's happening here:
- CREATE tells Neo4j we're adding something new
- (alice:Customer ...) creates a node. The word before the colon (alice) is a variable we can use in this query, and the word after (:Customer) is a label that categorizes this node
- {id: 'C001', name: 'Alice', since: date('2020-01-15')} are properties—key-value pairs that store information about this customer
- The date() function creates a proper date object rather than just text

Run that query, then create a few more customers:

```Cypher
CREATE (bob:Customer {id: 'C002', name: 'Bob', since: date('2021-03-20')})
CREATE (carol:Customer {id: 'C003', name: 'Carol', since: date('2019-07-10')})
CREATE (david:Customer {id: 'C004', name: 'David', since: date('2022-06-05')})
```

Each CREATE statement adds one node to your graph. You should see a confirmation message after each one: "Added 1 node."

### Creating Products
Now let's add the banking products these customers might use:

```Cypher
CREATE (savings:Product {code: 'SAV-001', name: 'Savings Account', category: 'Deposit'})
CREATE (checking:Product {code: 'CHK-001', name: 'Checking Account', category: 'Deposit'})
CREATE (credit:Product {code: 'CRD-001', name: 'Credit Card', category: 'Credit'})
CREATE (loan:Product {code: 'LON-001', name: 'Personal Loan', category: 'Credit'})
CREATE (mortgage:Product {code: 'MTG-001', name: 'Mortgage', category: 'Credit'})
```

Notice we're using different properties here (code, name, category) because products need different information than customers. This flexibility is one of the strengths of graph databases—different node types can have completely different properties.

### Creating Relationships
Now comes the interesting part: connecting customers to products. This is where graphs really shine. We need to find the nodes we want to connect, then create a relationship between them:

```Cypher
MATCH (alice:Customer {id: 'C001'})
MATCH (savings:Product {code: 'SAV-001'})
CREATE (alice)-[:USES {since: date('2020-01-15'), status: 'active'}]->(savings)
```

Let's understand this step by step:
- The first MATCH finds Alice (the customer we created earlier)
- The second MATCH finds the Savings Account product
- CREATE (alice)-[:USES ...]-> (savings) creates a relationship from Alice to the Savings Account
- The relationship type is USES (inside the square brackets)
- The direction matters: the arrow -> points from customer to product, meaning "Alice uses Savings Account"
- Relationships can have properties too: we're storing when the relationship started and its current status

Add several more relationships to build out our dataset:


```Cypher
MATCH (alice:Customer {id: 'C001'})
MATCH (credit:Product {code: 'CRD-001'})
CREATE (alice)-[:USES {since: date('2020-06-10'), status: 'active'}]->(credit)
--

MATCH (bob:Customer {id: 'C002'})
MATCH (checking:Product {code: 'CHK-001'})
CREATE (bob)-[:USES {since: date('2021-03-20'), status: 'active'}]->(checking)
--

MATCH (bob:Customer {id: 'C002'})
MATCH (credit:Product {code: 'CRD-001'})
CREATE (bob)-[:USES {since: date('2021-08-15'), status: 'active'}]->(credit)
--
MATCH (bob:Customer {id: 'C002'})
MATCH (loan:Product {code: 'LON-001'})
CREATE (bob)-[:USES {since: date('2023-01-10'), status: 'active'}]->(loan)
--
MATCH (carol:Customer {id: 'C003'})
MATCH (savings:Product {code: 'SAV-001'})
CREATE (carol)-[:USES {since: date('2019-07-10'), status: 'active'}]->(savings)
--
MATCH (carol:Customer {id: 'C003'})
MATCH (checking:Product {code: 'CHK-001'})
CREATE (carol)-[:USES {since: date('2019-07-10'), status: 'active'}]->(checking)
--
MATCH (carol:Customer {id: 'C003'})
MATCH (mortgage:Product {code: 'MTG-001'})
CREATE (carol)-[:USES {since: date('2020-11-20'), status: 'active'}]->(mortgage)
--
MATCH (david:Customer {id: 'C004'})
MATCH (credit:Product {code: 'CRD-001'})
CREATE (david)-[:USES {since: date('2022-06-05'), status: 'active'}]->(credit)
--
MATCH (david:Customer {id: 'C004'})
MATCH (loan:Product {code: 'LON-001'})
CREATE (david)-[:USES {since: date('2023-09-12'), status: 'active'}]->(loan)
--
```
After running all these queries, we've built a small but complete banking graph. We have customers, products, and the relationships between them—including metadata about when each relationship started and whether it's currently active.




