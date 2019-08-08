arguments:
- position: 6
  separate: true
  shellQuote: true
  valueFrom: --i_lat
baseCommand:
- python3
class: CommandLineTool
cwlVersion: v1.0
hints: []
inputs:
  input_1:
    default:
      class: File
      path: ../../src_py/write_namelist.py
    inputBinding:
      position: 1
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_10:
    default: 1.23d-5
    inputBinding:
      position: 10
      prefix: --i_ksat
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_11:
    default: 0.065d0
    inputBinding:
      position: 11
      prefix: --i_thetar
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_12:
    default: 0.41d0
    inputBinding:
      position: 12
      prefix: --i_thetas
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_13:
    default: 1.89d0
    inputBinding:
      position: 13
      prefix: --i_nvg
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_14:
    default: 7.5d0
    inputBinding:
      position: 14
      prefix: --i_avg
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_15:
    default: '0.5'
    inputBinding:
      position: 15
      prefix: --i_delz
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_16:
    default: 2000
    inputBinding:
      position: 16
      prefix: --i_firstyear
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_17:
    default: 2005
    inputBinding:
      position: 17
      prefix: --i_lastyear
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_18:
    default: 0
    inputBinding:
      position: 18
      prefix: --opt_rgdepth
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_19:
    default: work/additional_analyses/comp2015/10_hydro1/vom_namelist
    inputBinding:
      position: 19
      prefix: -o
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_2:
    default: s
    inputBinding:
      position: 2
      prefix: -i
      separate: false
      shellQuote: true
    streamable: false
    type: string
  input_3:
    default:
      class: File
      path: ../../data/ELVIS/howard_stats.txt
    inputBinding:
      position: 3
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_4:
    default: 30
    inputBinding:
      position: 4
      prefix: --i_maxyear
      separate: true
      shellQuote: true
    streamable: false
    type: int
  input_5:
    default: 1.0d-6
    inputBinding:
      position: 5
      prefix: --i_cpccf
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_7:
    default: '2.49'
    inputBinding:
      position: 7
      prefix: '-1'
      separate: false
      shellQuote: true
    streamable: false
    type: string
  input_8:
    default: '2.0'
    inputBinding:
      position: 8
      prefix: --i_cgs
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_9:
    default: '6.6'
    inputBinding:
      position: 9
      prefix: --i_zr
      separate: true
      shellQuote: true
    streamable: false
    type: string
outputs:
  output_0:
    outputBinding:
      glob: $(inputs.input_19)
    streamable: false
    type: File
permanentFailCodes: []
requirements:
- class: InlineJavascriptRequirement
- class: InitialWorkDirRequirement
  listing:
  - entry: '$({"listing": [], "class": "Directory"})'
    entryname: work/additional_analyses/comp2015/10_hydro1
    writable: true
successCodes: []
temporaryFailCodes: []
