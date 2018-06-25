graph [
  directed 1
  node [
    id 0
    label "-8|"
  ]
  node [
    id 1
    label "-12|"
  ]
  node [
    id 2
    label "128|"
  ]
  node [
    id 3
    label "-10|"
  ]
  node [
    id 4
    label "-5|"
  ]
  node [
    id 5
    label "128|-12"
  ]
  node [
    id 6
    label "128|-10"
  ]
  edge [
    source 1
    target 5
    weight 1.0
  ]
  edge [
    source 2
    target 1
    weight 0.5
  ]
  edge [
    source 2
    target 4
    weight 0.125
  ]
  edge [
    source 2
    target 0
    weight 0.125
  ]
  edge [
    source 2
    target 3
    weight 0.25
  ]
  edge [
    source 3
    target 6
    weight 1.0
  ]
  edge [
    source 5
    target 1
    weight 1.0
  ]
  edge [
    source 6
    target 3
    weight 1.0
  ]
]
