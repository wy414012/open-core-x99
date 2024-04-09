# ALC声卡定制辅助工具

### 声卡code整理脚本，用法
```bash
./verbit.sh acl892code.txt
```
### 指定输出文件名

```bash
./verbit.sh acl892code.txt >整理的ID.md

```

### python 脚本
- 用于整理节点信息
```bash
python3 verbit.py aclCode.txt >aclCode.md
```
- 用于推导节点
```bash
python3 FindNodePath.py aclCode.txt
```
- 中间直接输入要查询的节点给出正向推导和反向推导