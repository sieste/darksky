## pyfcio: Command line weather forecasts from forecast.io ##

### Requirements ###

* Python2
* a forecast.io API Key (register [here](https://developer.forecast.io/register))
* tested under Arch Linux (3.12.7)

### Install and config ###

* download the executable `fcst.py` 
* create the file `.pyfcio.conf` in your home directory with the following options (adjusted to your location):

```
[Settings]
forecastioApiKey: yOUr_foRecAST_dOt_Io_Api_Key
lat: 50.7166
lon: -3.5333
downloadIfOlder: 120
jsonFile: /tmp/forecastio.json
plotsize: 2
```



### Usage ###

```
./fcst.py mode
```

The following modes are currently implemented

* **rain**: probability of precipitation over the next 60 minutes
* **rain2**: probability of precipitation over the next 48 hours
* the markers indicate intensity of precipitation:
    + `.` = 0 - 1 mm/h
    + `o` = 1 - 2 mm/h
    + `X` = 2 - 5 mm/h
    + `#` =   > 5 mm/h
* **temp**: temperature forecast over the next 48 hours


For example, the command

```
./fcst.py rain2
```

will produce output similar to

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


