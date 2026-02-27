# LinkRep
非素链环的跨平台通用表示形式

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

## LinkRep 格式

LinkRep 的内容由四部分组成：

1. 注释行 (Comment)：使用 `//` 开头的行，以及仅仅包含空字符的行是注释行。仅仅包含空字符的行应该在解析时被忽略，而注释行应该作为信息保留下来。

2. 变量命名 (VarDef)：用于定义变量，使用变量表示 PdCode，例如：

```
L2a1: [[4, 1, 3, 2], [2, 3, 1, 4]]
```

上述语句定义了一个名为 `L2a1` 的变量，其中存储一个 PdCode `[[4, 1, 3, 2], [2, 3, 1, 4]]`。其中变量名 (VarName) 应该是字母、数字、下划线构成的不以数字作为开头的字符串。可以命名多个不同名字的变量。

规则上允许变量名任意定义，但实践中建议使用标准的扭结或者链环名称对 PdCode 进行命名。使用非标准 PdCode 进行变量定义应该被警告

3. 描述链环集合 (LinkSet)：使用一个变量名序列描述所有使用到的链环，这里的顺序会影响后续的使用。该描述在 LinkRep 中只可以存在一次。

```
[L2a1, L4a1, K3a1]
```

这一行内容用于描述进行连通和之前的扭结信息。在连接方式描述符中，将使用 `L[i, j]` 表示第 `i` 个链环变量的第 `j` 个连通分支。其中 `i` 与 `j` 的编号从 `1` 开始向上编号。

4. 连接方式描述符 (LinkMethod)：描述哪些链环的哪些连通分支应该被连接在一起，例如：

```
L[1, 1]#L[2, 2]
```

可以用来表示第一个链环的第一个连通分支应该和第二个链环的第二个连通分支做连通和。

```
L[1, 2]#L[2, 2]#L[3, 1]
```

可以用来表示第一个链环的第二个连通分支应该和第二个链环的第二个连通分支做连通和，在此之后该连通分支应该再和第三个链环的第一个连通分支做连通和。

## 形式化定义

词法单元：
```
CommentLine => "//[^\n]*\n"
VarName => "[A-Za-z_][A-Za-z0-9_]*"
PdCode  => "(\[\])|(\[\[\d+,\s*\d+,\s*\d+,\s*\d+\](,\[\d+,\s*\d+,\s*\d+,\s*\d+\])*\])"
PosName => "L\[\d+,\s*\d+\]"
```

VarLine：定义一个变量
```
VarLine -> VarName ":" PdCode "\n"
```

VarDef：定义所有变量
```
VarDef -> VarLine
VarDef -> VarLine VarDef
```

VarNameList：变量名列表
```
VarNameList -> VarName
VarNameList -> VarName "," VarNameList
```

LinkSet：定义要使用的所有链环
```
LinkSet -> "[" VarNameList "]" "\n"
```

LinkLineList：不换行的前提下用于连接连通分支
```
LinkLineList -> PosName "#" PosName
LinkLineList -> PosName "#" PosName "#" LinkLineList
```

LinkLine: 描述一个连通分支的连接
```
LinkLine -> LinkLineList "\n"
```

LinkMethod：描述连通分支的连接情况
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

LinkRep：
```
LinkRep -> Comment VarDef LinkSet LinkMethod
```
