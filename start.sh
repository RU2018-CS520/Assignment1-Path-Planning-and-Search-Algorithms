#!/bin/bash
cnt=1
testPath='./codes/testgenetic.py'
filename='./data/astar'
starting="{'mazeSize': 100, 'mazeWallRate': -1, 'populationSize': "
maxIterationStr=",'maxIteration': "
reproductionRateStr=", 'reproductionRate': "
mutationRateStr=", 'mutationRate': "
solutionFunctionStr=", 'hugeMutation': 'True', 'weight': [0, 1, 0], 'solutionFunction': "
solutionConfigStr=", 'solutionConfig': {'LIFO': 'True', 'distFunction': "
ending="}}"
aStar="'aStar'"
manhattanDist="'manhattanDist'"
for ((populationSize = 100; populationSize <= 300; populationSize += 50)); do
	for ((maxIteration = 100; maxIteration <= 150; maxIteration += 10)); do
		for ((mutationRate = 5; mutationRate <= 15; mutationRate += 2)); do
			realMutationRate="$(printf "%02d" "$mutationRate")"
			argu="${starting}${populationSize}${maxIterationStr}${maxIteration}${reproductionRateStr}0.7${mutationRateStr}${realMutationRate}${solutionFunctionStr}${aStar}${solutionConfigStr}${manhattanDist}${ending}"
			echo $argu > "${filename}$(printf "%03d" $cnt).txt"
			python "$testPath" "$argu" >> "${filename}$(printf "%03d" $cnt).txt" &
			((cnt++))
		done
	done
done
