# Expense_Tracker
Takes in bank statements (csv format), automatically categorizes, appends appropriate data fields, and triggers a prompt for further information in the case of an unknown entry. Uses Python.

## Table of Contents:
- [A Look Under the Hood](#a-look-under-the-hood)
- [Statements](#statements)
- [Exports](#exports)
- [Masterfile](#masterfile)

## A Look Under the Hood
There is a single code file used for this project, consisting of five functions, with the fifth function using the prior four functions to execute the entire concept.
- masterfile_import: Imports a file of unique keywords and associations.
- statement_info: Prompts the user for information about which statement to manipulate.
- import_statement: Imports the statement the user specified in statement_info.
- gather_keys: Parses through specified statement to look for new unique keys to add to the mastefile, updates the export file as well as masterfile. Will prompt user if a new unique key is found.
- run_export: This brings together the above functions, and will save the updated masterfile as well as save a new export file with nomenclature specific to the statement.

[Table of Contents](#table-of-contents)

## Statements

[Table of Contents](#table-of-contents)

## Exports

[Table of Contents](#table-of-contents)

## Masterfile

[Table of Contents](#table-of-contents)
