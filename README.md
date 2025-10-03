# Batch Modify Relates (ArcPy)
![Batch Modify Relates Demo](docs/demo_800.gif)

This ArcPy tool automates the process of modifying relationships between 
feature classes and related tables in bulk.  

It can:
- Add new relates
- Remove invalid ones
- Reassign records to the correct feature  

Originally designed for utility workflows in Arcmap, this script is general-purpose:  
**any feature class + table with matching key fields can be used.**  
For this repository, I demonstrate it with a Work Order History (WOH) table, 
but the logic applies to any dataset.

Requirements: Arcpy, ArcGIS Pro/Arcmap
