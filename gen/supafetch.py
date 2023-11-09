
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import itertools

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def log(msg:str):
    print('[CERTIFY CORE] ' + msg)

def fetchEventDetails(event_id: str):
    log('FETCHING EVENT DETAILS FOR ' + event_id)
    details = supabase.table('event').select('*').eq('id', event_id).single().execute().data
    return details


def fetchMainStudentsFromEvent(event_id: str):
    log('FETCHING MAIN STUDENTS FOR ' + event_id)
    mainPosition = supabase.table('eventresult').select(
        "winner, runner_up, second_runner_up").eq('event_id', event_id).execute()
    mainPosition = mainPosition.data[0]
    winnerId = mainPosition['winner']
    runnerupId = mainPosition['runner_up']
    secondRunnerupId = mainPosition['second_runner_up']
    winnerMembers = []
    firstRunnerUpMembers = []
    secondRunnerUpMembers = []
    if winnerId != None:
        winnerMembers = supabase.table('groupmember').select(
            "student_id").eq('group_id', mainPosition['winner']).execute().data

    if runnerupId != None:

        firstRunnerUpMembers = supabase.table('groupmember').select(
            "student_id").eq('group_id', mainPosition['runner_up']).execute().data

    if secondRunnerupId != None:
        secondRunnerUpMembers = supabase.table('groupmember').select(
            "student_id").eq('group_id', mainPosition['second_runner_up']).execute().data

    return {'winner': winnerMembers, 'runnerup': firstRunnerUpMembers, 'secondrunnerup': secondRunnerUpMembers}


def fetchStudentDetailsFromId(student_id: str):
    log('FETCHING STUDENT DETAILS FROM STUDENT ID ' + student_id)
    response = supabase.table('student').select(
        'first_name, last_name, class').eq('id', student_id).single().execute().data
    return response


def fetchAllOnlyParticipants(event_id: str):
    log('FETCHING ONLY PARTICIPANTS FROM ' + event_id)
    participantIds = []
    mainStudentIds = fetchMainStudentsFromEvent(event_id)
    mainStudentCollection = list(itertools.chain(
        mainStudentIds['winner'], mainStudentIds['runnerup'], mainStudentIds['secondrunnerup']))
    participatedGroups = supabase.table('eventparticipant').select(
        'group_id').eq('event_id', event_id).execute().data
    mainStudentCollectionIds = []

    for i in mainStudentCollection:
        mainStudentCollectionIds.append(i['student_id'])

    for group in participatedGroups:
        
        groupmembers = supabase.table('groupmember').select('student_id').eq('group_id', group['group_id']).execute().data
        for member in groupmembers:
            # print(mainStudentCollectionIds)
            if member['student_id'] not in mainStudentCollectionIds:
                participantIds.append(member['student_id'])
            

    return participantIds

def saveToBucket(eventid:str, data):
    log('SAVING A CERTIFICATE TO BUCKET IN : ' + eventid)
    supabase.storage.from_("certificates").upload(file=data['bytes'],path=f'{eventid}/{data["name"]}.png', file_options={"content-type": "image/png"})

