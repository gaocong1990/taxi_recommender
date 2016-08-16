from numpy import *
def loadDataSetFile(fileName):
	dataMat = []
	f = open(fileName)
	for line in f.readlines():
		curLine = line.strip().split(',')
		proj_lonlats_string = [curLine[1],curLine[2]]
		proj_lonlats = map(float, proj_lonlats_string)
		dataMat.append(proj_lonlats)
	return dataMat

def distEclud_lonlats(A_lonlats, B_lonlats):
	A_lonlat = A_lonlats.tolist()[0]
	B_lonlat = B_lonlats.tolist()[0]
	dlat = 111.0 * abs(A_lonlat[1] - B_lonlat[1])
	dlon = 111.0 * abs(math.cos(math.radians((A_lonlat[1] + B_lonlat[1])/2)))*abs(A_lonlat[0]-B_lonlat[0])
	return math.sqrt(dlat**2 + dlon**2)

def randCent(dataSet, k):
	n = shape(dataSet)[1]
	centroids = mat(zeros((k, n)))#create centroid mat
	for j in range(n):
		minJ = min(dataSet[:,j])
		rangeJ = float(max(dataSet[:,j]) - minJ)
		centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
	return centroids

def kMeans(dataSet, k, distMeans=distEclud_lonlats, createCent = randCent):
	m = shape(dataSet)[0] #jilu de tiao shu

	# first column stores which cluster this sample belongs to,  
    # second column stores the error between this sample and its centroid 
	clusterAssment = mat(zeros((m, 2)))

	## step 1: init centroids 
	centroids = createCent(dataSet, k)
	print "Initial centroid: "
	print centroids
	clusterChanged = True
	count = 1
	while clusterChanged:
		print "iterating " + str(count) + " times"
		clusterChanged = False
		for i in range(m):
			#set thi min distance
			minDist = 10000000000000000
			minIndex = 0

			# step 2: find the centroid who is closest  
			for j in range(k):
				distJI = distMeans(centroids[j,:], dataSet[i,:])
				if distJI < minDist:
					minDist = distJI
					minIndex = j

			# step 3: update its cluster  
			if clusterAssment[i,0] != minIndex: 
				clusterChanged = True
				clusterAssment[i,:] = minIndex,0#minDist**2

		## step 4: update centroids
		for cent in range(k):
			ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
			centroids[cent,:] = mean(ptsInClust, axis=0)
		count = count + 1
	return centroids, clusterAssment
pickup_file_dir = 'D:/Data/Tmp/'
pickup_filename = '04.txt'
datMat = mat(loadDataSetFile(pickup_file_dir + pickup_filename))
print 'begin k-means clustering'
Centroids, clustAssing = kMeans(datMat,20)
print 'finish k-means clustering'

datMat_list = datMat.tolist()
Centroids_list = Centroids.tolist()
clustAssing_list = clustAssing.tolist()

filename_suffix = pickup_filename.split('_')[1] + '_' + pickup_filename.split('_')[2].split('.')[0]
centroid_f = open(pickup_file_dir + 'centroids' + '.txt','w')
for centroid in Centroids_list:
	centroid_f.write(str(centroid[0]) + ',' + str(centroid[1]) + '\n')

cluster_f = open(pickup_file_dir + 'pickup_cluster_' + filename_suffix + '.txt','w')
centroids_number = len(Centroids_list)
centroid_number = 0
while centroid_number < centroids_number:
	print 'centroid_number:',centroid_number
	for i in range(len(clustAssing_list)):
		if int(clustAssing_list[i][0]) == centroid_number:
			cluster_f.write(str(centroid_number) + ',' + str(datMat_list[i][0]) + ',' + str(datMat_list[i][1]) + '\n')
	centroid_number = centroid_number + 1
