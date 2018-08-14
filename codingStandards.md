A simple C# coding standard (found at: https://github.com/nikhilk/scriptsharp/wiki/Coding-Guidelines)

## Code Organization
### Classes and Files
* Each file should contain at most one top-level class. Consider using nested classes if a class is only meaningful in the scope of another class (which is often the primary motivation for grouping classes into the same file).
* The class name and the file name should match.
* The file’s location on the file system should be indicative of the namespace that the class belongs to.
* Favor keeping code for a class together, rather than split into a bunch of partial classes. The one exception to this rule is for extremely big classes that are in fact a union of logically independent pieces of functionality. In this case, the file name should be ClassName.LogicalGroup.cs.
* Include a header comment consistent with the rest of the codebase in each file.

### File Layout and Member Order
* Namespace imports should occur top-level in the class (outside of the namespace scope), and listed alphabetically, with the exception that System.* namespaces should appear first. Do import the implicit System namespace.
* Members within a class should exist in the following order: static fields and constants, member fields, constructors, properties, events, methods, explicitly implemented interface members, and finally nested classes.
* Member fields may be logically grouped, but other members (properties, events and methods) should be alphabetically ordered. Do not group by member visibility.
* Use region blocks for explicitly implemented interfaces. Do not use region blocks for other grouping.
* Initialize members within the constructor, and not at the point of their declaration. This helps avoid the jumping around in the debugger when debugging instantiation of a class.

## Style and Formatting
### Bracing Style and Indentation
* Use K&R style bracing, where the open brace is on the end of the line rather than on a line by itself.
* Separate out open/close braces across lines, i.e. do not begin a scope and end a scope on the same line.
* Always use braces for block statements, even if a block only contains a single statement.
* Indent each level using 4 spaces in c# code, and 2 spaces in script or html/markup. Do not use any tabs.

### Spacing
* Use single space between arguments
* Do not use spaces between method names and parentheses or between parentheses and arguments.
* Do not use spaces in indexer-brackets.
* Use a single space after keywords in control-flow statements.
* Use a single space between operators.

### New Lines and Line Length
* Use a single new line as separator between consecutive members.
* Use two lines as separator between nested classes.
* Do use a single new line between namespace declaration and the class declaration and the first member within the class.
* Within a method, use new line based on judgement to group logically related set of statements. In particular do not go the extreme and introduce a blank line between every consecutive pair of statements.
* Exercise good judgement for how long a line of code runs. There isn't a fixed rule, but as a general hint, try to limit a line to 120 columns.

### Parenthesizing
Use parentheses around expressions involving binary operators (esp. in if/while statements). Also use them where they help readability, i.e. do not rely on requiring one to think about operator precedence rules while reading code.

### Modifiers
Always be explicit about visibility of classes and members. Do not implicitly use default "internal" and "private" visibility.

## Naming
### Class and Member Names
* Use PascalCasing (first letter of each word is capitalized) for type names, namespaces and members (properties, methods, events, and static fields).
* Use camelCasing (first letter lowercase, first letter of each subsequent word capitalized) for parameters, locals and member fields.
* Use leading underscore for private fields.

## Miscellaneous
* Use C# keywords for primitive types (string, int etc.) unless you are referring to a static method (eg. String.Empty).
* Use namespace import instead of namespace-qualified type names.
