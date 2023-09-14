from supafetch import *
from PIL import Image, ImageDraw, ImageFont


def generator(name, classs, status, eventname, date):  # changes on gen.py

    output = f'output/{eventname}'

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
                  studentDetails['class'], 1, eventname, eventdate)

    # for runner up
    print(mainStudents['runnerup'])
    for runnerup in mainStudents['runnerup']:
        runnerupid = runnerup['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerupid)
        generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 2, eventname, eventdate)

    # for second runner up

    for runnerup2 in mainStudents['secondrunnerup']:
        runnerup2id = runnerup2['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerup2id)
        generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 3, eventname, eventdate)

    # for participants

    for participantid in onlyParticipantStudents:
        studentDetails = fetchStudentDetailsFromId(participantid)
        generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 0, eventname, eventdate)


supagenerate('9a67e80c-712c-4e9c-9ec4-1b7f29dc2b6f')
