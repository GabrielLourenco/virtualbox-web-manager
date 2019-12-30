import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { VMService } from 'src/services/vm.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  form: FormGroup
  vms: any;
  selectedVm: any;
  editMode: boolean;
  loading: boolean;

  constructor(private vmService: VMService) {
    this.form = new FormGroup({
      nome: new FormControl('', [Validators.required]),
      ip: new FormControl('', [Validators.required]),
      cpuQtde: new FormControl('', [Validators.required]),
      cpuCap: new FormControl('', [Validators.required]),
      memory: new FormControl('', [Validators.required]),
      hd: new FormControl('', [Validators.required]),
    })
  }

  ngOnInit() {
    this.getMachines()
  }

  getMachines() {
    this.vmService.get().subscribe( res => {
      this.vms = res.data
    })
  }

  selectVm(machine, type) {
    this.selectedVm = machine;
    this.form.controls.nome.setValue(machine.name)
    this.form.controls.ip.setValue('192.168.1.4')
    this.form.controls.cpuQtde.setValue(2)
    this.form.controls.cpuCap.setValue(50)
    this.form.controls.memory.setValue(2048)
    this.form.controls.hd.setValue(13100)

    this.editMode = type === 'edit' ? true : false;
  }

  deleteVm(machine) {
    machine['delete'] = true
    this.vmService.post(machine).subscribe(res => {
      console.log(res);
      this.getMachines()
    })
  }

  toogleOnOffVm(machine) {
    this.selectedVm = undefined;
    if (machine.on) {
      delete machine['start']
      machine['turnOff'] = true;
    } else {
      delete machine['turnOff']
      machine['start'] = true;
    }
    this.vmService.post(machine).subscribe(res => {
      console.log(res);
      this.getMachines()
    })
  }

  enviar() {
    this.loading = true;
    const controls = this.form.controls
    if (!this.editMode) {
      this.selectedVm['clone'] = true
      this.selectedVm['newName'] = controls.nome.value.replace(/ /g, '_');

      this.vmService.post(this.selectedVm).subscribe(res => {
        alert(res.data)
        this.vmService.get().subscribe( res => {
          this.selectedVm = undefined
          res.data.map(machine => {
            if (machine.name === controls.nome.value.replace(/ /g, '_')) {
              this.selectedVm = machine
            }
          })
          this.setVM()
        })
      })
    } else {
      this.setVM()
    }
  }
  setVM() {
    const controls = this.form.controls
    this.selectedVm['hdSize'] = controls.hd.value;
    this.selectedVm['name'] = controls.nome.value.replace(/ /g, '_');
    this.vmService.post(this.selectedVm).subscribe(res => {
      alert(res.data)
      delete this.selectedVm['hdSize']
      this.selectedVm['config'] = {
        cpuCount: controls.cpuQtde.value,
        ip: controls.ip.value,
        cpuCap: controls.cpuCap.value,
        memorySize: controls.memory.value
      }
      this.vmService.post(this.selectedVm).subscribe(res => {
        alert(res.data);
        this.getMachines()
        this.selectedVm = undefined;
        this.loading = false;
      })
    })

  }
}
