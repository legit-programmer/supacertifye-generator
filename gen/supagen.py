from supafetch import *
from PIL import Image, ImageDraw, ImageFont


def generator(name, classs, status, eventname, date):  # changes on gen.py
    folders = os.listdir('output/')
    if eventname not in folders:
        os.mkdir(f'output/{eventname}')

    output = f'output/{eventname}/'

    if status == 1:
        win_path = os.path.join('files', 'win.png')

    elif status == 2:
        win_path = os.path.join('files', '1run.png')

    elif status == 3:
        win_path = os.path.join('files', '2run.png')

    else:
        win_path = os.path.join('files', 'par.png')

    image = Image.open(win_path)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 25)

    draw.text((550, 375), name, font=font, fill=(0, 0, 0))
    draw.text((215, 405), classs, font=font, fill=(0, 0, 0))
    draw.text((700, 405), eventname, font=font, fill=(0, 0, 0))
    draw.text((400, 435), date, font=font, fill=(0, 0, 0))

    image.save(output + f'{name}{classs}.png')
    


def supagenerate(event_id: str):
    event = fetchEventDetails(event_id)
    mainStudents = fetchMainStudentsFromEvent(event_id)
    onlyParticipantStudents = fetchAllOnlyParticipants(event_id)
    eventname = event['name']
    eventdate = event['date']

    # for winners

    for winner in mainStudents['winner']:
        winnerid = winner['student_id']
        studentDetails = fetchStudentDetailsFromId(winnerid)
        generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 1, event_id, eventdate)
        
    # for runner up
    
    for runnerup in mainStudents['runnerup']:
        runnerupid = runnerup['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerupid)
        generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 2, event_id, eventdate)

    # for second runner up

    for runnerup2 in mainStudents['secondrunnerup']:
        runnerup2id = runnerup2['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerup2id)
        generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 3, event_id, eventdate)

    # for participants

    for participantid in onlyParticipantStudents:
        studentDetails = fetchStudentDetailsFromId(participantid)
        generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 0, event_id, eventdate)

def uploadAllToBucket(eventid:str):
    for file in os.listdir(f'output/{eventid}'):
        saveToBucket(eventid, f'output/{eventid}/{file}')
        os.remove(f'output/{eventid}/{file}')
    os.rmdir(f'output/{eventid}')



