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
* **temp**: temperature forecast over the next 48 hours
* **rain2**: probability of precipitation over the next 48 hours


For example, the command

```
./fcst.py rain
```

will produce output similar to

```

      ------------------------------------------------------------- 
1.0  :                             *********                       :
     |                           **         *                      |
     |                          *            *                     |
0.75 :                                        *                    :
     |                        *                *                   |
     |                      ** *                *                  |
0.5  :                     *                     *****             :
     |                                                *            |
     |       **           *                            *           |
0.25 :      *  *                                        *          :
     |     *    *        *                               *****     |
     | ****      *      *                                     *    |
0.0  :*           ******                                       ****:
      |--------------|--------------|--------------|--------------- 
      01:08          +15min         +30min         +45min          
                                              (src: www.forecast.io)

```


