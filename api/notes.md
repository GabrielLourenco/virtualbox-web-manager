- Quantidade de processadores: `echo %NUMBER_OF_PROCESSORS%`
- Quantidade de memória: `wmic ComputerSystem get TotalPhysicalMemory`
- Quantidade de hd: `wmic logicaldisk get freespace`

# VMCommands
- Listar VMs: `vboxmanage list vms`
- Listar VMs ativas: `vboxmanage list runningvms`
- Iniciar VM: `vboxmanage startvm fea1fdc2-f542-4aea-9509-0b4bc0245de2`
- Desligar VM: `vboxmanage controlvm "victim2" poweroff`
- Clonar VM: `VBoxManage export UbuntuServer --output UbuntuServer_3/UbuntuServer_3.ova` e `VBoxManage import UbuntuServer_3/UbuntuServer_3.ova`
- Aumentar tamanho do HD: `VBoxManage modifyhd "C:\Users\Martin\VirtualBox VMs\windows 7\windows 7.vdi" −−resize 40000`
- Mudar IP e mascara da rede NAT: (talvez) `VBoxManage modifyvm "VM name" --natbindip1 "the external IP you want"`
- Mudar capacidade cpu: `VBoxManage modifyvm "C:\Users\Martin\VirtualBox VMs\windows 7\windows 7.vdi" −−cpuexecutioncap 50`
- Mudar quantidade cpu: `VBoxManage modifyvm "VM name" --cpus 2`
- Mudar qtde memória: `VBoxManage modifyvm "C:\Users\Martin\VirtualBox VMs\windows 7\windows 7.vdi" −−memory 2048`

# Passos
1) escolher (liga ou desliga máquina) ou criar uma máquina nova (clonar)
2) Caso clonar, escolher qual SO. (Ubuntu, Lubuntu)
3) Configurar as coisas com base no que a API retornar (cpu, memoria e hd size)
4) configurar capacidade cpu
5) Finalizar com a opção de ligar e atualizar lista de vms

# Atenção
Só da pra mudar as coisas com a máquina desligada.
O tamanho do HD só aumenta, não diminui