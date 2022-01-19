def two(value):
    n = int(0)
    while True:
        if value == 1:
            n += 1
            break
        elif value > 1:
            n += 1
            value = value - 2
    return n


inputFile = r"C:\Users\boroda\OneDrive\Macro Script\ChangeAxis\plane_export_row_1_Main_Blade_ag4format_Nsections(9)_Nstream(25_101_25_96)_Width(1_1).geomTurbo"
outputFile = ""

sectionCheckNumber = int(3)

file = []

fileOpen = open(inputFile, 'r')
file = fileOpen.read().splitlines()
fileOpen.close()

for i in range(len(file)):
    if file[i] == 'SECTIONAL':
        sectionNumber = int(file[i + 1])
        break
    else:
        sectionNumber = int(file[14])
for i in range(len(file)):
    if file[i] == 'XYZ':
        pointNumber = int(file[i + 1])
        break
    else:
        pointNumber = int(file[17])


sectionPosition = []

zSuctionRelative = [0.15, 0.45, 0.70]
zPressureRelative = [0.10, 0.35, 0.80]

if sectionCheckNumber == sectionNumber:
    for i in range(sectionCheckNumber):
        sectionPosition.append(i)
elif two(sectionCheckNumber) < sectionNumber and sectionCheckNumber % 2 == 1:
    for i in range(sectionCheckNumber):
        sectionPosition.append(int((sectionNumber - 1) / (sectionCheckNumber - 1) * i))
elif two(sectionCheckNumber) > sectionNumber and sectionCheckNumber % 2 == 1 and sectionNumber >= 3:
    sectionPosition = [int(0), int((sectionNumber - 1) / 2), int(sectionNumber - 1)]
    print("Warning, out just 3 section")
elif sectionNumber == 1:
    sectionPosition = [int(0)]
    print("Warning, out just 1 section")
else:
    print("Error")
    exit(0)

numberSuction = int(0)
numberPressure = int(0)

for i in range(len(file)):
    if file[i] == 'suction':
        numberSuction = i
    if file[i] == 'pressure':
        numberPressure = i

suctionCoord = []
pressureCoord = []

for i in range(len(sectionPosition)):
    bufSuction = [[], [], []]
    bufPressure = [[], [], []]
    for j in range(pointNumber):
        bufSuctionLine = file[numberSuction + 6 + j + (3 + pointNumber) * sectionPosition[i]].split(' ')
        bufPressureLine = file[numberPressure + 6 + j + (3 + pointNumber) * sectionPosition[i]].split(' ')
        bufSuction[0].append(float(bufSuctionLine[0]))  # X
        bufSuction[1].append(float(bufSuctionLine[1]))  # Y
        bufSuction[2].append(float(bufSuctionLine[2]))  # Z
        bufPressure[0].append(float(bufPressureLine[0]))    # X
        bufPressure[1].append(float(bufPressureLine[1]))    # Y
        bufPressure[2].append(float(bufPressureLine[2]))    # Z
    suctionCoord.append(bufSuction)
    pressureCoord.append(bufPressure)

# Determination of the maximum axial coord

maxZ = []
minZ = []

for i in range(len(sectionPosition)):
    if max(suctionCoord[i][2]) > max(pressureCoord[i][2]):
        maxZ.append(max(suctionCoord[i][2]))
    elif max(suctionCoord[i][2]) < max(pressureCoord[i][2]):
        maxZ.append(max(pressureCoord[i][2]))
    else:
        maxZ.append(max(suctionCoord[i][2]))

    if min(suctionCoord[i][2]) > min(pressureCoord[i][2]):
        minZ.append(min(pressureCoord[i][2]))
    elif min(suctionCoord[i][2]) < min(pressureCoord[i][2]):
        minZ.append(min(suctionCoord[i][2]))
    else:
        minZ.append(min(suctionCoord[i][2]))

zValue = []

for i in range(len(sectionPosition)):
    zValueBuf1 = []
    zValueBuf2 = []
    zValueBuf = []
    for j in range(len(zSuctionRelative)):
        zValueBuf1.append(minZ[i] + (maxZ[i] - minZ[i]) * zSuctionRelative[j])
    for j in range(len(zPressureRelative)):
        zValueBuf2.append(minZ[i] + (maxZ[i] - minZ[i]) * zPressureRelative[j])
    zValueBuf.append(zValueBuf1)
    zValueBuf.append(zValueBuf2)
    zValue.append(zValueBuf)
# [Hub -> Shroud][Suction -> Pressure][First -> Last value of relative axial coord]

# Determining the deviation from a straight line

dzSuction = []
numPointSuction = []
dzPressure = []
numPointPressure = []

for i in range(len(sectionPosition)):
    dzSuctionBuf2 = []
    numPointSuctionBuf2 = []
    dzPressureBuf2 = []
    numPointPressureBuf2 = []
    for j in range(len(zValue[i][0])):
        dzSuctionBuf1 = float(1000)
        numPointSuctionBuf1 = int(0)
        for k in range(pointNumber):
            deltaSuctionBuf = abs(suctionCoord[i][2][k] - zValue[i][0][j])
            if deltaSuctionBuf <= dzSuctionBuf1:
                dzSuctionBuf1 = deltaSuctionBuf
                numPointSuctionBuf1 = k
        dzSuctionBuf2.append(dzSuctionBuf1)
        numPointSuctionBuf2.append(numPointSuctionBuf1)
    dzSuction.append(dzSuctionBuf2)
    numPointSuction.append(numPointSuctionBuf2)
    for j in range(len(zValue[i][1])):
        dzPressureBuf1 = float(1000)
        numPointPressureBuf1 = int(0)
        for k in range(pointNumber):
            deltaPressureBuf = abs(pressureCoord[i][2][k] - zValue[i][1][j])
            if deltaPressureBuf <= dzPressureBuf1:
                dzPressureBuf1 = deltaPressureBuf
                numPointPressureBuf1 = k
        dzPressureBuf2.append(dzPressureBuf1)
        numPointPressureBuf2.append(numPointPressureBuf1)
    dzPressure.append(dzPressureBuf2)
    numPointPressure.append(numPointPressureBuf2)
# [Hub -> Shroud][First -> Last value of relative axial coord]

dSuction = []
dPressure = []

for i in range(len(sectionPosition)):
    dSuctionBuf = []
    dPressureBuf = []
    for j in range(len(numPointSuction[i])):
        x1 = suctionCoord[0][0][numPointSuction[0][j]]
        x2 = suctionCoord[-1][0][numPointSuction[-1][j]]
        y1 = suctionCoord[0][1][numPointSuction[0][j]]
        y2 = suctionCoord[-1][1][numPointSuction[-1][j]]
        z1 = suctionCoord[0][2][numPointSuction[0][j]]
        z2 = suctionCoord[-1][2][numPointSuction[-1][j]]
        xI = suctionCoord[i][0][numPointSuction[i][j]]
        yI = suctionCoord[i][1][numPointSuction[i][j]]
        zI = suctionCoord[i][2][numPointSuction[i][j]]
        y = (xI - x1) / (x2 - x1) * (y2 - y1) + y1
        z = (xI - x1) / (x2 - x1) * (z2 - z1) + z1
        d = pow(((yI - y) ** 2 + (zI - z) ** 2), 0.5)
        dSuctionBuf.append(d)
    for j in range(len(numPointPressure[i])):
        x1 = pressureCoord[0][0][numPointPressure[0][j]]
        x2 = pressureCoord[-1][0][numPointPressure[-1][j]]
        y1 = pressureCoord[0][1][numPointPressure[0][j]]
        y2 = pressureCoord[-1][1][numPointPressure[-1][j]]
        z1 = pressureCoord[0][2][numPointPressure[0][j]]
        z2 = pressureCoord[-1][2][numPointPressure[-1][j]]
        xI = pressureCoord[i][0][numPointPressure[i][j]]
        yI = pressureCoord[i][1][numPointPressure[i][j]]
        zI = pressureCoord[i][2][numPointPressure[i][j]]
        y = (xI - x1) / (x2 - x1) * (y2 - y1) + y1
        z = (xI - x1) / (x2 - x1) * (z2 - z1) + z1
        d = pow(((yI - y) ** 2 + (zI - z) ** 2), 0.5)
        dPressureBuf.append(d)
    dSuction.append(dSuctionBuf)
    dPressure.append(dPressureBuf)
# [Hub -> Shroud][First -> Last value of relative axial coord]

# Determination of the thickness distribution in airfoil

thickness = []

for i in range(len(sectionPosition)):
    bufThicknessValue = []
    for j in range(pointNumber):
        bufThicknessList = []
        for k in range(pointNumber):
            bufThicknessList.append(((suctionCoord[i][1][j] - pressureCoord[i][1][k]) ** 2
                                     + (suctionCoord[i][2][j] - pressureCoord[i][2][k]) ** 2) ** 0.5)
        bufThicknessValue.append(min(bufThicknessList))
    thickness.append(bufThicknessValue)

# Determination maximum thickness

maxThickness = []
minThickness = []

for i in range(len(sectionPosition)):
    maxThickness.append(max(thickness[i]))
    minThickness.append(min(thickness[i]))


# Determination the number of kinks

kink = []

for i in range(len(sectionPosition)):
    deltaParam = []
    kinkBuf = int(0)
    for j in range(pointNumber - 1):
        deltaParam.append(thickness[i][j + 1] - thickness[i][j])
    for j in range(len(deltaParam) - 1):
        if deltaParam[j] > 0 and deltaParam[j + 1] > 0:
            kinkBuf += 0
        elif deltaParam[j] < 0 and deltaParam[j + 1] < 0:
            kinkBuf += 0
        elif deltaParam[j] > 0 and deltaParam[j + 1] < 0:
            kinkBuf += 1
        elif deltaParam[j] < 0 and deltaParam[j + 1] > 0:
            kinkBuf += 1
    kink.append(kinkBuf)
# [Hub -> Shroud]