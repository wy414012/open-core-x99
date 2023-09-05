# RamDiskApp

RamDiskApp


### 概要
ramdisk一般指虚拟内存盘。虚拟内存盘是通过软件将一部分内存（RAM）模拟为硬盘来使用的一种技术；
EDK中支持ramdisk协议的`gEfiRamDiskProtocolGuid`，bootManage，httpboot使用；

### UEFI中RamDiskDxe驱动
头文件位置：
MdePkg/Include/Protocol/RamDisk.h|104| extern EFI_GUID gEfiRamDiskProtocolGuid;

驱动位置：
MdeModulePkg/Universal/Disk/RamDiskDxe/RamDiskDriver.c

```
  //
  // Install the EFI_RAM_DISK_PROTOCOL and RAM disk private data onto a
  // new handle
  //
  Status = gBS->InstallMultipleProtocolInterfaces (
                  &mRamDiskHandle,
                  &gEfiRamDiskProtocolGuid,
                  &mRamDiskProtocol,
                  &gEfiCallerIdGuid,
                  ConfigPrivate,
                  NULL
                  );
  if (EFI_ERROR (Status)) {
    goto ErrorExit;
  }
```

注册接口
```
//
// The EFI_RAM_DISK_PROTOCOL instances that is installed onto the driver
// handle
//
EFI_RAM_DISK_PROTOCOL  mRamDiskProtocol = {
  RamDiskRegister,
  RamDiskUnregister
};
```
提供了2个函数，一个用来注册 RAM Disk 的Register，一个用来销毁 RAM Disk 的 Unregister。对于我们来说，注册的函数是最重要的。

RamDiskRegister原型
```
ypedef
EFI_STATUS
(EFIAPI *EFI_RAM_DISK_REGISTER_RAMDISK) (
  IN UINT64                       RamDiskBase,
  IN UINT64                       RamDiskSize,
  IN EFI_GUID                     *RamDiskType,
  IN EFI_DEVICE_PATH              *ParentDevicePath     OPTIONAL,
  OUT EFI_DEVICE_PATH_PROTOCOL    **DevicePath
  );

```
注册一个Ram Disk 需要给定：
RamDiskBase: 新的 Ram Disk 的基地址
RamDiskSize: 新的 Ram Disk 的大小
RamDiskType: 新的 Ram Disk 的类型（似乎可以定义 ISO/RAW之类的）
ParentDevicePath: 指向父设备的 Device Path（不明白这个功能有什么意义）。如果没有可以设置为 NULL
DevicePath: 返回的创建的 Ram Disk 的 Device Path

RamDiskUnregister 原型
```
typedef
EFI_STATUS
(EFIAPI *EFI_RAM_DISK_UNREGISTER_RAMDISK) (
  IN  EFI_DEVICE_PATH_PROTOCOL    *DevicePath
  );

///
/// RAM Disk Protocol structure.
///
struct _EFI_RAM_DISK_PROTOCOL {
  EFI_RAM_DISK_REGISTER_RAMDISK        Register;
  EFI_RAM_DISK_UNREGISTER_RAMDISK      Unregister;
};
```

RamDiskDxe驱动交互界面，在Device Manager->RAM Disk Configuration

![2021-12-10 16-19-34屏幕截图](https://gitee.com/zhubo-gitee/mydoc/raw/master/202112101621120.png)

`> Create raw `创建的是raw格式，这个格式在biso下显示的是BLK，无法直接使用；
` Create from file `可以选择镜像进行加载，可以选择fat镜像进行加载，这样的话在Shell下就可以看到`FSx`了

### 制作镜像

采用dd命令生成的镜像文件（raw镜像，这个映射出来是FS0:）

```

dd if=/dev/zero of=~/hda.img bs=1 count=10M
mkfs -t vfat ~/hda.img
losetup /dev/loop0 ~/hda.img  #映射loop设备，要找不使用的；
sudo mount /dev/loop0 /mnt/image  #挂载loop设备
......（work in mnt dir）
umount /mnt/image              #卸载loop设备
losetup -d /dev/loop0           #解除loop映射
```

### RamDisk应用

应用就是将上面的界面设置用代码实现；

步骤如下：
1.	查找 RamDiskProtocol 是否安装，因为我们的应用需要协议的支持；
2.	读取 “”hda.img”到内存中,这是一个fat服务器的二进制镜像，为了在uefi shell中显示`FSx`必须要用fat镜像；
3.	用 RamDiskProtocol 的 Register 函数将上面的内存注册为 Ram Disk

代码实现

```
#include <Uefi.h>
#include <Library/PcdLib.h>
#include <Library/UefiApplicationEntryPoint.h>
#include <Library/BaseLib.h>
#include <Library/UefiLib.h>
#include <Library/PrintLib.h>
// #include <Library/ShellCEntryLib.h>
#include <Protocol/RamDisk.h>
#include <Protocol/DevicePathToText.h>
// #include <Protocol/EfiShell.h>
// #include <Library/ShellLib.h>
#include "diskimage-16MB.h"

extern EFI_BOOT_SERVICES         *gBS;
/*
EFI_GUID gEfiVirtualDiskGuid =
           { 0x77AB535A, 0x45FC, 0x624B,
                {0x55, 0x60, 0xF7, 0xB2, 0x81, 0xD1, 0xF9, 0x6E }};
   */
/**
  The user Entry Point for Application. The user code starts with this function
  as the real entry point for the application.

  @param[in] ImageHandle    The firmware allocated handle for the EFI image.
  @param[in] SystemTable    A pointer to the EFI System Table.

  @retval EFI_SUCCESS       The entry point is executed successfully.
  @retval other             Some error occurs when executing this entry point.

**/
EFI_STATUS
EFIAPI
UefiMain (
  IN EFI_HANDLE        ImageHandle,
  IN EFI_SYSTEM_TABLE  *SystemTable
  )
{
      EFI_STATUS               Status;
      EFI_RAM_DISK_PROTOCOL    *RamDiskApp;
      EFI_DEVICE_PATH_PROTOCOL *DevicePath;

      // Look for Ram Disk Protocol
      Status = gBS->LocateProtocol (
                      &gEfiRamDiskProtocolGuid,
                      NULL,
                      &RamDiskApp
               );
      if (EFI_ERROR (Status)) {
          Print(L"Couldn't find RamDiskProtocol\n");
          return EFI_ALREADY_STARTED;
      }

      //
      // Register the newly created RAM disk.
      //
      Status = RamDiskApp->Register (
           ((UINT64)(UINTN) hda_img),
            sizeof(hda_img),
           &gEfiVirtualDiskGuid,
           NULL,
           &DevicePath
           );
      if (EFI_ERROR (Status)) {
          Print(L"Can't create RAM Disk!\n");
          return EFI_SUCCESS;
      }

     Print(L"Creat Ram Disk success!\n");
  return 0;
}

```



执行过程

```
FS0:\> RamDiskApp.efi
FSOpen: Open '\RamDiskApp.efi' Success
FSOpen: Open '\RamDiskApp.efi' Success
FSOpen: Open '\RamDiskApp.efi' Success
FSOpen: Open '\RamDiskApp.efi' Success
InstallProtocolInterface: 5B1B31A1-9562-11D2-8E3F-00A0C969723B 90000000F5ABBAC0
Loading driver at 0x90000000F1946000 EntryPoint=0x90000000F1946240 RamDiskApp.efi
InstallProtocolInterface: BC62157E-3E33-4FEC-9920-2D3B36D750DF 90000000F674C798
InstallProtocolInterface: 6A1EE763-D47A-43B4-AABE-EF1DE2AB56FC 90000000F2349EB0
ProtectUefiImageCommon - 0xF5ABBAC0
  - 0x90000000F1946000 - 0x0000000000A04180
InstallProtocolInterface: 752F3136-4E16-4FDC-A22A-E5F46812F4CA 90000000FE480998
InstallProtocolInterface: 964E5B21-6459-11D2-8E39-00A0C969723B 90000000F5AB91A8
InstallProtocolInterface: A77B2472-E282-4E9F-A245-C2C0E27BBCC1 90000000F5AB91D8
InstallProtocolInterface: 09576E91-6D3F-11D2-8E39-00A0C969723B 90000000F674C998
InstallProtocolInterface: CE345171-BA0B-11D2-8E4F-00A0C969723B 90000000F5AB9EA0
InstallProtocolInterface: 151C8EAE-7F2C-472C-9E54-9828194F6A88 90000000F5AB9EB8
 BlockSize : 512
 LastBlock : 4FFF
InstallProtocolInterface: 964E5B22-6459-11D2-8E39-00A0C969723B 90000000F5A76030
Installed Fat filesystem on 90000000F5ABC918
Creat Ram Disk success!
FSOpen: Open '\' Success
FS0:\>
FS0:\>
FS0:\>
FS0:\>
FS0:\> map -r
Mapping table
      FS0: Alias(s):HD1a0b:;BLK1:
          PciRoot(0x0)/Pci(0x5,0x1)/USB(0x0,0x0)/HD(1,MBR,0x37C937C8,0xFDF00,0x67A100)
      FS1: Alias(s):F0:;BLK2:
          VirtualDisk(0x90000000F1949D28,0x90000000F2349D27,0)
     BLK0: Alias(s):
          PciRoot(0x0)/Pci(0x5,0x1)/USB(0x0,0x0)
FSOpen: Open '\' Success
FS0:\>

```



### 参考文档
http://www.lab-z.com/stu132rd/
http://www.lab-z.com/utrad/
https://github.com/rcpao-enmotus/RamDiskPkg


