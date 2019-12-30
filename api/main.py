import subprocess
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

class VBox():
    machine = {'name': '', 'uid': '', 'path': 'C:\\Users\\gabri\VirtualBox VMs\\'}
    def __init__(self):
        self.VBoxManage = 'cd C:/Program Files/Oracle/VirtualBox/ & VBoxManage.exe '
        self.cmd = {
            'listVm': self.VBoxManage + 'list vms',
            'listRunningVm': self.VBoxManage + 'list runningvms',
            'startVm': self.startVm,
            'powerOffVm': self.offVm,
            'cloneVm': self.cloneVm,
            'deleteVm': self.deleteVm,
            'hdResize': self.hdResize,
            'modifyVm': self.cpuMemoryIp
        }

    def startVm(self):
        return self.VBoxManage + 'startvm ' + self.machine['uid']

    def offVm(self):
        return self.VBoxManage + 'controlvm ' + self.machine['uid'] + ' poweroff'
    
    def deleteVm(self):
        return self.VBoxManage + 'unregistervm ' + self.machine['uid'] + ' --delete'

    def cloneVm(self, newName):
        return self.VBoxManage + 'clonevm %s --name %s --register' % (self.machine['name'], newName)
        # return self.VBoxManage + 'export %s --output %s.ova & VBoxManage.exe import %s.ova' % (self.machine['name'], self.machine['path'] + newName, self.machine['path'] + newName)

    def cpuMemoryIp(self, cpuCount, cpuCap, memorySize, ip):
        # ip, mask = ip.split('/') 
        return self.VBoxManage + 'modifyvm ' + self.machine['uid'] + ' --cpus %i --memory %i --natbindip1 %s --name %s --cpuexecutioncap %i' %(cpuCount, memorySize, ip, self.machine['name'], cpuCap)

    def hdResize(self, size):
        return self.VBoxManage + 'modifyhd "%s\\%s.vdi" --resize %i' %(self.machine['path'] + self.machine['name'], self.machine['name'], size)

def runCmd(command):
    return subprocess.check_output(command, shell=True, text=True)

def createMachineList(cmd):
    machines = []
    for item in cmd.split('\n'):
        if len(item) > 0:
            items = item.split(' ')
            machines.append({'uid': items[1].replace('{', '').replace('}', ''), 'on': False, 'name': items[0].replace('"', '')})

    return machines

def matchOnMachines(machines, onMachines):
    for machine in machines:
        if machine in onMachines:
            machine['on'] = True

    return machines

app = Flask(__name__)
api = Api(app)
vBox = VBox()

cors = CORS(app, resources={'/*': {'origins': '*'}})


class VMs(Resource):
    def get(self):
        machines = createMachineList(runCmd(vBox.cmd['listVm']))
        machines = matchOnMachines(machines, createMachineList(runCmd(vBox.cmd['listRunningVm'])))


        return {'data': machines}

    def post(self):
        data = request.get_json()
        vBox.machine['uid'] = data['uid']
        vBox.machine['name'] = data['name']

        if data.get('start') is not None:
            return {'data': runCmd(vBox.cmd['startVm']())}
        
        if data.get('turnOff') is not None:
            return {'data': runCmd(vBox.cmd['powerOffVm']())}
        
        if data.get('clone') is not None:
            newName = data['newName']
            runCmd(vBox.cmd['cloneVm'](newName))
            return {'data': 'Clone realizado com sucesso'}
        
        if data.get('delete') is not None:
            return {'data': runCmd(vBox.cmd['deleteVm']())}

        if data.get('hdSize') is not None:
            try:
                runCmd(vBox.cmd['hdResize'](data['hdSize']))
                return {'data': 'Tamanho do HD alterado com sucesso'}
            except:
                return {'data': "O tamanho do HD deve ser maior do que o informado. Ignorando..."}
        
        if data.get('config') is not None:
            spec = data['config']
            runCmd(vBox.cmd['modifyVm'](spec['cpuCount'], spec['cpuCap'], spec['memorySize'], spec['ip']))
            return {'data': "Máquina atualizada com sucesso"}



api.add_resource(VMs, '/vms')

if __name__ == '__main__':
    app.run(debug=True)
