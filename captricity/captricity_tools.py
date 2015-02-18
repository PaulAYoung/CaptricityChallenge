#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from captools.api import Client

from captricity.config import captricity_token, ConfigBase
from captricity.models import Image, Batch, db_session

client = Client(captricity_token)

def create_batch(name="New Batch", document="test"):
    documents = client.read_documents()
    # Select the id of the template you would like to use. In this example, we will use the example job template.
    document_id = filter(lambda x: x['name'] == document, documents).pop()['id']
    batch = client.create_batches({'name': name, "documents": document_id})

    return batch


def add_files_to_batch(batch, file_paths):
    batch_id = batch['id']
    for f in file_paths:
        fobj = open(f, 'rb')
        client.create_batch_files(batch_id, {'uploaded_file': fobj})


def submit_job(batch):
    batch_id=batch['id']
    readiness = client.read_batch_readiness(batch_id)
    error = readiness['errors']
    price = client.read_batch_price(batch_id)

    out = {
            "errors": error,
            "price": price
            }

    if price["total_user_cost_in_cents"] == 0 and len(error) == 0:
        batch = client.submit_batch(batch_id, {})
        out['job'] = batch['related_job_id']

    return out


def process_images():
    """
    Finds unprocessed images and submits them
    """
    image_dir = ConfigBase.UPLOAD_FOLDER
    images = []
    query = Image.query.filter(Image.batch.is_(None))
    print query.count()
    if query.count()>0:
        new_batch = create_batch()
        batch = Batch(batch_id= new_batch['id'], status="In process")
        db_session.add(batch)

        for image in query:
            images.append(path.join(image_dir, image.path))
            image.batch = new_batch['id']
            db_session.add(image)

        add_files_to_batch(new_batch, images)
        print submit_job(new_batch)
        db_session.commit()


def check_jobs():
    batches = Batch.query.filter(Batch.status!="Finished")
    for batch in batches:
        b = client.read_batch(batch.batch_id)
        job = client.read_job(b['related_job_id'])
        completion = job['percent_completed']
        if completion == 100:
            batch.status = "Finished"
        else:
            batch.status = "{}% complete".format(completion)
        db_session.add(batch)

    db_session.commit()
