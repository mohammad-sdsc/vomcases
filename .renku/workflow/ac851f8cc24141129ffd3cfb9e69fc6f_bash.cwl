arguments: []
baseCommand:
- bash
class: CommandLineTool
cwlVersion: v1.0
hints: []
inputs:
  input_1:
    default:
      class: File
      path: ../../src_sh/run_vom2.sh
    inputBinding:
      position: 1
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_2:
    default:
      class: Directory
      listing: []
      path: ../../src/VOM/VOM_Fortran
    inputBinding:
      position: 2
      separate: true
      shellQuote: true
    streamable: false
    type: Directory
  input_3:
    default:
      class: Directory
      listing: []
      path: ../../work/additional_analyses/prescribed_cover/AdelaideRiver/best/input
    inputBinding:
      position: 3
      separate: true
      shellQuote: true
    streamable: false
    type: Directory
  input_4:
    default:
      class: File
      path: ../../work/additional_analyses/prescribed_cover/AdelaideRiver/best/input/dailyweather.prn
    inputBinding:
      position: 4
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_5:
    default:
      class: File
      path: ../../work/additional_analyses/prescribed_cover/AdelaideRiver/best/input/soilprofile.par
    inputBinding:
      position: 5
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_6:
    default:
      class: File
      path: ../../work/additional_analyses/prescribed_cover/AdelaideRiver/best/vom_namelist
    inputBinding:
      position: 6
      separate: true
      shellQuote: true
    streamable: false
    type: File
  input_7:
    default: data/VOM_output/additional_analyses/prescribed_cover/AdelaideRiver/sce_best
    inputBinding:
      position: 7
      separate: true
      shellQuote: true
    streamable: false
    type: string
  input_8:
    default:
      class: File
      path: ../../work/additional_analyses/prescribed_cover/AdelaideRiver/best/input/perc_cov.txt
    inputBinding:
      position: 8
      separate: true
      shellQuote: true
    streamable: false
    type: File
outputs:
  output_0:
    outputBinding:
      glob: $(inputs.input_7)
    streamable: false
    type: Directory
permanentFailCodes: []
requirements:
- class: InlineJavascriptRequirement
- class: InitialWorkDirRequirement
  listing:
  - entry: $(inputs.input_1)
    entryname: src_sh/run_vom2.sh
    writable: false
  - entry: $(inputs.input_2)
    entryname: src/VOM/VOM_Fortran
    writable: false
  - entry: $(inputs.input_3)
    entryname: work/additional_analyses/prescribed_cover/AdelaideRiver/best/input
    writable: false
  - entry: $(inputs.input_4)
    entryname: work/additional_analyses/prescribed_cover/AdelaideRiver/best/input/dailyweather.prn
    writable: false
  - entry: $(inputs.input_5)
    entryname: work/additional_analyses/prescribed_cover/AdelaideRiver/best/input/soilprofile.par
    writable: false
  - entry: $(inputs.input_6)
    entryname: work/additional_analyses/prescribed_cover/AdelaideRiver/best/vom_namelist
    writable: false
  - entry: $(inputs.input_8)
    entryname: work/additional_analyses/prescribed_cover/AdelaideRiver/best/input/perc_cov.txt
    writable: false
successCodes: []
temporaryFailCodes: []
