Cheat Sheet: https://cheatography.com/flltech2019/cheat-sheets/pybricks-cheatsheet-by-fll-techtacos-sugarland/


Reference values: 
https://github.com/pybricks/pybricks-micropython/blob/master/lib/pbio/platform/prime_hub/pbdrvconfig.h
``` c
#define PBDRV_CONFIG_BATTERY_ADC_VOLTAGE_RAW_MAX    4096
#define PBDRV_CONFIG_BATTERY_ADC_VOLTAGE_SCALED_MAX 9900
#define PBDRV_CONFIG_BATTERY_ADC_CURRENT_RAW_MAX    4096
#define PBDRV_CONFIG_BATTERY_ADC_CURRENT_SCALED_MAX 7300
```

https://github.com/pybricks/pybricks-micropython/blob/master/lib/pbio/sys/battery.c
```c
// These values are for LEGO rechargeable battery packs
#define LIION_FULL_MV           8300    // 4.15V per cell
#define LIION_OK_MV             7200    // 3.6V per cell
#define LIION_LOW_MV            6800    // 3.4V per cell
#define LIION_CRITICAL_MV       6000    // 3.0V per cell

```

Measuring battery voltage is important because it allows you to determine the battery’s state of charge

- After full charge: Battery Voltage: 7670, Battery Current: 28
