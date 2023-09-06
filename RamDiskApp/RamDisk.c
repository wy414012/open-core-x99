/** @file
  This sample application bases on RamDisk

  Copyright (c) 2006 - 2016, Intel Corporation. All rights reserved.<BR>
  This program and the accompanying materials
  are licensed and made available under the terms and conditions of the BSD License
  which accompanies this distribution.  The full text of the license may be found at
  http://opensource.org/licenses/bsd-license.php

  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

**/

#include <Uefi.h>
#include <Library/PcdLib.h>
#include <Library/UefiApplicationEntryPoint.h>
#include <Library/BaseLib.h>
#include <Library/UefiLib.h>
#include <Library/PrintLib.h>
#include <Protocol/RamDisk.h>
#include <Protocol/DevicePathToText.h>
#include "diskimage-16MB.h"

extern EFI_BOOT_SERVICES         *gBS;

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

      // 寻找Ram-Disk协议
      Status = gBS->LocateProtocol (
                      &gEfiRamDiskProtocolGuid,
                      NULL,
                      (VOID **)&RamDiskApp
               );
      if (EFI_ERROR (Status)) {
          Print(L"Couldn't find RamDiskProtocol\n");
          return EFI_ALREADY_STARTED;
      }

      //
      // 注册新的RAM 磁盘驱动
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

