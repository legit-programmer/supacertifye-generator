from .supafetch import *
from PIL import Image, ImageDraw, ImageFont
import io
import os



def generator(name, classs, status, eventname, date, eventid):  # changes on gen.py
    

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
    font = ImageFont.truetype('arial', 25)

    draw.text((550, 375), name, font=font, fill=(0, 0, 0))
    draw.text((215, 405), classs, font=font, fill=(0, 0, 0))
    draw.text((700, 405), eventname, font=font, fill=(0, 0, 0))
    draw.text((400, 435), date, font=font, fill=(0, 0, 0))

    im_bytes_arr = io.BytesIO()
    image.save(im_bytes_arr, format='PNG')

    return im_bytes_arr.getvalue()


def supagenerate(event_id: str):
    event = fetchEventDetails(event_id)
    mainStudents = fetchMainStudentsFromEvent(event_id)
    onlyParticipantStudents = fetchAllOnlyParticipants(event_id)
    eventname = event['name']
    eventdate = event['date']

    metadatas = list()
    
    # for winners

    for winner in mainStudents['winner']:
        winnerid = winner['student_id']
        studentDetails = fetchStudentDetailsFromId(winnerid)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                                 studentDetails['class'], 1, eventname, eventdate, event_id)
        im_name = studentDetails['first_name'] + studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name':im_name, 'bytes':im_bytes})
    # for runner up

    for runnerup in mainStudents['runnerup']:
        runnerupid = runnerup['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerupid)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                                 studentDetails['class'], 2, eventname, eventdate, event_id)
        im_name = studentDetails['first_name'] + studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name':im_name, 'bytes':im_bytes})
    # for second runner up

    for runnerup2 in mainStudents['secondrunnerup']:
        runnerup2id = runnerup2['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerup2id)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 3, eventname, eventdate, event_id)
        im_name = studentDetails['first_name'] + studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name':im_name, 'bytes':im_bytes})
    # for participants

    for participantid in onlyParticipantStudents:
        studentDetails = fetchStudentDetailsFromId(participantid)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                  studentDetails['class'], 0, eventname, eventdate, event_id)
        im_name = studentDetails['first_name'] + studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name':im_name, 'bytes':im_bytes})
    
    return metadatas

def uploadAllToBucket(eventid: str, metadata_arr):
    
    for data in metadata_arr:
        saveToBucket(eventid, data)
    
