graph [
  directed 1
  node [
    id 0
    label "128|"
  ]
  node [
    id 1
    label "-17|"
  ]
  node [
    id 2
    label "128|-17"
  ]
  node [
    id 3
    label "-24|"
  ]
  edge [
    source 0
    target 3
    weight 0.8
  ]
  edge [
    source 0
    target 1
    weight 0.2
  ]
  edge [
    source 1
    target 2
    weight 1.0
  ]
  edge [
    source 2
    target 1
    weight 1.0
  ]
  edge [
    source 3
    target 0
    weight 1.0
  ]
]
