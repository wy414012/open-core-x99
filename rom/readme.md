## 已修复ACPI的固件
- [Fix-x99-f8-acpi-20240329.fd](./Fix-x99-f8-acpi-20240329.fd) 华南X99-F8
- 添加了`NTFS`U盘启动支持
- 集成`hfs`驱动
- 集成`exfat`驱动
- 集成`ext4`支持
- 修复`macOS`所需要的`ACPI`补丁，完美不影响win系统
- 刷新请使用`fpt -f Fix-x99-f8-acpi-20240329.fd`
