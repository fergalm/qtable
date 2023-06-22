# Vtable
A QT based table viewer with filters

Vtable is a command line tool to display tabular data. It features a simple command line interface, easy sorting and filtering, and support for csv, parquet and fits binary table files

## Installation
`pip install vtable`

## Usage
`vtable file.csv`
or 
`vtable file.fits`

Currently the file formats csv, parquet, and fits binary tables are supported, although only tables in the first header extension are supported for fits files.

## Sorting
Clicking on a column name in the table sorts the data by that column.

## Filtering

### Categorical Filters
If there are fewer than 10 unique values in a column, you can filter on category by checking and unchecking in the drop-down window 

### Numeric Filters
Columns with numeric data can be filtered with standard equalities and inequalities. For examples

```
> 5  # Select all rows where the value is greater than 5
<= 6 # Select all rows where the value is less than or equal to 6
== 9  #Select only rows where the value is exactly 9
```

There is also the ability to filter on nan

```
nan  #Select rows where this column is either nan or inf 
~nan  #select only rows where this column is actually a number
```

#### Coming soon
Ability to combine filters, e.g 

```
< 5 & > 9
< 0 | nan
```

### String Filters
Columns containing strings can be filtered with regular expressions. For example 

```
abc   #Matches 'abcdefg' and 'xyzabcefg'
^abc  #Matches pattern at start of string only
abc$  #Matches pattern at end of string only
\d{2} #Matches two digits, e.g 12, or 99
```

### Date Filters
Coming soon. 

Date filters will let you filter by year, month, hour, dayofweek, etc. 

## Disclaimer
This is a personal project, maintained with best effort. It will typically have a few rough edges