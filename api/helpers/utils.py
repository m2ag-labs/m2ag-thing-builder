import subprocess
import time
import os


class Utils:

    @staticmethod
    def i2cdetect():
        p = subprocess.Popen(['/usr/sbin/i2cdetect', '-y', '1'], stdout=subprocess.PIPE, )
        line = ''
        for i in range(0, 9):
            line += str(p.stdout.readline().decode('utf-8'))
        return line

    @staticmethod
    def service_action(service, action):
        if action in ['start', 'stop', 'restart', 'enable', 'disable']:
            subprocess.Popen(['sudo', '/bin/systemctl', action, service], stdout=subprocess.PIPE, )
            time.sleep(2)

        p = subprocess.Popen(['sudo', '/bin/systemctl', 'status', service], stdout=subprocess.PIPE, )
        line = ''
        for i in range(0, 15):
            line += str(p.stdout.readline().decode('utf-8'))
        return line

    @staticmethod
    def pinout():
        p = subprocess.Popen(['/usr/bin/pinout', '-m'], stdout=subprocess.PIPE, )
        line = ''
        for i in range(0, 50):
            line += str(p.stdout.readline().decode('utf-8'))
        return line

    @staticmethod
    def get_pip(package):
        p = subprocess.Popen([f'{os.getcwd()}/venv/bin/pip3', 'show', package], stdout=subprocess.PIPE)
        line = ''
        for i in range(0, 50):
            line += str(p.stdout.readline().decode('utf-8'))
        return line

    @staticmethod
    def get_pip_list():
        p = subprocess.Popen([f'{os.getcwd()}/venv/bin/pip3', 'list'], stdout=subprocess.PIPE)
        line = ''
        for i in range(0, 50):
            line += str(p.stdout.readline().decode('utf-8'))
        return line

    @staticmethod
    def put_pip(package):
        p = subprocess.Popen([f'{os.getcwd()}/venv/bin/pip3', 'install', package], stdout=subprocess.PIPE)
        line = ''
        for i in range(0, 50):
            line += str(p.stdout.readline().decode('utf-8'))
        return line

    @staticmethod
    def delete_pip(package):
        p = subprocess.Popen([f'{os.getcwd()}/venv/bin/pip3', 'uninstall', package, '-y'], stdout=subprocess.PIPE)
        line = ''
        for i in range(0, 50):
            line += str(p.stdout.readline().decode('utf-8'))
        return line

