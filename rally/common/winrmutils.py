# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from base64 import b64encode

from rally.common import logging

LOG = logging.getLogger(__name__)

try:
    import winrm
except ImportError:
    raise Exception("PyWinrm is not installed")


class WinrmClient(object):
    _URL_TEMPLATE = '%(protocol)s://%(ip)s:%(port)s/wsman'
    _PROTOCOL = None
    _PORT = None

    def __init__(self, server_ip, username, password, transport='plaintext',
                 cmd_timeout=None):
        """
        @param string server_ip: the server ip
        @param string username: username used to login
        @param string password: password used to login
        @param string transport: transport type, one of 'plaintext' (default),
            'kerberos', 'ssl'
        @param int cmd_timeout: WinRM command execution timeout
        """
        self._PROTOCOL = 'http' if transport == 'plaintext' else 'https'
        self._PORT = 5985 if self._PROTOCOL == 'http' else 5986

        _url = self._get_url(server_ip)
        self._conn = winrm.protocol.Protocol(
            endpoint=_url, username=username, password=password,
            transport=transport)

        if cmd_timeout:
            self._conn.set_timeout(cmd_timeout)

    def exec_cmd(self, command, args=(), check_output=True):
        shell_id = self._conn.open_shell()
        command_id = self._conn.run_command(shell_id, command, args)
        if check_output is True:
            rs = winrm.Response(
                self._conn.get_command_output(shell_id, command_id))
            if rs.status_code != 0:
                raise Exception(rs)
            else:
                return rs
        return None

    def run_powershell(self, script):
        encoded_ps = b64encode(script.encode('utf_16_le')).decode('ascii')
        cmd = 'powershell -encodedcommand {0}'.format(encoded_ps)
        return self.exec_cmd(cmd)

    def _get_url(self, ip):
        return self._URL_TEMPLATE % {'protocol': self._PROTOCOL,
                                     'ip': ip,
                                     'port': self._PORT}

    def test_winrm(self, cmd):
        return self.run_powershell(cmd)
