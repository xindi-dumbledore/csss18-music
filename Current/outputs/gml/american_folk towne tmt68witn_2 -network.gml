graph [
  directed 1
  node [
    id 0
    label "-3|"
  ]
  node [
    id 1
    label "-5|-3"
  ]
  node [
    id 2
    label "-8|"
  ]
  node [
    id 3
    label "-5|-8"
  ]
  node [
    id 4
    label "-7|"
  ]
  node [
    id 5
    label "-5|"
  ]
  edge [
    source 0
    target 1
    weight 1.0
  ]
  edge [
    source 1
    target 4
    weight 1.0
  ]
  edge [
    source 2
    target 3
    weight 1.0
  ]
  edge [
    source 3
    target 0
    weight 1.0
  ]
  edge [
    source 4
    target 2
    weight 1.0
  ]
  edge [
    source 5
    target 4
    weight 0.5
  ]
  edge [
    source 5
    target 0
    weight 0.5
  ]
]
