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
rainheader: Probability of precipitation for Exeter, Devon, UK
```



### Usage ###

Currently, only the option `rain` is implemented. So the command 

```
fcst.py rain
```

will produce output similar to

```


      Probability of precipitation for Exeter, Devon, UK

      -------------------------------------------------------------
1.0  :                                                             :
     |                                                             |
     |                                                             |
     |                                                             |
0.75 :         **                                                  :
     |           *                                                 |
     |        *   *                                                |
     |                                                             |
0.5  :       *     *                                               :
     |                                                             |
     |      *                                                      |
     |              *                                              |
0.25 :               *                                             :
     |                                                       ******|
     |     *          **                                *****      |
     |    *             ********                   *****           |
0.0  :****                      *******************                :
      ---------------|--------------|--------------|---------------
                    15             30             45              
                             lead time [min]
     t_0 = 09:37                                  (www.forecast.io)


```


