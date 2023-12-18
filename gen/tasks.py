from .generation_controllers import *
from .fetch_controllers import setGenerationState



def generation_process(data):
    cords = {'name': data['name_cords'],
                 'class': data['class_cords'],
                 'eventname': data['eventname_cords'],
                 'date': data['date_cords'],
                 'position': data['postion_cords'],
                 }
    template_url = data['template_url']
    fontSize = data['fontSize']
    test = data['test']
    if not test:
        setGenerationState(data['event_id'], True)
        arr = supagenerate(
            data['event_id'], cords, template_url, fontSize)
        zipAndUpload(data['event_id'], arr)
        setGenerationState(data['event_id'], False)
        # uploadAllToBucket(data['event_id'], arr)
    else:
        getTemplate(data['event_id'], template_url)
        img_bytes = generator(
            'This is a test', 'TYIF', data['event_id'], 'Testing Certificate', '2005-04-18', 'Winner', cords, fontSize)

        supabase.storage.from_('certificates').upload(path=f'{data["event_id"]}.png', file=img_bytes, file_options={
            'x-upsert': "true", 'content-type': 'image/png'})
        # deleting template after generat
        os.remove(f'{data["event_id"]}.png')