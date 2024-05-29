import sys
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

sys.path.append(os.getenv("PY_MODULES_PATH"))

import logger_tool as logger
log_level = os.getenv('LOG_LEVEL')
logger_name = 'logger_tool'
logging = logger.get_logger(name=logger_name, log_level=log_level)

import time
from neo4j import GraphDatabase as gd

logging.prod(f"Importing Neo4j driver tools...")

# Function to get the Neo4j driver
def get_driver(url=None, auth=None):
    if url is None:
        host = os.getenv("NEO_HOST")
        port = os.getenv("NEO_PORT")
        url = f"bolt://{host}:{port}"
        auth = (os.getenv("NEO_USER"), os.getenv("NEO_PASSWORD"))
    else:
        logging.testing(f"Using scripted Neo4j connection: {url}")
    logging.prod(f"Creating a Neo4j driver with URL and auth: {url}, {auth}")
    driver = None
    # Try to create the driver. If it fails, retry in 10 seconds and repeat 3 times
    connection_attempts = 0
    while driver is None:
        connection_attempts += 1
        try:
            driver = gd.driver(url, auth=auth)
        except Exception as e:
            if connection_attempts < 3:
                logging.prod(f"Retrying Neo4j driver creation in 3 seconds... (Attempt {connection_attempts})")
                time.sleep(3)
            else:
                logging.error(f"Failed to create Neo4j driver after {connection_attempts} attempts.")
                return None            
    logging.prod(f"Neo4j driver created: {driver}")
    # Test the connection
    with driver.session() as session:
        logging.prod(f"Testing Neo4j connection with session: {session}")
        query = "RETURN 1 AS number"
        logging.query("Running query: {query}")
        result = session.run(query)
        if result.single()["number"] == 1:
            logging.prod("Neo4j connection test passed.")
        else:
            logging.error("Neo4j connection test failed.")
    return driver

def close_session(session):
    """
    Closes a Neo4j session.

    Parameters:
    - session: The Neo4j session to be closed.
    """
    if session:
        try:
            # Attempt to close the session if it's not already closed
            logging.database(f"Closing Neo4j session: {session}")
            session.close()
        except Exception as e:
            # Handle any exceptions that occur during session closure
            logging.error(f"An error occurred while closing the Neo4j session: {e}")


# Function to close the Neo4j driver
def close_driver(driver):
    logging.prod(f"Closing Neo4j driver: {driver}")
    driver.close()

# Function to create a node in Neo4j
def create_node(session, label, properties, returns=False):
    """
    Function to create a node in Neo4j database.
    
    Args:
        driver (neo4j.Driver): The Neo4j driver.
        session (str): The Neo4j session.
        label (str): The label of the node.
        properties (dict): A dictionary of properties for the node.
        
    Example usage:
        create_node(neo4j_driver, "Topic", {"TopicID": "AP.PAG10", "Title": "Topic 10"})
        
    Returns:
        None
    """
    transaction = session.write_transaction(_create_node, label, properties)
    if returns:
        transaction_id = transaction.id
        logging.database(f"Created {label} node with transaction ID {transaction_id} and properties {properties}")
        created_node = find_node_by_transaction_id(session, transaction_id)
        return created_node
    else:
        
        logging.warning(f"Failed to create {label} node with properties {properties}")
        return None

def _create_node(tx, label, properties):
    query = f"""
    CREATE (n:{label} $properties)
    RETURN n
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, properties=properties)
    return result.single()[0]

# Function to find a node by its element ID
def find_node_by_transaction_id(session, transaction_id):
    """
    Function to find a node in Neo4j database by its element ID.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        element_id (str): The element ID of the node to find.

    Returns:
        The matched node.
    """
    return session.read_transaction(_find_node_by_element_id, transaction_id)
    
def _find_node_by_element_id(tx, transaction_id):
    query = f"""
    MATCH (n)
    WHERE id(n) = $transaction_id
    RETURN n
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, transaction_id=transaction_id)
    record = result.single()  # Get the single result record, if any
    if record is None:
        logging.warning("No node found with the given transaction ID.")
        return None
    else:
        node = record[0]
        return node

# Function to create a relationship between two nodes in Neo4j
def create_relationship(session, start_node, end_node, label, properties=None, returns=False):
    """
    Function to create a relationship between two nodes in Neo4j database.
    
    Args:
        driver (neo4j.Driver): The Neo4j driver.
        session (str): The Neo4j session.
        start_node (str): The ID of the start node.
        end_node (str): The ID of the end node.
        rel_type (str): The type of the relationship.
        properties (dict): A dictionary of properties for the relationship.
        
    Example usage:
        create_relationship(neo4j_driver, "AP.PAG10", "AP.PAG11", "HAS_NEXT")
        
    Returns:
        None
    """
    relationship = session.write_transaction(_create_relationship, start_node, end_node, label, properties)
    if returns:
        relationship_id = relationship.id
        created_relationship = find_relationship_by_relationship_id(session, relationship_id)
        return created_relationship
    else:
        return None
        
def _create_relationship(tx, start_node, end_node, label, properties):
    query = f"""
    MATCH (a), (b)
    WHERE ID(a) = $start_node_id AND ID(b) = $end_node_id
    CREATE (a)-[r:{label}]->(b)
    RETURN r
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, start_node_id=start_node.id, end_node_id=end_node.id, properties=properties)
    single_result = result.single()
    if single_result is not None:
        logging.database(f"Created relationship between nodes: {start_node} {label} {end_node}")
        return single_result[0]
    else:
        logging.warning(f"Failed to create relationship between nodes: {start_node}, {end_node}")
        return None

def order_list_of_nodes_by_property(session, label, property_name, order="ASC"):
    """
    Function to order a list of nodes in Neo4j database by a property.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        property_name (str): The name of the property to order by.
        order (str): The order of the sorting (ASC or DESC).

    Returns:
        List of matched nodes.
    """
    return session.read_transaction(_order_list_of_nodes_by_propery, label, property_name, order)

def _order_list_of_nodes_by_propery(tx, label, property_name, order):
    query = f"""
    MATCH (n:{label})
    RETURN n
    ORDER BY n.{property_name} {order}
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query)
    records = [record["n"] for record in result]
    return records

def find_relationship_by_relationship_id(session, relationship_id):
    """
    Function to find a relationship in Neo4j database by its relationship ID.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        relationship_id (str): The relationship ID of the relationship to find.

    Returns:
        The matched relationship.
    """
    return session.read_transaction(_find_relationship_by_relationship_id, relationship_id)
    
def _find_relationship_by_relationship_id(tx, relationship_id):
    query = f"""
    MATCH ()-[r]->()
    WHERE id(r) = $relationship_id
    RETURN r
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, relationship_id=relationship_id)
    record = result.single()  # Get the single result record, if any
    if record is None:
        logging.warning("No relationship found with the given relationship ID.")
        return None
    else:
        relationship = record[0]
        return relationship

# Function to create a relationship between two nodes in two different databases
def create_relationship_between_databases(session, start_database, start_node, end_database, end_node, label, properties=None, returns=False):
    """
    BROKEN function to create a relationship between two nodes in two different databases.
    
    Args:
        driver (neo4j.Driver): The Neo4j driver.
        start_database (str): The name of the start database.
        start_node (str): The ID of the start node.
        end_database (str): The name of the end database.
        end_node (str): The ID of the end node.
        rel_type (str): The type of the relationship.
        properties (dict): A dictionary of properties for the relationship.
        
    Example usage:
        create_relationship_between_databases(neo4j_driver, "AP", "AP.PAG10", "PAG", "PAG.PAG11", "HAS_NEXT")
        
    Returns:
        None
    """
    relationship = session.write_transaction(_create_relationship_between_databases, start_database, start_node, end_database, end_node, label, properties)
    if returns:
        relationship_id = relationship.id
        created_relationship = find_relationship_by_relationship_id(session, relationship_id)
        return created_relationship
    else:
        return None

def _create_relationship_between_databases(tx, start_database, start_node, end_database, end_node, label, properties):
    query = f"""
    MATCH (a:{start_database}), (b:{end_database})
    WHERE a.id = $start_node_id AND b.id = $end_node_id
    CREATE (a)-[r:{label}]->(b)
    RETURN r
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, start_node_id=start_node, end_node_id=end_node, properties=properties)
    single_result = result.single()
    if single_result is not None:
        return single_result[0]
    else:
        logging.warning(f"Failed to create relationship between nodes: {start_node}, {end_node}")
        return None

# Function to find nodes in Neo4j database by label
def find_nodes_by_label(session, label):
    """
    Function to find nodes in Neo4j database by label.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        
    Example usage:
        find_nodes_by_label(neo4j_driver, "Topic")

    Returns:
        List of matched nodes.
    """
    return session.read_transaction(_find_nodes_by_label, label)

def _find_nodes_by_label(tx, label):
    query = f"""
    MATCH (n:{label})
    RETURN n
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query)
    records = [record["n"] for record in result]
    return records

# Function to find nodes in Neo4j database by label and properties
def find_nodes_by_label_and_properties(session, label, properties):
    """
    Function to find nodes in Neo4j database by label and properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        properties (dict): A dictionary of properties to match.

    Returns:
        List of matched nodes.
    """
    with session:
        return session.read_transaction(_find_nodes_by_label_and_properties, label, properties)

def _find_nodes_by_label_and_properties(tx, label, properties):
    query = f"""
    MATCH (n:{label})
    WHERE {' AND '.join([f'n.{key} = ${key}' for key in properties.keys()])}
    RETURN n
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, **properties)
    records = [record["n"] for record in result]
    return records

# Function to find relationships in Neo4j database by type
def find_relationships_by_type(session, rel_type):
    """
    Function to find relationships in Neo4j database by type.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        rel_type (str): The type of the relationships to find.

    Returns:
        List of matched relationships.
    """
    return session.read_transaction(_find_relationships_by_type, rel_type)
    
def _find_relationships_by_type(tx, rel_type):
    query = f"""
    MATCH ()-[r:{rel_type}]->()
    RETURN r
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query)
    records = [record["r"] for record in result]
    return records

# Function to find relationships in Neo4j database by type and properties
def find_relationships_by_type_and_properties(session, label, properties):
    """
    Function to find relationships in Neo4j database by type and properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        rel_type (str): The type of the relationships to find.
        properties (dict): A dictionary of properties to match.

    Returns:
        List of matched relationships.
    """
    return session.read_transaction(_find_relationships_by_type_and_properties, label, properties)
    

def _find_relationships_by_type_and_properties(tx, label, properties):
    query = f"""
    MATCH (a)-[r:{label}]->(b)
    WHERE {' AND '.join([f'r.{key} = ${key}' for key in properties.keys()])}
    RETURN r
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, **properties)
    records = [record["r"] for record in result]
    return records

# Function to find nodes and relationships in Neo4j database by label and properties
def find_nodes_and_relationships_by_label_and_properties(session, label, properties):
    """
    Function to find nodes and relationships in Neo4j database by label and properties.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        label (str): The label of the nodes to find.
        properties (dict): A dictionary of properties to match.

    Returns:
        List of matched nodes and relationships.
    """
    return session.read_transaction(_find_nodes_and_relationships_by_label_and_properties, label, properties)
    
def _find_nodes_and_relationships_by_label_and_properties(tx, label, properties):
    query = f"""
    MATCH (n:{label})
    WHERE {' AND '.join([f'n.{key} = ${key}' for key in properties.keys()])}
    RETURN n
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, **properties)
    records = [record["n"] for record in result]
    return records

# Function to delete nodes in Neo4j based on given criteria
def delete_nodes(session, criteria, delete_related=False):
    """
    Function to delete nodes in Neo4j based on given criteria.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        criteria (dict): A dictionary containing the properties to match for deletion.
        delete_related (bool): If True, deletes related nodes and relationships; otherwise, deletes only the matched nodes.

    Example usage:
        # Delete only the nodes matching the criteria
        delete_nodes(neo4j_driver, {'TopicID': 'AP.PAG10'})

        # Delete the nodes and their related relationships
        delete_nodes(neo4j_driver, {'TopicID': 'AP.PAG10'}, delete_related=True)
    """
    session.write_transaction(_delete_nodes, criteria, delete_related)

def _delete_nodes(tx, criteria, delete_related=False):
    """
    Internal function to execute a Cypher query to delete nodes based on criteria.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
        criteria (dict): A dictionary containing the properties to match for deletion.
        delete_related (bool): Specifies whether to delete related nodes and relationships.
    """
    condition_str = " AND ".join([f"n.{key} = ${key}" for key in criteria])
    if delete_related:
        query = f"""
        MATCH (n)-[r]-()
        WHERE {condition_str}
        DELETE n, r
        """
    else:
        query = f"""
        MATCH (n)
        WHERE {condition_str}
        DELETE n
        """
    logging.query(f"Running query: {query}")
    tx.run(query, **criteria)

# Function to delete all nodes and relationships in the Neo4j database in batches
def delete_lots_of_nodes_and_relationships(session):
    """
    Function to delete all nodes and relationships in the Neo4j database in batches.

    Args:
        driver (neo4j.Driver): The Neo4j driver.
        session (str): The Neo4j session.
    """
    total_deleted = 0
    while True:
        deleted_count = session.write_transaction(_delete_batch)
        total_deleted += deleted_count
        if deleted_count == 0:
            break  # Exit the loop if no more nodes are deleted
    logging.prod(f"All nodes and relationships have been deleted. Total deleted: {total_deleted}")

def _delete_batch(tx):
    """
    Function to execute a Cypher query to delete a batch of nodes and relationships.

    Args:
        tx (neo4j.Transaction): The Neo4j transaction.
    """
    batch_size = 10000  # Adjust the batch size according to your needs
    query = """
    MATCH (n)
    WITH n LIMIT $batch_size
    DETACH DELETE n
    RETURN count(*)
    """
    logging.query(f"Running query: {query}")
    result = tx.run(query, batch_size=batch_size)
    result_data = result.single()
    
    if result_data is None:
        return 0
    deleted_count = result_data[0]
    if deleted_count is None:  # This check might be redundant, but kept for clarity
        return 0
    if deleted_count > 0:
        logging.database(f"Deleted {deleted_count} nodes.")
    return deleted_count

def delete_all_constraints(session):
    # Correct command to fetch all constraints for Neo4j 4.x and later
    constraints_query = "SHOW CONSTRAINTS"
    logging.query(f"Running query: {constraints_query}")
    constraints_query_result = session.run(constraints_query).data()

    if constraints_query_result:
        for constraint in constraints_query_result:
            # Ensure correct key is used to extract constraint name
            constraint_name = constraint['name']  # Adjust this if necessary
            drop_query = f"DROP CONSTRAINT {constraint_name}"
            logging.query(f"Running query: {drop_query}")
            session.run(drop_query)
            logging.database(f"Dropped constraint: {constraint_name}")
    else:
        logging.warning("No constraints found to delete.")
        
def reset_all_indexes(session):
    indexes = session.run("SHOW INDEXES").data()
    for index in indexes:
        index_name = index['name']
        session.run(f"DROP INDEX {index_name}")
        logging.info(f"Deleted index: {index_name}")

def reset_database(session):
    delete_lots_of_nodes_and_relationships(session)
    delete_all_constraints(session)
    reset_all_indexes(session)