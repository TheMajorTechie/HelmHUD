'''
   HelmHUD GPS module to gather and publish GPS information.
   
   For use with the DFRobot Gravity GNSS GPS Beidou Receiver module (https://www.dfrobot.com/product-2651.html)
   Use in I2C mode with the pins for I2C number 0. 
   Requires the smbus_wrapper library and the modified DFRobot_GNSS library in order to work. 
   
   Written by Carter Edginton 2024
'''
import DFRobot_GNSS as GNSS

'''
    HelmHUD GPS class. use this as an interface to collect GPS information.
    
    -instantiate a gps module with HelmHUD_GPS()
    -collect data as a string only by calling .get_data() on your GPS object.
    
    you are free to collect and modify as necessary for function, but the interface should be all that you really need.
'''
class HelmHUD_GPS: 
    
    #MEMBER VARIABLES
    data = ["[!]NO SIGNAL","/NOT READY[!]"]
    gnss = 0
    location = GNSS.struct_lat_lon()
    
    #converts a GNSS.struct_lat_lon's location into a readable string. Only call when you have a valid GNSS.struct_lat_lon.
    def location_to_str(loc):
        lat = loc.latitude_degree
        lon = loc.lonitude_degree
        if (loc.lat_direction == "S"):
            lat *= -1
        if (loc.lon_direction == "W"):
            lon *= -1
        return ["{0:.5f}".format(lat)+"," , " "+"{0:.5f}".format(lon)]
    
    #collects and prints data. Use to grab lat/lon. Will print an error string if it does not work. 
    def get_data(self):
        #collect sensor data for both lat and lon.
        new_loc_lat = self.gnss.get_lat()
        new_loc_lon = self.gnss.get_lon()
        
        '''the only directions that have info that will work are new_loc_lat.lon (for lon direction) and new_loc_lon.lat (for lat direction)
           the calls get the wrong direction for lat/lon. This is a quirk with the API of the gnss. This is corrected for in this code.
        Example:
        print("RIGHTWAY")
        print("LAT: " +str(new_loc_lat.latitude_degree) + new_loc_lon.lat_direction)
        print("LON: "+str(new_loc_lon.lonitude_degree) + new_loc_lat.lon_direction)
        print("WRONGWAY:")#wrong way to call
        print("LAT: " +str(new_loc_lon.latitude_degree) + new_loc_lat.lat_direction)
        print("LON: "+str(new_loc_lat.lonitude_degree) + new_loc_lon.lon_direction)

        ''' 
        if (new_loc_lon.lat_direction == '\x00' or new_loc_lon.lat_direction == 'Y'):
            #Comms have failed. Print correct error statement.
            if (self.location.lat_direction == 'Y'):
                #There has been no previous signal. GPS is either not ready or has no signal.
                self.data = ["[!]NO SIGNAL","/NOT READY[!]"] 
            else:
                #There has been a previous signal, print last known location with a warning.
                if self.data[0][0] != "[":
                    self.data[0] = "[!]" + self.data[0]
                    self.data[1] = self.data[1] + "[!]"
            
        else:
            #Comms have succeeded! change the last known location to this one, and print it out.
            #set the location to the new location
            self.location.latitude_degree = new_loc_lat.latitude_degree
            self.location.lat_direction = new_loc_lon.lat_direction
            self.location.lonitude_degree = new_loc_lon.lonitude_degree
            self.location.lon_direction =  new_loc_lat.lon_direction
            
            self.data = HelmHUD_GPS.location_to_str(self.location)
        return self.data
    
   
    #initializer of class.
    def __init__(self):
        self.gnss = GNSS.DFRobot_GNSS_I2C(0x00, GNSS.GNSS_DEVICE_ADDR)
        self.location = GNSS.struct_lat_lon()
        self.data = ["[!]NO SIGNAL","/NOT READY[!]"]
        
    