from .supafetch import *
from PIL import Image, ImageDraw, ImageFont
import io
import os
import requests
from PIL import UnidentifiedImageError


def generator(name, classs, event_id, eventname, date, position, cords: dict):  # changes on gen.py

    image = Image.open(event_id + '.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial', 25)

    draw.text((cords['name'][0], cords['name'][1]-25),
              name, font=font, fill=(0, 0, 0))
    draw.text((cords['class'][0], cords['class'][1]-25),
              classs, font=font, fill=(0, 0, 0))
    draw.text((cords['eventname'][0], cords['eventname'][1]-25),
              eventname, font=font, fill=(0, 0, 0))
    draw.text((cords['date'][0], cords['date'][1]-25),
              date, font=font, fill=(0, 0, 0))
    draw.text((cords['position'][0], cords['position'][1]-25),
              position, font=font, fill=(0, 0, 0))

    im_bytes_arr = io.BytesIO()
    image.save(im_bytes_arr, format='PNG')

    return im_bytes_arr.getvalue()


def supagenerate(event_id: str, cords: dict, template_url: str):
    event = fetchEventDetails(event_id)
    mainStudents = fetchMainStudentsFromEvent(event_id)
    onlyParticipantStudents = fetchAllOnlyParticipants(event_id)
    eventname = event['name']
    eventdate = event['date']

    # generating template in local directory

    if '.supabase.co' not in template_url:
        raise ValueError

    res = requests.get(template_url)

    try:
        res.content.decode()
        raise UnidentifiedImageError("Please provide correct template")
    except UnicodeDecodeError:
        pass

    with open(event_id + '.png', 'wb') as file:
        file.write(res.content)

    metadatas = list()

    # for winners

    log('STARTED GENERATING CERTIFICATES FOR WINNERS')
    for winner in mainStudents['winner']:
        winnerid = winner['student_id']
        studentDetails = fetchStudentDetailsFromId(winnerid)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                             studentDetails['class'], event_id, eventname, eventdate, 'Winner', cords)
        im_name = studentDetails['first_name'] + \
            studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name': im_name, 'bytes': im_bytes})
    log('GENERATED CERTIFICATES FOR WINNERS')

    # for runner up

    log('STARTED GENERATING CERTIFICATES FOR RUNNER UPS')

    for runnerup in mainStudents['runnerup']:
        runnerupid = runnerup['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerupid)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                             studentDetails['class'], event_id, eventname, eventdate, 'First-Runner-Up', cords)
        im_name = studentDetails['first_name'] + \
            studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name': im_name, 'bytes': im_bytes})

    log('GENERATED CERTIFICATES FOR RUNNER UPS')

    # for second runner up
    log('STARTED GENERATING CERTIFICATES FOR SECOND RUNNER UPS')
    for runnerup2 in mainStudents['secondrunnerup']:
        runnerup2id = runnerup2['student_id']
        studentDetails = fetchStudentDetailsFromId(runnerup2id)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                             studentDetails['class'], event_id, eventname, eventdate, 'Second-Runner-Up', cords)
        im_name = studentDetails['first_name'] + \
            studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name': im_name, 'bytes': im_bytes})

    log('GENERATED CERTIFICATES FOR SECOND RUNNER UPS')

    # for participants
    log('STARTED GENERATING CERTIFICATES FOR PARTICIPANTS')
    for participantid in onlyParticipantStudents:
        studentDetails = fetchStudentDetailsFromId(participantid)
        im_bytes = generator(f'{studentDetails["first_name"]} {studentDetails["last_name"]}',
                             studentDetails['class'], event_id, eventname, eventdate, 'Participant', cords)
        im_name = studentDetails['first_name'] + \
            studentDetails['last_name'] + studentDetails['class']
        metadatas.append({'name': im_name, 'bytes': im_bytes})
    log('GENERATED CERTIFICATES FOR PARTICIPANTS')

    return metadatas


def uploadAllToBucket(eventid: str, metadata_arr):

    for data in metadata_arr:
        saveToBucket(eventid, data)

    # deleting template after generating certificates
    os.remove(eventid + '.png')
    supabase.storage.from_('templates').remove([eventid + '.png'])
