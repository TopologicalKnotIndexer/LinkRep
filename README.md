# LinkRep
A Cross-Platform Universal Representation for Composite Links

## Installation

```bash
pip install link-rep
```

## Usage

```python
from link_rep import LinkRep

real_serial = ( # human readable presentation
"""
// this is comment line 1
// this is comment line 2
L2a1: [[4, 1, 3, 2], [2, 3, 1, 4]]
L4a1: [[6, 1, 7, 2], [8, 3, 5, 4], [2, 5, 3, 6], [4, 7, 1, 8]]
K3a1: [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
[L2a1, L4a1, K3a1]
L[1, 1]#L[2, 1]
L[2, 2]#L[3, 1]
""").lstrip()

link_r = LinkRep()
link_r.deserialize(real_serial)

print(link_r.json_serialize()) # machine readable presentation
print(link_r.serialize())      # human readable presentation

json_str = link_r.json_serialize()
new_link_r = LinkRep()
new_link_r.json_deserialize(json_str) # get data from json serial
```

## LinkRep Format

The content of LinkRep consists of four parts:

1. Comment Lines: Lines starting with `//`, as well as lines containing only whitespace characters, are comment lines. Lines containing only whitespace should be ignored during parsing, while comment lines should be retained as informational content.

2. Variable Definitions (VarDef): Used to define variables that represent PdCodes (Planar Diagram Codes), for example:

```
L2a1: [[4, 1, 3, 2], [2, 3, 1, 4]]
```

The above statement defines a variable named `L2a1` that stores a PdCode `[[4, 1, 3, 2], [2, 3, 1, 4]]`. The variable name (VarName) should be a string composed of letters, numbers, and underscores, and must not start with a number. Multiple variables with different names can be defined.

While the rules allow arbitrary variable naming, in practice it is recommended to use standard knot or link names to name PdCodes. Warnings should be issued for variable definitions using non-standard PdCodes.

3. Link Set Description (LinkSet): A sequence of variable names describing all links used, where the order affects subsequent usage. This description can only appear once in LinkRep.

```
[L2a1, L4a1, K3a1]
```

This line describes the knot information before performing connected sums. In the connection method descriptor, `L[i, j]` is used to denote the j-th connected component of the i-th link variable. Both `i` and `j` are numbered starting from 1 and increment upwards.

4. Connection Method Descriptor (LinkMethod): Describes which connected components of which links should be connected together, for example:

```
L[1, 1]#L[2, 2]
```

This can be used to indicate that the first connected component of the first link should be connected (via connected sum) with the second connected component of the second link.

```
L[1, 2]#L[2, 2]#L[3, 1]
```

This can be used to indicate that the second connected component of the first link should be connected (via connected sum) with the second connected component of the second link, and this connected component should then be connected (via connected sum) with the first connected component of the third link. The order of the components is defined by the order of minimal arc number in the component.

## Formal Definition

Lexical Units:
```
CommentLine => "//[^\n]*\n"
VarName => "[A-Za-z_][A-Za-z0-9_]*"
PdCode  => "\[\[\d+,\s*\d+,\s*\d+,\s*\d+\](,\[\d+,\s*\d+,\s*\d+,\s*\d+\])*\]"
PosName => "L\[\d+,\s*\d+\]"
```

VarLine: Defines a single variable
```
VarLine -> VarName ":\s*" PdCode "\n"
```

VarDef: Defines all variables
```
VarDef -> VarLine
VarDef -> VarLine VarDef
```

VarNameList: List of variable names
```
VarNameList -> VarName
VarNameList -> VarName "," VarNameList
```

LinkSet: Defines all links to be used
```
LinkSet -> "[" VarNameList "]" "\n"
```

LinkLineList: Connects connected components without line breaks
```
LinkLineList -> PosName "#" PosName
LinkLineList -> PosName "#" PosName "#" LinkLineList
```

LinkLine: Describes the connection of connected components
```
LinkLine -> LinkLineList "\n"
```

LinkMethod: Describes the connection of connected components
```
LinkMethod ->
LinkMethod -> LinkLine
LinkMethod -> LinkLine LinkMethod
```

Comment:
```
Comment ->
Comment -> CommentLine
Comment -> CommentLine Comment
```

LinkRep:
```
LinkRep -> Comment VarDef LinkSet LinkMethod
```
