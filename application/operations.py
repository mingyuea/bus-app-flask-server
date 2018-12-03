from flask import (Blueprint, request, current_app)
from application.cors_response import cors_res
import pickle
from datetime import datetime
from application.stopDict import masterStopDict
from application.stopLocation import stopArr
from pytz import timezone

bp = Blueprint('operations', __name__, url_prefix='/operations')


@bp.route('/getStops', methods=('GET',))
def getStops():
	stopObj = {}
	'''with current_app.open_resource('stopLocation.pkl', mode='rb') as f:
		stopArr = pickle.load(f)
		stopObj['stopArr'] = stopArr'''
	stopObj['stopArr'] = stopArr
	return cors_res(stopObj)


@bp.route('/locationUpdate', methods=('OPTIONS', 'POST'))
def locationUpdate():
	if request.method == 'OPTIONS':
		return cors_res()
	else:
		reqDict = request.get_json()
		stopID = str(reqDict['stopID'])

		'''with current_app.open_resource('stops/'+stopID+'.pkl', mode='rb') as f:
			timeArr = pickle.load(f)'''

		timeArr = masterStopDict[stopID]
		tz = timezone('EST')
		timestamp = datetime.now(tz)
		convertTime = float(timestamp.hour) + round(int(timestamp.minute)/60, 3)

		resObj = {}
		for ind, timeTup in enumerate(timeArr):
			if convertTime < timeTup[0]:
				if ind == len(timeArr) - 1:
					resObj['time'] = [timeTup]
				elif ind == len(timeArr) - 2:
					resObj['time'] = [timeTup, timeArr[ind+1]]
				else:
					resObj['time'] = [timeTup, timeArr[ind+1], timeArr[ind+2]]
				resObj['available'] = True
				break
		else:
			resObj['available'] = False
		return cors_res(resObj)



@bp.route('/getTime', methods=('GET',))
def getTime():
	tz = timezone('EST')
	timestamp = datetime.now(tz)
	convertTime = float(timestamp.hour) + round(int(timestamp.minute)/60, 3)
	newDict = {'time': convertTime}
	return cors_res(newDict)