import math 


"""


"""

AiryDiscRadius_pupilSize = [
    (2.247320061255743, 1.0),
    (2.2052067381316998, 1.0510951391490957),
    (2.0482388973966312, 1.187348843546684),
    (1.7304747320061256, 1.4201155885592307),
    (1.5735068912710568, 1.562046530640052),
    (1.4280245022970903, 1.6755912843047087),
    (1.2978560490045943, 1.8175222263855297),
    (1.1944869831546707, 1.9310669800501867),
    (1.110260336906585, 2.0446117337148437),
    (1.037519142419602, 2.186542675795665),
    (0.9800918836140888, 2.300087429460322),
    (0.9341500765696784, 2.4193094208082115),
    (0.8767228177641654, 2.67478511655369),
    (0.8039816232771823, 2.930260812299168),
    (0.7465543644716692, 3.185736508044646),
    (0.6891271056661562, 3.4185032530571924),
    (0.6163859111791731, 3.929454644548149),
    (0.5436447166921899, 4.440406036039105),
    (0.501531393568147, 4.951357427530061),
    (0.45941807044410415, 5.462308819021017),
    (0.4287901990811639, 5.944874022095809),
    (0.37136294027565087, 6.94406785434479),
    (0.329249617151608, 8.0000340634261)
    ]

maxAiryDiscDiameter = 2*max([a for a,b in AiryDiscRadius_pupilSize])
minAiryDiscDiameter = 2*min([a for a,b in AiryDiscRadius_pupilSize])
maxPupilDiameter = max([b for a,b in AiryDiscRadius_pupilSize])
minPupilDiameter = min([b for a,b in AiryDiscRadius_pupilSize])


epsilon = 1e-12

def pupilSizeToAiryDiscRadius(pupilSize):
    """ Approximate the Airy disc radius in the eye, based on the
        values extracted from the Roorda graph.
        pupilSize in mm
        airyDisk in arc minutes
    """
    if pupilSize <= AiryDiscRadius_pupilSize[0][1]:
        return AiryDiscRadius_pupilSize[0][0]
    elif pupilSize >= AiryDiscRadius_pupilSize[-1][1]:
        return AiryDiscRadius_pupilSize[-1][0]
    for i in range(1, len(AiryDiscRadius_pupilSize)-1, 1):
        current = AiryDiscRadius_pupilSize[i]
        next = AiryDiscRadius_pupilSize[i+1]
        #print current[1], pupilSize, next[1]
        if current[1] <= pupilSize <= next[1]:
            factor = (pupilSize-current[1])/(next[1]-current[1])
            return current[0]+factor*(next[0]-current[0])
            
print "pupilSizeToAiryDiscRadius", pupilSizeToAiryDiscRadius(8)
print "pupilSizeToAiryDiscRadius", pupilSizeToAiryDiscRadius(1)

def distanceToAngular(eyeDistance, fontSize):
    """
        eye distance in mm
        fontSize in point
        
        out: the angular size of the full em in arc minutes
    """
    pt_mm = 0.352777778
    em_mm = (fontSize * pt_mm)
    print "em mm", em_mm
    t = em_mm/eyeDistance
    return math.atan(t) * 60

def pupilSizeEyeDistanceFontSizeUnitsPerEmToAiryDiameterInEm(pupilSize, eyeDistance, fontSize, unitsPerEm):
    angularSize = distanceToAngular(eyeDistance, fontSize)
    print "eyeDistance", eyeDistance
    print "angularSize", math.degrees(angularSize)
    print "fontSize", fontSize
    airyDiameter = 2 * pupilSizeToAiryDiscRadius(pupilSize)
    print "airyDiameter", airyDiameter
    airyFraction = unitsPerEm * airyDiameter/math.degrees(angularSize)
    print airyFraction
    

a = distanceToAngular(400, 8)
print 'aa', math.degrees(a)


pupilSize = 2
eyeDistance = 1000
fontSize = 10
unitsPerEm = 1000

pupilSizeEyeDistanceFontSizeUnitsPerEmToAiryDiameterInEm(pupilSize, eyeDistance, fontSize, unitsPerEm)