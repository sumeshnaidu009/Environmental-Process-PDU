import DataInputStream
import DataOutputStream


class PduSuperclass( object ):
    """The superclass for all PDUs, including classic and Live Entity (LE) PDUs. This incorporates the PduHeader record, section 7.2.2"""

    def __init__(self):
        """ Initializer for PduSuperclass"""
        self.protocolVersion = 7
        """ The version of the protocol. 5=DIS-1995, 6=DIS-1998, 7=DIS-2009."""
        self.exerciseID = 0
        """ Exercise ID"""
        self.pduType = 0
        """ Type of pdu, unique for each PDU class"""
        self.protocolFamily = 0
        """ value that refers to the protocol family, eg SimulationManagement, et"""
        self.timestamp = 0
        """ Timestamp value"""
        self.length = 0
        """ Length, in bytes, of the PDU"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_byte(self.protocolVersion);
        outputStream.write_unsigned_byte(self.exerciseID);
        outputStream.write_unsigned_byte(self.pduType);
        outputStream.write_unsigned_byte(self.protocolFamily);
        outputStream.write_unsigned_int(self.timestamp);
        outputStream.write_unsigned_short(self.length);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.protocolVersion = inputStream.read_unsigned_byte();
        self.exerciseID = inputStream.read_unsigned_byte();
        self.pduType = inputStream.read_unsigned_byte();
        self.protocolFamily = inputStream.read_unsigned_byte();
        self.timestamp = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_short();


        
class Pdu( PduSuperclass ):
    """Adds some fields to the the classic PDU"""

    def __init__(self):
        """ Initializer for Pdu"""
        super(Pdu, self).__init__()
        self.pduStatus = 0
        """ PDU Status Record. Described in 6.2.67. This field is not present in earlier DIS versions """
        self.padding = 0
        """ zero-filled array of padding"""

    def serialize(self, outputStream):
        """serialize the class """
        super( Pdu, self ).serialize(outputStream)
        outputStream.write_unsigned_byte(self.pduStatus);
        outputStream.write_unsigned_byte(self.padding);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        super( Pdu, self).parse(inputStream)
        self.pduStatus = inputStream.read_unsigned_byte();
        self.padding = inputStream.read_unsigned_byte();


        
class SyntheticEnvironmentFamilyPdu( Pdu ):
    """Section 5.3.11: Abstract superclass for synthetic environment PDUs"""

    def __init__(self):
        """ Initializer for SyntheticEnvironmentFamilyPdu"""
        super(SyntheticEnvironmentFamilyPdu, self).__init__()
        self.protocolFamily = 9
        """ initialize value """

    def serialize(self, outputStream):
        """serialize the class """
        super( SyntheticEnvironmentFamilyPdu, self ).serialize(outputStream)


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        super( SyntheticEnvironmentFamilyPdu, self).parse(inputStream)


        
class SimulationAddress( object ):
    """A Simulation Address record shall consist of the Site Identification number and the Application Identification number. Section 6.2.79 """

    def __init__(self):
        """ Initializer for SimulationAddress"""
        self.site = 0
        """ A site is defined as a facility, installation, organizational unit or a geographic location that has one or more simulation applications capable of participating in a distributed event. """
        self.application = 0
        """ An application is defined as a software program that is used to generate and process distributed simulation data including live, virtual and constructive data."""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_short(self.site);
        outputStream.write_unsigned_short(self.application);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.site = inputStream.read_unsigned_short();
        self.application = inputStream.read_unsigned_short();


        
class ObjectIdentifier( object ):
    """The unique designation of an environmental object. Section 6.2.63"""

    def __init__(self):
        """ Initializer for ObjectIdentifier"""
        self.simulationAddress = SimulationAddress();
        """  Simulation Address"""
        self.objectNumber = 0
        """ object number"""

    def serialize(self, outputStream):
        """serialize the class """
        self.simulationAddress.serialize(outputStream)
        outputStream.write_unsigned_short(self.objectNumber);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.simulationAddress.parse(inputStream)
        self.objectNumber = inputStream.read_unsigned_short();


        
class EntityType( object ):
    """Identifies the type of Entity"""

    def __init__(self):
        """ Initializer for EntityType"""
        self.entityKind = 0
        """ Kind of entity"""
        self.domain = 0
        """ Domain of entity (air, surface, subsurface, space, etc)"""
        self.country = 0
        """ country to which the design of the entity is attributed"""
        self.category = 0
        """ category of entity"""
        self.subcategory = 0
        """ subcategory of entity"""
        self.specific = 0
        """ specific info based on subcategory field. Renamed from specific because that is a reserved word in SQL."""
        self.extra = 0

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_byte(self.entityKind);
        outputStream.write_unsigned_byte(self.domain);
        outputStream.write_unsigned_short(self.country);
        outputStream.write_unsigned_byte(self.category);
        outputStream.write_unsigned_byte(self.subcategory);
        outputStream.write_unsigned_byte(self.specific);
        outputStream.write_unsigned_byte(self.extra);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.entityKind = inputStream.read_unsigned_byte();
        self.domain = inputStream.read_unsigned_byte();
        self.country = inputStream.read_unsigned_short();
        self.category = inputStream.read_unsigned_byte();
        self.subcategory = inputStream.read_unsigned_byte();
        self.specific = inputStream.read_unsigned_byte();
        self.extra = inputStream.read_unsigned_byte();


        
class EnvironmentalProcessPdu( SyntheticEnvironmentFamilyPdu ):
    
    def __init__(self):
        """Initializer for EnvironmentalProcessPdu"""
        super(EnvironmentalProcessPdu, self).__init__()
        self.environementalProcessID = ObjectIdentifier();
        self.environmentType = EntityType();
        self.modelType = 0
        self.environmentStatus = 0
        self.numberOfEnvironmentRecords = 0
        self.sequenceNumber = 0
        self.environmentRecords = []
        self.pduType = 41
        
    def serialize(self, outputStream):
        """serialize the class """
        super( EnvironmentalProcessPdu, self ).serialize(outputStream)
        self.environementalProcessID.serialize(outputStream)
        self.environmentType.serialize(outputStream)
        outputStream.write_unsigned_byte(self.modelType);
        outputStream.write_unsigned_byte(self.environmentStatus);
        outputStream.write_unsigned_short(self.numberOfEnvironmentRecords);
        outputStream.write_unsigned_short(self.sequenceNumber);
        for anObj in self.environmentRecords:
            anObj.serialize(outputStream)
    
    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        super( EnvironmentalProcessPdu, self).parse(inputStream)
        self.environementalProcessID.parse(inputStream)
        self.environmentType.parse(inputStream)
        self.modelType = inputStream.read_unsigned_byte();
        self.environmentStatus = inputStream.read_unsigned_byte();
        self.numberOfEnvironmentRecords = inputStream.read_unsigned_short();
        self.sequenceNumber = inputStream.read_unsigned_short();
        for idx in range(0, self.numberOfEnvironmentRecords):
            element = null()
            element.parse(inputStream)
            self.environmentRecords.append(element)



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
        """ Initializer for EnvironmentGeneral"""
        self.environmentRecordType = 0
        """ Record type"""
        self.length = 0
        """ length, in bits"""
        self.index = 0
        """ Identify the sequentially numbered record index"""
        self.padding1 = 0
        """ padding"""
        self.horizontalWindSpeed = 0
        self.verticalWindSpeed = 0
        self.windDirection = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_float(self.horizontalWindSpeed);
        outputStream.write_float(self.verticalWindSpeed);
        outputStream.write_float(self.windDirection);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

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
        """ Initializer for EnvironmentGeneral"""
        self.environmentRecordType = 0
        """ Record type"""
        self.length = 0
        """ length, in bits"""
        self.index = 0
        """ Identify the sequentially numbered record index"""
        self.padding1 = 0
        """ padding"""
        self.precipitationType = 0
        self.precipitationDensity = 0
        self.rainsoak = 0
        self.precipitationRate = 0
        self.precipitationVelocity = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
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
        """"Parse a message. This may recursively call embedded objects."""

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
        """ Initializer for EnvironmentGeneral"""
        self.environmentRecordType = 0
        """ Record type"""
        self.length = 0
        """ length, in bits"""
        self.index = 0
        """ Identify the sequentially numbered record index"""
        self.padding1 = 0
        """ padding"""
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
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
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
        """"Parse a message. This may recursively call embedded objects."""

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
        
        
        
        
        
class FogRecord( object ):
    
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
        self.groundFogStatus = 0
        self.groundFogCeilingHeight = 0
        self.groundFogVisibilityRange = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_unsigned_byte(self.groundFogStatus);
        outputStream.write_float(self.groundFogCeilingHeight);
        outputStream.write_float(self.groundFogVisibilityRange);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.groundFogStatus = inputStream.read_unsigned_byte();
        self.groundFogCeilingHeight = inputStream.read_float();
        self.groundFogVisibilityRange = inputStream.read_float();
        self.padding2 = inputStream.read_unsigned_byte();
        
        
        
        
class HazeRecord( object ):
    
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
        self.hazeStatus = 0
        self.hazeType = 0
        self.hazeCeilingHeight = 0
        self.hazeVisibilityRange = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_unsigned_byte(self.hazeStatus);
        outputStream.write_unsigned_byte(self.hazeType);
        outputStream.write_float(self.hazeCeilingHeight);
        outputStream.write_float(self.hazeVisibilityRange);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.hazeStatus = inputStream.read_unsigned_byte();
        self.hazeType = inputStream.read_unsigned_byte();
        self.hazeCeilingHeight = inputStream.read_float();
        self.hazeVisibilityRange = inputStream.read_float();
        self.padding2 = inputStream.read_unsigned_byte();
        
        
        
        
        
        
class LightningRecord( object ):
    
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
        self.lightningStatus = 0
        self.lightningFrequency = 0
        self.lightningDuration = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_unsigned_byte(self.lightningStatus);
        outputStream.write_unsigned_int(self.lightningFrequency);
        outputStream.write_unsigned_int(self.lightningDuration);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.lightningStatus = inputStream.read_unsigned_byte();
        self.lightningFrequency = inputStream.read_unsigned_int();
        self.lightningDuration = inputStream.read_unsigned_int();
        self.padding2 = inputStream.read_unsigned_byte();
        
        
        
        
        
        
class ThunderRecord( object ):
    
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
        self.thunderStatus = 0
        self.thunderOffset = 0
        self.thunderFrequency = 0
        self.thunderDuration = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_unsigned_byte(self.thunderStatus);
        outputStream.write_unsigned_byte(self.thunderOffset);
        outputStream.write_unsigned_int(self.thunderFrequency);
        outputStream.write_unsigned_int(self.thunderDuration);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.thunderStatus = inputStream.read_unsigned_byte();
        self.thunderOffset = inputStream.read_unsigned_byte();
        self.thunderFrequency = inputStream.read_unsigned_int();
        self.thunderDuration = inputStream.read_unsigned_int();
        self.padding2 = inputStream.read_unsigned_byte();
        
        
        
        
        
class LayerRecord( object ):
    
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
        self.layerType = 0
        self.layerBaseHeight = 0
        self.layerCeilingHeight = 0
        self.layerVisibilityRange = 0
        self.layerTransitionBand = 0
        self.padding2 = 0
        """ padding to bring the total size up to a 64 bit boundry"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_unsigned_int(self.environmentRecordType);
        outputStream.write_unsigned_byte(self.length);
        outputStream.write_unsigned_byte(self.index);
        outputStream.write_unsigned_byte(self.padding1);
        outputStream.write_unsigned_byte(self.layerType);
        outputStream.write_float(self.layerBaseHeight);
        outputStream.write_float(self.layerCeilingHeight);
        outputStream.write_float(self.layerVisibilityRange);
        outputStream.write_float(self.layerTransitionBand);
        outputStream.write_unsigned_byte(self.padding2);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.environmentType = inputStream.read_unsigned_int();
        self.length = inputStream.read_unsigned_byte();
        self.index = inputStream.read_unsigned_byte();
        self.padding1 = inputStream.read_unsigned_byte();
        self.layerType = inputStream.read_unsigned_byte();
        self.layerBaseHeight = inputStream.read_float();
        self.layerCeilingHeight = inputStream.read_float();
        self.layerVisibilityRange = inputStream.read_float();
        self.layerTransitionBand = inputStream.read_float();
        self.padding2 = inputStream.read_unsigned_byte();
        
        
        
        
class Vector3Double( object ):
    """Three double precision floating point values, x, y, and z. Used for world coordinates Section 6.2.97."""

    def __init__(self):
        """ Initializer for Vector3Double"""
        self.x = 0
        """ X value"""
        self.y = 0
        """ y Value"""
        self.z = 0
        """ Z value"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_double(self.x);
        outputStream.write_double(self.y);
        outputStream.write_double(self.z);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.x = inputStream.read_double();
        self.y = inputStream.read_double();
        self.z = inputStream.read_double();


        
class EulerAngles( object ):
    """Three floating point values representing an orientation, psi, theta, and phi, are the euler angles, in radians. Section 6.2.33"""

    def __init__(self):
        """ Initializer for EulerAngles"""
        self.psi = 0
        self.theta = 0
        self.phi = 0

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_float(self.psi);
        outputStream.write_float(self.theta);
        outputStream.write_float(self.phi);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.psi = inputStream.read_float();
        self.theta = inputStream.read_float();
        self.phi = inputStream.read_float();


        
class Vector3Float( object ):
    """Three floating point values, x, y, and z. Section 6.2.95"""

    def __init__(self):
        """ Initializer for Vector3Float"""
        self.x = 0
        """ X value"""
        self.y = 0
        """ y Value"""
        self.z = 0
        """ Z value"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_float(self.x);
        outputStream.write_float(self.y);
        outputStream.write_float(self.z);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.x = inputStream.read_float();
        self.y = inputStream.read_float();
        self.z = inputStream.read_float();


        
class AngularVelocityVector( object ):
    """Angular velocity measured in radians per second out each of the entity's own coordinate axes. Order of measurement is angular velocity around the x, y, and z axis of the entity. The positive direction is determined by the right hand rule. Section 6.2.7"""

    def __init__(self):
        """ Initializer for AngularVelocityVector"""
        self.x = 0
        """ velocity about the x axis"""
        self.y = 0
        """ velocity about the y axis"""
        self.z = 0
        """ velocity about the zaxis"""

    def serialize(self, outputStream):
        """serialize the class """
        outputStream.write_float(self.x);
        outputStream.write_float(self.y);
        outputStream.write_float(self.z);


    def parse(self, inputStream):
        """"Parse a message. This may recursively call embedded objects."""

        self.x = inputStream.read_float();
        self.y = inputStream.read_float();
        self.z = inputStream.read_float();


        
class RectangularRecord2(object):
    
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
        """ padding to bring the total size up to a 64 bit boundry"""
        
    def serialize(self, outputStream):
        """serialize the class """
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
        """"Parse a message. This may recursively call embedded objects."""

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
