import socket
import time
import urllib.request, json
t = int(time.time())
import sys
from RangeCoordinates import GPS

sys.path.append("/home/pi/Master_Thesis")
sys.path.append("/home/pi/Master_Thesis")

from DataInputStream import DataInputStream
from DataOutputStream import DataOutputStream

from dis7 import EnvironmentalProcessPdu
from io import BytesIO
#from RangeCoordinates import GPS

    
UDP_PORT = 3000
DESTINATION_ADDRESS = "192.168.2.255"

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

"""Creating Time Machine Request URL with respect to timestamp"""

f = 'https://api.darksky.net/forecast/c260318659d78342a4f516ccfd74b27c/47.67228,9.384921,'
m = str(t)
l = '?exclude=daily,hourly,minutely,alerts,flags'
fml = f+m+l

class AtmosphericRecord( object ):
    
    def __init__(self):
        """ Initializer for EnvironmentGeneral"""
        self.environmentRecordType = 0
        """ Record type"""
        self.length = 0
        """ length, in bits"""
        self.index = 0
        """ Identify the sequentially numbered record index"""
        self.padding1 = 0
        """ padding"""
        self.visibilityRange = 0
        self.airTemperature = 0
        self.pressure = 0
        self.humidity = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_float(self.visibilityRange);
        outputStream.write_float(self.airTemperature);
        outputStream.write_float(self.pressure);
        outputStream.write_unsigned_int(self.humidity);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""
        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.visibilityRange = inputStream.read_float();
        self.airTemperature = inputStream.read_float();
        self.pressure = inputStream.read_float();
        self.humidity = inputStream.read_unsigned_int();
        self.padding2 = inputStream.read_unsigned_byte();



class WindRecord( object ):
    
    def __init__(self):
        self.environmentRecordType = 0
        self.length = 0
        self.index = 0
        self.padding1 = 0
        self.horizontalWindSpeed = 0
        self.verticalWindSpeed = 0
        self.windDirection = 0
        self.padding2 = 0

    def serialize(self, outputStream):
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_float(self.horizontalWindSpeed);
        outputStream.write_float(self.verticalWindSpeed);
        outputStream.write_float(self.windDirection);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.horizontalWindSpeed = inputStream.read_float();
        self.verticalWindSpeed = inputStream.read_float();
        self.windDirection = inputStream.read_float();
        self.padding2 = inputStream.read_unsigned_byte();


        
class PrecipitationRecord( object ):
    
    def __init__(self):
        self.environmentRecordType = 0
        self.length = 0
        self.index = 0
        self.padding1 = 0
        self.precipitationType = 0
        self.precipitationDensity = 0
        self.rainsoak = 0
        self.precipitationRate = 0
        self.precipitationVelocity = 0
        self.padding2 = 0

    def serialize(self, outputStream):
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_unsigned_byte(self.precipitationType);
        outputStream.write_unsigned_int(self.precipitationDensity);
        outputStream.write_unsigned_byte(self.rainsoak);
        outputStream.write_unsigned_byte(self.precipitationRate);
        outputStream.write_float(self.precipitationVelocity);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.precipitationType = inputStream.read_unsigned_byte();
        self.precipitationDensity = inputStream.read_unsigned_int();
        self.rainsoak = inputStream.read_unsigned_byte();
        self.precipitationRate = inputStream.read_unsigned_byte();
        self.precipitationVelocity = inputStream.read_float();
        self.padding2 = inputStream.read_unsigned_byte();
        
        
        
        
class CloudsRecord( object ):
    
    def __init__(self):
        self.environmentRecordType = 0
        self.length = 0
        self.index = 0
        self.padding1 = 0
        self.cloudStatus = 0
        self.cloudType = 0
        self.cloudDensity = 0
        self.scudFlags = 0
        self.scudBottomFrequency = 0
        self.scudTopFrequency = 0
        self.cloudBaseHeight = 0
        self.cloudCeilingHeight = 0
        self.cloudVisibilityRange = 0
        self.padding2 = 0

    def serialize(self, outputStream):
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_unsigned_byte(self.cloudStatus);
        outputStream.write_unsigned_byte(self.cloudType);
        outputStream.write_unsigned_byte(self.cloudDensity);
        outputStream.write_unsigned_byte(self.scudFlags);
        outputStream.write_unsigned_int(self.scudBottomFrequency);
        outputStream.write_unsigned_int(self.scudTopFrequency);
        outputStream.write_float(self.cloudBaseHeight);
        outputStream.write_float(self.cloudCeilingHeight);
        outputStream.write_float(self.cloudVisibilityRange);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.cloudStatus = inputStream.read_unsigned_byte();
        self.cloudType = inputStream.read_unsigned_byte();
        self.cloudDensity = inputStream.read_unsigned_byte();
        self.scudFlags = inputStream.read_unsigned_byte();
        self.scudBottomFrequency = inputStream.read_unsigned_int();
        self.scudTopFrequency = inputStream.read_unsigned_int();
        self.cloudBaseHeight = inputStream.read_float();
        self.cloudCeilingHeight = inputStream.read_float();
        self.cloudVisibilityRange = inputStream.read_float();
        self.padding2 = inputStream.read_unsigned_byte();



class Vector3Double( object ):
    """Three double precision floating point values, x, y, and z. Used for world coordinates Section 6.2.97."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def serialize(self, outputStream):
        outputStream.write_double(self.x);
        outputStream.write_double(self.y);
        outputStream.write_double(self.z);


    def parse(self, inputStream):
        self.x = inputStream.read_double();
        self.y = inputStream.read_double();
        self.z = inputStream.read_double();


        
class EulerAngles( object ):
    """Three floating point values representing an orientation, psi, theta, and phi, are the euler angles, in radians. Section 6.2.33"""

    def __init__(self):
        self.psi = 0
        self.theta = 0
        self.phi = 0

    def serialize(self, outputStream):
        outputStream.write_float(self.psi);
        outputStream.write_float(self.theta);
        outputStream.write_float(self.phi);


    def parse(self, inputStream):
        self.psi = inputStream.read_float();
        self.theta = inputStream.read_float();
        self.phi = inputStream.read_float();


        
class Vector3Float( object ):
    """Three floating point values, x, y, and z. Section 6.2.95"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def serialize(self, outputStream):
        outputStream.write_float(self.x);
        outputStream.write_float(self.y);
        outputStream.write_float(self.z);


    def parse(self, inputStream):
        self.x = inputStream.read_float();
        self.y = inputStream.read_float();
        self.z = inputStream.read_float();


        
class AngularVelocityVector( object ):
    """Angular velocity measured in radians per second out each of the entity's own coordinate axes.
       Order of measurement is angular velocity around the x, y, and z axis of the entity.
       The positive direction is determined by the right hand rule. Section 6.2.7"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def serialize(self, outputStream):
        outputStream.write_float(self.x);
        outputStream.write_float(self.y);
        outputStream.write_float(self.z);


    def parse(self, inputStream):
        self.x = inputStream.read_float();
        self.y = inputStream.read_float();
        self.z = inputStream.read_float();


        
class RectangularRecord2(object):
    
    def __init__(self):
        self.environmentRecordType = 1
        self.length = 0
        self.index = 0
        self.padding1 = 0
        self.cornerLocation = Vector3Double();
        self.xLength = 0
        self.yLength = 0
        self.zLength = 0
        self.diffxLength = 0
        self.diffyLength = 0
        self.diffzLength = 0
        self.orientation = EulerAngles();
        self.velocity = Vector3Float();
        self.angularVelocity = AngularVelocityVector();
        self.padding2 = 0
        
    def serialize(self, outputStream):
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        self.cornerLocation.serialize(outputStream)
        outputStream.write_float(self.xLength);
        outputStream.write_float(self.yLength);
        outputStream.write_float(self.zLength);
        outputStream.write_float(self.diffxLength);
        outputStream.write_float(self.diffyLength);
        outputStream.write_float(self.diffzLength);
        self.orientation.serialize(outputStream)
        self.velocity.serialize(outputStream)
        self.angularVelocity.serialize(outputStream)
        outputStream.write_unsigned_byte(self.padding2);
        
    def parse(self, inputStream):
        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.cornerLocation.parse(inputStream)
        self.xLength = inputStream.read_float();
        self.yLength = inputStream.read_float();
        self.zLength = inputStream.read_float();
        self.diffxLength = inputStream.read_float();
        self.diffyLength = inputStream.read_float();
        self.diffzLength = inputStream.read_float();
        self.orientation.parse(inputStream)
        self.velocity.parse(inputStream)
        self.angularVelocity.parse(inputStream)
        self.padding2 = inputStream.read_unsigned_byte();


        
def weather():
    while True:
        pdu = EnvironmentalProcessPdu()
        pdu.exerciseID = 1
        ts = int(time.time())
        pdu.timestamp = ts

        pdu.environementalProcessID.simulationAddress.site = 1
        pdu.environementalProcessID.simulationAddress.application = 1000
        pdu.environementalProcessID.objectNumber = 1

        pdu.environmentType.entityKind = 4
        pdu.environmentType.domain = 2
        pdu.environmentType.country = 0
        pdu.environmentType.category = 4
        pdu.environmentType.subcategory = 0
        pdu.environmentType.specific = 0
        pdu.environmentType.extra = 0

        pdu.modelType = 0

        pdu.environmentStatus = 2

        pdu.sequenceNumber = 0
            
        pdu.environmentRecords = [AtmosphericRecord(),WindRecord(),PrecipitationRecord(),CloudsRecord(),RectangularRecord2()]

        pdu.numberOfEnvironmentRecords = len(pdu.environmentRecords)

        """Making an online API Time Machine request and reading the weather data in it""" 
        with urllib.request.urlopen(fml) as url:
            dat = json.loads(url.read().decode())
            
            pdu.environmentRecords[0].visibilityRange = dat['currently']['visibility']
            pdu.environmentRecords[0].airTemperature = dat['currently']['temperature']
            pdu.environmentRecords[0].pressure = dat['currently']['pressure']
            pdu.environmentRecords[0].humidity = int((dat['currently']['humidity'])*100)
            pdu.environmentRecords[1].horizontalWindSpeed = dat['currently']['windSpeed']
            pdu.environmentRecords[2].precipitationDensity = int(dat['currently']['precipIntensity'])
            pdu.environmentRecords[3].cloudDensity = int((dat['currently']['cloudCover'])*100)

        pdu.environmentRecords[0].index = 1
        pdu.environmentRecords[1].index = 2
        pdu.environmentRecords[2].index = 3
        pdu.environmentRecords[3].index = 4
        pdu.environmentRecords[4].index = 5

        gps = GPS() # A function that converts latitude, longitude and altitude to earth centered earth fixed three dimensional coordinates.

        montereyLocation = gps.lla2ecef((47.67228, 9.384921, 6547) ) # User defined latitude, longitude and altitude.
            
        pdu.environmentRecords[4].cornerLocation.x = montereyLocation[0]
        pdu.environmentRecords[4].cornerLocation.y = montereyLocation[1]
        pdu.environmentRecords[4].cornerLocation.z = montereyLocation[2]

        pdu.environmentRecords[4].xLength = 784000 # User defined length
        pdu.environmentRecords[4].yLength = 688800 # User defined length
        pdu.environmentRecords[4].zLength = 869000 # User defined length

        """Orientation is maintained zero due to lack of data"""
        pdu.environmentRecords[4].orientation.psi = 0
        pdu.environmentRecords[4].orientation.theta = 0
        pdu.environmentRecords[4].orientation.phi = 0

        """Velocity is maintained zero due to lack of data"""
        pdu.environmentRecords[4].velocity.x = 0
        pdu.environmentRecords[4].velocity.y = 0
        pdu.environmentRecords[4].velocity.z = 0

        """Angular velocity is maintained zero due to lack of data"""
        pdu.environmentRecords[4].angularVelocity.x = 0
        pdu.environmentRecords[4].angularVelocity.y = 0
        pdu.environmentRecords[4].angularVelocity.z = 0
        
        memoryStream = BytesIO()
        outputStream = DataOutputStream(memoryStream)
        pdu.serialize(outputStream)
        data = memoryStream.getvalue()
        pdu.length = len(data)
        print ("data length is ", pdu.length)
        
        """I found that the pdu.length variable was not being populated when the pdu was being serialised.
           To get around this I serialised the packet, got the pdulength, inserted this value then re-serialised."""

        memoryStream = BytesIO()
        outputStream = DataOutputStream(memoryStream)
        pdu.serialize(outputStream)
        data1 = memoryStream.getvalue()
        udpSocket.sendto(data1, (DESTINATION_ADDRESS, UDP_PORT)) # Sending data to DIS network
        print ("message sent")

if __name__ == "__main__":    
    try:
        weather()
    except KeyboardInterrupt:
        print('Forced reset')
