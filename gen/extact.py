import openpyxl as xl
import os
from PIL import ImageFont, ImageDraw, Image


# Templates
first_runner_temp = Image.open(os.path.join(os.getcwd(), 'files/1run.png'))
participant_temp = Image.open(os.path.join(os.getcwd(), 'files/par.png'))
second_runner_temp = Image.open(os.path.join(os.getcwd(), 'files/2run.png'))
winner_temp = Image.open(os.path.join(os.getcwd(), 'files/win.png'))


poster = os.path.join(os.getcwd(), 'files/poster.xls')
model = os.path.join(os.getcwd(), 'files/model.xls')


branches = {

    'Information Technology Engineering': 'IF',
    'Computer Engineering': 'CO',
    'Civil Engineering': 'CE',
    'Mechanical Engineering': 'ME',
    'Interior Design': 'ID',
    'Electronics & Telecommunication': 'EJ',

}

year = {
    'First Year': 'FY',
    'Second Year': 'SY',
    'Third Year': 'TY',

}


def generateCertsRowise(Event: str, Names: list, Branch: int, Year: int, State: int, row, ):
    if not row[0].value == 'Branch':

        names = Names
        branch = branches[row[Branch].value]
        year_m = year[row[Year].value]
        event = Event
        state = row[State].value

        temp = None
        temp2 = None

        if state == 'WINNER':
            temp = winner_temp.copy()

        elif state == 'FIRST RUNNER-UP':
            temp = first_runner_temp.copy()

        elif state == 'SECOND RUNNER-UP':
            temp = second_runner_temp.copy()

        else:
            temp = participant_temp.copy()

        temp2 = temp.copy()
        for name in names:
            temp = temp2.copy()
            if name != None:
                draw = ImageDraw.Draw(temp)
                font = ImageFont.truetype("arial.ttf", 30)
                draw.text((550, 373), name, font=font, fill=(0, 0, 0))
                font = ImageFont.truetype("arial.ttf", 25)
                draw.text((215, 405), f'{year_m}{branch}',
                          font=font, fill=(0, 0, 0))
                draw.text((700, 405), event,
                          font=font, fill=(0, 0, 0))
                draw.text((400, 435), '15/09/2023',
                          font=font, fill=(0, 0, 0))

                temp.save(os.getcwd() + '/output/' +
                          f'/{event}/' + f'{name}{branch}.png')


print("""------------------------------------------------
      ------------------------------------------------
      ------------------------------------------------""")
poster_wb = xl.open(poster)
poster_sheet = poster_wb.worksheets[0]

count = 1
for row in poster_sheet:
    generateCertsRowise(
        'Poster Making', [row[2].value, row[3].value], 0, 6, 5, row)
    print(f'Generated {count} for poster....')
    count += 1
poster_wb.close()
count = 1

print("""------------------------------------------------
      ------------------------------------------------
      ------------------------------------------------""")
model_wb = xl.open(model)
model_sheet = model_wb.worksheets[0]
for row in model_sheet:
    generateCertsRowise('Model Making', [
                        row[2].value, row[3].value, row[4].value, row[5].value], 0, 8, 7, row)
    print(f'Generated {count} for model....')
    count += 1

model_wb.close()
first_runner_temp.close()
participant_temp.close()
second_runner_temp.close()
winner_temp.close()
