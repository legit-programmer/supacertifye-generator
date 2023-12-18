
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import itertools
from colorama import Fore

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def log(msg):
    print(Fore.YELLOW + '[CERTIFY CORE] ' +
          Fore.LIGHTGREEN_EX + str(msg) + Fore.WHITE)

def setGenerationState(event_id:str, is_generating:bool):
    supabase.from_('generation_state').upsert({
        'event_id':event_id,
        'generating':is_generating
    }).execute()

def fetchEventDetails(event_id: str):
    log('FETCHING EVENT DETAILS FOR ' + event_id)
    details = supabase.table('event').select(
        '*').eq('id', event_id).single().execute().data
    return details


def fetchMainStudentsFromEvent(event_id: str):
    log('FETCHING MAIN STUDENTS FOR ' + event_id)

    mainPosition = supabase.table('eventresult').select(
        "winner, runner_up, second_runner_up").eq('event_id', event_id).execute().data
    
    
    winnerGrpIds = []
    runnerUpGrpIds = []
    secondRunnerUpGrpIds = []

    for secondaryPostion in mainPosition:
        if secondaryPostion['winner'] != None:
            winnerGrpIds.append(secondaryPostion['winner'])
        if secondaryPostion['runner_up'] != None:
            runnerUpGrpIds.append(secondaryPostion['runner_up'])
        if secondaryPostion['second_runner_up'] != None:
            secondRunnerUpGrpIds.append(secondaryPostion['second_runner_up'])

    mainPosition = {
        'winner': winnerGrpIds, 'runner_up': runnerUpGrpIds, 'second_runner_up': secondRunnerUpGrpIds} if mainPosition != [] else {
        'winner': None, 'runner_up': None, 'second_runner_up': None}

    winnerMembers = []
    firstRunnerUpMembers = []
    secondRunnerUpMembers = []

    for group in winnerGrpIds:
        winnerMembers = list(itertools.chain(winnerMembers, supabase.table('groupmember').select(
            "student_id").eq('group_id', group).execute().data))

    for group in runnerUpGrpIds:
        firstRunnerUpMembers = list(itertools.chain(firstRunnerUpMembers, supabase.table('groupmember').select(
            "student_id").eq('group_id', group).execute().data))

    for group in secondRunnerUpGrpIds:
        secondRunnerUpMembers = list(itertools.chain(secondRunnerUpMembers, supabase.table('groupmember').select(
            "student_id").eq('group_id', group).execute().data))
    log({'winner': winnerMembers, 'runnerup': firstRunnerUpMembers,
        'secondrunnerup': secondRunnerUpMembers})
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
        groupmembers = supabase.table('groupmember').select(
            'student_id').eq('group_id', group['group_id']).execute().data
        for member in groupmembers:
            # print(mainStudentCollectionIds)
            if member['student_id'] not in mainStudentCollectionIds:
                participantIds.append(member['student_id'])
    return participantIds


def saveToBucket(eventid: str, data):
    log('SAVING A CERTIFICATE TO BUCKET IN : ' + eventid)
    def upload():
        supabase.storage.from_("certificates").upload(
        file=data['bytes'], path=f'{eventid}/{data["name"]}.png', file_options={"upsert": "true", "content-type": "image/png"})
    try:
        upload()
    except Exception:
        supabase.storage.from_('certificates').remove([f'{eventid}/{data["name"]}.png'])
        upload()

