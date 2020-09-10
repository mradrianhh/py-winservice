import socket
import time
import random

from win32.lib import win32serviceutil

from win32 import servicemanager
from win32 import win32event
from win32 import win32service

from pathlib import Path

class SMWinservice(win32serviceutil.ServiceFramework):
    """Base class to create winservice in python."""
    
    _svc_name_ = "pythonService"
    _svc_display_name_ = "Python Service"
    _svc_description_ = "Python Service Description"

    @classmethod
    def parse_command_line(cls):
        """
        ClassMethod to parse the command line.
        """
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        """
        Constructor of the winservice.
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """
        Called when the service is asked to stop.
        """
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """
        Called when the service is asked to start.
        """
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        while self.isrunning:
            random.seed()
            x = random.randint(1, 1000000)
            Path(f'c:{x}.txt').touch()
            time.sleep(5)

if __name__ == '__main__':
    SMWinservice.parse_command_line()