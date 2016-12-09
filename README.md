# Final Grade Calculator
Calculates the final grade for Master Business Informatic students of the University of Mannheim using the examination regulations that can be found [here](http://www.uni-mannheim.de/studienbueros/pruefungen/pruefungsordungen/). Especially § 10 (7) is applied: 
> When calculating the module grades, the grades for the subject areas and the final grade, only the first decimal place is considered in the calculation. All other decimal places are eliminated without rounding up or down.

## How To
Just run `python grades.py -f '<path_to_file>'` in the console

## Input Format
Expects the grades in a CSV format where each row corresponds to a module and columns 
* `group`: name of the group (e.g. MMM fundamentals),
* `grade`: grade for module,
* `ects`: number of ECTS points for module.
Use `#` to comment a line.
