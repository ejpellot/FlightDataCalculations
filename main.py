import numpy as np
import csv




#Different Calculations

def airSpeed(distance, deltaIngestTime):
    return (3600*1000*distance)/deltaIngestTime

def distance(lat1, lon1, lat2, lon2):
    MILES = 3959
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    total_miles = MILES * c
    return total_miles/0.621371

def minusfunct (a1, a2):
    return a2-a1
def deltaAltitude(altitude1,altitude2):
    return minusfunct(altitude1,altitude2)

def deltaIngestTime(ingestDateTime1,ingestDateTime2):
    return minusfunct(ingestDateTime1,ingestDateTime2)

def derivedClimbRate(deltaAltitude, deltaIngestTime):
    return (60000*deltaAltitude)/deltaIngestTime

def deltaGroundSpeed(groundSpeed1, groundSpeed2):
    return minusfunct(groundSpeed1, groundSpeed2)

def deltaLatitude(latitude1, latitude2):
    return minusfunct(latitude1, latitude2)

def deltaLongitude(longitude1, longitude2):
    return minusfunct(longitude1, longitude2)

def deltaMessageTime(messageDateTime1, messageDateTime2):
    return minusfunct(messageDateTime1, messageDateTime2)

def deltaClimbRate(verticalClimbRate1, verticalClimbRate2):
    return minusfunct(verticalClimbRate1, verticalClimbRate2)

#Unpacking data from Sample CSV file then creating new CSV file to store new outputs.
#New outputs are then going to be used for Neural Network Model. 

def main():
    (aircraftIdentifier,callSign,altitude,
    groundSpeed,ingestDateTime,latitude,
    longitude,messageDateTime,squawkCode,
    verticalClimbRate,track,aircraftType) = np.loadtxt('sampleFlightData.csv',
                                                        delimiter=',', 
                                                        unpack=True, 
                                                        dtype='str')  

    with open('newFlightData.csv', 'w', newline='') as newFile: #New CSV file for data
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['RowID','DeltaAltitude','DerivedClimbRate',
        'DeltaGroundSpeed','DeltaIngestTime','DeltaLatitude','DeltaLongitude',
        'DeltaMessageTime','DeltaClimbRate','Distance (KM)','AirSpeed (km/Hour)']) 
        x=1 #Skips Header
        with open ('sampleFlightData.csv', 'r') as tmp: #opens original csv file
            for row in range(1,len(altitude)-1): #for every row in original csv file
                newFileWriter.writerow([  #Writes function to each row
                x+1,
                deltaAltitude(int(altitude[x]), int(altitude[x+1])),
                derivedClimbRate(
                    int(deltaAltitude(int(altitude[x]), int(altitude[x+1]))),
                    int(deltaIngestTime(int(ingestDateTime[x]),int(ingestDateTime[x+1])))
                    ),
                deltaGroundSpeed(int(groundSpeed[x]),int(groundSpeed[x+1])),
                deltaIngestTime(int(ingestDateTime[x]),int(ingestDateTime[x+1])),
                deltaLatitude(float(latitude[x]), float(latitude[x+1])),
                deltaLongitude(float(longitude[x]),float(longitude[x+1])),
                deltaMessageTime(int(messageDateTime[x]), int(messageDateTime[x+1])),
                deltaClimbRate(int(verticalClimbRate[x]), int(verticalClimbRate[x+1])),
                distance(float(latitude[x]), float(longitude[x]), float(latitude[x+1]), float(longitude[x+1])),
                airSpeed(
                    float( distance(float(latitude[x]), float(longitude[x]), float(latitude[x+1]), float(longitude[x+1]))), 
                    int(deltaIngestTime(int(ingestDateTime[x]),int(ingestDateTime[x+1])))
                )
             ])
                x+=1 

if __name__=="__main__":
    main()
    print("done")

