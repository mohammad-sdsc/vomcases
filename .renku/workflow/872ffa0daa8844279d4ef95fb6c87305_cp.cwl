arguments: []
baseCommand:
- cp
class: CommandLineTool
cwlVersion: v1.0
hints: []
inputs:
  input_1:
    default:
      class: File
      path: ../../work/HowardSprings/nofreedrainage_cpcff1.0/vom_namelist
    inputBinding:
      position: 1
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_2:
    default: work/HowardSprings/nofreedrainage_cpcff1.0/best/vom_namelist
    inputBinding:
      position: 2
      separate: true
      shellQuote: true
    streamable: false
    type: string
outputs:
  output_0:
    outputBinding:
      glob: $(inputs.input_2)
    streamable: false
    type: File
permanentFailCodes: []
requirements:
- class: InlineJavascriptRequirement
- class: InitialWorkDirRequirement
  listing:
  - entry: '$({"listing": [], "class": "Directory"})'
    entryname: work/HowardSprings/nofreedrainage_cpcff1.0/best
    writable: true
successCodes: []
temporaryFailCodes: []
