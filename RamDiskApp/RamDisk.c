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

