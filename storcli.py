# -*-coding: utf-8 -*-
"""
Python library for Storcli
"""

import os
import subprocess
import json

class Storcli:
    def __init__(self, cli_path = '/opt/MegaRAID/storcli/storcli64'):
        self.cli_path = cli_path

        if not os.path.exists(cli_path):
            raise RuntimeError('{0} not found'.format(cli_path))

    def execute(self, cmd):
        proc = subprocess.Popen('{0} {1} J'.format(self.cli_path, cmd), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out, err = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode(errors='ignore')
        if isinstance(err, bytes):
            err = err.decode(errors='ignore')
       
        return out

    def adapter(self):
        pass

    def Physical_disks(self, adapter=0):
        '''
        Get Physical disks
        :param adapter: specifies the drive's controller
        :return: a json of all configured physical disks
        :return type: json
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")

        cmd = '/c{0}/eall/sall show'.format(adapter)
        return self.execute(cmd)

    def Virtual_disk(self, adapter=0):
        '''
        Get Virtual disks
        :param adapter: specifies the drive's controller
        :param adapter type: int
        :return: a json of all configured physical disks
        :return type: json
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        
        cmd = '/call/vall show'
        return self.execute(cmd)

    def Create_ld(self, raid_level, name, drives, pdcache='default', write_policy='wt', read_policy='ra', cache_policy='direct', size='all', strip='', spares=[], adapter=0, force=False):
        '''
        Create virtual disk
        :param adapter: specifices the drive's controller
        :param adapter type: int
        :param raid_level: raid level egg: 0|1|5|6|10
        :param raid_level type: int
        :param name: virtual disk name
        :param name type: str
        :param drive: specifies the drive enclosures and slot numbers to construct the drive group. E.g.: ['E0:S0', 'E0:S1', 'E0:S2']
        :param drive type: list
        :param pdcache: Enables or disables PD cache.
        :type write_policy: string
        :param write_policy: specifies the device write policy. Valid arguments: WT (write through) or WB (write back)
        :type write_policy: string
        :param read_policy: specifies the device read policy. Valid arguments: NORA (no read ahead), RA (read ahead), ADRA (adaptive read ahead).
        :type read_policy: string
        :param cache_policy: specifies the device cache policy. Valid arguments: Direct, Cached.
        :type cache_policy: string
        :param size: virtual disk size. E.g.: [Size=<VD1_Sz>,<VD2_Sz>,..|*all]
        :param size type: str
        :param strip: specifies the stripe size. Valid arguments: 8, 16, 32, 64, 128, 256, 512, or 1024.
        :param strip type: int
        :param spares: specifies the device hot spares. E.g.: ['E5:S5', ..]
        :type spares: list
        :param force: whether to force or not the creation of the logical drive
        :type force: bool
        '''
        if not isinstance(adapter,int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if not isinstance(raid_level, int):
            raise ValueError("raid_level must be type int")
        if not isinstance(drives, list):
            raise ValueError("drives must be list")
        if not isinstance(spares, list):
            raise ValueError("spares must be list")
        if pdcache not in ['off', 'on', 'default']:
            raise ValueError("pdcache must be off, on or default")
        if write_policy not in ['wt', 'wb']:
            raise ValueError("write_policy must be WT or WB")
        if read_policy not in ['ra', 'nora']:
            raise ValueError("read_policy must be ra or nora")
        if cache_policy not in ['cached', 'direct']:
            raise ValueError("cache_policy must be direct or cached")
        if spares:
            cmd = '/c{0} add vd type=raid{1} size={2} name={3} drives={4} pdcache={5} {6} {7} {8} strip={9} spares={10} '.format(adapter, raid_level,
                size, name, ','.join(drives), pdcache, write_policy, read_policy, cache_policy, strip, ','.join(spares))
        else:
            cmd = '/c{0} add vd type=raid{1} size={2} name={3} drives={4} pdcache={5} {6} {7} {8} strip={9}'.format(adapter, raid_level,
                size, name, ','.join(drives), pdcache, write_policy, read_policy, cache_policy, strip)
        return self.execute(cmd)

    def Remove_ld(self, ld_id, adapter=0):
        '''
        Remove ld
        :param adapter: specifies the drive's controller
        :param adapter type: int
        :param ld_id: virtual disk id
        :param ld_id type: int
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if not isinstance(ld_id, int):
            raise ValueError("ld_id must be type int")
        
        cmd = '/c{0}/v{1} del'.format(adapter, ld_id)
        return self.execute(cmd)

    def Update_ld(self, adapter=0):
        pass
    
    def Disk_status(self, drive, active, adapter=0):
        '''
        Setting disk status
        :param adapter: specifies the drive's controller
        :param adapter type: int
        :param drive: specifies the drive enclosures and slot numbers to construct the drive group. E.g.: 'E0:S0'
        :param drive type: string
        :param active: good, online, offline, missing, jbod
        :param active type: string
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if not drive:
            raise ValueError("drive not null")
        if not isinstance(active, str):
            raise ValueError("active must be type str")
        device = drive.split(':')
        if active == 'good':
            cmd = '/c{0}/e{1}/s{2} set {3} force'.format(adapter, device[0], device[1], active)
        else:
            cmd = '/c{0}/e{1}/s{2} set {3}'.format(adapter, device[0], device[1], active)
        return self.execute(cmd)

    def Disk_rebuild(self, drive, active, adapter=0):
        '''
        Setting disk rebuild
        :param adapter: specifies the drive's controller
        :param adapter type: int
        :param drive: specifies the drive enclosures and slot numbers to construct the drive group. E.g.: 'E0:S0'
        :param drive type: string
        :param active: start, stop, show
        :param active type: string
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if not drive:
            raise ValueError("drive not null")
        if not isinstance(active, str):
            raise ValueError("active must be type str")
        
        device = drive.split(':')
        cmd = '/c{0}/e{1}/s{2} {3} rebuild'.format(adapter, device[0], device[1], active)
        return self.execute(cmd)

    def Disk_gps(self, drive, active, adapter=0):
        '''
        Setting disk locate
        :param adapter: specifies the drive's controller
        :param adapter type: int
        :param drive: specifies the drive enclosures and slot numbers to construct the drive group. E.g.: 'E0:S0'
        :param drive type: string
        :param active: start, stop
        :param active type: string
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if not drive:
            raise ValueError("drive not null")
        if not isinstance(active, str):
            raise ValueError("active must be type str")
        
        device = drive.split(':')
        cmd = '/c{0}/e{1}/s{2} {3} locate'.format(adapter, device[0], device[1], active)
        return self.execute(cmd)

    def Disk_hot(self, drive, dgs, action, adapter=0):
        '''
        Setting disk host
        :param adapter: specifies the drive's controller
        :param adapter type: int
        :param drive: specifies the drive enclosures and slot numbers to construct the drive group. E.g.: 'E0:S0'
        :param drive type: string
        :param dgs: local hot.if dgs is not ,hot is golbal hot
        :param active type: int
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if not drive:
            raise ValueError("drive not null")
        device = drive.split(':')
        if isinstance(dgs, int):
            dgs = 'dgs={0}'.format(dgs)
        else:
            dgs = ''
        cmd = '/c{0}/e{1}/s{2} {3} hotsparedrive {4}'.format(adapter, device[0], device[1], action, dgs)
        print(cmd)
        return self.execute(cmd)

    def Controller_alarm(self, active, adapter=0):
        '''
        Setting Controller alarm
        :param adapter: specifies the drive's controller
        :param adapter type: int
        :param active: on 、 off or show
        :param active type: str
        '''
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if active == 'show':
            cmd = '/c{0} show alarm'.format(adapter)
        else:
            cmd = '/c{0} set alarm={1}'.format(adapter, active)

        return self.execute(cmd)

    def Disk_init(self, drive, active, adapter=0):
        '''
        Disk init options
        :param active: init options. show, start or stop
        :param active type: str
        '''
        if active not in ['show', 'start', 'stop']:
            raise ValueError("active must be show, start or stop")
        if not isinstance(adapter, int):
            raise ValueError("Logical drive's adapter ID must be type int")
        if not drive:
            raise ValueError("drive not null")
        device = drive.split(':')
        cmd = '/c{0}/e{1}/s{2} {3} initialization'.format(adapter, device[0], device[1], active)
        return self.execute(cmd)
        
    def Virtual_init(self, ld_id, active, adapter=0, _type='full'):
        '''
        Virtual init options
        :param active: init active. e.g. show, start or stop
        :param active type: string
        :param ld_id: virtual id 
        :param ld_id type: int
        '''
        
        if not isinstance(ld_id, int):
            raise ValueError("ld_id must be int")
        if active not in ['show', 'start', 'stop']:
            raise ValueError("active must be start, show or stop")
        if _type:
            cmd = '/{0}/v{1} {2} init {3} force'.format(adapter, ld_id, active, _type)
        else:
            cmd = '/c{0}/v{1} {2} init'.format(adapter, ld_id, active)
        print(cmd)
        return self.execute(cmd)
    
    def jbodStatus(self, active="show", adapter=0):
        if active == 'show':
            cmd = '/c{0} {1} jbod'.format(adapter, active)
        else:
            cmd = '/c{0} set jbod={1}'.format(adapter, active)
        return self.execute(cmd)
