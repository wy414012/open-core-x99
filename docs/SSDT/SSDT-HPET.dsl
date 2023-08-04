/*
 * Intel ACPI Component Architecture
 * AML/ASL+ Disassembler version 20230331 (64-bit version)
 * Copyright (c) 2000 - 2023 Intel Corporation
 * 
 * Disassembling to symbolic ASL+ operators
 *
 * Disassembly of SSDT-HPET.aml, Fri Aug  4 16:32:09 2023
 *
 * Original Table Header:
 *     Signature        "SSDT"
 *     Length           0x00000112 (274)
 *     Revision         0x02
 *     Checksum         0xAE
 *     OEM ID           "YMWL"
 *     OEM Table ID     "HPET"
 *     OEM Revision     0x00001000 (4096)
 *     Compiler ID      "INTL"
 *     Compiler Version 0x20230331 (539165489)
 */
DefinitionBlock ("", "SSDT", 2, "YMWL", "HPET", 0x00001000)
{
    External (_SB_.PCI0, DeviceObj)
    External (_SB_.PCI0.HPET, DeviceObj)
    External (_SB_.PCI0.LPC0.HPET, DeviceObj)

    If (CondRefOf (\_SB.PCI0.LPC0.HPET))
    {
        Device (\_SB.PCI0.HPET)
        {
            Name (_HID, EisaId ("PNP0103") /* HPET System Timer */)  // _HID: Hardware ID
            OperationRegion (HPTC, SystemMemory, 0xFED1F404, 0x04)
            Field (HPTC, DWordAcc, NoLock, Preserve)
            {
                HPTS,   2, 
                    ,   5, 
                HPTE,   1, 
                Offset (0x04)
            }

            Method (_STA, 0, NotSerialized)  // _STA: Status
            {
                If (HPTE)
                {
                    Return (0x0F)
                }
                Else
                {
                    Return (Zero)
                }
            }

            Name (CRS, ResourceTemplate ()
            {
                IRQNoFlags ()
                    {0}
                IRQNoFlags ()
                    {8}
                Memory32Fixed (ReadWrite,
                    0xFED00000,         // Address Base
                    0x00000400,         // Address Length
                    _Y00)
            })
            Method (_CRS, 0, NotSerialized)  // _CRS: Current Resource Settings
            {
                CreateDWordField (CRS, \_SB.PCI0.HPET._Y00._BAS, HTBS)  // _BAS: Base Address
                Local0 = (HPTS * 0x1000)
                HTBS = (Local0 + 0xFED00000)
                Return (CRS) /* \_SB_.PCI0.HPET.CRS_ */
            }
        }
    }
}

