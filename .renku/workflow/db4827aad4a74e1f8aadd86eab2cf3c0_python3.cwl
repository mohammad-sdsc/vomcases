arguments: []
baseCommand:
- python3
class: CommandLineTool
cwlVersion: v1.0
hints: []
inputs:
  input_1:
    default:
      class: File
      path: ../../src_py/sce_uncertainty.py
    inputBinding:
      position: 1
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_10:
    default: 1
    inputBinding:
      position: 10
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_11:
    default: 1
    inputBinding:
      position: 11
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_12:
    default: 0
    inputBinding:
      position: 12
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_13:
    default: 1
    inputBinding:
      position: 13
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_14:
    default:
      class: File
      path: ../../data/VOM_input/DalyUncleared/dailyweather.prn
    inputBinding:
      position: 14
      prefix: -d
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_15:
    default:
      class: Directory
      listing: []
      path: ../../work/DalyUncleared/nofreedrainage_cpcff1.0/best
    inputBinding:
      position: 15
      prefix: -w
      separate: true
      shellQuote: true
    streamable: false
    type: Directory
  input_16:
    default:
      class: File
      path: ../../src/VOM/VOM_Fortran/VOM-code/coreprog.f90
    inputBinding:
      position: 16
      prefix: -c
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_17:
    default:
      class: File
      path: ../../src/VOM/VOM_Fortran/VOM-code/modules.f90
    inputBinding:
      position: 17
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_18:
    default:
      class: File
      path: ../../src/VOM/VOM_Fortran/VOM-code/sample.f90
    inputBinding:
      position: 18
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_19:
    default:
      class: File
      path: ../../src/VOM/VOM_Fortran/VOM-code/sce.f90
    inputBinding:
      position: 19
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_2:
    default:
      class: File
      path: ../../data/VOM_output/DalyUncleared/nofreedrainage_cpcff1.0/sce_out.txt
    inputBinding:
      position: 2
      prefix: -i
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_20:
    default:
      class: File
      path: ../../src/VOM/VOM_Fortran/VOM-code/transpmodel.f90
    inputBinding:
      position: 20
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_21:
    default:
      class: File
      path: ../../src/VOM/VOM_Fortran/VOM-code/watbal.f90
    inputBinding:
      position: 21
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_3:
    default: data/VOM_output/DalyUncleared/nofreedrainage_cpcff1.0/bestruns
    inputBinding:
      position: 3
      prefix: -o
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_4:
    default: 5
    inputBinding:
      position: 4
      prefix: -p
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_5:
    default: p
    inputBinding:
      position: 5
      prefix: -o
      separate: false
      shellQuote: true
    streamable: false
    type: string
  input_6:
    default: 1
    inputBinding:
      position: 6
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_7:
    default: 1
    inputBinding:
      position: 7
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_8:
    default: 1
    inputBinding:
      position: 8
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_9:
    default: 1
    inputBinding:
      position: 9
      separate: true
      shellQuote: true
    streamable: false
    type: int
outputs:
  output_0:
    outputBinding:
      glob: src/VOM
    streamable: false
    type: Directory
  output_1:
    outputBinding:
      glob: $(inputs.input_3)
    streamable: false
    type: Directory
permanentFailCodes: []
requirements:
- class: InlineJavascriptRequirement
- class: InitialWorkDirRequirement
  listing:
  - entry: '$({"listing": [], "class": "Directory"})'
    entryname: src/VOM
    writable: true
  - entry: '$({"listing": [], "class": "Directory"})'
    entryname: data/VOM_output/DalyUncleared/nofreedrainage_cpcff1.0/bestruns
    writable: true
successCodes: []
temporaryFailCodes: []
