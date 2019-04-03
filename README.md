## `darksky`: Command line weather forecasts 

Plot weather forecast charts into the command line terminal. **Powered by [Dark Sky](https://darksky.net/poweredby)**




### Example and usage ###


```
./darksky rain2
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

```


The generic call is 

```
./darksky [mode]
```

where `mode` is one of the following:

* **rain**: probability of precipitation over the next 60 minutes (not available in all locations)
* **rain2**: probability of precipitation over the next 48 hours
* the markers indicate intensity of precipitation:
   `.` 0 - 1 mm/h | `o` 1 - 2 mm/h | `X` 2 - 5 mm/h | `#`   > 5 mm/h
* **temp**: temperature forecast over the next 48 hours
* **now**: print current weather conditions

For all command line arguments, see

```
./darksky --help
```

 
### Requirements ###

* Python2
* for a limited number of queries API key is not required for continuous use
* a darksky.net API key (get one at [darksky.net/dev](https://darksky.net/dev))


### Install and config ###

* clone the repository (or just download the [darksky](darksky) python script)
* the configuration will be writen at the first launch of the program to `~/.darksky.conf` when you also need to fill the location data and optionaly the API key



