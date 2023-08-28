# OpenCore-x99

#### 介绍
OpenCore华南金牌x99黑苹果
#### 当前支持的OS版本
| 机型 | 最低版本 | 最大版本 | 是否验证 |
| :---: | :---: | :---: | :---: |
| Mac Pro7,1 | macOS Catalina(10.15) | latest | 是 |

#### 硬件：
| 主板 | CPU | 内存 | 显卡 |
| :---: | :---: | :---: | :---: |
| 华南x99-F8 | E5 2695 V4 | 技嘉 RX580 8G （2304sp) | 三星单条32g DDR4 2133 RegECC x8 |

##### 主板图片：
![](./docs/1678384164320320621.png)

#### 软件架构说明:
- 使用`OpenCore`简称`OC`来引导主板进行macOS系统安装


#### 安装教程
##### 1)主板bios设置
- 1、`IntelRCSetup-->Processor Configuration-->MSR Lock control 配置 Disable`
- 2、`Setup-->Advanced-->NCT5532D Super IO Configuration-->Serial Port 配置 Disable`
- 3、`Setup-->CSM Configuration-->CSM Support 配置 Disable`如何配置请自行查阅相关教程
- 4、 `Above 4G Decoding`可以开启也可以不开启

##### 2)制作安装U盘
##### mac下制作制作安装U盘

[macOS Ventura :](https://apps.apple.com/cn/app/macos-ventura/id1638787999?mt=12)
```bash
sudo /Applications/Install\ macOS\ Ventura.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
```
[macOS Monterey:](https://apps.apple.com/cn/app/macos-monterey/id1576738294?mt=12)
```bash
sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
```
[macOS BigSur:](https://apps.apple.com/cn/app/macos-big-sur/id1526878132?mt=12)
```bash
sudo /Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
```
[macOS Catalina:](https://itunes.apple.com/cn/app/macos-catalina/id1466841314?ls=1&mt=12)
```bash
sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
```
[macOS Mojave:](https://itunes.apple.com/cn/app/macos-mojave/id1398502828?ls=1&mt=12)
```bash
sudo /Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
```
[macOS El Capitan:](http://updates-http.cdn-apple.com/2019/cert/061-41424-20191024-218af9ec-cf50-4516-9011-228c78eda3d2/InstallMacOSX.dmg)
```bash
sudo /Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install\ OS\ X\ El\ Capitan.app
```

#### 关于CPU E5-26xx V3 V4变频数据

##### V3: 
`Kernel -> Emulate`
- Cpuid1Data: `C3060300 00000000 00000000 00000000`
- Cpuid1Mask: `FFFFFFFF 00000000 00000000 00000000`
##### V4:
`Kernel -> Emulate`
- Cpuid1Data: `D4060300 00000000 00000000 00000000`
- Cpuid1Mask: `FFFFFFFF 00000000 00000000 00000000`
#### 关于单盘双系统
- 推荐采用配置文件上的示范，在`EFI`目录中新建一个名为`win`的文件夹来存放`win引导`避免引导覆盖,示范目录结构如下：
```
EFI|
---|BOOT
---|OC
---|win
---|----|Microsoft
```
#### 关于自定义内存分布序号
| 内存组 | 插槽 | 设备位置 | 对应Mac Pro插槽位置 | 通道 |
| :---: | :---: | :---: | :---: | :---: |
| 0 | BANK 0 | ChannelF-DIMM0 | 8 | F |
| 0 | BANK 1 | ChannelF-DIMM1 | 7 | F |
| 0 | BANK 2 | ChannelE-DIMM0 | 10 | E |
| 0 | BANK 3 | ChannelE-DIMM1 | 9 | E |
| 0 | BANK 4 | ChannelD-DIMM0 | 12 | D |
| 0 | BANK 5 | ChannelD-DIMM1 | 11 | D |
| 1 | BANK 6 | ChannelA-DIMM0 | 5 | A |
| 1 | BANK 7 | ChannelA-DIMM1 | 6 | A |
| 1 | BANK 8 | ChannelB-DIMM0 | 3 | B |
| 1 | BANK 9 | ChannelB-DIMM1 | 4 | B |
| 1 | BANK 10 | ChannelC-DIMM0 | 1 | C |
| 1 | BANK 11 | ChannelC-DIMM1 | 2 | C |

#### 关于不同内存数量配置
 
#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md

