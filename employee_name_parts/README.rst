Employee First/Middle/Last Names for Odoo 18
==================================================

This module was written to extend the functionality of employees to
support name parts of an employee. There are three parts of employee.
If contact is a person name will not be editable and firs/mi/last names will
be shown. On saving the changes, name will be first + middle + last names.
On creating employee, the app will split the full name into three parts
if no name parts are found. This module can splits names from 2 formats of a name:

* Last, First Middle
* First Middle Last

It also can detect if the name is double-word name (first or last). This is useful
for Arabic people where a single name can be two words. This might be useful for
other cultures. Just populate first_part and second_part global lists with your
name parts. This list is found at line 7 and 8 in hr_employee.py file.

Upon installing this modules, all employee full names will automatically split
to populate name parts.

This module also adds multi language feature into full and part names, so you
can write the same name by different languages.

Usage
=====
First/Middle/Last fields are added into employee data. Whenever the contact is a
person, these fields are shown. First and Last names are required, then
employee.

Setup
=====
No setup.
