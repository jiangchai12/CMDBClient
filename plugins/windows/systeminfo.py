# Author:jiangcaiyun
import wmi, platform, win32com, os
from win32com.client import *
class win32info(object):
    def __init__(self):
        self.wmi_obj = wmi.WMI()
        self.win32_obj = Dispatch("WbemScripting.SWbemLocator")
        self.win32_sevice_conn = self.win32_obj.ConnectServer(".","root\cimv2")

    def get_system_info(self):
        data = {}
        computer_info = self.wmi_obj.Win32_ComputerSystem()[0]
        system_info = self.wmi_obj.Win32_OperatingSystem()
        data["comp_manufacturer"] = computer_info.Manufacturer
        data["comp_model"] = computer_info.Model
        data["comp_wake_up_type"] = computer_info.WakeUpType
        for sys in system_info:
            data["sys_model"] = sys.Caption
            data["system_vertion"] = sys.BuildNumber
            data["sys_32or64_bit"] = sys.OSArchitecture
            data["sn"] = sys.SerialNumber

        # print(data)
        return data

    def get_cpu_info(self):
        data = {}
        cpu_listsss = self.wmi_obj.Win32_Processor()
        # print(cpu_listsss.DeviceID, cpu_listsss.LoadPercentage)
        cpu_core_count = 0
        cpu_model = ''
        for cpu in cpu_listsss:
            cpu_core_count =+ cpu.NumberOfCores
            cpu_model = cpu.Name
        data["cpu_model"] = cpu_model
        data["cpu_core_count"] = cpu_core_count
        data["cpu_count"] = len(cpu_listsss)
        # print(data)
        return data
    def get_ram_info(self):
        ram_collections = self.wmi_obj.ExecQuery("Select * from Win32_PhysicalMemory")
        MB = 1024 * 1024
        data = []
        for s in ram_collections:
            data_item = {}
            ram_size = int(s.Capacity)/int(MB)
            slot = s.DeviceLocator.strip()
            model = s.Caption
            manufacturer = s.Manufacturer
            serialNumber = s.SerialNumber
            data_item = {
                "slot": slot,
                "model": model,
                "manufacturer": manufacturer,
                "sn": serialNumber,
                "ram_size_MB": ram_size,
            }
            data.append(data_item)
        # print(data)
        return {"ram": data}
    def get_disk_info(self):
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():
            data_item = {}
            # print(disk.Model,disk.Size,disk.DeviceID,disk.Name,disk.Index,disk.SerialNumber,disk.SystemName,disk.Description)
            # print("SerialNumber=", disk.SerialNumber)
            iface_choices = ["SAS", "SCSI", "SATA", "SSD"]
            for iface in iface_choices:
                if iface in disk.Model:
                    data_item["iface_type"] = iface
                    break
                else:
                    data_item["iface_type"] = 'unknown'
            capacity = int(disk.Size)/(1024*1024*1024)
            data_item["index"] = disk.Index
            data_item["Model"] = disk.Model
            data_item["capacity_GB"] = round(capacity, 2)
            data_item["sn"] = disk.SerialNumber.strip()
            # data_item["Description"] = disk.Description
            data_item["Manufacturer"] = disk.Manufacturer
            data_item["SystemName"] = disk.SystemName
            data.append(data_item)
            # print(data_item)
        # print(data)
        return {"disk": data}

    def get_nic_info(self):
        data = []
        nic_inf_list = self.wmi_obj.Win32_NetworkAdapterConfiguration()
        for nic in nic_inf_list:
            if nic.MACAddress is not None:
                data_item = {}
                data_item["macaddress"] = nic.MACAddress
                data_item["Model"] = nic.Caption
                data_item["name"] = nic.Index
                if nic.IPAddress is not None:
                    data_item["ipaddress"] = nic.IPAddress
                    data_item["netmask"] = nic.IPSubnet
                else:
                    data_item["ipaddress"] = ''
                    data_item["netmask"] = ''
                bonding = 0
                data.append(data_item)
                # print("data_item=", data_item)
        return {"nic": data}


def collect():
    data = {
        "os_type": platform.system(),
        "os_release": "%s %s  %s " % (platform.release(), platform.architecture()[0], platform.version()),
        "os_distribution": "Microsoft",
        "asset_type": 'server'
    }

    asset_info = win32info()
    data.update(asset_info.get_system_info())
    data.update(asset_info.get_cpu_info())
    data.update(asset_info.get_ram_info())
    data.update(asset_info.get_disk_info())
    data.update(asset_info.get_nic_info())
    # print(data)
    return data
if __name__ == "__main__":
    collect()

# w = win32info()
# w.get_system_info()
# w.get_cpu_info()
# w.get_ram_info()
# w.get_disk_info()
# w.get_nic_info()







