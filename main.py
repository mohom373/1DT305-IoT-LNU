from machine import Pin, ADC
import utime

#Select ADC input 0 (GPIO26)
COV_RATIO     =  0.2 #ug/mmm / mv
NO_DUST_VOLTAGE = 400  #mv
SYS_VOLTAGE = 3300


class Dust:
    def __init__(self):
         #Select ADC input 0 (GPIO26)
        self.ADC_ConvertedValue = ADC(0)
        self.DIN = Pin(22,Pin.OUT)
        self.conversion_factor = 3.3 / (65535)
        self.flag_first = 0
        self.buff = [0,0,0,0,0,0,0,0,0,0]
        self.sum1 = 0
    
    def _median(self, lst) -> float:
        n = len(lst)
        s = sorted(lst)
        mid = n // 2
        if n % 2 == 0:
            return (s[mid - 1] + s[mid]) / 2
        else:
            return s[mid]
    
    def _IQR(self, lst) -> tuple[float, float, float]:
        n = len(lst)
        s = sorted(lst)
        q1 = self._median(s[:n//2])
        q3 = self._median(s[(n+1)//2:])
        return q1, q3, q3 - q1
    
    def _remove_outliers(self, lst: list[float]) -> tuple[float]:
        # Compute Q1, Q3, and IQR
        q1, q3, iqr = self._IQR(lst)
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Filter the data
        return tuple(x for x in lst if lower_bound <= x <= upper_bound)
            
    def Filter(self,ad_value):      
        buff_max = 10
        if self.flag_first == 0:
            self.flag_first = 1
            for i in range (buff_max):
                self.buff[i] = ad_value
                self.sum1 = self.sum1+self.buff[i]
            return ad_value
        else:
            self.sum1 = self.sum1-self.buff[0]
            for i in range (buff_max-1):
                self.buff[i] = self.buff[i+1]
            self.buff[9] = ad_value
            self.sum1 = self.sum1 + self.buff[9]
            i = self.sum1 / 10.0
            return i
    
    def read(self) -> float:
        AD_value = self.ADC_ConvertedValue.read_u16()
        AD_value = self.Filter(AD_value)
        voltage = (SYS_VOLTAGE / 65536.0) * AD_value * 11
        if voltage >= NO_DUST_VOLTAGE:
            voltage = voltage - NO_DUST_VOLTAGE
            density = voltage * COV_RATIO
        else:
            density = 0
        return density
    
    def big_read(self): 
        lst = []
        for i in range(45):
            lst.append(self.read())
            utime.sleep(0.05)
            
        new_lst = self._remove_outliers(lst)
        return sum(new_lst) / len(new_lst)

try:
    Dust=Dust()

    while True :
        
        average_density = Dust.big_read()    
        print(f'The average dust concentration is: {average_density} ug/m3')  
        
except Exception as e:
    print(e + " Anything")
    