# api-consistency-checker
a library to check data consistency across different endpoint responses
prerequisites-

1. python==3.7
2. decorator==4.4.1
3. graphviz==0.13.2
4 .networkx==2.4
5. pydot==1.4.1
6. pyparsing==2.4.6
7. xmltodict==0.12.0

For installing the dependency run the requirements.txt
pip3 install -r requirements.txt


running the script-
python3 main.py path/to/data_model.json path/to/data.json path/to/state.json path/to/validated-page.xml

Order of arguments should be - 1. data_model.json 2. data.json  3. state.json  4. validate-page.xml

sample output -
[{'entityDefinition_body': []}, {'each_entity_outside_body__0': []}, {'each_entity_outside_body__1': []},
{'each_entity_entityDefinition__0': []}, {'each_entity_entityDefinition__1': []},
{'listItemPrototype_outside_body': [{'value not found for the key>> entities__entityDefinitions__Quote_Locations__Location': 'entities__entityDefinitions__Quote_Locations__Location__Lin'}]},
{'listItemPrototype_entity_entityDefinition': []}, {'listItemPrototype_entityDefintion': []}]

Types of hierarchy of entities in the state.json
1. entityDefinition_body - Every entities contains only the hierarchy of elements at the top of each entityDefinition.
2. each_entity_outside_body - Every entity containing the hierarchy map inside children, it has 0, 1 etc added in case if it contains the the same map multiple type.
3. each_entity_entityDefinition -  Every entity containing the hierarchy map inside children as entityDefinition

 ListItemPrototype-  Some entity has the map inside the ListItemPrototype
4. listItemPrototype_outside_body - Every entity containing the hierarchy map inside children
5. listItemPrototype_entity_entityDefinition - Each entity containing the entity definition inside children
6. listItemPrototype_entityDefintion - Map in the top of each entity


# saving the state and data_model tree, flattened tree and hierarchy map
data_model_tree = "data/data_model_tree.json"
state_tree = "data/state_tree.json"
state_flattened_tree = "data/state_flattened_tree.json"
data_model_flattened_tree = "data/data_model_flattened_tree.json"
data_model_hierarchy_image = "data/data_model"




