## pyfcio: Command line weather forecasts from forecast.io ##


### Requirements ###

* Python2
* a forecast.io API Key (register [here](https://developer.forecast.io/register))


### Install and config ###

* clone the repository (or just download the executable `fcst.py`)
* copy `.pyfcio.conf` to your home directory and add your forecast.io API key



### Example ###

```
./fcst.py rain2
```


```

      ------------------------------------------------- 
1.0  :                                                 :
     |                             X                   |
     |                           ##                    |
0.75 :                          X   o                  :
     |                        oo                       |
     |                       .                         |
0.5  :                               o                 :
     |                      o                          |
     |                                o                |
0.25 :                     .            .              :
     |                                   ..            |
     |                    .                .......... .|
0.0  :....................             .             . :
      -----------|-----------|-----------|-----------|- 
                Tue         12:00       Wed         12:00 
                                  (src: www.forecast.io)

```


### Usage ###

```
./fcst.py mode
```

where `mode` is one of the following:

* **rain**: probability of precipitation over the next 60 minutes (not available in all locations)
* **rain2**: probability of precipitation over the next 48 hours
* the markers indicate intensity of precipitation:
   `.` 0 - 1 mm/h | `o` 1 - 2 mm/h | `X` 2 - 5 mm/h | `#`   > 5 mm/h
* **temp**: temperature forecast over the next 48 hours
* **now**: print current weather conditions

For more information type

```
./fcst.py --help
```

 
