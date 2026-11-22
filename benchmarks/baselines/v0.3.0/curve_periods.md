# v0.3.0 full curve-period comparison

See [protocol and summary](README.md). Each time is the median of three
fresh-process trials. The two untimed rows are expected singular rejections.

| Workload | Digits | v0.2.0 seconds | Candidate seconds | Candidate / v0.2.0 | Scaled error |
| --- | ---: | ---: | ---: | ---: | ---: |
| hyper-g1-lemniscatic | 30 | 0.0153505 | 0.0155987 | 1.01617 | 0.0 |
| hyper-g1-lemniscatic | 50 | 0.0354237 | 0.0352512 | 0.995129 | 0.0 |
| hyper-g2-symmetric | 30 | 0.055814 | 0.055455 | 0.993567 | 0.0 |
| hyper-g2-symmetric | 50 | 0.127386 | 0.126913 | 0.996287 | 0.0 |
| hyper-g3-symmetric | 30 | 0.135993 | 0.135983 | 0.999923 | 0.0 |
| hyper-g3-symmetric | 50 | 0.308116 | 0.307017 | 0.996435 | 0.0 |
| hyper-g2-even | 30 | 0.0736218 | 0.0733384 | 0.99615 | 0.0 |
| hyper-g2-even | 50 | 0.16792 | 0.167097 | 0.9951 | 0.0 |
| hyper-g2-clustered | 30 | 0.0840123 | 0.0831086 | 0.989243 | 0.0 |
| hyper-g2-clustered | 50 | 0.114746 | 0.114913 | 1.00146 | 0.0 |
| hyper-g3-generic | 30 | 0.170022 | 0.170079 | 1.00033 | 0.0 |
| hyper-g3-generic | 50 | 0.322661 | 0.322333 | 0.998982 | 0.0 |
| hyper-g4-symmetric | 30 | 0.265639 | 0.265024 | 0.997688 | 0.0 |
| hyper-g4-symmetric | 50 | 0.600818 | 0.628846 | 1.04665 | 0.0 |
| general-g1-lemniscatic | 30 | 0.393106 | 0.394112 | 1.00256 | 0.0 |
| general-g1-lemniscatic | 50 | 0.606308 | 0.607606 | 1.00214 | 0.0 |
| general-trig-g3 | 30 | 2.54764 | 2.52587 | 0.991451 | 0.0 |
| general-trig-g3 | 50 | 3.11684 | 3.10139 | 0.995043 | 0.0 |
| general-trig-pure-g3 | 30 | 0.952399 | 0.95297 | 1.0006 | 0.0 |
| general-trig-pure-g3 | 50 | 1.63517 | 1.62599 | 0.994384 | 0.0 |
| general-trig-dense-g3 | 30 | 1.86 | 1.81787 | 0.977353 | 3.421138828918010427059886677953896804883451963e-49 |
| general-trig-dense-g3 | 50 | 2.79172 | 2.74718 | 0.984045 | 2.8978173052245479576029181730840933698184099834045242206664367647e-70 |
| general-klein-quartic-g3 | 30 | 1.51496 | 1.50749 | 0.995066 | 0.0 |
| general-klein-quartic-g3 | 50 | 2.33524 | 2.35437 | 1.00819 | 0.0 |
| general-fermat-quartic-g3 | 30 | 1.13731 | 1.13039 | 0.993911 | 0.0 |
| general-fermat-quartic-g3 | 50 | 2.07411 | 2.07889 | 1.0023 | 0.0 |
| general-super-g4 | 30 | 1.22282 | 1.22213 | 0.999437 | 0.0 |
| general-super-g4 | 50 | 2.07111 | 2.07689 | 1.00279 | 0.0 |
| general-kovalevskaya-g3 | 30 | 8.87555 | 8.6532 | 0.974948 | 7.4751399258098194922689830705520610246427123e-49 |
| general-kovalevskaya-g3 | 50 | 13.3865 | 12.0754 | 0.902059 | 2.6922390344685467283172769480272354468362550760723642432531214114092717191618295e-68 |
| nonmonic-elliptic | 30 | 0.398524 | 0.397 | 0.996178 | 0.0 |
| nonmonic-elliptic | 50 | 0.653481 | 0.651805 | 0.997435 | 0.0 |
| general-trig-test-g3 | 30 | 0.999283 | 0.993122 | 0.993834 | 0.0 |
| general-trig-test-g3 | 50 | 1.56415 | 1.59052 | 1.01686 | 0.0 |
| general-trig-infinity-g3 | 30 | 0.959501 | 0.956559 | 0.996933 | 0.0 |
| general-trig-infinity-g3 | 50 | 1.65588 | 1.64158 | 0.991365 | 0.0 |
| klein-x-translated | 30 | 2.19633 | 2.17852 | 0.991895 | 0.0 |
| klein-x-translated | 50 | 3.16969 | 3.18856 | 1.00595 | 0.0 |
| klein-x-scaled | 30 | 1.5257 | 1.5198 | 0.996133 | 0.0 |
| klein-x-scaled | 50 | 2.35747 | 2.35559 | 0.999203 | 0.0 |
| general-mu-x-translated | 30 | 2.55085 | 2.51171 | 0.984658 | 0.0 |
| general-mu-x-translated | 50 | 3.81183 | 3.766 | 0.987978 | 0.0 |
| hyper-g2-close-001 | 30 | 0.0843639 | 0.0848029 | 1.0052 | 0.0 |
| hyper-g2-close-001 | 50 | 0.181806 | 0.184678 | 1.0158 | 0.0 |
| hyper-g2-close-00001 | 30 | 0.137101 | 0.136612 | 0.996437 | 0.0 |
| hyper-g2-close-00001 | 50 | 0.234373 | 0.240668 | 1.02686 | 0.0 |
| hyper-g2-complex | 30 | 0.515657 | 0.507893 | 0.984943 | 0.0 |
| hyper-g2-complex | 50 | 0.629103 | 0.623952 | 0.991812 | 0.0 |
| hyper-g1-linear-y | 30 | 0.0154715 | 0.0154585 | 0.999154 | 0.0 |
| hyper-g1-linear-y | 50 | 0.0357115 | 0.0358643 | 1.00428 | 0.0 |
| singular-g1-double-point | 30 | — | — | — | 0.0 |
| singular-g1-double-point | 50 | — | — | — | 0.0 |
